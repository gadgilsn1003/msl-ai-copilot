"""
👤 KOL Briefing Generator Module

Generate comprehensive, compliant briefing documents for KOL interactions
based on field notes, publication history, and research focus.
"""

import streamlit as st
import os
import sys
from datetime import datetime, date
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# =================================================================================
# PAGE CONFIG
# =================================================================================
st.set_page_config(
    page_title="MSL AI Copilot · KOL Briefing Generator",
    page_icon="👤",
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

    /* Page Header */
    .page-header {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 8px;
    }

    .page-header-icon {
        width: 52px;
        height: 52px;
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.12), rgba(139, 92, 246, 0.04));
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

    /* KOL Card */
    .kol-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 12px;
        transition: all 0.2s ease;
        cursor: pointer;
    }

    .kol-card:hover {
        border-color: #8b5cf6;
        box-shadow: 0 4px 16px rgba(139, 92, 246, 0.1);
    }

    .kol-name {
        font-size: 15px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 4px;
    }

    .kol-meta {
        font-size: 12px;
        color: #64748b;
    }

    /* Briefing Section */
    .briefing-section {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 16px;
    }

    .briefing-section h3 {
        font-size: 16px;
        font-weight: 700;
        color: #0f172a;
        margin: 0 0 12px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .briefing-section p {
        font-size: 14px;
        color: #475569;
        line-height: 1.7;
        margin: 0;
    }

    /* Interaction Log */
    .interaction-item {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
        border-left: 3px solid #8b5cf6;
    }

    .interaction-type {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #8b5cf6;
        margin-bottom: 4px;
    }

    .interaction-notes {
        font-size: 13px;
        color: #475569;
        line-height: 1.6;
    }

    .interaction-date {
        font-size: 11px;
        color: #94a3b8;
        margin-top: 6px;
    }

    /* Empty State */
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

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6, #7c3aed) !important;
        color: white !important;
        border: none !important;
        padding: 10px 20px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(139, 92, 246, 0.2) !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3) !important;
    }

    /* Sidebar */
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
        background: rgba(139, 92, 246, 0.06) !important;
        border-color: #8b5cf6 !important;
        color: #8b5cf6 !important;
        transform: none !important;
    }

    /* Hide Streamlit chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =================================================================================
# IMPORTS
# =================================================================================
try:
    from backend.llm_engine import generate_kol_briefing, extract_insights
    from backend.compliance_filter import screen_content
    from backend.database import (
        save_interaction, get_interactions_by_kol,
        save_kol_profile, get_all_kol_profiles, get_kol_profile
    )
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False

# =================================================================================
# SESSION STATE
# =================================================================================
if "kol_interactions" not in st.session_state:
    st.session_state.kol_interactions = []

if "kol_profiles" not in st.session_state:
    st.session_state.kol_profiles = []

if "current_briefing" not in st.session_state:
    st.session_state.current_briefing = None

# =================================================================================
# SIDEBAR
# =================================================================================
with st.sidebar:
    st.markdown("### 🧬 MSL AI Copilot")
    st.caption("KOL Briefing Generator")
    st.markdown("---")

    if st.button("🏠  Home", use_container_width=True, key="nav_home"):
        st.switch_page("app.py")
    if st.button("📚  Literature", use_container_width=True, key="nav_lit"):
        st.switch_page("pages/1_Literature_Intelligence.py")
    if st.button("📊  Impact Dashboard", use_container_width=True, key="nav_dash"):
        st.switch_page("pages/3_Impact_Dashboard.py")

    st.markdown("---")

    st.markdown("**KOL Profiles**")

    # Load profiles
    if BACKEND_AVAILABLE:
        try:
            profiles = get_all_kol_profiles()
            if profiles:
                for profile in profiles:
                    st.markdown(f"• **{profile['name']}**")
                    st.caption(f"  {profile.get('institution', 'Unknown')}")
            else:
                st.caption("No profiles saved yet")
        except Exception:
            st.caption("Add your first KOL below")
    else:
        st.caption("Backend not connected")

# =================================================================================
# PAGE HEADER
# =================================================================================
st.markdown("""
<div class="page-header">
    <div class="page-header-icon">👤</div>
    <div class="page-header-text">
        <h1>KOL Briefing Generator</h1>
        <p>Generate AI-powered pre-meeting briefings from field notes and publication history</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# =================================================================================
# MAIN INTERFACE
# =================================================================================
tab_briefing, tab_log, tab_profiles = st.tabs(["📋 Generate Briefing", "📝 Log Interaction", "👥 KOL Profiles"])

# =================================================================================
# TAB 1: GENERATE BRIEFING
# =================================================================================
with tab_briefing:
    st.markdown("### Generate Pre-Meeting Briefing")
    st.caption("Enter KOL details and field notes to generate a structured, compliant briefing document.")

    col_input, col_output = st.columns([1, 1], gap="large")

    with col_input:
        st.markdown("**KOL Information**")

        kol_name = st.text_input("KOL Name", placeholder="e.g., Dr. Sarah Chen", key="kol_name")
        kol_institution = st.text_input("Institution", placeholder="e.g., Memorial Sloan Kettering", key="kol_inst")
        kol_specialty = st.text_input("Specialty / Therapeutic Area", placeholder="e.g., Neuro-Oncology", key="kol_spec")

        st.markdown("---")
        st.markdown("**Field Notes & Context**")

        field_notes = st.text_area(
            "Meeting Notes / Context",
            placeholder="Paste your field notes, previous interaction summaries, or any context about this KOL...\n\nExample:\n- Met at ASCO 2024, discussed GBM treatment landscape\n- Interested in novel immunotherapy combinations\n- Raised concerns about BBB penetration of new agents\n- Currently running Phase II trial on tumor-treating fields",
            height=200,
            key="field_notes"
        )

        include_literature = st.checkbox("🔬 Enrich with live PubMed literature", value=True, key="include_lit")

        interaction_type = st.selectbox(
            "Upcoming Interaction Type",
            ["Pre-meeting briefing", "Congress follow-up", "Advisory board prep", "Routine field call"],
            key="interaction_type"
        )

        if st.button("🧠 Generate Briefing", use_container_width=True, key="gen_briefing"):
            if not kol_name or not field_notes:
                st.warning("Please enter KOL name and field notes.")
            elif not os.getenv("OPENAI_API_KEY"):
                st.error("OpenAI API key required. Configure in environment variables.")
            elif not BACKEND_AVAILABLE:
                st.error("Backend modules not available.")
            else:
                with st.spinner("Generating comprehensive briefing..."):
                    try:
                        briefing = generate_kol_briefing(
                            kol_name=kol_name,
                            institution=kol_institution,
                            specialty=kol_specialty,
                            field_notes=field_notes,
                            interaction_type=interaction_type,
                            include_literature=include_literature
                        )

                        # Compliance screen
                        compliance_result = screen_content(briefing)

                        st.session_state.current_briefing = {
                            "content": briefing,
                            "compliance": compliance_result,
                            "kol_name": kol_name,
                            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                        }

                    except Exception as e:
                        st.error(f"Briefing generation failed: {str(e)}")

    with col_output:
        if st.session_state.current_briefing:
            briefing_data = st.session_state.current_briefing

            st.markdown(f"**Briefing for {briefing_data['kol_name']}**")
            st.caption(f"Generated: {briefing_data['generated_at']}")

            # Compliance status
            if briefing_data["compliance"].get("passed", True):
                st.success("✅ Compliance screening passed")
            else:
                st.warning("⚠️ Compliance flags detected")
                for flag in briefing_data["compliance"].get("flags", []):
                    st.write(f"- **[{flag['severity']}]** {flag['message']}")

            st.markdown("---")

            # Display briefing
            st.markdown(briefing_data["content"])

            st.markdown("---")

            # Export options
            col_export1, col_export2 = st.columns(2)
            with col_export1:
                st.download_button(
                    "📥 Export as Markdown",
                    briefing_data["content"],
                    f"KOL_Briefing_{briefing_data['kol_name'].replace(' ', '_')}_{date.today()}.md",
                    "text/markdown",
                    use_container_width=True,
                    key="export_md"
                )
            with col_export2:
                if st.button("💾 Save to Profile", use_container_width=True, key="save_profile"):
                    st.toast("Briefing saved to KOL profile!", icon="✅")

        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">📋</div>
                <h3>Briefing will appear here</h3>
                <p>Fill in KOL details and field notes, then click Generate</p>
            </div>
            """, unsafe_allow_html=True)

# =================================================================================
# TAB 2: LOG INTERACTION
# =================================================================================
with tab_log:
    st.markdown("### Log Field Interaction")
    st.caption("Record KOL interactions for tracking and future briefing enrichment.")

    col_form, col_history = st.columns([1, 1], gap="large")

    with col_form:
        with st.form("interaction_form", clear_on_submit=True):
            log_kol_name = st.text_input("KOL Name", placeholder="Dr. Sarah Chen", key="log_kol")
            log_type = st.selectbox(
                "Interaction Type",
                ["Field Call", "Congress Meeting", "Advisory Board", "Investigator Meeting", "Email/Virtual", "Other"],
                key="log_type"
            )
            log_date = st.date_input("Date", value=date.today(), key="log_date")
            log_ta = st.selectbox(
                "Therapeutic Area",
                ["Oncology", "Immunology", "Cardiology", "Neurology", "Rare Disease", "Other"],
                key="log_ta"
            )
            log_notes = st.text_area(
                "Interaction Notes",
                placeholder="What was discussed? Key insights, questions raised, follow-up needed...",
                height=150,
                key="log_notes"
            )
            log_followup = st.text_input("Follow-up Actions", placeholder="e.g., Send Phase III data, schedule follow-up call", key="log_followup")

            submitted = st.form_submit_button("📝 Log Interaction", use_container_width=True)

            if submitted:
                if log_kol_name and log_notes:
                    interaction = {
                        "kol_name": log_kol_name,
                        "type": log_type,
                        "date": str(log_date),
                        "therapeutic_area": log_ta,
                        "notes": log_notes,
                        "followup": log_followup,
                        "logged_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    st.session_state.kol_interactions.append(interaction)

                    if BACKEND_AVAILABLE:
                        try:
                            save_interaction(interaction)
                        except Exception:
                            pass

                    st.success("✅ Interaction logged successfully!")
                else:
                    st.warning("Please enter KOL name and notes.")

    with col_history:
        st.markdown("**Recent Interactions**")

        if st.session_state.kol_interactions:
            for interaction in reversed(st.session_state.kol_interactions[-10:]):
                st.markdown(f"""
                <div class="interaction-item">
                    <div class="interaction-type">{interaction['type']} · {interaction['therapeutic_area']}</div>
                    <div class="kol-name">{interaction['kol_name']}</div>
                    <div class="interaction-notes">{interaction['notes'][:200]}{'...' if len(interaction['notes']) > 200 else ''}</div>
                    <div class="interaction-date">📅 {interaction['date']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">📝</div>
                <h3>No interactions logged yet</h3>
                <p>Use the form to record your KOL interactions</p>
            </div>
            """, unsafe_allow_html=True)

# =================================================================================
# TAB 3: KOL PROFILES
# =================================================================================
with tab_profiles:
    st.markdown("### KOL Profile Library")
    st.caption("Manage your KOL profiles and view interaction history.")

    col_add, col_list = st.columns([1, 1], gap="large")

    with col_add:
        st.markdown("**Add New KOL Profile**")

        with st.form("kol_profile_form", clear_on_submit=True):
            prof_name = st.text_input("Full Name", placeholder="Dr. Jane Smith", key="prof_name")
            prof_institution = st.text_input("Institution", placeholder="Johns Hopkins University", key="prof_inst")
            prof_specialty = st.text_input("Specialty", placeholder="Medical Oncology", key="prof_spec")
            prof_ta = st.selectbox("Primary Therapeutic Area",
                ["Oncology", "Immunology", "Cardiology", "Neurology", "Rare Disease", "Other"],
                key="prof_ta"
            )
            prof_tier = st.selectbox("KOL Tier", ["Tier 1 (National)", "Tier 2 (Regional)", "Tier 3 (Local)"], key="prof_tier")
            prof_notes = st.text_area("Notes", placeholder="Key research interests, relationship status, etc.", height=100, key="prof_notes")

            if st.form_submit_button("➕ Add Profile", use_container_width=True):
                if prof_name:
                    profile = {
                        "name": prof_name,
                        "institution": prof_institution,
                        "specialty": prof_specialty,
                        "therapeutic_area": prof_ta,
                        "tier": prof_tier,
                        "notes": prof_notes,
                        "created_at": datetime.now().strftime("%Y-%m-%d")
                    }
                    st.session_state.kol_profiles.append(profile)

                    if BACKEND_AVAILABLE:
                        try:
                            save_kol_profile(profile)
                        except Exception:
                            pass

                    st.success(f"✅ Profile created for {prof_name}")
                else:
                    st.warning("Please enter KOL name.")

    with col_list:
        st.markdown("**Saved Profiles**")

        profiles_to_show = st.session_state.kol_profiles

        if profiles_to_show:
            search_profiles = st.text_input("🔍 Search profiles", placeholder="Filter by name...", key="search_prof")

            for profile in profiles_to_show:
                if search_profiles and search_profiles.lower() not in profile["name"].lower():
                    continue

                st.markdown(f"""
                <div class="kol-card">
                    <div class="kol-name">{profile['name']}</div>
                    <div class="kol-meta">
                        🏥 {profile.get('institution', 'N/A')} · 🔬 {profile.get('specialty', 'N/A')} · {profile.get('tier', '')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">👥</div>
                <h3>No KOL profiles yet</h3>
                <p>Add your first KOL profile using the form</p>
            </div>
            """, unsafe_allow_html=True)
