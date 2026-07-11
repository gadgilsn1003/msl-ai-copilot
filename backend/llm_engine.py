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

def summarize_article(article_text: str, model: str = "gpt-4") -> str:
    """Mock article summarization."""
    return f"""**Summary (Demo Mode)**

This is a demonstration version of the MSL AI Copilot.

**Key Findings:**
- Article content would be analyzed here
- Clinical relevance highlighted
- Implications for healthcare providers summarized

**To enable real AI summarization:**
1. Add your OpenAI API key in the sidebar
2. Replace this mock function with actual OpenAI API calls

*Article preview: {article_text[:200]}...*
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
