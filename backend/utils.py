"""
MSL AI Copilot — Shared Utility Functions

Provides reusable helpers for text processing, formatting,
caching, and MSL-specific data transformations used across
all pages of the application.
"""

from __future__ import annotations

import hashlib
import re
import time
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Dict, List, Optional

import streamlit as st


# ---------------------------------------------------------------------------
# Text Utilities
# ---------------------------------------------------------------------------

def truncate_text(text: str, max_chars: int = 500, suffix: str = "...") -> str:
    """Truncate text to max_chars, appending suffix if truncated."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0] + suffix


def clean_abstract(abstract: str) -> str:
    """Remove XML/HTML tags and normalize whitespace from PubMed abstracts."""
    clean = re.sub(r"<[^>]+>", "", abstract)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean


def extract_year(date_str: str) -> Optional[int]:
    """Extract year from various date string formats."""
    match = re.search(r"(\d{4})", str(date_str))
    return int(match.group(1)) if match else None


def format_authors(authors: List[str], max_authors: int = 3) -> str:
    """Format author list, truncating to max_authors with et al."""
    if not authors:
        return "Unknown authors"
    if len(authors) <= max_authors:
        return ", ".join(authors)
    return ", ".join(authors[:max_authors]) + " et al."


def build_pubmed_url(pmid: str) -> str:
    """Build a direct PubMed URL from a PMID."""
    return f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"


def build_doi_url(doi: str) -> str:
    """Build a DOI URL."""
    doi = doi.strip().lstrip("https://doi.org/")
    return f"https://doi.org/{doi}"


# ---------------------------------------------------------------------------
# Caching / Rate Limiting
# ---------------------------------------------------------------------------

def make_cache_key(*args: Any) -> str:
    """Create a deterministic SHA-256 cache key from arbitrary arguments."""
    raw = "|".join(str(a) for a in args)
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def rate_limit(calls_per_second: float = 0.34):
    """
    Decorator to enforce a rate limit on API calls.
    Default 0.34 calls/sec = 3 sec between calls (NCBI polite rate).
    """
    min_interval = 1.0 / calls_per_second
    last_called: Dict[str, float] = {}

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = func.__name__
            elapsed = time.time() - last_called.get(key, 0)
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_called[key] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator


# ---------------------------------------------------------------------------
# MSL Domain Helpers
# ---------------------------------------------------------------------------

THERAPEUTIC_AREA_KEYWORDS: Dict[str, List[str]] = {
    "Oncology": ["cancer", "tumor", "oncology", "carcinoma", "lymphoma", "leukemia",
                 "glioblastoma", "metastasis", "chemotherapy", "immunotherapy"],
    "Neurology": ["alzheimer", "parkinson", "multiple sclerosis", "epilepsy", "dementia",
                  "neurodegenerative", "stroke", "neuropathy", "seizure"],
    "Cardiology": ["heart failure", "atrial fibrillation", "hypertension", "myocardial",
                   "cardiovascular", "coronary", "arrhythmia", "atherosclerosis"],
    "Immunology": ["autoimmune", "rheumatoid", "lupus", "inflammatory", "cytokine",
                   "immunosuppression", "biologics", "JAK", "TNF"],
    "Endocrinology": ["diabetes", "insulin", "thyroid", "obesity", "metabolic syndrome",
                      "HbA1c", "GLP-1", "SGLT2"],
    "Respiratory": ["asthma", "COPD", "pulmonary", "bronchial", "spirometry",
                    "respiratory", "inhaler", "bronchodilator"],
    "Rare Disease": ["orphan drug", "rare disease", "ultra-rare", "genetic disorder",
                     "enzyme replacement", "gene therapy"],
}


def classify_therapeutic_area(text: str) -> str:
    """Classify text into a therapeutic area based on keyword matching."""
    text_lower = text.lower()
    scores: Dict[str, int] = {}
    for area, keywords in THERAPEUTIC_AREA_KEYWORDS.items():
        scores[area] = sum(1 for kw in keywords if kw in text_lower)
    best = max(scores, key=lambda k: scores[k])
    return best if scores[best] > 0 else "General Medicine"


EVIDENCE_LEVEL_MAP: Dict[str, int] = {
    "systematic review": 1,
    "meta-analysis": 1,
    "randomized controlled trial": 2,
    "rct": 2,
    "phase 3": 2,
    "phase iii": 2,
    "cohort study": 3,
    "phase 2": 3,
    "phase ii": 3,
    "case-control": 4,
    "phase 1": 5,
    "phase i": 5,
    "case report": 6,
    "expert opinion": 7,
    "in vitro": 8,
    "animal": 8,
    "preclinical": 8,
}


def classify_evidence_level(text: str) -> tuple[int, str]:
    """
    Returns (level_number, label) for the highest evidence level found.
    Lower number = higher evidence.
    """
    text_lower = text.lower()
    best_level = 9
    best_label = "Unclassified"
    for pattern, level in EVIDENCE_LEVEL_MAP.items():
        if pattern in text_lower and level < best_level:
            best_level = level
            best_label = pattern.title()
    return best_level, best_label


EVIDENCE_BADGES: Dict[int, tuple[str, str]] = {
    1: ("IA", "#1a7f2e"),   # Systematic review / meta-analysis
    2: ("IB", "#2e7d32"),   # RCT / Phase 3
    3: ("IIA", "#558b2f"),  # Cohort / Phase 2
    4: ("IIB", "#f9a825"),  # Case-control
    5: ("III", "#ef6c00"),  # Phase 1
    6: ("IV", "#d84315"),   # Case report
    7: ("V", "#b71c1c"),    # Expert opinion
    8: ("Pre", "#6a1b9a"),  # Preclinical / in vitro
    9: ("?", "#78909c"),    # Unknown
}


def evidence_badge_html(level: int) -> str:
    """Return an HTML badge for an evidence level."""
    label, color = EVIDENCE_BADGES.get(level, ("?", "#78909c"))
    return (
        f'<span style="background:{color};color:white;padding:2px 8px;'
        f'border-radius:4px;font-size:11px;font-weight:bold;">{label}</span>'
    )


# ---------------------------------------------------------------------------
# Streamlit UI Helpers
# ---------------------------------------------------------------------------

def render_metric_card(label: str, value: Any, delta: Optional[str] = None,
                       icon: str = "", color: str = "#0066CC") -> None:
    """Render a styled metric card using Streamlit markdown."""
    delta_html = f'<p style="color:#2e7d32;font-size:12px;margin:0;">\u25b2 {delta}</p>' if delta else ""
    st.markdown(
        f"""
        <div style="background:white;border-left:4px solid {color};
                    padding:16px;border-radius:8px;
                    box-shadow:0 2px 4px rgba(0,0,0,0.05);margin-bottom:8px;">
            <p style="color:#6b7280;font-size:12px;margin:0;text-transform:uppercase;">
                {icon} {label}</p>
            <p style="font-size:28px;font-weight:700;color:#1a2332;margin:4px 0;">{value}</p>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_info_banner(message: str, banner_type: str = "info") -> None:
    """Render a styled info/warning/success/error banner."""
    colors = {
        "info": ("#dbeafe", "#1d4ed8", "\u2139\ufe0f"),
        "warning": ("#fef9c3", "#854d0e", "\u26a0\ufe0f"),
        "success": ("#dcfce7", "#166534", "\u2705"),
        "error": ("#fee2e2", "#991b1b", "\u274c"),
    }
    bg, text, icon = colors.get(banner_type, colors["info"])
    st.markdown(
        f'<div style="background:{bg};color:{text};padding:12px 16px;'
        f'border-radius:8px;margin-bottom:12px;">{icon} {message}</div>',
        unsafe_allow_html=True,
    )


