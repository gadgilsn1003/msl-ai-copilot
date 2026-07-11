"""
backend/llm_engine.py

Simplified OpenAI engine for MSL AI Copilot.
Handles article summarization, KOL briefing generation, and insight extraction.
"""

import os
from typing import Optional
from openai import OpenAI

def get_llm(model: str = "gpt-4", temperature: float = 0.2):
    """Initialize and return OpenAI client."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set. Please add it in the sidebar.")
    
    return OpenAI(api_key=api_key), model, temperature

def summarize_article(article_text: str, model: str = "gpt-4") -> str:
    """Summarize a scientific article for MSLs."""
    try:
        client, model_name, temp = get_llm(model, 0.3)
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are an expert Medical Science Liaison. Summarize scientific articles with focus on clinical relevance, key findings, and implications for healthcare providers."},
                {"role": "user", "content": f"Summarize this article:\n\n{article_text[:4000]}"}
            ],
            temperature=temp,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error summarizing article: {str(e)}"

def generate_kol_briefing(kol_name: str, research_area: str, recent_papers: str) -> str:
    """Generate a KOL briefing document."""
    try:
        client, model_name, temp = get_llm("gpt-4", 0.2)
        
        prompt = f"""Create a professional briefing document for engaging with Key Opinion Leader (KOL):

KOL Name: {kol_name}
Research Area: {research_area}
Recent Publications: {recent_papers}

Include:
1. Research Summary
2. Key Interests & Expertise
3. Recent Contributions
4. Suggested Discussion Topics
5. Engagement Strategy
"""
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are an expert Medical Science Liaison specializing in KOL engagement. Create professional, comprehensive briefing documents."},
                {"role": "user", "content": prompt}
            ],
            temperature=temp,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating briefing: {str(e)}"

def extract_insights(text: str, focus_area: Optional[str] = None) -> str:
    """Extract key insights from text."""
    try:
        client, model_name, temp = get_llm("gpt-4", 0.2)
        
        focus_prompt = f" Focus on: {focus_area}" if focus_area else ""
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are an expert at extracting key insights from medical and scientific literature. Provide concise, actionable insights."},
                {"role": "user", "content": f"Extract key insights from this text:{focus_prompt}\n\n{text[:3000]}"}
            ],
            temperature=temp,
            max_tokens=400
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error extracting insights: {str(e)}"
