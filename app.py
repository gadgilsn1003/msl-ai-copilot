import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="MSL AI Copilot",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sidebar branding ──────────────────────────────────────────────────────────
with st.sidebar:
    st.image(
        "https://img.icons8.com/fluency/96/medical-doctor.png",
        width=80,
    )
    st.title("MSL AI Copilot")
    st.caption("AI-powered intelligence for Medical Science Liaisons")
    st.divider()
    st.markdown(
        """
        **Modules**
        - 📚 Literature Intelligence
        - 🧠 KOL Briefing Generator
        - 📊 Impact Dashboard
        """
    )
    st.divider()
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=os.getenv("OPENAI_API_KEY", ""),
        help="Paste your key here or set OPENAI_API_KEY in .env",
    )
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        st.success("✓ API Key set", icon="✅")
    else:
        st.warning("Add your OpenAI API key to unlock AI features.")

# ── Home page ─────────────────────────────────────────────────────────────────
st.title("🧠 MSL AI Copilot")
st.subheader("Your intelligent partner for scientific engagement")

st.markdown(
    """
    Welcome to **MSL AI Copilot** — a purpose-built tool for Medical Science Liaisons
    that turns information overload into strategic insight.

    ### What can you do here?
    """
)

col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        """
        ### 📚 Literature Intelligence
        - Search PubMed in real-time
        - AI-powered article summaries
        - Compliance-flagged insights
        - Therapeutic area filtering
        """
    )

with col2:
    st.success(
        """
        ### 🧠 KOL Briefing Generator
        - Upload or enter field notes
        - Auto-generate HCP briefing sheets
        - Map literature to KOL interests
        - Export to PDF-ready format
        """
    )

with col3:
    st.warning(
        """
        ### 📊 Impact Dashboard
        - Track engagement trends
        - Visualize insight themes
        - Log field interactions
        - Demonstrate MSL value/ROI
        """
    )

st.divider()
st.markdown(
    """
    > **Built for MSLs, by someone who understands pharma.**  
    > Powered by OpenAI GPT-4, PubMed API, LangChain RAG, and Streamlit.
    """
)

st.markdown("---")
st.caption("⚠️ Disclaimer: This tool is for internal scientific exchange support only. "
           "Content generated does not constitute promotional material. "
           "Always verify AI-generated summaries against original publications.")
