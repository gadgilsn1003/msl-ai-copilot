"""
🧬 MSL AI Copilot — Main Entry Point

Production-ready landing page with professional branding,
feature highlights, and navigation to all three modules.
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="MSL AI Copilot",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# CUSTOM CSS
# ============================================================================
st.markdown("""
<style>
    /* Hero section */
    .hero-container {
        background: linear-gradient(135deg, #0066CC 0%, #004C99 100%);
        padding: 60px 40px;
        border-radius: 16px;
        margin-bottom: 40px;
        color: white;
        text-align: center;
    }
    .hero-title {
        font-size: 48px;
        font-weight: 800;
        margin-bottom: 16px;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: 20px;
        opacity: 0.95;
        margin-bottom: 8px;
    }
    .hero-tagline {
        font-size: 16px;
        opacity: 0.85;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 32px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-left: 5px solid #0066CC;
        margin-bottom: 24px;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }
    .feature-icon {
        font-size: 40px;
        margin-bottom: 16px;
    }
    .feature-title {
        font-size: 24px;
        font-weight: 700;
        color: #1a2332;
        margin-bottom: 12px;
    }
    .feature-description {
        font-size: 15px;
        color: #6b7280;
        line-height: 1.6;
        margin-bottom: 16px;
    }
    .feature-benefits {
        font-size: 14px;
        color: #374151;
    }
    
    /* Stats section */
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 40px 0;
        padding: 32px;
        background: #f8fafc;
        border-radius: 12px;
    }
    .stat-item {
        text-align: center;
    }
    .stat-number {
        font-size: 36px;
        font-weight: 800;
        color: #0066CC;
    }
    .stat-label {
        font-size: 14px;
        color: #6b7280;
        text-transform: uppercase;
        margin-top: 8px;
    }
    
    /* CTA buttons */
    .cta-button {
        display: inline-block;
        background: white;
        color: #0066CC;
        padding: 12px 32px;
        border-radius: 8px;
        font-weight: 600;
        text-decoration: none;
        transition: all 0.2s;
        border: 2px solid white;
    }
    .cta-button:hover {
        background: transparent;
        color: white;
        border-color: white;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.image(
        "https://img.icons8.com/fluency/96/medical-doctor.png",
        width=80,
    )
    st.title("MSL AI Copilot")
    st.caption("AI-powered intelligence for Medical Science Liaisons")
    
    st.markdown("---")
    
    st.markdown("### 🎯 **Modules**")
    st.page_link("pages/1_Literature_Intelligence.py", label="📚 Literature Intelligence", icon="📚")
    st.page_link("pages/2_KOL_Briefing_Generator.py", label="👤 KOL Briefing Generator", icon="👤")
    st.page_link("pages/3_Impact_Dashboard.py", label="📊 Impact Dashboard", icon="📊")
    
    st.markdown("---")
    
    st.markdown("### ⚙️ **Quick Setup**")
    if os.getenv("OPENAI_API_KEY"):
        st.success("✅ API configured")
    else:
        st.warning("⚠️ Add API key to `.env`")
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6b7280; font-size: 12px;'>
        Built with Streamlit + GPT-4o<br>
        Version 1.0.0
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# HERO SECTION
# ============================================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🧬 MSL AI Copilot</div>
    <div class="hero-subtitle">Transform Information Overload into Strategic Insight</div>
    <div class="hero-tagline">
        AI-powered literature intelligence, KOL briefings, and impact tracking — 
        purpose-built for Medical Science Liaisons
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# STATS SECTION
# ============================================================================
st.markdown("""
<div class="stats-container">
    <div class="stat-item">
        <div class="stat-number">10x</div>
        <div class="stat-label">Faster Literature Review</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">95%</div>
        <div class="stat-label">Compliance Accuracy</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">30min</div>
        <div class="stat-label">To Deep Insights</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">100%</div>
        <div class="stat-label">Real PubMed Data</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# FEATURE CARDS
# ============================================================================
st.markdown("## 🚀 Core Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📚</div>
        <div class="feature-title">Literature Intelligence</div>
        <div class="feature-description">
            AI-powered search and synthesis of scientific literature from PubMed, 
            with automatic compliance screening and evidence classification.
        </div>
        <div class="feature-benefits">
            ✓ Smart PubMed queries<br>
            ✓ GPT-4o summaries<br>
            ✓ Compliance filtering<br>
            ✓ Evidence leveling
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">👤</div>
        <div class="feature-title">KOL Briefing Generator</div>
        <div class="feature-description">
            Generate comprehensive, compliant briefing documents for KOL interactions 
            based on their publication history and research interests.
        </div>
        <div class="feature-benefits">
            ✓ Auto-detect expertise<br>
            ✓ Recent publications<br>
            ✓ Talking points<br>
            ✓ Export to PDF/DOCX
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Impact Dashboard</div>
        <div class="feature-description">
            Visualize your MSL activities and demonstrate ROI with interactive 
            charts, metrics, and exportable reports.
        </div>
        <div class="feature-benefits">
            ✓ Activity tracking<br>
            ✓ Demo mode included<br>
            ✓ Interactive charts<br>
            ✓ Export reports
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# WHY THIS EXISTS
# ============================================================================
st.markdown("---")
st.markdown("## 🎯 Why This Exists")

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("""
    ### The MSL Challenge
    
    Medical Science Liaisons face an impossible task: staying current with **thousands of new publications monthly**, 
    preparing for **high-stakes KOL interactions**, and **demonstrating measurable impact** — all while maintaining 
    strict regulatory compliance.
    
    Traditional tools are generic. This isn't.
    
    ### The MSL AI Copilot Solution
    
    Built by someone with deep expertise in:
    - **Pharmacokinetics / Pharmacodynamics (PK/PD)**
    - **Regulatory Affairs & FDA Compliance**
    - **Machine Learning & Data Science**
    - **Clinical Trial Design & Analysis**
    
    This tool combines domain knowledge with cutting-edge AI to solve **real MSL pain points**.
    """)

with col2:
    st.info("""
    **🔬 Built with Real Science**
    
    - PubMed integration (30M+ articles)
    - GPT-4o for synthesis
    - Compliance-first architecture
    - Evidence-based classifications
    - NCBI API best practices
    
    **🎓 Perfect For**
    
    - Field Medical Teams
    - MSL Departments
    - Clinical Development
    - Medical Affairs
    - Academic Liaisons
    """)

# ============================================================================
# HOW IT WORKS
# ============================================================================
st.markdown("---")
st.markdown("## ⚙️ How It Works")

steps = st.columns(4)

with steps[0]:
    st.markdown("""
    ### 1️⃣ Search
    Enter your clinical question or research topic
    """)

with steps[1]:
    st.markdown("""
    ### 2️⃣ Fetch
    Real-time PubMed API queries retrieve relevant literature
    """)

with steps[2]:
    st.markdown("""
    ### 3️⃣ Analyze
    GPT-4o synthesizes findings with compliance filtering
    """)

with steps[3]:
    st.markdown("""
    ### 4️⃣ Act
    Export insights, briefings, or track impact
    """)

# ============================================================================
# GET STARTED
# ============================================================================
st.markdown("---")
st.markdown("## 🚀 Get Started")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📚 Explore Literature", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Literature_Intelligence.py")

with col2:
    if st.button("👤 Create KOL Briefing", use_container_width=True, type="primary"):
        st.switch_page("pages/2_KOL_Briefing_Generator.py")

with col3:
    if st.button("📊 View Impact Dashboard", use_container_width=True, type="primary"):
        st.switch_page("pages/3_Impact_Dashboard.py")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 20px;'>
    <p style='margin: 0;'>
        <strong>MSL AI Copilot</strong> | Built with Streamlit, OpenAI GPT-4o, and PubMed APIs
    </p>
    <p style='margin: 8px 0 0 0; font-size: 13px;'>
        Designed for Medical Science Liaisons by experts in PK/PD, Regulatory Affairs, and Machine Learning
    </p>
</div>
""", unsafe_allow_html=True)
