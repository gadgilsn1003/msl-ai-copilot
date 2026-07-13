"""
🧠 LLM Engine - Google Gemini Integration

Handles all AI-powered features:
- Article summarization (3 formats)
- RAG-based Q&A over retrieved articles
- KOL briefing generation
- Insight extraction from field notes
- Activity report generation
"""

import os
from dotenv import load_dotenv

load_dotenv()

import google.generativeai as genai

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

GENERATION_CONFIG = {
    "temperature": 0.3,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 4096,
}

SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Model preference order - will try each until one works
MODEL_NAMES = [
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-pro-latest",
    "gemini-pro",
]

# Cache the working model name so we don't retry every call
_working_model_name = None


def _call_gemini(prompt: str, temperature: float = 0.3) -> str:
    """
    Call Gemini API with automatic model fallback.
    Tries multiple model names until one works, then caches the working one.
    """
    global _working_model_name

    config = GENERATION_CONFIG.copy()
    config["temperature"] = temperature

    # If we already found a working model, use it directly
    if _working_model_name:
        try:
            model = genai.GenerativeModel(
                model_name=_working_model_name,
                generation_config=config,
                safety_settings=SAFETY_SETTINGS,
            )
            response = model.generate_content(prompt)
            return response.text
        except Exception:
            # Model stopped working, reset and try all again
            _working_model_name = None

    # Try each model until one works
    last_error = None
    for model_name in MODEL_NAMES:
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                generation_config=config,
                safety_settings=SAFETY_SETTINGS,
            )
            response = model.generate_content(prompt)
            # Success! Cache this model name
            _working_model_name = model_name
            return response.text
        except Exception as e:
            last_error = e
            continue

    # All models failed
    raise Exception(f"All Gemini models failed. Last error: {str(last_error)}")


# =================================================================================
# ARTICLE SUMMARIZATION
# =================================================================================
def summarize_article(abstract: str, format_type: str = "standard") -> str:
    """Summarize a scientific article abstract using Gemini."""
    if not GOOGLE_API_KEY:
        return "⚠️ AI summarization requires GOOGLE_API_KEY. Please configure in environment variables."

    if not abstract or abstract.strip() == "":
        return "No abstract available for summarization."

    format_instructions = {
        "standard": (
            "Provide a clear, concise scientific summary in 3-4 paragraphs. "
            "Include: key objective, methodology, main findings, and clinical implications. "
            "Use precise scientific language appropriate for a Medical Science Liaison."
        ),
        "bullet points": (
            "Provide a structured bullet-point summary with the following sections:\n"
            "- **Objective:** (1-2 bullets)\n"
            "- **Methods:** (2-3 bullets)\n"
            "- **Key Findings:** (3-4 bullets)\n"
            "- **Clinical Implications:** (1-2 bullets)\n"
            "- **Limitations:** (1 bullet)\n"
            "Use precise scientific language."
        ),
        "hcp talking points": (
            "Generate 4-6 concise talking points that an MSL could use when discussing "
            "this study with a healthcare professional. Each point should:\n"
            "- Be evidence-based and reference specific data from the abstract\n"
            "- Be compliant (no promotional language, no comparative claims without data)\n"
            "- Be conversational yet scientifically rigorous\n"
            "- Include relevant statistics where available\n"
            "Format as numbered talking points."
        ),
    }

    instruction = format_instructions.get(format_type.lower(), format_instructions["standard"])

    prompt = (
        "You are a Medical Science Liaison AI assistant. Your role is to provide "
        "accurate, balanced, and compliant scientific summaries.\n\n"
        "IMPORTANT RULES:\n"
        "- Do NOT use promotional language\n"
        "- Do NOT make comparative efficacy claims unless directly supported by the data\n"
        "- Do NOT minimize safety findings\n"
        "- Do NOT make absolute claims\n"
        "- Present findings objectively and include limitations\n\n"
        f"TASK: {instruction}\n\n"
        f"ABSTRACT:\n{abstract}\n\n"
        "SUMMARY:"
    )

    try:
        return _call_gemini(prompt, temperature=0.3)
    except Exception as e:
        return f"⚠️ Summarization failed: {str(e)}"


