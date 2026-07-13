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

# =================================================================================
# GEMINI CLIENT SETUP
# =================================================================================
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


def get_model(temperature=0.3):
    """Get configured Gemini model instance."""
    config = GENERATION_CONFIG.copy()
    config["temperature"] = temperature

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=config,
        safety_settings=SAFETY_SETTINGS,
    )
    return model


def check_api_available():
    """Check if Gemini API is configured and available."""
    if not GOOGLE_API_KEY:
        return False, "GOOGLE_API_KEY not configured"
    try:
        model = get_model()
        response = model.generate_content("Say ok")
        return True, "Connected"
    except Exception as e:
        return False, str(e)


# =================================================================================
# ARTICLE SUMMARIZATION
# =================================================================================
def summarize_article(abstract: str, format_type: str = "standard") -> str:
    """
    Summarize a scientific article abstract using Gemini.

    Args:
        abstract: The article abstract text
        format_type: One of 'standard', 'bullet points', 'hcp talking points'

    Returns:
        Formatted summary string
    """
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

    instruction = format_instructions.get(
        format_type.lower(),
        format_instructions["standard"]
    )

    prompt = (
        "You are a Medical Science Liaison AI assistant. Your role is to provide "
        "accurate, balanced, and compliant scientific summaries.\n\n"
        "IMPORTANT RULES:\n"
        "- Do NOT use promotional language\n"
        "- Do NOT make comparative efficacy claims unless directly supported by the data\n"
        "- Do NOT minimize safety findings\n"
        "- Do NOT make absolute claims (e.g., 'this drug cures...')\n"
        "- Present findings objectively and include limitations\n\n"
        f"TASK: {instruction}\n\n"
        f"ABSTRACT:\n{abstract}\n\n"
        "SUMMARY:"
    )

    try:
        model = get_model(temperature=0.3)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Summarization failed: {str(e)}"


# =================================================================================
# RAG-BASED Q&A OVER ARTICLES
# =================================================================================
def ask_question_over_articles(question: str, articles: list) -> str:
    """
    Answer a question using retrieved articles as context (RAG).

    Args:
        question: User's natural language question
        articles: List of article dicts with 'title', 'abstract', etc.

    Returns:
        AI-generated answer grounded in the provided articles
    """
    if not GOOGLE_API_KEY:
        return "⚠️ AI Q&A requires GOOGLE_API_KEY. Please configure in environment variables."

    if not articles:
        return "No articles available to answer questions. Please search for articles first."

    # Build context from articles
    context_parts = []
    for i, article in enumerate(articles[:10], 1):
        title = article.get("title", "Untitled")
        abstract = article.get("abstract", "No abstract available")
        authors = article.get("authors", "Unknown")
        year = article.get("year", "")
        pmid = article.get("pmid", "")

        context_parts.append(
            f"[Article {i}] {title}\n"
            f"Authors: {authors}\n"
            f"Year: {year} | PMID: {pmid}\n"
            f"Abstract: {abstract}\n"
        )

    context = "\n---\n".join(context_parts)

    prompt = (
        "You are a Medical Science Liaison AI assistant answering questions based on "
        "scientific literature.\n\n"
        "IMPORTANT RULES:\n"
        "- ONLY answer based on the provided articles below\n"
        "- Cite specific articles by number when making claims (e.g., [Article 1])\n"
        "- If the articles don't contain enough information to answer, say so clearly\n"
        "- Do NOT speculate beyond what the data shows\n"
        "- Do NOT use promotional language\n"
        "- Present findings objectively\n\n"
        f"RETRIEVED ARTICLES:\n{context}\n\n"
        f"QUESTION: {question}\n\n"
        "ANSWER (cite sources by article number):"
    )

    try:
        model = get_model(temperature=0.2)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Q&A failed: {str(e)}"


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
    """
    Generate a structured KOL briefing document.
    """
    if not GOOGLE_API_KEY:
        return "⚠️ Briefing generation requires GOOGLE_API_KEY. Please configure in environment variables."

    # Build literature context if available
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
        "Brief overview of the KOL based on available information.\n\n"
        "## 2. Research Interests & Focus Areas\n"
        "Key scientific interests and therapeutic focus areas.\n\n"
        "## 3. Discussion History & Key Topics\n"
        "Summary of previous interactions and recurring themes.\n\n"
        "## 4. Recommended Discussion Points\n"
        "Suggested topics for the upcoming interaction (compliant, non-promotional).\n\n"
        "## 5. Relevant Literature\n"
        "Recent publications or data that may be relevant to discuss.\n\n"
        "## 6. Identified Unmet Needs\n"
        "Scientific or clinical unmet needs expressed by or relevant to this KOL.\n\n"
        "## 7. Relationship Notes & Follow-up Actions\n"
        "Relationship status, pending items, and recommended next steps.\n\n"
        "---\nGenerate the briefing now:"
    )

    try:
        model = get_model(temperature=0.4)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Briefing generation failed: {str(e)}"


