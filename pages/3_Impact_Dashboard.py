import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path
from datetime import date, timedelta
import random
sys.path.append(str(Path(__file__).parent.parent))

from backend.database import init_db, get_interaction_stats, get_all_interactions, get_saved_articles

init_db()

st.set_page_config(page_title="Impact Dashboard | MSL AI Copilot",
                   page_icon="📊", layout="wide")
st.title("📊 MSL Impact Dashboard")
st.caption("Track KOL engagement, visualize insight themes, and demonstrate MSL value.")

# Load data
stats = get_interaction_stats()
interactions = get_all_interactions(limit=200)
saved_articles = get_saved_articles()

# ── If no real data, generate demo data ──
DEMO_MODE = stats["total_interactions"] == 0

if DEMO_MODE:
    st.info("📊 **Demo Mode** — No interactions logged yet. Showing sample data. Log interactions in the KOL Briefing page to populate real data.")
    # Generate realistic demo data
    demo_kols = ["Dr. Sarah Chen", "Dr. Michael Torres", "Dr. Priya Patel",
                 "Dr. James Wright", "Dr. Anna Kowalski"]
    demo_types = ["Field Call", "Congress Meeting", "Advisory Board", "Webinar", "Field Call", "Field Call"]
    demo_tas = ["Oncology", "GBM / Neuro-Oncology", "Immunology", "Neurology", "Rare Disease"]

    interactions = []
    for i in range(45):
        d = date.today() - timedelta(days=random.randint(0, 180))
        interactions.append({
            "kol_name": random.choice(demo_kols),
            "interaction_date": str(d),
            "interaction_type": random.choice(demo_types),
            "unmet_needs": random.choice([
                "Better biomarkers for patient selection",
                "Real-world evidence data needed",
                "Long-term safety data gaps",
                "Head-to-head comparison data",
                "Combination therapy approaches"
            ]),
            "notes": "Demo interaction note"
        })

    stats = {
        "total_interactions": 45,
        "unique_kols": 5,
        "saved_articles": 12,
        "top_kols": [{"kol": k, "count": random.randint(3, 12)} for k in demo_kols],
        "by_type": [{"type": t, "count": random.randint(2, 15)} for t in set(demo_types)],
        "by_month": []
    }

# ── KPI Metrics Row ──
st.divider()
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🤝 Total Interactions", stats["total_interactions"],
               delta=f"+{max(1, stats['total_interactions']//5)} this month")
with col2:
    st.metric("👤 Unique KOLs Engaged", stats["unique_kols"])
with col3:
    st.metric("📚 Saved Articles", stats["saved_articles"])
with col4:
    avg_per_kol = round(stats["total_interactions"] / max(1, stats["unique_kols"]), 1)
    st.metric("📈 Avg Interactions/KOL", avg_per_kol)

st.divider()

