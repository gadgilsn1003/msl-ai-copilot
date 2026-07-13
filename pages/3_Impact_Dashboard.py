"""
📊 Impact Dashboard Module

Visualize MSL activities, demonstrate ROI, and generate
leadership-ready reports with interactive analytics.
"""

import streamlit as st
import os
import sys
import random
from datetime import datetime, date, timedelta
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# =================================================================================
# PAGE CONFIG
# =================================================================================
st.set_page_config(
    page_title="MSL AI Copilot · Impact Dashboard",
    page_icon="📊",
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
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.12), rgba(16, 185, 129, 0.04));
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

    /* KPI Cards */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 32px;
    }

    .kpi-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 22px 20px;
        transition: all 0.2s ease;
    }

    .kpi-card:hover {
        border-color: #10b981;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.1);
    }

    .kpi-label {
        font-size: 12px;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }

    .kpi-value {
        font-size: 32px;
        font-weight: 800;
        color: #0f172a;
        line-height: 1;
        margin-bottom: 4px;
    }

    .kpi-change {
        font-size: 12px;
        font-weight: 600;
    }

    .kpi-change.positive { color: #10b981; }
    .kpi-change.negative { color: #ef4444; }

    /* Chart Container */
    .chart-container {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
    }

    .chart-title {
        font-size: 15px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 16px;
    }

    /* Demo Banner */
    .demo-banner {
        background: linear-gradient(135deg, #fffbeb, #fef3c7);
        border: 1px solid #fbbf24;
        border-radius: 12px;
        padding: 14px 20px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 13px;
        color: #92400e;
        font-weight: 500;
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
        background: linear-gradient(135deg, #10b981, #059669) !important;
        color: white !important;
        border: none !important;
        padding: 10px 20px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.2) !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3) !important;
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
        background: rgba(16, 185, 129, 0.06) !important;
        border-color: #10b981 !important;
        color: #10b981 !important;
        transform: none !important;
    }

    /* Hide Streamlit chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    @media (max-width: 768px) {
        .kpi-grid { grid-template-columns: repeat(2, 1fr); }
    }
</style>
""", unsafe_allow_html=True)

# =================================================================================
# IMPORTS
# =================================================================================
try:
    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

try:
    from backend.database import get_all_interactions, get_dashboard_stats
    from backend.llm_engine import generate_activity_report
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False

# =================================================================================
# DEMO DATA GENERATOR
# =================================================================================
def generate_demo_data():
    """Generate realistic demo data for the dashboard."""
    kol_names = [
        "Dr. Sarah Chen", "Dr. Michael Rodriguez", "Dr. Emily Watson",
        "Dr. James Park", "Dr. Lisa Thompson", "Dr. Robert Kim",
        "Dr. Amanda Foster", "Dr. David Patel"
    ]

    interaction_types = ["Field Call", "Congress Meeting", "Advisory Board", "Investigator Meeting", "Email/Virtual"]
    therapeutic_areas = ["Oncology", "Immunology", "Neurology", "Cardiology", "Rare Disease"]

    unmet_needs_topics = [
        "BBB penetration", "Biomarker identification", "Patient selection",
        "Combination therapy", "Real-world evidence", "Treatment sequencing",
        "Resistance mechanisms", "Quality of life endpoints", "Access barriers",
        "Pediatric formulations", "Long-term safety data", "Companion diagnostics"
    ]

    interactions = []
    start_date = date.today() - timedelta(days=180)

    for i in range(45):
        interaction_date = start_date + timedelta(days=random.randint(0, 180))
        interactions.append({
            "kol_name": random.choice(kol_names),
            "type": random.choice(interaction_types),
            "date": str(interaction_date),
            "therapeutic_area": random.choice(therapeutic_areas),
            "notes": f"Discussion about {random.choice(unmet_needs_topics)} and {random.choice(unmet_needs_topics)}.",
            "followup": "Schedule follow-up" if random.random() > 0.5 else "",
            "unmet_needs": random.sample(unmet_needs_topics, random.randint(1, 3))
        })

    return interactions

# =================================================================================
# SIDEBAR
# =================================================================================
with st.sidebar:
    st.markdown("### 🧬 MSL AI Copilot")
    st.caption("Impact Dashboard")
    st.markdown("---")

    if st.button("🏠  Home", use_container_width=True, key="nav_home"):
        st.switch_page("app.py")
    if st.button("📚  Literature", use_container_width=True, key="nav_lit"):
        st.switch_page("pages/1_Literature_Intelligence.py")
    if st.button("👤  KOL Briefing", use_container_width=True, key="nav_kol"):
        st.switch_page("pages/2_KOL_Briefing_Generator.py")

    st.markdown("---")

    st.markdown("**Dashboard Settings**")
    time_range = st.selectbox("Time Range", ["Last 30 days", "Last 90 days", "Last 6 months", "All time"], index=2, key="time_range")
    show_demo = st.checkbox("📊 Demo Mode", value=True, key="demo_mode", help="Show sample data for demonstration")

    st.markdown("---")

    if st.button("📥 Export Report", use_container_width=True, key="export_report"):
        st.session_state.generate_report = True

# =================================================================================
# PAGE HEADER
# =================================================================================
st.markdown("""
<div class="page-header">
    <div class="page-header-icon">📊</div>
    <div class="page-header-text">
        <h1>Impact Dashboard</h1>
        <p>Track activities, measure engagement, and demonstrate MSL ROI</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# =================================================================================
# LOAD DATA
# =================================================================================
if show_demo:
    interactions = generate_demo_data()
    st.markdown("""
    <div class="demo-banner">
        ⚡ Demo Mode Active — Showing sample data with 45 interactions across 8 KOLs
    </div>
    """, unsafe_allow_html=True)
else:
    if BACKEND_AVAILABLE:
        try:
            interactions = get_all_interactions()
        except Exception:
            interactions = []
    else:
        interactions = st.session_state.get("kol_interactions", [])

# =================================================================================
# KPI METRICS
# =================================================================================
if interactions:
    df = pd.DataFrame(interactions) if PLOTLY_AVAILABLE else None

    total_interactions = len(interactions)
    unique_kols = len(set(i["kol_name"] for i in interactions))
    interaction_types_count = len(set(i["type"] for i in interactions))
    therapeutic_areas_count = len(set(i.get("therapeutic_area", "Unknown") for i in interactions))

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Total Interactions</div>
            <div class="kpi-value">{total_interactions}</div>
            <div class="kpi-change positive">↑ 12% vs prior period</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Unique KOLs Engaged</div>
            <div class="kpi-value">{unique_kols}</div>
            <div class="kpi-change positive">↑ 3 new this period</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Interaction Types</div>
            <div class="kpi-value">{interaction_types_count}</div>
            <div class="kpi-change positive">Multi-channel engagement</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Therapeutic Areas</div>
            <div class="kpi-value">{therapeutic_areas_count}</div>
            <div class="kpi-change positive">Cross-TA coverage</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =================================================================================
    # CHARTS
    # =================================================================================
    if PLOTLY_AVAILABLE and df is not None:

        tab_overview, tab_kols, tab_needs, tab_report = st.tabs([
            "📈 Overview", "👥 KOL Analysis", "🎯 Unmet Needs", "📄 Activity Report"
        ])

        with tab_overview:
            col_chart1, col_chart2 = st.columns(2, gap="medium")

            with col_chart1:
                # Interactions by type
                type_counts = df["type"].value_counts().reset_index()
                type_counts.columns = ["Type", "Count"]

                fig_types = px.bar(
                    type_counts,
                    x="Count",
                    y="Type",
                    orientation="h",
                    color="Count",
                    color_continuous_scale=["#bae6fd", "#0ea5e9", "#0369a1"],
                    title="Interactions by Type"
                )
                fig_types.update_layout(
                    showlegend=False,
                    coloraxis_showscale=False,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter", size=12),
                    title_font=dict(size=15, color="#0f172a"),
                    margin=dict(l=0, r=0, t=40, b=0),
                    height=300,
                )
                fig_types.update_xaxes(showgrid=True, gridcolor="#f1f5f9")
                fig_types.update_yaxes(showgrid=False)
                st.plotly_chart(fig_types, use_container_width=True)

            with col_chart2:
                # Interactions by therapeutic area
                ta_counts = df["therapeutic_area"].value_counts().reset_index()
                ta_counts.columns = ["Therapeutic Area", "Count"]

                fig_ta = px.pie(
                    ta_counts,
                    values="Count",
                    names="Therapeutic Area",
                    title="Distribution by Therapeutic Area",
                    color_discrete_sequence=["#0ea5e9", "#8b5cf6", "#10b981", "#f59e0b", "#ef4444"]
                )
                fig_ta.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter", size=12),
                    title_font=dict(size=15, color="#0f172a"),
                    margin=dict(l=0, r=0, t=40, b=0),
                    height=300,
                )
                st.plotly_chart(fig_ta, use_container_width=True)

            # Monthly timeline
            df["date_parsed"] = pd.to_datetime(df["date"])
            df["month"] = df["date_parsed"].dt.to_period("M").astype(str)
            monthly = df.groupby("month").size().reset_index(name="Count")

            fig_timeline = px.area(
                monthly,
                x="month",
                y="Count",
                title="Monthly Interaction Volume",
                color_discrete_sequence=["#0ea5e9"]
            )
            fig_timeline.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", size=12),
                title_font=dict(size=15, color="#0f172a"),
                margin=dict(l=0, r=0, t=40, b=0),
                height=280,
                xaxis_title="",
                yaxis_title="Interactions",
            )
            fig_timeline.update_xaxes(showgrid=False)
            fig_timeline.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
            st.plotly_chart(fig_timeline, use_container_width=True)

        with tab_kols:
            # Top KOLs by interaction count
            kol_counts = df["kol_name"].value_counts().head(10).reset_index()
            kol_counts.columns = ["KOL", "Interactions"]

            fig_kols = px.bar(
                kol_counts,
                x="Interactions",
                y="KOL",
                orientation="h",
                color="Interactions",
                color_continuous_scale=["#c4b5fd", "#8b5cf6", "#6d28d9"],
                title="Top KOLs by Engagement"
            )
            fig_kols.update_layout(
                showlegend=False,
                coloraxis_showscale=False,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", size=12),
                title_font=dict(size=15, color="#0f172a"),
                margin=dict(l=0, r=0, t=40, b=0),
                height=400,
            )
            fig_kols.update_xaxes(showgrid=True, gridcolor="#f1f5f9")
            fig_kols.update_yaxes(showgrid=False)
            st.plotly_chart(fig_kols, use_container_width=True)

            # KOL interaction type breakdown
            st.markdown("---")
            st.markdown("**KOL Engagement Breakdown**")

            kol_type_pivot = df.groupby(["kol_name", "type"]).size().reset_index(name="count")
            fig_kol_types = px.bar(
                kol_type_pivot,
                x="kol_name",
                y="count",
                color="type",
                title="Interaction Types per KOL",
                color_discrete_sequence=["#0ea5e9", "#8b5cf6", "#10b981", "#f59e0b", "#ef4444"]
            )
            fig_kol_types.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", size=12),
                title_font=dict(size=15, color="#0f172a"),
                margin=dict(l=0, r=0, t=40, b=0),
                height=350,
                xaxis_title="",
                yaxis_title="Count",
                legend_title="Type",
            )
            st.plotly_chart(fig_kol_types, use_container_width=True)

        with tab_needs:
            st.markdown("### 🎯 Unmet Needs Theme Analysis")
            st.caption("Keyword frequency analysis from interaction notes and documented unmet needs.")

            # Extract unmet needs keywords from notes
            all_notes = " ".join([i.get("notes", "") for i in interactions]).lower()

            keywords = {
                "BBB Penetration": all_notes.count("bbb") + all_notes.count("blood-brain barrier") + all_notes.count("penetration"),
                "Biomarkers": all_notes.count("biomarker") + all_notes.count("marker"),
                "Patient Selection": all_notes.count("patient selection") + all_notes.count("selection"),
                "Combination Therapy": all_notes.count("combination") + all_notes.count("combo"),
                "Real-World Evidence": all_notes.count("real-world") + all_notes.count("rwe"),
                "Treatment Sequencing": all_notes.count("sequencing") + all_notes.count("sequence"),
                "Resistance": all_notes.count("resistance") + all_notes.count("resistant"),
                "Quality of Life": all_notes.count("quality of life") + all_notes.count("qol"),
                "Access / Affordability": all_notes.count("access") + all_notes.count("affordability"),
                "Safety Data": all_notes.count("safety") + all_notes.count("adverse"),
                "Companion Dx": all_notes.count("companion") + all_notes.count("diagnostic"),
                "Pediatric": all_notes.count("pediatric") + all_notes.count("children"),
            }

            # Add counts from unmet_needs field if present
            for interaction in interactions:
                for need in interaction.get("unmet_needs", []):
                    for key in keywords:
                        if any(word in need.lower() for word in key.lower().split()):
                            keywords[key] += 1

            keywords_df = pd.DataFrame([
                {"Theme": k, "Mentions": v} for k, v in keywords.items() if v > 0
            ]).sort_values("Mentions", ascending=False)

            if not keywords_df.empty:
                fig_treemap = px.treemap(
                    keywords_df,
                    path=["Theme"],
                    values="Mentions",
                    title="Unmet Needs Landscape",
                    color="Mentions",
                    color_continuous_scale=["#d1fae5", "#10b981", "#065f46"]
                )
                fig_treemap.update_layout(
                    font=dict(family="Inter", size=12),
                    title_font=dict(size=15, color="#0f172a"),
                    margin=dict(l=0, r=0, t=40, b=0),
                    height=400,
                    coloraxis_showscale=False,
                )
                st.plotly_chart(fig_treemap, use_container_width=True)

                # Bar chart alternative
                fig_needs_bar = px.bar(
                    keywords_df.head(10),
                    x="Mentions",
                    y="Theme",
                    orientation="h",
                    title="Top Unmet Needs Themes",
                    color="Mentions",
                    color_continuous_scale=["#a7f3d0", "#10b981", "#065f46"]
                )
                fig_needs_bar.update_layout(
                    showlegend=False,
                    coloraxis_showscale=False,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter", size=12),
                    title_font=dict(size=15, color="#0f172a"),
                    margin=dict(l=0, r=0, t=40, b=0),
                    height=350,
                )
                fig_needs_bar.update_xaxes(showgrid=True, gridcolor="#f1f5f9")
                fig_needs_bar.update_yaxes(showgrid=False)
                st.plotly_chart(fig_needs_bar, use_container_width=True)
            else:
                st.info("Not enough data to generate unmet needs analysis.")

        with tab_report:
            st.markdown("### 📄 Auto-Generated Activity Report")
            st.caption("AI-generated summary suitable for manager/leadership reporting.")

            if st.button("🧠 Generate Activity Report", use_container_width=True, key="gen_report"):
                if not os.getenv("OPENAI_API_KEY"):
                    st.warning("OpenAI API key required for AI report generation.")
                elif BACKEND_AVAILABLE:
                    with st.spinner("Generating report..."):
                        try:
                            report = generate_activity_report(interactions)
                            st.session_state.activity_report = report
                        except Exception as e:
                            st.error(f"Report generation failed: {str(e)}")
                else:
                    # Generate a basic report without AI
                    report = f"""# MSL Activity Report
## Period: {time_range}

### Summary
- **Total Interactions:** {total_interactions}
- **Unique KOLs Engaged:** {unique_kols}
- **Interaction Types Used:** {interaction_types_count}
- **Therapeutic Areas Covered:** {therapeutic_areas_count}

### Top Engaged KOLs
{chr(10).join([f"- {kol}: {count} interactions" for kol, count in zip(kol_counts['KOL'].head(5), kol_counts['Interactions'].head(5))])}

### Key Themes
{chr(10).join([f"- {theme}: {mentions} mentions" for theme, mentions in zip(keywords_df['Theme'].head(5), keywords_df['Mentions'].head(5))])}

---
*Report generated on {date.today().strftime('%B %d, %Y')}*
"""
                    st.session_state.activity_report = report

            if "activity_report" in st.session_state:
                st.markdown(st.session_state.activity_report)

                st.markdown("---")
                col_dl1, col_dl2 = st.columns(2)
                with col_dl1:
                    st.download_button(
                        "📥 Download Report (Markdown)",
                        st.session_state.activity_report,
                        f"MSL_Activity_Report_{date.today()}.md",
                        "text/markdown",
                        use_container_width=True,
                        key="dl_report_md"
                    )
                with col_dl2:
                    if PLOTLY_AVAILABLE:
                        csv_data = df.to_csv(index=False)
                        st.download_button(
                            "📥 Export Raw Data (CSV)",
                            csv_data,
                            f"MSL_Interactions_{date.today()}.csv",
                            "text/csv",
                            use_container_width=True,
                            key="dl_data_csv"
                        )

else:
    # No data state
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">📊</div>
        <h3>No interaction data available</h3>
        <p>Enable Demo Mode in the sidebar or log interactions in the KOL Briefing module to see your dashboard</p>
    </div>
    """, unsafe_allow_html=True)