def format_date_relative(date_str: str) -> str:
    """Convert a date string to a relative description (e.g., '2 years ago')."""
    try:
        dt = datetime.strptime(date_str[:4], "%Y")
        diff = datetime.now() - dt
        years = diff.days // 365
        if years == 0:
            return "This year"
        elif years == 1:
            return "1 year ago"
        else:
            return f"{years} years ago"
    except Exception:
        return date_str


# ---------------------------------------------------------------------------
# Export / Formatting
# ---------------------------------------------------------------------------

def articles_to_markdown_table(articles: List[Dict]) -> str:
    """Convert a list of article dicts to a markdown table string."""
    if not articles:
        return "_No articles found._"
    headers = ["Title", "Authors", "Journal", "Year", "PMID"]
    rows = [
        [
            a.get("title", "")[:60],
            format_authors(a.get("authors", [])),
            a.get("journal", ""),
            str(a.get("year", "")),
            a.get("pmid", ""),
        ]
        for a in articles
    ]
    header_line = "| " + " | ".join(headers) + " |"
    sep_line = "| " + " | ".join(["---"] * len(headers)) + " |"
    row_lines = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header_line, sep_line] + row_lines)


def sanitize_filename(name: str) -> str:
    """Create a safe filename from a string."""
    safe = re.sub(r"[^\w\s-]", "", name).strip()
    safe = re.sub(r"[\s]+", "_", safe)
    return safe[:50]
