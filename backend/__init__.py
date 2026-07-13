# MSL AI Copilot - Backend Package

from .pubmed_fetcher import search_pubmed, fetch_articles, search_and_fetch
from .llm_engine import summarize_article, generate_kol_briefing, extract_insights, build_rag_index, ask_literature, extract_insights_from_notes, generate_activity_report
from .compliance_filter import scan_text, get_compliance_badge
from .database import init_db, save_article, get_all_kols, add_kol, log_interaction, get_all_interactions, get_interaction_stats, search_kols, get_saved_articles

__all__ = [
    "search_pubmed",
    "fetch_articles",
    "search_and_fetch",
    "summarize_article",
    "generate_kol_briefing",
    "extract_insights",
    "build_rag_index",
    "ask_literature",
    "extract_insights_from_notes",
    "generate_activity_report",
    "scan_text",
    "get_compliance_badge",
    "init_db",
    "save_article",
    "get_all_kols",
    "add_kol",
    "log_interaction",
    "get_all_interactions",
    "get_interaction_stats",
    "search_kols",
    "get_saved_articles",
]