# =================================================================================
# RAG-BASED Q&A
# =================================================================================
def ask_literature(question: str, articles: list) -> str:
    """Answer a question using retrieved articles as context."""
    if not GOOGLE_API_KEY:
        return "⚠️ AI Q&A requires GOOGLE_API_KEY. Please configure in environment variables."

    if not articles:
        return "No articles available to answer questions."

    context_parts = []
    for i, article in enumerate(articles[:10], 1):
        title = article.get("title", "Untitled")
        abstract = article.get("abstract", "No abstract available")
        authors = article.get("authors", "Unknown")
        year = article.get("year", "")
        pmid = article.get("pmid", "")
        context_parts.append(
            f"[Article {i}] {title}\n"
            f"Authors: {authors}\nYear: {year} | PMID: {pmid}\n"
            f"Abstract: {abstract}\n"
        )

    context = "\n---\n".join(context_parts)

    prompt = (
        "You are a Medical Science Liaison AI assistant answering questions based on "
        "scientific literature.\n\n"
        "IMPORTANT RULES:\n"
        "- ONLY answer based on the provided articles below\n"
        "- Cite specific articles by number when making claims (e.g., [Article 1])\n"
        "- If the articles don't contain enough information, say so clearly\n"
        "- Do NOT speculate beyond what the data shows\n"
        "- Do NOT use promotional language\n"
        "- Present findings objectively\n\n"
        f"RETRIEVED ARTICLES:\n{context}\n\n"
        f"QUESTION: {question}\n\n"
        "ANSWER (cite sources by article number):"
    )

    try:
        return _call_gemini(prompt, temperature=0.2)
    except Exception as e:
        return f"⚠️ Q&A failed: {str(e)}"


def build_rag_index(articles: list):
    """Placeholder for FAISS index building - using direct context for now."""
    return articles


# =================================================================================
# KOL BRIEFING GENERATION
# =================================================================================
def generate_kol_briefing(
    kol_name: str,
    institution: str = "",
    specialty: str = "",
    field_notes: str = "",
    interaction_type: str = "Pre-meeting briefing",
    include_literature: bool = False,
    literature_results: list = None,
) -> str:
    """Generate a structured KOL briefing document."""
    if not GOOGLE_API_KEY:
        return "⚠️ Briefing generation requires GOOGLE_API_KEY. Please configure in environment variables."

    lit_context = ""
    if include_literature and literature_results:
        lit_parts = []
        for article in literature_results[:5]:
            lit_parts.append(
                f"- {article.get('title', 'Untitled')} "
                f"({article.get('journal', '')}, {article.get('year', '')})"
            )
        lit_context = "\n\nRELEVANT RECENT LITERATURE:\n" + "\n".join(lit_parts)

    prompt = (
        "You are an AI assistant for Medical Science Liaisons. Generate a comprehensive "
        "pre-meeting briefing document for an upcoming KOL interaction.\n\n"
        "IMPORTANT RULES:\n"
        "- All content must be compliant with FDA medical affairs guidance\n"
        "- Do NOT include promotional language\n"
        "- Focus on scientific exchange and medical education\n"
        "- Be factual and evidence-based\n"
        "- Flag any areas where additional information is needed\n\n"
        f"KOL INFORMATION:\n"
        f"- Name: {kol_name}\n"
        f"- Institution: {institution}\n"
        f"- Specialty: {specialty}\n"
        f"- Upcoming Interaction Type: {interaction_type}\n\n"
        f"FIELD NOTES / CONTEXT:\n{field_notes}\n"
        f"{lit_context}\n\n"
        "Generate a structured briefing with the following 7 sections:\n\n"
        "## 1. KOL Profile Summary\n"
        "## 2. Research Interests & Focus Areas\n"
        "## 3. Discussion History & Key Topics\n"
        "## 4. Recommended Discussion Points\n"
        "## 5. Relevant Literature\n"
        "## 6. Identified Unmet Needs\n"
        "## 7. Relationship Notes & Follow-up Actions\n\n"
        "Generate the briefing now:"
    )

    try:
        return _call_gemini(prompt, temperature=0.4)
    except Exception as e:
        return f"⚠️ Briefing generation failed: {str(e)}"


