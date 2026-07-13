"""
🛡️ Compliance Filter - FDA Regulatory Compliance Scanner

Rule-based scanning aligned with FDA 21 CFR Part 202 and PhRMA Code.
Three-tier severity: HIGH / MEDIUM / LOW
"""

import re


COMPLIANCE_RULES = [
    {
        "id": "OFF_LABEL_001",
        "severity": "HIGH",
        "category": "Off-Label Promotion",
        "patterns": [
            r"\b(should be used for|recommended for|indicated for)\b",
            r"\b(off-label use is|can be used for)\b",
            r"\b(we recommend|we suggest using)\b",
        ],
        "message": "Potential off-label promotion detected.",
    },
    {
        "id": "COMP_001",
        "severity": "HIGH",
        "category": "Comparative Efficacy Claims",
        "patterns": [
            r"\b(superior to|better than|more effective than|outperforms)\b",
            r"\b(best in class|first in class|only treatment)\b",
            r"\b(preferred over|drug of choice)\b",
        ],
        "message": "Comparative efficacy claim detected.",
    },
    {
        "id": "ABS_001",
        "severity": "HIGH",
        "category": "Absolute Claims",
        "patterns": [
            r"\b(cures|eliminates|eradicates|guarantees)\b",
            r"\b(100% effective|completely safe|no side effects)\b",
            r"\b(always works|never fails|zero risk)\b",
        ],
        "message": "Absolute claim detected.",
    },
    {
        "id": "SAFETY_001",
        "severity": "MEDIUM",
        "category": "Safety Minimization",
        "patterns": [
            r"\b(well.tolerated|excellent safety|benign side effect)\b",
            r"\b(minimal risk|negligible adverse|safe for all)\b",
            r"\b(no serious|no significant adverse)\b",
        ],
        "message": "Potential safety minimization.",
    },
    {
        "id": "PROMO_001",
        "severity": "MEDIUM",
        "category": "Promotional Language",
        "patterns": [
            r"\b(breakthrough|revolutionary|game.changing|miracle)\b",
            r"\b(transformative|unparalleled|unprecedented efficacy)\b",
            r"\b(amazing results|remarkable outcomes|extraordinary)\b",
        ],
        "message": "Promotional language detected.",
    },
    {
        "id": "QUAL_001",
        "severity": "LOW",
        "category": "Unqualified Statements",
        "patterns": [
            r"\b(clearly|obviously|undoubtedly|certainly)\b",
        ],
        "message": "Consider adding qualifiers or citing specific evidence.",
    },
]


def scan_text(content: str) -> dict:
    """
    Screen content for compliance issues.

    Returns dict with: passed, flags, summary, score
    """
    if not content or content.strip() == "":
        return {
            "passed": True,
            "flags": [],
            "summary": "No content to screen.",
            "score": 100,
        }

    flags = []
    content_lower = content.lower()

    for rule in COMPLIANCE_RULES:
        for pattern in rule["patterns"]:
            try:
                matches = re.findall(pattern, content_lower)
                if matches:
                    match = re.search(pattern, content_lower)
                    context = ""
                    if match:
                        start = max(0, match.start() - 30)
                        end = min(len(content), match.end() + 30)
                        context = content[start:end].strip()

                    flags.append({
                        "id": rule["id"],
                        "severity": rule["severity"],
                        "category": rule["category"],
                        "message": rule["message"],
                        "context": f"...{context}...",
                        "match_count": len(matches),
                    })
                    break
            except re.error:
                continue

    high_count = sum(1 for f in flags if f["severity"] == "HIGH")
    medium_count = sum(1 for f in flags if f["severity"] == "MEDIUM")
    low_count = sum(1 for f in flags if f["severity"] == "LOW")

    score = 100 - (high_count * 25) - (medium_count * 10) - (low_count * 5)
    score = max(0, min(100, score))

    passed = high_count == 0

    if not flags:
        summary = "Content passed compliance screening. No issues detected."
    else:
        parts = []
        if high_count:
            parts.append(f"{high_count} HIGH severity issue(s)")
        if medium_count:
            parts.append(f"{medium_count} MEDIUM severity issue(s)")
        if low_count:
            parts.append(f"{low_count} LOW severity issue(s)")
        summary = f"Compliance screening found: {', '.join(parts)}."

    return {
        "passed": passed,
        "flags": flags,
        "summary": summary,
        "score": score,
        "counts": {"high": high_count, "medium": medium_count, "low": low_count},
    }


def get_compliance_badge(score: int) -> str:
    """Get a compliance badge based on score."""
    if score >= 90:
        return "✅ Compliant"
    elif score >= 70:
        return "⚠️ Minor Issues"
    elif score >= 50:
        return "🟠 Review Needed"
    else:
        return "🔴 Non-Compliant"
