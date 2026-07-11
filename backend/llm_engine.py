"""
backend/llm_engine.py

Mock LLM engine for MSL AI Copilot - Demo Version.
Returns placeholder responses. Users can replace with real OpenAI integration.
"""

import os
from typing import Optional


def get_llm(model: str = "gpt-4", temperature: float = 0.2):
    """Mock LLM initialization. Returns placeholder."""
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        return None, model, temperature
    return "mock_client", model, temperature


def summarize_article(
    title: str,
    abstract: str,
    focus: Optional[str] = None,
    style: str = "standard",
    model: str = "gpt-4",
) -> str:
    """Mock article summarization with focus and style support."""
    focus_note = f" (Focus: {focus})" if focus else ""
    style_labels = {
        "standard": "Standard Paragraph",
        "bullet": "Bullet Points",
        "hcp_talking_points": "HCP Talking Points",
    }
    style_label = style_labels.get(style, "Standard Paragraph")

    return f"""**Summary ({style_label} - Demo Mode){focus_note}**

This is a demonstration version of the MSL AI Copilot.

**Article:** {title}

**Key Findings:**
- Article content would be analyzed here using {model}
- Clinical relevance highlighted based on the abstract
- Implications for healthcare providers summarized

**To enable real AI summarization:**
1. Ensure your OpenAI API key is set in environment variables
2. Replace this mock function with actual OpenAI API calls

*Abstract preview: {abstract[:200]}...*
"""


def generate_kol_briefing(kol_name: str, research_area: str, recent_papers: str) -> str:
    """Mock KOL briefing generation."""
    return f"""**KOL Briefing Document (Demo Mode)**

**KOL:** {kol_name}
**Research Area:** {research_area}

**1. Research Summary**
{kol_name} is a recognized expert in {research_area}. This demonstration shows the structure of automated briefing documents.

**2. Key Interests & Expertise**
- Domain expertise analysis would appear here
- Research focus areas
- Publication patterns

**3. Recent Contributions**
{recent_papers[:200] if recent_papers else 'Recent publications would be analyzed here'}

**4. Suggested Discussion Topics**
- Topic 1: Latest research directions
- Topic 2: Clinical applications
- Topic 3: Collaborative opportunities

**5. Engagement Strategy**
- Personalized approach based on research interests
- Follow-up recommendations
- Resource sharing suggestions

**To enable real AI briefing generation:**
Add your OpenAI API key and replace mock functions with actual API integration.
"""


def extract_insights(text: str, focus_area: Optional[str] = None) -> str:
    """Mock insight extraction."""
    focus_msg = f" (Focus: {focus_area})" if focus_area else ""
    return f"""**Key Insights (Demo Mode){focus_msg}**

1. **Clinical Relevance**: Key findings would be extracted and prioritized
2. **Actionable Intelligence**: Specific insights for MSL activities
3. **Strategic Value**: Business implications highlighted
4. **Follow-up Actions**: Next steps recommended

*Text preview: {text[:150]}...*

---
**This is a demonstration. Enable real AI by:**
- Adding OpenAI API key
- Implementing actual API integration
"""


def build_rag_index(articles: list) -> dict:
    """Mock RAG index builder."""
    return {"index": "mock_index", "articles": len(articles), "data": articles}


def ask_literature(question: str, index: dict = None, model: str = "gpt-4") -> dict:
    """Mock literature Q&A. Returns dict with 'answer' and 'sources'."""
    articles = index.get("data", []) if index else []
    sources = [
        {"title": a.get("title", "Unknown"), "url": a.get("url", "#")}
        for a in articles[:3]
    ]
    return {
        "answer": f"""**Answer (Demo Mode)**

Question: {question}

This is a demonstration response. In the full version, this would query your
saved literature index using RAG (Retrieval-Augmented Generation) and return
AI-generated answers grounded in the retrieved papers.

**To enable real answers:**
1. Ensure your OpenAI API key is set
2. Build a literature index by searching and saving articles first
""",
        "sources": sources,
    }


def extract_insights_from_notes(notes: str, kol_name: str = "", model: str = "gpt-4") -> dict:
    """Extract structured insights from field interaction notes."""
    return {
        "key_themes": ["Clinical efficacy", "Safety profile", "Unmet needs"],
        "sentiment": "positive",
        "follow_up_actions": ["Send follow-up literature", "Schedule next meeting"],
        "scientific_interests": ["Mechanism of action", "Real-world evidence"],
        "unmet_needs": ["Better biomarkers", "Long-term safety data"],
        "summary": f"Demo insights extracted from notes for {kol_name}. Enable real AI for detailed analysis."
    }