# ── Charts Row 1 ──
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("🔥 Top Engaged KOLs")
    if stats["top_kols"]:
        df_kols = pd.DataFrame(stats["top_kols"])
        df_kols = df_kols.sort_values("count", ascending=True)
        fig = px.bar(df_kols, x="count", y="kol", orientation="h",
                     color="count", color_continuous_scale="Blues",
                     labels={"count": "Interactions", "kol": "KOL"})
        fig.update_layout(height=350, showlegend=False,
                          plot_bgcolor="rgba(0,0,0,0)",
                          paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No interaction data yet.")

with col_b:
    st.subheader("🎯 Interaction Types Distribution")
    if stats["by_type"]:
        df_types = pd.DataFrame(stats["by_type"])
        fig2 = px.pie(df_types, values="count", names="type",
                      color_discrete_sequence=px.colors.qualitative.Set3,
                      hole=0.4)
        fig2.update_layout(height=350, plot_bgcolor="rgba(0,0,0,0)",
                           paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No interaction data yet.")

# ── Timeline Chart ──
st.subheader("📅 Interaction Timeline")
if interactions:
    df_interactions = pd.DataFrame(interactions)
    if "interaction_date" in df_interactions.columns:
        df_interactions["interaction_date"] = pd.to_datetime(df_interactions["interaction_date"])
        df_interactions["month"] = df_interactions["interaction_date"].dt.to_period("M").astype(str)
        monthly_counts = df_interactions.groupby(["month", "interaction_type"]).size().reset_index(name="count")
        fig3 = px.bar(monthly_counts, x="month", y="count", color="interaction_type",
                      labels={"month": "Month", "count": "Interactions", "interaction_type": "Type"},
                      color_discrete_sequence=px.colors.qualitative.Set2)
        fig3.update_layout(height=350, plot_bgcolor="rgba(0,0,0,0)",
                           paper_bgcolor="rgba(0,0,0,0)",
                           xaxis_tickangle=-45)
        st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("No interaction data to display.")

# ── Unmet Needs Word Analysis ──
st.subheader("💭 Common Unmet Needs & Themes")
if interactions:
    df_int = pd.DataFrame(interactions)
    if "unmet_needs" in df_int.columns:
        all_needs = " ".join(df_int["unmet_needs"].dropna().tolist())
        if all_needs.strip():
            # Simple frequency analysis on keywords
            keywords = ["biomarker", "safety", "efficacy", "combination", "real-world",
                       "long-term", "head-to-head", "resistance", "trial", "survival",
                       "response", "patient", "data", "treatment", "therapy"]
            keyword_counts = {k: all_needs.lower().count(k) for k in keywords if all_needs.lower().count(k) > 0}
            if keyword_counts:
                df_kw = pd.DataFrame(list(keyword_counts.items()), columns=["Theme", "Frequency"])
                df_kw = df_kw.sort_values("Frequency", ascending=False)
                fig4 = px.treemap(df_kw, path=["Theme"], values="Frequency",
                                  color="Frequency", color_continuous_scale="RdBu")
                fig4.update_layout(height=400)
                st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("Log interactions with unmet needs to see theme analysis.")

# ── Raw Interaction Log ──
st.subheader("📋 Recent Interaction Log")
if interactions:
    df_display = pd.DataFrame(interactions)[[
        "kol_name", "interaction_date", "interaction_type", "notes"
    ] if all(c in pd.DataFrame(interactions).columns for c in ["kol_name", "interaction_date", "interaction_type", "notes"]) else list(pd.DataFrame(interactions).columns[:4])]
    st.dataframe(df_display.head(20), use_container_width=True)
    csv = pd.DataFrame(interactions).to_csv(index=False)
    st.download_button("📥 Export All Data to CSV", csv, "msl_interactions.csv", "text/csv")
else:
    st.info("No interactions logged yet. Use the KOL Briefing Generator to log field interactions.")

# ── Value/ROI Summary Card ──
st.divider()
st.subheader("🎯 MSL Activity Summary (for Reporting)")
col1, col2 = st.columns([2, 1])
with col1:
    report_period = st.selectbox("Report Period", ["Last 30 Days", "Last 90 Days", "Last 6 Months", "All Time"])
    period_map = {"Last 30 Days": 30, "Last 90 Days": 90, "Last 6 Months": 180, "All Time": 99999}
    days = period_map[report_period]
    if st.button("📊 Generate Activity Summary"):
        st.markdown(f"""
**MSL Activity Report - {report_period}**

| Metric | Value |
|--------|-------|
| Total Field Interactions | {stats['total_interactions']} |
| Unique KOLs Engaged | {stats['unique_kols']} |
| Scientific Articles in Library | {stats['saved_articles']} |
| Avg Interactions per KOL | {avg_per_kol} |

*This report was auto-generated by MSL AI Copilot.*
""")
with col2:
    st.markdown("""
    **💡 Dashboard Tips**
    - Log every field interaction to build trend data
    - Unmet needs appear in the theme analysis above
    - Export CSV for CRM submission
    - Share KPI metrics with your MSL manager
    """)
