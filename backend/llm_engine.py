"""
backend/llm_engine.py
LangChain + OpenAI RAG engine for MSL AI Copilot.
Handles article summarization, KOL briefing generation, and insight extraction.
"""

import os
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
# from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.schema.document import Document


def get_llm(model: str = "gpt-4o", temperature: float = 0.2):
    """Initialize and return OpenAI LLM."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set. Please add it in the sidebar.")
    return ChatOpenAI(model=model, temperature=temperature, openai_api_key=api_key)


# ── Article Summarization ──────────────────────────────────────────────────────

SUMMARY_SYSTEM_PROMPT = """You are an expert Medical Science Liaison (MSL) with deep knowledge
of clinical pharmacology, oncology, and drug development. Your role is to create concise,
scientifically accurate summaries of medical literature for MSL field use.

Guidelines:
- Use precise scientific terminology appropriate for HCP conversations
- Highlight clinical relevance and implications for patient care
- Note study design, sample size, and statistical significance
- Flag any limitations or confounding factors
- Keep summaries to 3-5 sentences unless otherwise specified
- Do NOT make promotional claims about specific drugs"""


def summarize_article(
    title: str,
    abstract: str,
    focus: Optional[str] = None,
    style: str = "standard",
) -> str:
    """
    Generate an MSL-optimized summary of a PubMed article.

    Args:
        title: Article title
        abstract: Full abstract text
        focus: Optional focus area (e.g., 'efficacy', 'safety', 'mechanism')
        style: 'standard' | 'bullet' | 'hcp_talking_points'

    Returns:
        Formatted summary string
    """
    llm = get_llm()

    style_instructions = {
        "standard": "Write a concise 3-4 sentence paragraph summary.",
        "bullet": "Write as 4-6 bullet points highlighting key findings.",
        "hcp_talking_points": "Write as 3 talking points an MSL would use in an HCP conversation.",
    }.get(style, "Write a concise 3-4 sentence paragraph summary.")

    focus_note = f"\nFocus particularly on aspects related to: {focus}" if focus else ""

    prompt = ChatPromptTemplate.from_messages([
        ("system", SUMMARY_SYSTEM_PROMPT),
        ("human", f"""Please summarize the following medical article for MSL field use.

{style_instructions}{focus_note}

Title: {title}

Abstract: {abstract}

Summary:""")
    ])

    chain = prompt | llm
    response = chain.invoke({})
    return response.content


# ── KOL Briefing Generator ─────────────────────────────────────────────────────

KOL_BRIEFING_SYSTEM_PROMPT = """You are a senior Medical Science Liaison preparing
a comprehensive pre-meeting briefing document for a KOL (Key Opinion Leader) interaction.
Your briefings are used by field MSLs to personalize scientific exchange conversations.

Your output must be:
- Scientifically rigorous and evidence-based
- Personalized to the KOL's known research interests
- Structured for quick field reference (not for promotional use)
- Compliant with medical affairs guidelines"""


def generate_kol_briefing(
    kol_name: str,
    specialty: str,
    institution: str,
    field_notes: str,
    relevant_articles: Optional[list] = None,
    therapeutic_area: str = "Oncology",
) -> str:
    """
    Generate a comprehensive KOL briefing sheet.

    Args:
        kol_name: HCP/KOL full name
        specialty: Medical specialty
        institution: Hospital/University affiliation
        field_notes: Raw notes from previous field interactions
        relevant_articles: List of article dicts from PubMed
        therapeutic_area: Therapeutic focus area

    Returns:
        Formatted briefing document as markdown string
    """
    llm = get_llm()

    articles_context = ""
    if relevant_articles:
        articles_context = "\n\nRelevant Recent Literature:\n"
        for i, art in enumerate(relevant_articles[:5], 1):
            articles_context += f"{i}. {art.get('title', 'N/A')} ({art.get('pub_date', 'N/A')}) - {art.get('journal', 'N/A')}\n"

    prompt = f"""Generate a comprehensive MSL Pre-Meeting Briefing for the following KOL:

KOL NAME: {kol_name}
SPECIALTY: {specialty}
INSTITUTION: {institution}
THERAPEUTIC AREA: {therapeutic_area}

FIELD NOTES FROM PREVIOUS INTERACTIONS:
{field_notes}
{articles_context}

Create a structured briefing with these sections:
1. KOL PROFILE SUMMARY (2-3 sentences)
2. KEY SCIENTIFIC INTERESTS (bullet points based on field notes)
3. PREVIOUS DISCUSSION THEMES (what has been discussed before)
4. RECOMMENDED DISCUSSION TOPICS FOR THIS MEETING (3-5 topics with rationale)
5. RELEVANT DATA POINTS TO SHARE (from literature above if available)
6. OPEN QUESTIONS / UNMET NEEDS IDENTIFIED
7. RELATIONSHIP NOTES (rapport builders, follow-up items)

Format as clean markdown. Keep it concise and field-ready."""

    messages = [
        SystemMessage(content=KOL_BRIEFING_SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ]
    response = llm.invoke(messages)
    return response.content


# ── RAG Pipeline for Literature Q&A ───────────────────────────────────────────

def build_rag_index(articles: list) -> Optional[FAISS]:
    """
    Build a FAISS vector index from a list of PubMed article dicts.

    Args:
        articles: List of article dicts with 'title' and 'abstract' keys

    Returns:
        FAISS vectorstore or None if articles list is empty
    """
    if not articles:
        return None

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    docs = []
    for art in articles:
        content = f"Title: {art.get('title', '')}\n\nAbstract: {art.get('abstract', '')}\n\nJournal: {art.get('journal', '')} ({art.get('pub_date', '')})"
        docs.append(Document(
            page_content=content,
            metadata={"pmid": art.get("pmid", ""), "url": art.get("url", ""), "title": art.get("title", "")}
        ))

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    splits = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    vectorstore = FAISS.from_documents(splits, embeddings)
    return vectorstore


def ask_literature(question: str, vectorstore: FAISS) -> dict:
    """
    Answer a scientific question using RAG over indexed articles.

    Args:
        question: Natural language question from the MSL
        vectorstore: Pre-built FAISS vectorstore

    Returns:
        Dict with 'answer' and 'source_documents'
    """
    llm = get_llm(temperature=0.1)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
        return_source_documents=True,
    )
    result = qa_chain.invoke({"query": question})
    return {
        "answer": result.get("result", ""),
        "sources": [
            {"title": doc.metadata.get("title", ""), "url": doc.metadata.get("url", "")}
            for doc in result.get("source_documents", [])
        ]
    }


# ── Insight Extraction ─────────────────────────────────────────────────────────

def extract_insights_from_notes(field_notes: str, therapeutic_area: str = "Oncology") -> dict:
    """
    Extract structured insights from raw MSL field notes.

    Returns:
        Dict with 'unmet_needs', 'hcp_sentiments', 'action_items', 'key_topics'
    """
    llm = get_llm(temperature=0.1)

    prompt = f"""You are an expert at analyzing MSL field call notes and extracting structured insights.

Analyze the following field notes from an MSL interaction in {therapeutic_area} and extract:

1. UNMET NEEDS: Clinical gaps or unmet needs expressed by the HCP
2. HCP SENTIMENTS: Key opinions or sentiments about treatments/data
3. ACTION ITEMS: Follow-up actions required by the MSL
4. KEY TOPICS DISCUSSED: Main scientific topics covered

Field Notes:
{field_notes}

Return your analysis as a structured response with clear section headers."""

    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)

    # Simple parsing - split by known headers
    content = response.content
    return {
        "raw_analysis": content,
        "therapeutic_area": therapeutic_area,
    }
