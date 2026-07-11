"""
backend/llm_engine.py

Real OpenAI LLM engine for MSL AI Copilot.
Uses GPT-4 for article summarization and RAG-based Q&A.
"""

import os
from typing import Optional
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


def get_llm(model: str = "gpt-4", temperature: float = 0.2):
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


def generate_kol_briefing(kol_name: str, research_area: str, recent_papers: str) -> str:
    """Generate a KOL briefing document using GPT-4o."""
    client = _get_client()
    if not client:
        return "Error: OpenAI API key not configured."

    prompt = (
        f"You are an MSL preparing a KOL briefing document.\n\n"
        f"KOL Name: {kol_name}\n"
        f"Research Area: {research_area}\n"
        f"Recent Papers/Context:\n{recent_papers[:2000]}\n\n"
        f"Generate a professional KOL briefing document with sections:\n"
        f"1. Research Summary\n2. Key Interests & Expertise\n"
        f"3. Recent Contributions\n4. Suggested Discussion Topics\n5. Engagement Strategy\n\n"
        f"Be concise, evidence-based, and MSL-compliant."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=800,
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
        return {
            "answer": "Error: OpenAI API key not configured.",
            "sources": [],
        }

    if not articles:
        return {
            "answer": "No articles in index. Please run a search first.",
            "sources": [],
        }

    # Build context from up to 8 articles
    context_parts = []
    for i, art in enumerate(articles[:8]):
        context_parts.append(
            f"[{i+1}] Title: {art.get('title', 'N/A')}\n"
            f"    Authors: {art.get('authors', 'N/A')} ({art.get('pub_date', 'N/A')})\n"
            f"    Abstract: {art.get('abstract', 'N/A')[:400]}"
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


def extract_insights_from_notes(notes: str, kol_name: str = "", model: str = "gpt-4o") -> dict:
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
        }

    prompt = (
        f"You are an MSL analyzing field interaction notes{' for ' + kol_name if kol_name else ''}.\n\n"
        f"Notes:\n{notes[:3000]}\n\n"
        f"Extract the following as JSON:\n"
        f"- key_themes: list of 3-5 main themes discussed\n"
        f"- sentiment: overall sentiment (positive/neutral/negative)\n"
        f"- follow_up_actions: list of 2-4 recommended follow-up actions\n"
        f"- scientific_interests: list of scientific topics the HCP showed interest in\n"
        f"- unmet_needs: list of unmet clinical or scientific needs mentioned\n"
        f"- summary: 2-3 sentence summary of the interaction\n\n"
        f"Respond with valid JSON only."
    )

    try:
        import json
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=500,
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {
            "key_themes": [],
            "sentiment": "unknown",
            "follow_up_actions": [],
            "scientific_interests": [],
            "unmet_needs": [],
            "summary": f"Error extracting insights: {e}",
        }