# =================================================================================
# INSIGHT EXTRACTION
# =================================================================================
def extract_insights(field_notes: str) -> str:
    """Extract structured insights from raw field notes."""
    if not GOOGLE_API_KEY:
        return "⚠️ Insight extraction requires GOOGLE_API_KEY."

    if not field_notes or field_notes.strip() == "":
        return "No field notes provided for analysis."

    prompt = (
        "You are an AI assistant for Medical Science Liaisons. Analyze the following "
        "field notes and extract structured insights.\n\n"
        f"FIELD NOTES:\n{field_notes}\n\n"
        "Extract and organize:\n"
        "### Key Scientific Insights\n"
        "### KOL Sentiment & Interests\n"
        "### Unmet Needs Identified\n"
        "### Action Items\n"
        "### Compliance Notes\n\n"
        "Provide the analysis:"
    )

    try:
        return _call_gemini(prompt, temperature=0.3)
    except Exception as e:
        return f"⚠️ Insight extraction failed: {str(e)}"


def extract_insights_from_notes(field_notes: str) -> str:
    """Alias for extract_insights."""
    return extract_insights(field_notes)


# =================================================================================
# ACTIVITY REPORT GENERATION
# =================================================================================
def generate_activity_report(interactions: list) -> str:
    """Generate a leadership-ready MSL activity report."""
    if not GOOGLE_API_KEY:
        return "⚠️ Report generation requires GOOGLE_API_KEY."

    if not interactions:
        return "No interactions available to generate a report."

    total = len(interactions)
    unique_kols = len(set(i.get("kol_name", "") for i in interactions))
    types = {}
    therapeutic_areas = {}
    all_notes = []

    for interaction in interactions:
        itype = interaction.get("type", "Unknown")
        types[itype] = types.get(itype, 0) + 1
        ta = interaction.get("therapeutic_area", "Unknown")
        therapeutic_areas[ta] = therapeutic_areas.get(ta, 0) + 1
        notes = interaction.get("notes", "")
        if notes:
            all_notes.append(f"- [{itype}] {interaction.get('kol_name', 'Unknown')}: {notes[:150]}")

    types_summary = ", ".join([f"{k}: {v}" for k, v in sorted(types.items(), key=lambda x: -x[1])])
    ta_summary = ", ".join([f"{k}: {v}" for k, v in sorted(therapeutic_areas.items(), key=lambda x: -x[1])])
    notes_sample = "\n".join(all_notes[:15])

    prompt = (
        "You are an AI assistant helping a Medical Science Liaison create an activity "
        "report for their manager/leadership team.\n\n"
        f"ACTIVITY DATA:\n"
        f"- Total Interactions: {total}\n"
        f"- Unique KOLs Engaged: {unique_kols}\n"
        f"- Interaction Types: {types_summary}\n"
        f"- Therapeutic Areas: {ta_summary}\n\n"
        f"SAMPLE INTERACTION NOTES:\n{notes_sample}\n\n"
        "Generate a professional MSL activity report with:\n"
        "## Executive Summary\n"
        "## Key Metrics\n"
        "## Strategic Highlights\n"
        "## Therapeutic Area Coverage\n"
        "## Emerging Themes & Unmet Needs\n"
        "## Planned Next Steps\n\n"
        "Generate the report:"
    )

    try:
        return _call_gemini(prompt, temperature=0.4)
    except Exception as e:
        return f"⚠️ Report generation failed: {str(e)}"
