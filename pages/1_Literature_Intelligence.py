import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from backend.pubmed_fetcher import search_and_fetch, THERAPEUTIC_AREA_QUERIES
from backend.llm_engine import summarize_article, build_rag_index, ask_literature
from backend.compliance_filter import scan_text, get_compliance_badge, MSL_BEST_PRACTICES
from backend.database import init_db, save_article

init_db()

st.set_page_config(page_title="Literature Intelligence | MSL AI Copilot",
                   page_icon="📚", layout="wide")
st.title("📚 Literature Intelligence")
st.caption("Search PubMed in real-time. Get AI summaries. Check compliance. Save to your library.")

col1, col2 = st.columns([3, 1])
with col1:
    query = st.text_input("🔍 Search Query",
        placeholder="e.g., glioblastoma temozolomide resistance mechanisms",
        help="Supports full PubMed/Entrez syntax")
with col2:
    ta_preset = st.selectbox("Or pick therapeutic area",
        options=["— Custom —"] + list(THERAPEUTIC_AREA_QUERIES.keys()))

col3, col4, col5 = st.columns(3)
with col3:
    max_results = st.slider("Max Results", 5, 50, 20)
with col4:
    sort_by = st.selectbox("Sort By", ["relevance", "pub_date"])
with col5:
    year_range = st.slider("Year Range", 2010, 2026, (2020, 2026))

search_btn = st.button("🔍 Search PubMed", type="primary", use_container_width=True)

if search_btn:
    final_query = THERAPEUTIC_AREA_QUERIES.get(ta_preset, query) if ta_preset != "— Custom —" else query
    if not final_query.strip():
        st.warning("Please enter a search query or select a therapeutic area.")
        st.stop()
    with st.spinner(f"Searching PubMed for: *{final_query}*..."):
        articles = search_and_fetch(query=final_query, max_results=max_results,
                                    date_range=(year_range[0], year_range[1]), sort_by=sort_by)
    if not articles:
        st.error("No articles found. Try broadening your search terms.")
        st.stop()
    st.success(f"Found **{len(articles)}** articles")
    st.session_state["articles"] = [a.to_dict() for a in articles]
    st.session_state["query"] = final_query
    if os.getenv("OPENAI_API_KEY"):
        with st.spinner("Building AI index for Q&A..."):
            st.session_state["rag_index"] = build_rag_index(st.session_state["articles"])

if "articles" in st.session_state and st.session_state["articles"]:
    articles = st.session_state["articles"]
    tab1, tab2, tab3 = st.tabs(["📝 Article List", "🧠 AI Summaries", "💬 Ask the Literature"])

    with tab1:
        st.subheader(f"Results for: *{st.session_state.get('query', '')}*")
        for i, art in enumerate(articles):
            with st.expander(f"📄 {art['title'][:100]}", expanded=(i == 0)):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"**Authors:** {art['authors']}")
                    st.markdown(f"**Journal:** {art['journal']} | **Date:** {art['pub_date']}")
                    if art.get('doi'):
                        st.markdown(f"**DOI:** {art['doi']}")
                    st.markdown("**Abstract:**")
                    st.write(art['abstract'])
                    if art.get('mesh_terms'):
                        st.markdown(f"**MeSH:** {', '.join(art['mesh_terms'][:6])}")
                with c2:
                    st.link_button("🔗 View on PubMed", art['url'])
                    if st.button("🔖 Save to Library", key=f"save_{i}"):
                        if save_article(art):
                            st.success("Saved!")
                        else:
                            st.error("Error saving.")
        df = pd.DataFrame(articles)
        st.download_button("📥 Export to CSV", df.to_csv(index=False), "pubmed_results.csv", "text/csv")

    with tab2:
        st.subheader("🧠 AI-Powered Summaries with Compliance Check")
        if not os.getenv("OPENAI_API_KEY"):
            st.warning("⚠️ Add OpenAI API key in the sidebar to enable AI summaries.")
        else:
            summary_style = st.selectbox("Summary Style",
                ["standard", "bullet", "hcp_talking_points"],
                format_func=lambda x: {"standard": "Standard Paragraph",
                                        "bullet": "Bullet Points",
                                        "hcp_talking_points": "HCP Talking Points"}[x])
            focus_area = st.text_input("Focus on (optional)",
                placeholder="e.g., safety profile, mechanism of action")
            for i, art in enumerate(articles[:10]):
                with st.expander(f"Summarize: {art['title'][:80]}"):
                    if st.button("Generate Summary", key=f"sum_{i}"):
                        with st.spinner("Generating AI summary..."):
                            try:
                                summary = summarize_article(art['title'], art['abstract'],
                                    focus=focus_area or None, style=summary_style)
                                report = scan_text(summary)
                                badge_color, badge_label = get_compliance_badge(report)
                                st.markdown("**AI Summary:**")
                                st.write(summary)
                                st.markdown(f"**Compliance:** :{badge_color}[{badge_label}]")
                                for flag in report.flags:
                                    st.warning(f"**{flag.severity.value} - {flag.category}**: {flag.suggestion}")
                            except ValueError as e:
                                st.error(str(e))

    with tab3:
        st.subheader("💬 Ask the Literature (RAG Q&A)")
        if "rag_index" not in st.session_state:
            st.info("Run a search first, then ask questions about the retrieved articles.")
        else:
            question = st.text_input("Ask a question",
                placeholder="What do these studies say about PD-L1 expression in GBM?")
            if st.button("Ask", type="primary") and question:
                with st.spinner("Searching through articles..."):
                    try:
                        result = ask_literature(question, st.session_state["rag_index"])
                        st.markdown("**Answer:**")
                        st.write(result["answer"])
                        if result.get("sources"):
                            st.markdown("**Sources:**")
                            for src in result["sources"]:
                                st.markdown(f"- [{src['title']}]({src['url']})")
                    except Exception as e:
                        st.error(f"Error: {e}")

with st.sidebar:
    st.markdown("### 📋 MSL Best Practices")
    for practice in MSL_BEST_PRACTICES:
        st.markdown(f"- {practice}")
