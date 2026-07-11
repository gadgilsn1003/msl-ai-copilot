import streamlit as st
import os
import sys
from pathlib import Path
from datetime import date
sys.path.append(str(Path(__file__).parent.parent))

from backend.llm_engine import generate_kol_briefing, extract_insights_from_notes
from backend.pubmed_fetcher import search_and_fetch, THERAPEUTIC_AREA_QUERIES
from backend.compliance_filter import scan_text, get_compliance_badge
from backend.database import init_db, add_kol, get_all_kols, log_interaction, search_kols

init_db()

st.set_page_config(page_title="KOL Briefing Generator | MSL AI Copilot",
                   page_icon="🧠", layout="wide")
st.title("🧠 KOL Briefing Generator")
st.caption("Generate personalized pre-meeting briefing sheets. Log field interactions. Extract insights.")

tab1, tab2, tab3, tab4 = st.tabs([
    "📄 Generate Briefing",
    "🗓️ Log Interaction",
    "🔍 Extract Insights",
    "👤 KOL Profiles"
])

with tab1:
    st.subheader("📄 Generate Pre-Meeting KOL Briefing")

    if not os.getenv("OPENAI_API_KEY"):
        st.warning("⚠️ Add your OpenAI API key in the sidebar to generate briefings.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            kol_name = st.text_input("KOL / HCP Name *", placeholder="Dr. Jane Smith")
            specialty = st.text_input("Specialty *", placeholder="Neuro-Oncology")
            institution = st.text_input("Institution *", placeholder="Massachusetts General Hospital")
        with c2:
            therapeutic_area = st.selectbox("Therapeutic Area",
                list(THERAPEUTIC_AREA_QUERIES.keys()))
            meeting_date = st.date_input("Meeting Date", value=date.today())

        field_notes = st.text_area(
            "Field Notes from Previous Interactions *",
            height=200,
            placeholder="""Example:
- Dr. Smith is interested in combination therapy approaches for recurrent GBM
- Previously discussed VEGF pathway inhibition - expressed skepticism about bevacizumab data
- Asked about ongoing clinical trials with CAR-T cell therapy in brain tumors
- Mentioned interest in biomarker-driven patient selection
- Follow up needed: send Phase III data from KEYNOTE-789"""
        )

        fetch_literature = st.checkbox("Also fetch relevant recent literature to include in briefing")

        if st.button("🧠 Generate Briefing", type="primary", use_container_width=True):
            if not all([kol_name, specialty, institution, field_notes]):
                st.error("Please fill in all required fields (marked with *)")
            else:
                relevant_articles = []
                if fetch_literature:
                    with st.spinner("Fetching relevant literature..."):
                        arts = search_and_fetch(
                            query=THERAPEUTIC_AREA_QUERIES.get(therapeutic_area, therapeutic_area),
                            max_results=5, sort_by="pub_date"
                        )
                        relevant_articles = [a.to_dict() for a in arts]

                with st.spinner("Generating personalized briefing..."):
                    try:
                        briefing = generate_kol_briefing(
                            kol_name=kol_name, specialty=specialty,
                            institution=institution, field_notes=field_notes,
                            relevant_articles=relevant_articles,
                            therapeutic_area=therapeutic_area
                        )
                        # Compliance check
                        report = scan_text(briefing)
                        badge_color, badge_label = get_compliance_badge(report)

                        st.divider()
                        st.markdown(f"### 📄 KOL Briefing: {kol_name}")
                        st.markdown(f"**Date:** {meeting_date} | **Compliance:** :{badge_color}[{badge_label}]")

                        if report.flags:
                            with st.expander("⚠️ Compliance Flags"):
                                for flag in report.flags:
                                    st.warning(f"**{flag.severity.value}** - {flag.category}: {flag.suggestion}")

                        st.markdown(briefing)

                        # Download button
                        st.download_button(
                            label="📥 Download Briefing (Markdown)",
                            data=f"# KOL Briefing: {kol_name}\n**Date:** {meeting_date}\n\n{briefing}",
                            file_name=f"briefing_{kol_name.replace(' ', '_')}_{meeting_date}.md",
                            mime="text/markdown"
                        )

                        # Auto-save KOL profile
                        kol_id = add_kol(kol_name, specialty, institution, therapeutic_area)
                        st.success(f"KOL profile auto-saved (ID: {kol_id})")

                    except Exception as e:
                        st.error(f"Error generating briefing: {e}")

with tab2:
    st.subheader("🗓️ Log Field Interaction")
    st.caption("Record MSL field calls, congress meetings, and advisory board interactions.")

    c1, c2 = st.columns(2)
    with c1:
        log_kol_name = st.text_input("HCP / KOL Name", placeholder="Dr. Jane Smith")
        interaction_date = st.date_input("Date", value=date.today())
    with c2:
        interaction_type = st.selectbox("Interaction Type",
            ["Field Call", "Congress Meeting", "Advisory Board",
             "Investigator Meeting", "Webinar", "Email Follow-up", "Other"])

    notes = st.text_area("Interaction Notes", height=150,
        placeholder="Describe the scientific topics discussed, questions asked, materials shared...")
    unmet_needs = st.text_area("Unmet Needs Identified", height=100,
        placeholder="What clinical gaps or unmet needs did the HCP express?")
    action_items = st.text_area("Action Items", height=100,
        placeholder="What follow-up actions are required? (e.g., send paper, schedule next call)")

    if st.button("💾 Save Interaction Log", type="primary"):
        if log_kol_name and notes:
            try:
                interaction_id = log_interaction(
                    kol_name=log_kol_name,
                    interaction_date=str(interaction_date),
                    interaction_type=interaction_type,
                    notes=notes,
                    unmet_needs=unmet_needs,
                    action_items=action_items
                )
                st.success(f"✅ Interaction logged successfully (ID: {interaction_id})")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please fill in at least HCP name and notes.")

with tab3:
    st.subheader("🔍 Extract Insights from Field Notes")
    st.caption("Paste raw field notes and let AI extract structured insights for reporting.")

    if not os.getenv("OPENAI_API_KEY"):
        st.warning("⚠️ OpenAI API key required for insight extraction.")
    else:
        ta_for_insights = st.selectbox("Therapeutic Area", list(THERAPEUTIC_AREA_QUERIES.keys()),
                                        key="ta_insights")
        raw_notes = st.text_area("Paste Field Notes Here", height=250,
            placeholder="Paste raw, unstructured field call notes here...")

        if st.button("🔍 Extract Insights", type="primary") and raw_notes:
            with st.spinner("Extracting structured insights..."):
                try:
                    result = extract_insights_from_notes(raw_notes, ta_for_insights)
                    st.markdown("### 📊 Extracted Insights")
                    st.markdown(result["raw_analysis"])
                    st.download_button("📥 Download Insights",
                        result["raw_analysis"], "insights.md", "text/markdown")
                except Exception as e:
                    st.error(f"Error: {e}")

with tab4:
    st.subheader("👤 KOL Profile Library")
    search_query = st.text_input("🔍 Search KOLs",
        placeholder="Search by name, institution, or specialty...")

    if search_query:
        kols = search_kols(search_query)
    else:
        kols = get_all_kols()

    if not kols:
        st.info("No KOL profiles yet. Generate a briefing or log an interaction to auto-create profiles.")
    else:
        st.markdown(f"**{len(kols)} KOL(s) found**")
        for kol in kols:
            with st.expander(f"👤 {kol['name']} - {kol.get('specialty', 'N/A')}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**Institution:** {kol.get('institution', 'N/A')}")
                    st.markdown(f"**Therapeutic Area:** {kol.get('therapeutic_area', 'N/A')}")
                with c2:
                    st.markdown(f"**Added:** {kol.get('created_at', 'N/A')[:10]}")
                    st.markdown(f"**ID:** {kol.get('id', 'N/A')}")
                if kol.get('notes'):
                    st.markdown(f"**Notes:** {kol['notes']}")
