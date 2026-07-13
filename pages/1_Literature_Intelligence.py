"""
📚 Literature Intelligence Module

Real-time PubMed search with AI-powered summarization,
RAG-based Q&A, and automatic compliance screening.
"""

import streamlit as st
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# =================================================================================
# PAGE CONFIG
# =================================================================================
st.set_page_config(
    page_title="MSL AI Copilot · Literature Intelligence",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =================================================================================
# PAGE CSS
# =================================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: #f8fafc;
    }

    .block-container {
        padding: 2rem 3rem;
        max-width: 1200px;
    }

    .page-header {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 8px;
    }

    .page-header-icon {
        width: 52px;
        height: 52px;
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.12), rgba(14, 165, 233, 0.04));
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 26px;
    }

    .page-header-text h1 {
        font-size: 28px;
        font-weight: 800;
        color: #0f172a;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .page-header-text p {
        font-size: 14px;
        color: #64748b;
        margin: 4px 0 0 0;
    }

    .empty-state {
        text-align: center;
        padding: 60px 20px;
        color: #94a3b8;
    }

    .empty-state-icon {
        font-size: 48px;
        margin-bottom: 16px;
        opacity: 0.5;
    }

    .empty-state h3 {
        font-size: 18px;
        font-weight: 600;
        color: #64748b;
        margin: 0 0 8px 0;
    }

    .empty-state p {
        font-size: 14px;
        margin: 0;
    }

    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
        color: white !important;
        border: none !important;
        padding: 10px 20px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(14, 165, 233, 0.2) !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(14, 165, 233, 0.3) !important;
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    [data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        color: #334155 !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: none !important;
        font-weight: 500 !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(14, 165, 233, 0.06) !important;
        border-color: #0ea5e9 !important;
        color: #0ea5e9 !important;
        transform: none !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =================================================================================
# IMPORTS - Backend modules
# =================================================================================
try:
    from backend.pubmed_fetcher import search_pubmed, fetch_articles
    from backend.llm_engine import summarize_article, ask_literature
    from backend.compliance_filter import scan_text
    BACKEND_AVAILABLE = True
except ImportError as e:
    BACKEND_AVAILABLE = False
    st.error(f"Backend import failed: {e}")
except Exception as e:
    BACKEND_AVAILABLE = False
    st.error(f"Backend error: {e}")

# =================================================================================
# SIDEBAR
# =================================================================================
with st.sidebar:
    st.markdown("### 🧬 MSL AI Copilot")
    st.caption("Literature Intelligence")
    st.markdown("---")

    if st.button("🏠  Home", use_container_width=True, key="nav_home"):
        st.switch_page("app.py")
    if st.button("👤  KOL Briefing", use_container_width=True, key="nav_kol"):
        st.switch_page("pages/2_KOL_Briefing_Generator.py")
    if st.button("📊  Impact Dashboard", use_container_width=True, key="nav_dash"):
        st.switch_page("pages/3_Impact_Dashboard.py")

    st.markdown("---")

    st.markdown("**Search Settings**")
    max_results = st.slider("Max results", 5, 50, 15, key="max_results")
    sort_order = st.selectbox("Sort by", ["Relevance", "Date (Newest)", "Date (Oldest)"], key="sort_order")

    st.markdown("---")

    st.markdown("**Quick Queries**")
    therapeutic_areas = {
        "Oncology – Immunotherapy": "immunotherapy[MeSH] AND cancer AND clinical trial[pt]",
        "GBM / Neuro-Oncology": "glioblastoma[MeSH] AND (temozolomide OR bevacizumab) AND 2023:2025[dp]",
        "Immunology – Autoimmune": "autoimmune diseases[MeSH] AND biologics AND treatment outcome",
        "Cardiology – Heart Failure": "heart failure[MeSH] AND SGLT2 inhibitors AND clinical trial[pt]",
        "Rare Disease – Gene Therapy": "gene therapy[MeSH] AND rare diseases AND 2023:2025[dp]",
        "Neurology – Alzheimer's": "alzheimer disease[MeSH] AND (lecanemab OR donanemab) AND 2023:2025[dp]",
    }

    selected_ta = st.selectbox("Therapeutic Area", ["Custom"] + list(therapeutic_areas.keys()), key="ta_select")

    if selected_ta != "Custom":
        st.code(therapeutic_areas[selected_ta], language=None)

    st.markdown("---")

    st.markdown("**📁 Saved Library**")
    if "saved_articles" not in st.session_state:
        st.session_state.saved_articles = []

    saved_count = len(st.session_state.saved_articles)
    st.caption(f"{saved_count} article{'s' if saved_count != 1 else ''} saved")

# =================================================================================
# PAGE HEADER
# =================================================================================
st.markdown("""
<div class="page-header">
    <div class="page-header-icon">📚</div>
    <div class="page-header-text">
        <h1>Literature Intelligence</h1>
        <p>Search, analyze, and synthesize scientific literature with AI-powered compliance screening</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# =================================================================================
# SEARCH INTERFACE
# =================================================================================
if selected_ta != "Custom":
    default_query = therapeutic_areas[selected_ta]
else:
    default_query = ""

search_query = st.text_input(
    "🔍 Search PubMed",
    value=default_query,
    placeholder="Enter search terms, MeSH terms, or paste a PubMed query...",
    key="search_input",
    help="Supports full PubMed/MeSH syntax. Example: 'glioblastoma[MeSH] AND immunotherapy AND 2024[dp]'"
)

col_search, col_clear = st.columns([4, 1])

with col_search:
    search_clicked = st.button("🔍 Search PubMed", use_container_width=True, key="btn_search")

with col_clear:
    if st.button("Clear", use_container_width=True, key="btn_clear"):
        if "search_results" in st.session_state:
            del st.session_state.search_results

# =================================================================================
# SEARCH EXECUTION
# =================================================================================
if search_clicked and search_query:
    if not BACKEND_AVAILABLE:
        st.error("⚠️ Backend modules not found. Please ensure `backend/` directory is properly configured.")
    else:
        with st.spinner("Searching PubMed..."):
            try:
                sort_map = {
                    "Relevance": "relevance",
                    "Date (Newest)": "date",
                    "Date (Oldest)": "date",
                }
                results = search_pubmed(
                    query=search_query,
                    max_results=max_results,
                    sort=sort_map.get(sort_order, "relevance")
                )
                st.session_state.search_results = results
                st.session_state.current_query = search_query
            except Exception as e:
                st.error(f"Search failed: {str(e)}")

# =================================================================================
# RESULTS DISPLAY
# =================================================================================
if "search_results" in st.session_state and st.session_state.search_results:
    results = st.session_state.search_results

    st.markdown(f"**{len(results)} articles found** for: `{st.session_state.get('current_query', '')}`")
    st.markdown("")

    tab_results, tab_qa, tab_library = st.tabs(["📄 Results", "🤖 AI Q&A", "📁 Saved Library"])

    with tab_results:
        for i, article in enumerate(results):
            with st.container():
                col_title, col_save = st.columns([6, 1])

                with col_title:
                    st.markdown(f"**{article.get('title', 'Untitled')}**")

                with col_save:
                    if st.button("💾", key=f"save_{i}", help="Save to library"):
                        if article not in st.session_state.saved_articles:
                            st.session_state.saved_articles.append(article)
                            st.toast("Article saved to library!", icon="✅")

                authors = article.get("authors", "Unknown authors")
                journal = article.get("journal", "Unknown journal")
                year = article.get("year", "")
                pmid = article.get("pmid", "")

                st.caption(f"👥 {str(authors)[:100]}{'...' if len(str(authors)) > 100 else ''}")
                st.caption(f"📰 {journal} · {year} · PMID: {pmid}")

                abstract = article.get("abstract", "")
                if abstract:
                    with st.expander("View Abstract"):
                        st.write(abstract)

                        summary_format = st.selectbox(
                            "Summary format",
                            ["Standard", "Bullet Points", "HCP Talking Points"],
                            key=f"fmt_{i}"
                        )

                        if st.button("🧠 AI Summarize", key=f"sum_{i}"):
                            if not os.getenv("GOOGLE_API_KEY"):
                                st.warning("Google Gemini API key required for AI summarization.")
                            else:
                                with st.spinner("Generating summary..."):
                                    try:
                                        summary = summarize_article(
                                            abstract,
                                            format_type=summary_format.lower()
                                        )

                                        compliance_result = scan_text(summary)

                                        st.markdown("---")
                                        st.markdown(f"**AI Summary ({summary_format})**")
                                        st.write(summary)

                                        if compliance_result.get("passed", True):
                                            st.success("✅ Compliance check passed")
                                        else:
                                            st.warning("⚠️ Compliance flags detected:")
                                            for flag in compliance_result.get("flags", []):
                                                st.write(f"- [{flag['severity']}] {flag['message']}")
                                    except Exception as e:
                                        st.error(f"Summarization failed: {str(e)}")

                st.markdown("---")

    with tab_qa:
        st.markdown("### 🤖 Ask Questions Over Retrieved Articles")
        st.caption("Uses RAG (Retrieval-Augmented Generation) to answer questions based on the retrieved literature.")

        question = st.text_input(
            "Ask a question",
            placeholder="e.g., What are the main efficacy endpoints reported across these studies?",
            key="qa_input"
        )

        if st.button("Get Answer", key="btn_qa") and question:
            if not os.getenv("GOOGLE_API_KEY"):
                st.warning("Google Gemini API key required for AI Q&A.")
            else:
                with st.spinner("Analyzing articles..."):
                    try:
                        answer = ask_literature(question, results)

                        st.markdown("**Answer:**")
                        st.write(answer)

                        compliance_result = scan_text(answer)
                        if compliance_result.get("passed", True):
                            st.success("✅ Compliance check passed")
                        else:
                            st.warning("⚠️ Compliance flags detected")
                            for flag in compliance_result.get("flags", []):
                                st.write(f"- [{flag['severity']}] {flag['message']}")
                    except Exception as e:
                        st.error(f"Q&A failed: {str(e)}")

    with tab_library:
        st.markdown("### 📁 Saved Article Library")

        if st.session_state.saved_articles:
            st.caption(f"{len(st.session_state.saved_articles)} articles in library")

            for i, article in enumerate(st.session_state.saved_articles):
                col_art, col_remove = st.columns([6, 1])
                with col_art:
                    st.markdown(f"**{article.get('title', 'Untitled')}**")
                    st.caption(f"{article.get('journal', '')} · {article.get('year', '')} · PMID: {article.get('pmid', '')}")
                with col_remove:
                    if st.button("🗑️", key=f"remove_{i}"):
                        st.session_state.saved_articles.pop(i)
                        st.rerun()
                st.markdown("---")

            if st.button("📥 Export Library as CSV", key="export_csv"):
                import pandas as pd
                df = pd.DataFrame(st.session_state.saved_articles)
                csv = df.to_csv(index=False)
                st.download_button(
                    "Download CSV",
                    csv,
                    "msl_literature_library.csv",
                    "text/csv",
                    key="download_csv"
                )
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">📁</div>
                <h3>No saved articles yet</h3>
                <p>Click the 💾 button on any search result to save it here</p>
            </div>
            """, unsafe_allow_html=True)

elif "search_results" in st.session_state and not st.session_state.search_results:
    st.info("No results found. Try adjusting your search terms.")

else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">🔍</div>
        <h3>Search scientific literature</h3>
        <p>Enter a query above or select a therapeutic area from the sidebar to get started</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**💡 Try these searches:**")

    suggestion_cols = st.columns(3)
    suggestions = [
        ("Oncology", "immunotherapy AND checkpoint inhibitors AND 2024[dp]"),
        ("Cardiology", "SGLT2 inhibitors AND heart failure AND meta-analysis"),
        ("Neurology", "lecanemab AND alzheimer AND clinical trial[pt]"),
    ]

    for col, (label, query) in zip(suggestion_cols, suggestions):
        with col:
            if st.button(f"🔬 {label}", use_container_width=True, key=f"sug_{label}"):
                st.session_state.search_input = query
                st.rerun()
