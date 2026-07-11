# 🧠 MSL AI Copilot

> **AI-powered Scientific Literature & KOL Insight Copilot for Medical Science Liaisons**

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![OpenAI](https://img.shields.io/badge/Powered%20by-GPT--4o-green)](https://openai.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A full-stack, production-ready AI tool built specifically for Medical Science Liaisons (MSLs) that transforms information overload into strategic scientific insight.

---

## 🎯 Why This Exists

MSLs spend enormous time:
- Manually scanning journals for relevant publications
- Preparing KOL-specific briefing documents before field meetings
- Logging interactions and proving ROI to leadership
- Ensuring their communications remain compliant with FDA medical affairs guidance

**MSL AI Copilot** addresses all four pain points in a single, deployable application.

---

## 🚀 Features

### 📚 Module 1: Literature Intelligence
- **Real-time PubMed search** via NCBI Entrez API (supports full MeSH syntax)
- **Pre-built therapeutic area queries** (Oncology, GBM/Neuro-Oncology, Immunology, Cardiology, Rare Disease, Neurology)
- **AI-powered article summarization** with 3 formats: Standard, Bullet Points, HCP Talking Points
- **RAG-based Q&A** — ask natural language questions over retrieved articles (LangChain + FAISS)
- **Compliance screening** of all AI-generated content
- **CSV export** and article library saving

### 🧠 Module 2: KOL Briefing Generator
- **Pre-meeting briefing sheets** auto-generated from field notes using GPT-4o
- **7-section structured briefing** (Profile, Interests, Discussion History, Recommendations, Literature, Unmet Needs, Relationship Notes)
- **Optionally pulls live literature** to enrich briefings
- **Field interaction logging** (field calls, congress meetings, advisory boards)
- **Insight extraction** from raw unstructured field notes
- **KOL profile library** with search
- **Markdown export** for offline use

### 📊 Module 3: Impact Dashboard
- **KPI metrics** — total interactions, unique KOLs, saved articles
- **Interactive Plotly charts** — top KOLs, interaction types, monthly timeline
- **Unmet needs theme analysis** via keyword frequency treemap
- **Auto-generates MSL activity reports** for manager/leadership reporting
- **Demo mode** with realistic sample data if no interactions are logged
- **CSV export** for CRM submission

### 🛡️ Compliance Filter (Regulatory Differentiator)
- Rule-based scanning aligned with **FDA 21 CFR Part 202** and **PhRMA Code**
- Flags: off-label promotion, comparative efficacy claims, absolute claims, safety minimization, promotional language
- Three-tier severity: HIGH / MEDIUM / LOW
- Applied to all AI-generated content automatically

---

## 🏗️ Architecture

```
msl-ai-copilot/
├── app.py                          # Main Streamlit entry point
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variable template
├── backend/
│   ├── pubmed_fetcher.py           # NCBI Entrez API integration
│   ├── llm_engine.py               # OpenAI + LangChain RAG pipeline
│   ├── compliance_filter.py        # FDA regulatory compliance scanner
│   └── database.py                 # SQLite CRUD + analytics queries
└── pages/
    ├── 1_Literature_Intelligence.py
    ├── 2_KOL_Briefing_Generator.py
    └── 3_Impact_Dashboard.py
```

---

## ⚡ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/gadgilsn1003/msl-ai-copilot.git
cd msl-ai-copilot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 4. Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🔑 API Keys Required

| Key | Required | Source |
|-----|----------|--------|
| `OPENAI_API_KEY` | Yes (for AI features) | [platform.openai.com](https://platform.openai.com) |
| `NCBI_API_KEY` | No (but recommended for rate limits) | [ncbi.nlm.nih.gov/account](https://www.ncbi.nlm.nih.gov/account/) |
| `NCBI_EMAIL` | No (but recommended) | Your email address |

> **Note:** PubMed search works without any API key. OpenAI is only required for AI summaries, briefings, and RAG Q&A.

---

## 💻 Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| LLM | OpenAI GPT-4o |
| RAG Pipeline | LangChain + FAISS |
| Literature API | NCBI Entrez (Biopython) |
| Database | SQLite (local) / Supabase (cloud) |
| Charts | Plotly Express |
| Compliance | Custom rule-based engine |

---

## 📊 Demo

The Impact Dashboard has a **built-in demo mode** that auto-populates with realistic sample data (45 interactions, 5 KOLs, multiple therapeutic areas) when no interactions are logged — perfect for live demos.

---

## ⚠️ Disclaimer

This tool is designed for **internal scientific exchange support** within Medical Affairs. Content generated does not constitute promotional material. Always verify AI-generated summaries against original publications. Compliance screening is assistive, not a substitute for formal medical/legal review.

---

## 📝 License

MIT License — see [LICENSE](LICENSE) for details.

---

*Built by a PhD candidate in Biomedical Sciences with expertise in pharmacokinetics, regulatory affairs, and machine learning. Designed to solve real problems faced by field MSLs.*
