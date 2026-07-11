"""
backend/llm_engine.py

Real OpenAI LLM engine for MSL AI Copilot.
Uses GPT-4o for article summarization, KOL briefings, and RAG-based Q&A.
"""

import os
import json
from typing import Optional, List
from openai import OpenAI

_client = None


def _get_client() -> Optional[OpenAI]:
    """Return a cached OpenAI client, or None if no API key."""
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY", "")
        if api_key:
            _client = OpenAI(api_key=api_key)
    return _client


def get_llm(model: str = "gpt-4o", temperature: float = 0.2):
    """Return OpenAI client, model, and temperature."""
    client = _get_client()
    return client, model, temperature


def summarize_article(
    title: str,
    abstract: str,
    focus: Optional[str] = None,
    style: str = "standard",
    model: str = "gpt-4o",
) -> str:
    """Summarize a PubMed article using GPT-4o."""
    client = _get_client()
    if not client:
        return "Error: OpenAI API key not configured."

    style_instructions = {
        "standard": "Write a concise 3-4 sentence paragraph summary suitable for an MSL.",
        "bullet": "Write a summary as 4-6 bullet points highlighting the key findings.",
        "hcp_talking_points": (
            "Write 3-5 HCP talking points an MSL could use when discussing this paper with "
            "a physician. Use conditional language ('data suggest', 'the study found'). "
            "Be concise and clinically relevant."
        ),
    }
    style_prompt = style_instructions.get(style, style_instructions["standard"])
    focus_prompt = f" Focus specifically on: {focus}." if focus else ""

    prompt = (
        f"You are a Medical Science Liaison (MSL) summarizing a scientific paper for internal use.\n\n"
        f"Article Title: {title}\n\n"
        f"Abstract:\n{abstract}\n\n"
        f"Task: {style_prompt}{focus_prompt}\n\n"
        f"Comply with MSL best practices: use conditional language, cite the study, "
        f"avoid absolute claims, present efficacy and safety in fair balance."
    )
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating summary: {e}"


def generate_kol_briefing(
    kol_name: str,
    specialty: str,
    institution: str,
    field_notes: str,
    relevant_articles: Optional[List[dict]] = None,
    therapeutic_area: str = "",
    model: str = "gpt-4o",
) -> str:
    """Generate a comprehensive KOL briefing document using GPT-4o."""
    client = _get_client()
    if not client:
        return "Error: OpenAI API key not configured."

    # Build literature context if articles provided
    lit_context = ""
    if relevant_articles:
        lit_parts = []
        for i, art in enumerate(relevant_articles[:5]):
            lit_parts.append(
                f"[{i+1}] {art.get('title', 'N/A')} "
                f"({art.get('pub_date', 'N/A')}) - "
                f"{art.get('abstract', '')[:200]}..."
            )
        lit_context = "\n\nRecent Relevant Literature:\n" + "\n".join(lit_parts)

    prompt = (
        f"You are a senior Medical Science Liaison preparing a pre-meeting KOL briefing document.\n\n"
        f"KOL Name: {kol_name}\n"
        f"Specialty: {specialty}\n"
        f"Institution: {institution}\n"
        f"Therapeutic Area: {therapeutic_area}\n\n"
        f"Field Notes from Previous Interactions:\n{field_notes[:2000]}\n"
        f"{lit_context}\n\n"
        f"Generate a professional, structured KOL briefing document with these sections:\n"
        f"## 1. KOL Profile Summary\n"
        f"## 2. Scientific Interests & Expertise\n"
        f"## 3. Previous Interaction Highlights\n"
        f"## 4. Suggested Discussion Topics\n"
        f"## 5. Recommended Literature to Share\n"
        f"## 6. Strategic Engagement Notes\n\n"
        f"Be concise, evidence-based, and MSL-compliant. Use professional language."
    )
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=1200,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating KOL briefing: {e}"