# =================================================================================
# INSIGHT EXTRACTION
# =================================================================================
def extract_insights(field_notes: str) -> str:
    """
    Extract structured insights from raw field notes.
    """
    if not GOOGLE_API_KEY:
        return "⚠️ Insight extraction requires GOOGLE_API_KEY. Please configure in environment variables."

    if not field_notes or field_notes.strip() == "":
        return "No field notes provided for analysis."

    prompt = (
        "You are an AI assistant for Medical Science Liaisons. Analyze the following "
        "field notes and extract structured insights.\n\n"
        f"FIELD NOTES:\n{field_notes}\n\n"
        "Extract and organize the following:\n\n"
        "### Key Scientific Insights\n"
        "- Main scientific topics discussed\n"
        "- Data or evidence mentioned\n\n"
        "### KOL Sentiment & Interests\n"
        "- KOL's attitude toward current treatments\n"
        "- Areas of scientific interest or curiosity\n"
        "- Concerns raised\n\n"
        "### Unmet Needs Identified\n"
        "- Clinical unmet needs mentioned\n"
        "- Research gaps identified\n"
        "- Patient population needs\n\n"
        "### Action Items\n"
        "- Follow-up items needed\n"
        "- Information requests\n"
        "- Suggested next steps\n\n"
        "### Compliance Notes\n"
        "- Any topics that require careful handling\n"
        "- Areas to avoid in future discussions\n\n"
        "Provide the analysis:"
    )

    try:
        model = get_model(temperature=0.3)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Insight extraction failed: {str(e)}"


# =================================================================================
# ACTIVITY REPORT GENERATION
# =================================================================================
def generate_activity_report(interactions: list) -> str:
    """
    Generate a leadership-ready MSL activity report.
    """
    if not GOOGLE_API_KEY:
        return "⚠️ Report generation requires GOOGLE_API_KEY. Please configure in environment variables."

    if not interactions:
        return "No interactions available to generate a report."

    # Summarize interactions for the prompt
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
            all_notes.append(
                f"- [{itype}] {interaction.get('kol_name', 'Unknown')}: {notes[:150]}"
            )

    types_summary = ", ".join(
        [f"{k}: {v}" for k, v in sorted(types.items(), key=lambda x: -x[1])]
    )
    ta_summary = ", ".join(
        [f"{k}: {v}" for k, v in sorted(therapeutic_areas.items(), key=lambda x: -x[1])]
    )
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
        "Generate a professional MSL activity report with:\n\n"
        "## Executive Summary\n"
        "2-3 sentence overview of the reporting period.\n\n"
        "## Key Metrics\n"
        "Present the quantitative data clearly.\n\n"
        "## Strategic Highlights\n"
        "Top 3-4 notable engagements or scientific exchanges.\n\n"
        "## Therapeutic Area Coverage\n"
        "Summary of activity across therapeutic areas.\n\n"
        "## Emerging Themes & Unmet Needs\n"
        "Scientific themes and unmet needs identified from KOL interactions.\n\n"
        "## Planned Next Steps\n"
        "Recommended actions for the next reporting period.\n\n"
        "---\n"
        "*This report was auto-generated by MSL AI Copilot.*\n\n"
        "Generate the report:"
    )

    try:
        model = get_model(temperature=0.4)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Report generation failed: {str(e)}"
