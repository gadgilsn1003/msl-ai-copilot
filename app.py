"""
MSL AI Copilot - Main Entry Point
Production-ready landing page with professional branding.
"""

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# =================================================================================
# PAGE CONFIG
# =================================================================================
st.set_page_config(
    page_title="MSL AI Copilot",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =================================================================================
# PRODUCTION CSS
# =================================================================================
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background: #f8fafc;
    }

    .block-container {
        padding: 2rem 3rem;
        max-width: 1200px;
    }

    .hero {
        background: linear-gradient(160deg, #0f172a 0%, #1e293b 40%, #0f172a 100%);
        padding: 72px 48px;
        border-radius: 20px;
        text-align: center;
        position: relative;
        overflow: hidden;
        margin-bottom: 40px;
        border: 1px solid rgba(14, 165, 233, 0.15);
    }

    .hero::before {
        content: '';
        position: absolute;
        inset: 0;
        background:
            radial-gradient(ellipse at 25% 0%, rgba(14, 165, 233, 0.18) 0%, transparent 50%),
            radial-gradient(ellipse at 75% 100%, rgba(56, 189, 248, 0.12) 0%, transparent 50%);
        pointer-events: none;
    }

    .hero::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(14, 165, 233, 0.5), transparent);
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(14, 165, 233, 0.1);
        border: 1px solid rgba(14, 165, 233, 0.25);
        color: #38bdf8;
        padding: 6px 14px;
        border-radius: 100px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        margin-bottom: 28px;
        position: relative;
        z-index: 1;
    }

    .hero-title {
        font-size: 48px;
        font-weight: 900;
        color: #f1f5f9;
        margin: 0 0 16px 0;
        line-height: 1.1;
        letter-spacing: -1.5px;
        position: relative;
        z-index: 1;
    }

    .hero-title .accent {
        background: linear-gradient(135deg, #38bdf8, #0ea5e9, #0284c7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-desc {
        font-size: 17px;
        color: #94a3b8;
        max-width: 580px;
        margin: 0 auto;
        line-height: 1.7;
        position: relative;
        z-index: 1;
        font-weight: 400;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 48px;
    }

    .stat-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 24px 16px;
        text-align: center;
        transition: all 0.2s ease;
    }

    .stat-card:hover {
        border-color: #0ea5e9;
        box-shadow: 0 4px 20px rgba(14, 165, 233, 0.1);
        transform: translateY(-2px);
    }

    .stat-value {
        font-size: 32px;
        font-weight: 800;
        color: #0ea5e9;
        margin-bottom: 4px;
        letter-spacing: -0.5px;
    }

    .stat-label {
        font-size: 12px;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .section-hdr {
        text-align: center;
        margin: 0 0 32px 0;
    }

    .section-hdr h2 {
        font-size: 28px;
        font-weight: 800;
        color: #0f172a;
        margin: 0 0 6px 0;
        letter-spacing: -0.5px;
    }

    .section-hdr p {
        font-size: 15px;
        color: #64748b;
        margin: 0;
        font-weight: 400;
    }

    .module-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 32px 28px;
        transition: all 0.25s ease;
        height: 100%;
        position: relative;
        overflow: hidden;
    }

    .module-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #0ea5e9, #38bdf8);
        opacity: 0;
        transition: opacity 0.25s ease;
    }

    .module-card:hover {
        border-color: #0ea5e9;
        box-shadow: 0 12px 40px rgba(14, 165, 233, 0.12);
        transform: translateY(-4px);
    }

    .module-card:hover::before {
        opacity: 1;
    }

    .module-icon {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.1), rgba(14, 165, 233, 0.05));
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        margin-bottom: 18px;
    }

    .module-title {
        font-size: 18px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 10px;
    }

    .module-desc {
        font-size: 14px;
        color: #64748b;
        line-height: 1.6;
        margin-bottom: 18px;
    }

    .module-features {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .module-features li {
        font-size: 13px;
        color: #475569;
        padding: 5px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .module-features li::before {
        content: '';
        width: 6px;
        height: 6px;
        background: #0ea5e9;
        border-radius: 50%;
        flex-shrink: 0;
    }

    .tech-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 12px;
        margin-top: 16px;
    }

    .tech-chip {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 14px 12px;
        text-align: center;
        font-size: 13px;
        font-weight: 600;
        color: #334155;
        transition: all 0.2s ease;
    }

    .tech-chip:hover {
        border-color: #0ea5e9;
        background: rgba(14, 165, 233, 0.04);
    }

    .tech-chip .tech-icon {
        display: block;
        font-size: 22px;
        margin-bottom: 6px;
    }

    .compliance-banner {
        background: linear-gradient(135deg, #f0fdf4, #ecfdf5);
        border: 1px solid #86efac;
        border-radius: 14px;
        padding: 24px 28px;
        display: flex;
        align-items: flex-start;
        gap: 16px;
        margin: 32px 0;
    }

    .compliance-icon {
        font-size: 28px;
        flex-shrink: 0;
    }

    .compliance-text h4 {
        font-size: 15px;
        font-weight: 700;
        color: #166534;
        margin: 0 0 4px 0;
    }

    .compliance-text p {
        font-size: 13px;
        color: #15803d;
        margin: 0;
        line-height: 1.6;
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
        letter-spacing: 0.2px !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(14, 165, 233, 0.3) !important;
        background: linear-gradient(135deg, #0284c7, #0369a1) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
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
        text-align: left !important;
        font-weight: 500 !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(14, 165, 233, 0.06) !important;
        border-color: #0ea5e9 !important;
        color: #0ea5e9 !important;
        transform: none !important;
    }

    .app-footer {
        text-align: center;
        padding: 28px 20px;
        margin-top: 48px;
        border-top: 1px solid #e2e8f0;
    }

    .app-footer p {
        font-size: 12px;
        color: #94a3b8;
        margin: 0;
        line-height: 1.8;
    }

    .app-footer .brand {
        color: #0ea5e9;
        font-weight: 700;
    }

    @media (max-width: 768px) {
        .stats-grid { grid-template-columns: repeat(2, 1fr); }
        .hero-title { font-size: 32px; }
        .hero { padding: 48px 24px; }
        .block-container { padding: 1rem 1.5rem; }
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# =================================================================================
# SIDEBAR
# =================================================================================
with st.sidebar:
    st.markdown("### 🧬 MSL AI Copilot")
    st.caption("v1.0 · AI-Powered MSL Intelligence")
    st.markdown("---")

    st.markdown("**Modules**")
    if st.button("📚  Literature Intelligence", use_container_width=True, key="sb_lit"):
        st.switch_page("pages/1_Literature_Intelligence.py")
    if st.button("👤  KOL Briefing Generator", use_container_width=True, key="sb_kol"):
        st.switch_page("pages/2_KOL_Briefing_Generator.py")
    if st.button("📊  Impact Dashboard", use_container_width=True, key="sb_dash"):
        st.switch_page("pages/3_Impact_Dashboard.py")

    st.markdown("---")

    st.markdown("**System Status**")

    openai_key = os.getenv("OPENAI_API_KEY")
    ncbi_key = os.getenv("NCBI_API_KEY")

    if openai_key:
        st.success("OpenAI API: Connected", icon="✅")
    else:
        st.warning("OpenAI API: Not configured", icon="⚠️")

    if ncbi_key:
        st.success("NCBI API: Connected", icon="✅")
    else:
        st.info("NCBI API: Using public access", icon="ℹ️")

    st.markdown("---")
    st.caption("Built with Streamlit · GPT-4o · PubMed")

# =================================================================================
# HERO
# =================================================================================
hero_html = """
<div class="hero">
    <div class="hero-badge">⚡ AI-POWERED SCIENTIFIC INTELLIGENCE</div>
    <h1 class="hero-title">MSL AI <span class="accent">Copilot</span></h1>
    <p class="hero-desc">
        Transform information overload into strategic scientific insight.
        Literature analysis, KOL profiling, and impact measurement — unified in one intelligent platform.
    </p>
</div>
"""
st.markdown(hero_html, unsafe_allow_html=True)

# =================================================================================
# STATS
# =================================================================================
stats_html = """
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-value">10x</div>
        <div class="stat-label">Faster Lit Review</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">95%</div>
        <div class="stat-label">Compliance Rate</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">&lt;30m</div>
        <div class="stat-label">To Deep Insights</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">3</div>
        <div class="stat-label">Integrated Modules</div>
    </div>
</div>
"""
st.markdown(stats_html, unsafe_allow_html=True)

# =================================================================================
# MODULES SECTION
# =================================================================================
section_header_html = """
<div class="section-hdr">
    <h2>Core Modules</h2>
    <p>Purpose-built tools for every stage of the MSL workflow</p>
</div>
"""
st.markdown(section_header_html, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    lit_card_html = """
    <div class="module-card">
        <div class="module-icon">📚</div>
        <div class="module-title">Literature Intelligence</div>
        <div class="module-desc">
            Real-time PubMed search with AI-powered summarization,
            RAG-based Q&A, and automatic compliance screening.
        </div>
        <ul class="module-features">
            <li>Full MeSH syntax support</li>
            <li>3 summary formats (Standard, Bullets, HCP Talking Points)</li>
            <li>LangChain + FAISS RAG pipeline</li>
            <li>Compliance-screened outputs</li>
            <li>CSV export and library saving</li>
        </ul>
    </div>
    """
    st.markdown(lit_card_html, unsafe_allow_html=True)
    if st.button("Open Literature Module →", use_container_width=True, key="mod_lit"):
        st.switch_page("pages/1_Literature_Intelligence.py")

with col2:
    kol_card_html = """
    <div class="module-card">
        <div class="module-icon">👤</div>
        <div class="module-title">KOL Briefing Generator</div>
        <div class="module-desc">
            Auto-generate structured pre-meeting briefings from field notes
            with live literature enrichment.
        </div>
        <ul class="module-features">
            <li>7-section structured briefings</li>
            <li>Live literature integration</li>
            <li>Field interaction logging</li>
            <li>Insight extraction from notes</li>
            <li>Markdown export for offline use</li>
        </ul>
    </div>
    """
    st.markdown(kol_card_html, unsafe_allow_html=True)
    if st.button("Open KOL Briefing →", use_container_width=True, key="mod_kol"):
        st.switch_page("pages/2_KOL_Briefing_Generator.py")

with col3:
    dash_card_html = """
    <div class="module-card">
        <div class="module-icon">📊</div>
        <div class="module-title">Impact Dashboard</div>
        <div class="module-desc">
            Visualize MSL activities, demonstrate ROI, and generate
            leadership-ready reports with interactive analytics.
        </div>
        <ul class="module-features">
            <li>KPI metrics and activity tracking</li>
            <li>Interactive Plotly visualizations</li>
            <li>Unmet needs theme analysis</li>
            <li>Auto-generated activity reports</li>
            <li>Demo mode with sample data</li>
        </ul>
    </div>
    """
    st.markdown(dash_card_html, unsafe_allow_html=True)
    if st.button("Open Dashboard →", use_container_width=True, key="mod_dash"):
        st.switch_page("pages/3_Impact_Dashboard.py")

# =================================================================================
# COMPLIANCE BANNER
# =================================================================================
compliance_html = """
<div class="compliance-banner">
    <div class="compliance-icon">🛡️</div>
    <div class="compliance-text">
        <h4>Built-In Regulatory Compliance</h4>
        <p>
            All AI-generated content is automatically screened against FDA 21 CFR Part 202 and PhRMA Code guidelines.
            The engine flags off-label promotion, comparative efficacy claims, absolute claims, safety minimization,
            and promotional language with three-tier severity scoring (HIGH / MEDIUM / LOW).
        </p>
    </div>
</div>
"""
st.markdown(compliance_html, unsafe_allow_html=True)

# =================================================================================
# TECH STACK
# =================================================================================
tech_header_html = """
<div class="section-hdr">
    <h2>Technology Stack</h2>
    <p>Enterprise-grade components powering the platform</p>
</div>
"""
st.markdown(tech_header_html, unsafe_allow_html=True)

tech_grid_html = """
<div class="tech-grid">
    <div class="tech-chip">
        <span class="tech-icon">🎯</span>
        Streamlit
    </div>
    <div class="tech-chip">
        <span class="tech-icon">🧠</span>
        GPT-4o
    </div>
    <div class="tech-chip">
        <span class="tech-icon">🔗</span>
        LangChain
    </div>
    <div class="tech-chip">
        <span class="tech-icon">📐</span>
        FAISS
    </div>
    <div class="tech-chip">
        <span class="tech-icon">📖</span>
        PubMed API
    </div>
    <div class="tech-chip">
        <span class="tech-icon">📊</span>
        Plotly
    </div>
    <div class="tech-chip">
        <span class="tech-icon">🗄️</span>
        SQLite
    </div>
    <div class="tech-chip">
        <span class="tech-icon">🐍</span>
        Python 3.10+
    </div>
</div>
"""
st.markdown(tech_grid_html, unsafe_allow_html=True)

# =================================================================================
# GET STARTED
# =================================================================================
st.markdown("---")

get_started_html = """
<div class="section-hdr">
    <h2>Get Started</h2>
    <p>Select a module to begin</p>
</div>
"""
st.markdown(get_started_html, unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    if st.button("📚 Literature Intelligence", use_container_width=True, key="gs_lit"):
        st.switch_page("pages/1_Literature_Intelligence.py")

with c2:
    if st.button("👤 KOL Briefing Generator", use_container_width=True, key="gs_kol"):
        st.switch_page("pages/2_KOL_Briefing_Generator.py")

with c3:
    if st.button("📊 Impact Dashboard", use_container_width=True, key="gs_dash"):
        st.switch_page("pages/3_Impact_Dashboard.py")

# =================================================================================
# FOOTER
# =================================================================================
footer_html = """
<div class="app-footer">
    <p>
        <span class="brand">MSL AI Copilot</span> · Built with Streamlit, OpenAI GPT-4o and NCBI PubMed APIs<br/>
        Designed for Medical Science Liaisons · Compliance-first architecture · MIT License
    </p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
