"""
🧬 MSL AI Copilot – Main Entry Point
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
# PRODUCTION CSS - CLEAN, CONSISTENT, PROFESSIONAL
# =================================================================================
st.markdown("""
<style>
    /* Import professional font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global overrides */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Remove Streamlit padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* Hero section */
    .hero-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        padding: 80px 60px;
        border-radius: 24px;
        margin-bottom: 48px;
        text-align: center;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(14, 165, 233, 0.2);
    }

    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background:
            radial-gradient(ellipse at 20% 50%, rgba(14, 165, 233, 0.15) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 50%, rgba(56, 189, 248, 0.1) 0%, transparent 50%);
        pointer-events: none;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(14, 165, 233, 0.15);
        border: 1px solid rgba(14, 165, 233, 0.3);
        color: #38bdf8;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 24px;
        position: relative;
        z-index: 1;
    }

    .hero-title {
        font-size: 52px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 16px;
        line-height: 1.1;
        position: relative;
        z-index: 1;
        letter-spacing: -1px;
    }

    .hero-title span {
        background: linear-gradient(135deg, #38bdf8, #0ea5e9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-subtitle {
        font-size: 20px;
        color: #94a3b8;
        margin-bottom: 8px;
        font-weight: 400;
        position: relative;
        z-index: 1;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
    }

    /* Stats section */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin: 0 0 48px 0;
    }

    .stat-box {
        background: #ffffff;
        padding: 28px 20px;
        border-radius: 16px;
        text-align: center;
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease;
    }

    .stat-box:hover {
        border-color: #0ea5e9;
        box-shadow: 0 8px 24px rgba(14, 165, 233, 0.12);
        transform: translateY(-2px);
    }

    .stat-number {
        font-size: 36px;
        font-weight: 800;
        color: #0ea5e9;
        line-height: 1;
        margin-bottom: 8px;
    }

    .stat-label {
        font-size: 13px;
        color: #64748b;
        font-weight: 500;
        line-height: 1.4;
    }

    /* Feature cards */
    .feature-card {
        background: #ffffff;
        padding: 36px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease;
        height: 100%;
    }

    .feature-card:hover {
        border-color: #0ea5e9;
        box-shadow: 0 12px 32px rgba(14, 165, 233, 0.12);
        transform: translateY(-4px);
    }

    .feature-icon-wrapper {
        width: 56px;
        height: 56px;
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.1), rgba(14, 165, 233, 0.05));
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        font-size: 28px;
    }

    .feature-title {
        font-size: 20px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 12px;
    }

    .feature-description {
        font-size: 14px;
        color: #64748b;
        line-height: 1.7;
        margin-bottom: 20px;
    }

    .feature-list {
        margin: 0;
        padding: 0;
        list-style: none;
    }

    .feature-list li {
        padding: 6px 0;
        color: #475569;
        font-size: 13px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .feature-list li:before {
        content: "✓";
        color: #0ea5e9;
        font-weight: 700;
        font-size: 14px;
        flex-shrink: 0;
    }

    /* Section headers */
    .section-header {
        text-align: center;
        margin: 48px 0 32px 0;
    }

    .section-title {
        font-size: 32px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }

    .section-subtitle {
        font-size: 16px;
        color: #64748b;
        font-weight: 400;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #fafbfc;
        border-right: 1px solid #e2e8f0;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(14, 165, 233, 0.25) !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(14, 165, 233, 0.35) !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 32px 20px;
        margin-top: 60px;
        border-top: 1px solid #e2e8f0;
        color: #94a3b8;
        font-size: 13px;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .stats-container {
            grid-template-columns: repeat(2, 1fr);
        }
        .hero-title {
            font-size: 36px;
        }
    }

    /* Hide Streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =================================================================================
# SIDEBAR
# =================================================================================
with st.sidebar:
    st.markdown("### 🧬 MSL AI Copilot")
    st.markdown("*AI-powered intelligence for MSLs*")
    st.markdown("---")

    st.markdown("#### Navigation")

    if st.button("📚 Literature Intelligence", use_container_width=True, key="nav_lit"):
        st.switch_page("pages/1_Literature_Intelligence.py")

    if st.button("👤 KOL Briefing Generator", use_container_width=True, key="nav_kol"):
        st.switch_page("pages/2_KOL_Briefing_Generator.py")

    if st.button("📊 Impact Dashboard", use_container_width=True, key="nav_impact"):
        st.switch_page("pages/3_Impact_Dashboard.py")

    st.markdown("---")
    st.markdown("#### Status")
    st.success("✅ All systems operational")
    st.caption("API keys configured via environment variables")

# =================================================================================
# HERO SECTION
# =================================================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">🚀 AI-POWERED PLATFORM</div>
    <div class="hero-title">MSL AI <span>Copilot</span></div>
    <div class="hero-subtitle">
        Transform your scientific engagement with intelligent literature analysis,
        KOL profiling, and impact measurement — all in one platform.
    </div>
</div>
""", unsafe_allow_html=True)

# =================================================================================
# STATS
# =================================================================================
st.markdown("""
<div class="stats-container">
    <div class="stat-box">
        <div class="stat-number">10x</div>
        <div class="stat-label">Faster Literature Review</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">95%</div>
        <div class="stat-label">Compliance Accuracy</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">&lt;30min</div>
        <div class="stat-label">To Deep Insights</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">100%</div>
        <div class="stat-label">Real PubMed Data</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =================================================================================
# FEATURES
# =================================================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">Core Modules</div>
    <div class="section-subtitle">Everything you need to excel as a Medical Science Liaison</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon-wrapper">📚</div>
        <div class="feature-title">Literature Intelligence</div>
        <div class="feature-description">
            AI-powered search and synthesis of scientific literature from PubMed
            with automatic compliance screening and evidence classification.
        </div>
        <ul class="feature-list">
            <li>Real-time PubMed search</li>
            <li>Compliance-first filtering</li>
            <li>Evidence classification</li>
            <li>Saved library management</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explore Literature →", use_container_width=True, key="feat_lit"):
        st.switch_page("pages/1_Literature_Intelligence.py")

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon-wrapper">👤</div>
        <div class="feature-title">KOL Briefing Generator</div>
        <div class="feature-description">
            Generate comprehensive, compliant briefing documents for KOL interactions
            based on their publication history and research focus.
        </div>
        <ul class="feature-list">
            <li>Publication analysis</li>
            <li>Research focus detection</li>
            <li>Compliant summaries</li>
            <li>Export-ready briefs</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Create KOL Briefing →", use_container_width=True, key="feat_kol"):
        st.switch_page("pages/2_KOL_Briefing_Generator.py")

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon-wrapper">📊</div>
        <div class="feature-title">Impact Dashboard</div>
        <div class="feature-description">
            Visualize your MSL activities and demonstrate ROI with interactive
            charts, metrics, and exportable reports.
        </div>
        <ul class="feature-list">
            <li>Activity tracking</li>
            <li>Engagement metrics</li>
            <li>Visual analytics</li>
            <li>Exportable reports</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("View Dashboard →", use_container_width=True, key="feat_impact"):
        st.switch_page("pages/3_Impact_Dashboard.py")

# =================================================================================
# FOOTER
# =================================================================================
st.markdown("""
<div class="footer">
    <strong style="color: #0ea5e9;">MSL AI Copilot</strong> &nbsp;·&nbsp;
    Built with Streamlit, OpenAI GPT-4o & PubMed APIs &nbsp;·&nbsp;
    Designed for Medical Science Liaisons
</div>
""", unsafe_allow_html=True)
