"""
🧬 MSL AI Copilot – Main Entry Point

Production-ready landing page with professional branding,
feature highlights, and navigation to all three modules.
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
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
# CUSTOM CSS - MODERN PREMIUM DESIGN
# =================================================================================
st.markdown("""
<style>
    /* Hero section */
    .hero-container {
        background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 50%, #0369A1 100%);
        padding: 80px 60px;
        border-radius: 24px;
        margin-bottom: 60px;
        color: white;
        text-align: center;
        box-shadow: 0 20px 60px rgba(14, 165, 233, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .hero-title {
        font-size: 56px;
        font-weight: 800;
        margin-bottom: 16px;
        line-height: 1.2;
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        font-size: 24px;
        opacity: 0.95;
        margin-bottom: 12px;
        font-weight: 300;
        position: relative;
        z-index: 1;
    }
    
    .hero-tagline {
        font-size: 18px;
        opacity: 0.85;
        font-weight: 300;
        position: relative;
        z-index: 1;
    }
    
    /* Stats section */
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 40px 0;
        gap: 24px;
        flex-wrap: wrap;
    }
    
    .stat-box {
        background: linear-gradient(145deg, #ffffff, #f8fafc);
        padding: 32px;
        border-radius: 20px;
        text-align: center;
        flex: 1;
        min-width: 200px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(14, 165, 233, 0.1);
    }
    
    .stat-box:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(14, 165, 233, 0.15);
    }
    
    .stat-number {
        font-size: 48px;
        font-weight: 800;
        color: #0EA5E9;
        line-height: 1;
        margin-bottom: 8px;
    }
    
    .stat-label {
        font-size: 14px;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Feature cards */
    .feature-card {
        background: linear-gradient(145deg, #ffffff, #f8fafc);
        padding: 40px;
        border-radius: 20px;
        margin-bottom: 24px;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(14, 165, 233, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #0EA5E9, #0369A1);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 50px rgba(14, 165, 233, 0.2);
        border-color: #0EA5E9;
    }
    
    .feature-card:hover::before {
        opacity: 1;
    }
    
    .feature-icon {
        font-size: 48px;
        margin-bottom: 20px;
        display: block;
    }
    
    .feature-title {
        font-size: 28px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 16px;
        line-height: 1.3;
    }
    
    .feature-description {
        font-size: 16px;
        color: #475569;
        line-height: 1.7;
        margin-bottom: 20px;
    }
    
    .feature-list {
        margin: 16px 0;
        padding-left: 0;
        list-style: none;
    }
    
    .feature-list li {
        padding: 8px 0;
        color: #64748b;
        font-size: 15px;
        display: flex;
        align-items: center;
    }
    
    .feature-list li:before {
        content: "✓";
        color: #0EA5E9;
        font-weight: bold;
        margin-right: 12px;
        font-size: 18px;
    }
    
    /* Section headers */
    .section-header {
        text-align: center;
        margin: 60px 0 40px 0;
    }
    
    .section-title {
        font-size: 42px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 12px;
    }
    
    .section-subtitle {
        font-size: 18px;
        color: #64748b;
        font-weight: 400;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
    }
    
    .sidebar-module {
        padding: 12px 16px;
        margin: 8px 0;
        border-radius: 12px;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .sidebar-module:hover {
        background: rgba(14, 165, 233, 0.1);
        transform: translateX(4px);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 40px 20px;
        margin-top: 80px;
        border-top: 2px solid #e2e8f0;
        color: #64748b;
    }
    
    .footer-strong {
        color: #0EA5E9;
        font-weight: 600;
    }
    
    /* Button enhancements */
    .stButton > button {
        background: linear-gradient(135deg, #0EA5E9, #0284C7);
        color: white;
        border: none;
        padding: 16px 32px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 12px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(14, 165, 233, 0.4);
        background: linear-gradient(135deg, #0284C7, #0369A1);
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =================================================================================
# SIDEBAR - NAVIGATION
# =================================================================================
with st.sidebar:
    st.markdown("### 🧬 MSL AI Copilot")
    st.markdown("AI-powered intelligence for Medical Science Liaisons")
    
    st.markdown("---")
    
    st.markdown("### 🎯 Modules")
    
    st.markdown('<div class="sidebar-module">', unsafe_allow_html=True)
    if st.button("📚 📚 Literature Intelligence", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Literature_Intelligence.py")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-module">', unsafe_allow_html=True)
    if st.button("👤 👤 KOL Briefing Generator", use_container_width=True, type="primary"):
        st.switch_page("pages/2_KOL_Briefing_Generator.py")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-module">', unsafe_allow_html=True)
    if st.button("📊 📊 Impact Dashboard", use_container_width=True, type="primary"):
        st.switch_page("pages/3_Impact_Dashboard.py")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Quick Setup")
    st.markdown("Ensure API keys are configured in Render environment variables.")

# =================================================================================
# HERO SECTION
# =================================================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🧬 MSL AI Copilot</div>
    <div class="hero-subtitle">AI-Powered Intelligence for Medical Science Liaisons</div>
    <div class="hero-tagline">Transform your scientific engagement with cutting-edge AI technology</div>
</div>
""", unsafe_allow_html=True)

# =================================================================================
# STATS SECTION
# =================================================================================
st.markdown("""
<div class="stats-container">
    <div class="stat-box">
        <div class="stat-number">10x</div>
        <div class="stat-label">Faster Literature<br/>Review</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">95%</div>
        <div class="stat-label">Compliance<br/>Accuracy</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">30min</div>
        <div class="stat-label">To Deep<br/>Insights</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">100%</div>
        <div class="stat-label">Real PubMed<br/>Data</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =================================================================================
# SECTION HEADER
# =================================================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">🚀 Core Features</div>
    <div class="section-subtitle">Everything you need to excel as a Medical Science Liaison</div>
</div>
""", unsafe_allow_html=True)

# =================================================================================
# FEATURE CARDS
# =================================================================================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">📚</span>
        <div class="feature-title">Literature Intelligence</div>
        <div class="feature-description">
            AI-powered search and synthesis of scientific literature from PubMed, 
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
    
    if st.button("🔍 Explore Literature", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Literature_Intelligence.py")

with col2:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">👤</span>
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
    
    if st.button("📝 Create KOL Briefing", use_container_width=True, type="primary"):
        st.switch_page("pages/2_KOL_Briefing_Generator.py")

with col3:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">📊</span>
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
    
    if st.button("📈 View Impact Dashboard", use_container_width=True, type="primary"):
        st.switch_page("pages/3_Impact_Dashboard.py")

# =================================================================================
# GET STARTED SECTION
# =================================================================================
st.markdown("---")
st.markdown("""
<div class="section-header">
    <div class="section-title">✨ Get Started</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔍 Explore Literature", use_container_width=True, type="primary", key="get_started_lit""):
        st.switch_page("pages/1_Literature_Intelligence.py")

with col2:
    if st.button("📝 Create KOL Briefing", use_container_width=True, type="primary", key="get_started_kol"):
        st.switch_page("pages/2_KOL_Briefing_Generator.py")

with col3:
    if st.button("📈 View Impact Dashboard", use_container_width=True, type="primary"), key="get_started_impact":
        st.switch_page("pages/3_Impact_Dashboard.py")

# =================================================================================
# FOOTER
# =================================================================================
st.markdown("---")
st.markdown("""
<div class="footer">
    <p style='margin: 0;'>
        <strong class='footer-strong'>MSL AI Copilot</strong> | Built with Streamlit, OpenAI GPT-4o, and PubMed APIs
    </p>
    <p style='margin: 8px 0 0 0; font-size: 13px;'>
        Designed for Medical Science Liaisons by experts in PK/PD, Regulatory Affairs, and Machine Learning
    </p>
</div>
""", unsafe_allow_html=True)