def extract_insights(text: str, focus_area: Optional[str] = None) -> str:
    """Extract key insights from text using GPT-4o."""
    client = _get_client()
    if not client:
        return "Error: OpenAI API key not configured."
    focus_msg = f" Focus on: {focus_area}." if focus_area else ""
    prompt = (
        f"Extract 4-5 key clinical insights from the following text for an MSL.{focus_msg}\n\n"
        f"Text:\n{text[:3000]}\n\n"
        f"Format as numbered insights, each with a bold header and 1-2 sentences."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=400,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error extracting insights: {e}"


def build_rag_index(articles: list) -> dict:
    """Build a simple in-memory index from article dicts."""
    return {
        "index": "live",
        "articles": len(articles),
        "data": articles,
    }


def ask_literature(question: str, index: dict = None, model: str = "gpt-4o") -> dict:
    """Answer a question using the retrieved articles as context (RAG)."""
    client = _get_client()
    articles = (index or {}).get("data", [])

    if not client:
        return {"answer": "Error: OpenAI API key not configured.", "sources": []}
    if not articles:
        return {"answer": "No articles in index. Please run a search first.", "sources": []}

    context_parts = []
    for i, art in enumerate(articles[:8]):
        context_parts.append(
            f"[{i+1}] Title: {art.get('title', 'N/A')}\n"
            f"   Authors: {art.get('authors', 'N/A')} ({art.get('pub_date', 'N/A')})\n"
            f"   Abstract: {art.get('abstract', 'N/A')[:400]}"
        )
    context = "\n\n".join(context_parts)

    prompt = (
        f"You are an expert MSL assistant. Answer the following question based ONLY on "
        f"the provided scientific articles. Cite article numbers like [1], [2] in your answer.\n\n"
        f"Question: {question}\n\n"
        f"Articles:\n{context}\n\n"
        f"Provide a clear, evidence-based answer in 3-5 sentences. "
        f"Use conditional language (data suggest, findings indicate). "
        f"If the articles don't contain enough information, say so."
    )
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=400,
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        answer = f"Error generating answer: {e}"

    sources = [
        {"title": a.get("title", "Unknown"), "url": a.get("url", "#")}
        for a in articles[:8]
    ]
    return {"answer": answer, "sources": sources}


def extract_insights_from_notes(
    notes: str,
    therapeutic_area: str = "",
    model: str = "gpt-4o",
) -> dict:
    """Extract structured insights from field interaction notes using GPT-4o."""
    client = _get_client()
    if not client:
        return {
            "key_themes": [],
            "sentiment": "unknown",
            "follow_up_actions": [],
            "scientific_interests": [],
            "unmet_needs": [],
            "summary": "Error: OpenAI API key not configured.",
            "raw_analysis": "Error: OpenAI API key not configured.",
        }

    ta_context = f" for therapeutic area: {therapeutic_area}" if therapeutic_area else ""
    prompt = (
        f"You are an MSL analyzing field interaction notes{ta_context}.\n\n"
        f"Notes:\n{notes[:3000]}\n\n"
        f"Extract the following as JSON:\n"
        f"- key_themes: list of 3-5 main themes discussed\n"
        f"- sentiment: overall sentiment (positive/neutral/negative)\n"
        f"- follow_up_actions: list of 2-4 recommended follow-up actions\n"
        f"- scientific_interests: list of scientific topics the HCP showed interest in\n"
        f"- unmet_needs: list of unmet clinical or scientific needs mentioned\n"
        f"- summary: 2-3 sentence summary of the interaction\n"
        f"- raw_analysis: a formatted markdown analysis suitable for MSL reporting\n\n"
        f"Respond with valid JSON only."
    )
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=600,
            response_format={"type": "json_object"},
        )
        result = json.loads(response.choices[0].message.content)
        if "raw_analysis" not in result:
            result["raw_analysis"] = result.get("summary", "No analysis available.")
        return result
    except Exception as e:
        return {
            "key_themes": [],
            "sentiment": "unknown",
            "follow_up_actions": [],
            "scientific_interests": [],
            "unmet_needs": [],
            "summary": f"Error extracting insights: {e}",
            "raw_analysis": f"Error extracting insights: {e}",
        }
