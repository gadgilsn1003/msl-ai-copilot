"""
📖 PubMed Fetcher - NCBI Entrez API Integration

Handles searching PubMed and fetching article details
using the Biopython Entrez module.
"""

import os
from dotenv import load_dotenv
from Bio import Entrez

load_dotenv()

# Configure Entrez
NCBI_EMAIL = os.getenv("NCBI_EMAIL", "msl-copilot@example.com")
NCBI_API_KEY = os.getenv("NCBI_API_KEY", None)

Entrez.email = NCBI_EMAIL
if NCBI_API_KEY:
    Entrez.api_key = NCBI_API_KEY


def search_pubmed(query: str, max_results: int = 15, sort: str = "relevance") -> list:
    """
    Search PubMed and return article details.
    """
    if not query or query.strip() == "":
        return []

    try:
        handle = Entrez.esearch(
            db="pubmed",
            term=query,
            retmax=max_results,
            sort=sort,
            retmode="xml"
        )
        search_results = Entrez.read(handle)
        handle.close()

        id_list = search_results.get("IdList", [])
        if not id_list:
            return []

        articles = fetch_articles(id_list)
        return articles

    except Exception as e:
        raise Exception(f"PubMed search failed: {str(e)}")


def fetch_articles(pmid_list: list) -> list:
    """
    Fetch detailed article information for a list of PMIDs.
    """
    if not pmid_list:
        return []

    try:
        handle = Entrez.efetch(
            db="pubmed",
            id=",".join(pmid_list),
            rettype="xml",
            retmode="xml"
        )
        records = Entrez.read(handle)
        handle.close()

        articles = []
        for article_data in records.get("PubmedArticle", []):
            article = _parse_article(article_data)
            if article:
                articles.append(article)

        return articles

    except Exception as e:
        raise Exception(f"Failed to fetch article details: {str(e)}")


def search_and_fetch(query: str, max_results: int = 15, sort: str = "relevance") -> list:
    """
    Combined search and fetch in one call.
    """
    return search_pubmed(query, max_results, sort)


def _parse_article(article_data: dict) -> dict:
    """
    Parse a single PubMed article record into a clean dictionary.
    """
    try:
        medline = article_data.get("MedlineCitation", {})
        article_info = medline.get("Article", {})
        pmid = str(medline.get("PMID", ""))

        # Title
        title = str(article_info.get("ArticleTitle", "Untitled"))

        # Authors
        author_list = article_info.get("AuthorList", [])
        authors = []
        for author in author_list:
            last_name = author.get("LastName", "")
            first_name = author.get("ForeName", "")
            if last_name:
                authors.append(f"{last_name} {first_name}".strip())

        authors_str = ", ".join(authors[:5])
        if len(authors) > 5:
            authors_str += f" et al. ({len(authors)} authors)"

        # Journal
        journal_info = article_info.get("Journal", {})
        journal = str(journal_info.get("Title", "Unknown Journal"))

        # Year
        pub_date = article_info.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {})
        year = str(pub_date.get("Year", ""))
        if not year:
            medline_date = pub_date.get("MedlineDate", "")
            if medline_date:
                year = medline_date[:4]

        # Abstract
        abstract_parts = article_info.get("Abstract", {}).get("AbstractText", [])
        if abstract_parts:
            abstract = " ".join([str(part) for part in abstract_parts])
        else:
            abstract = ""

        # Publication type
        pub_types = article_info.get("PublicationTypeList", [])
        pub_type_list = [str(pt) for pt in pub_types]

        # Classify study type
        study_type = _classify_study_type(pub_type_list, title, abstract)

        # MeSH terms
        mesh_list = medline.get("MeshHeadingList", [])
        mesh_terms = []
        for mesh in mesh_list:
            descriptor = mesh.get("DescriptorName", "")
            if descriptor:
                mesh_terms.append(str(descriptor))

        return {
            "pmid": pmid,
            "title": title,
            "authors": authors_str,
            "journal": journal,
            "year": year,
            "abstract": abstract,
            "pub_types": pub_type_list,
            "study_type": study_type,
            "mesh_terms": mesh_terms,
        }

    except Exception:
        return None


def _classify_study_type(pub_types: list, title: str, abstract: str) -> str:
    """
    Classify the study type based on publication types and content.
    """
    title_lower = title.lower()
    abstract_lower = abstract.lower()
    pub_types_lower = [pt.lower() for pt in pub_types]

    if "meta-analysis" in pub_types_lower or "meta-analysis" in title_lower:
        return "Meta-Analysis"
    elif "systematic review" in title_lower or "systematic review" in abstract_lower:
        return "Systematic Review"
    elif "randomized controlled trial" in pub_types_lower:
        return "RCT"
    elif "clinical trial" in pub_types_lower or "clinical trial" in title_lower:
        return "Clinical Trial"
    elif "review" in pub_types_lower:
        return "Review"
    elif "case reports" in pub_types_lower:
        return "Case Report"
    elif any(term in abstract_lower for term in ["cohort", "retrospective", "prospective", "observational"]):
        return "Observational"
    elif any(term in abstract_lower for term in ["in vitro", "in vivo", "preclinical", "mouse", "rat"]):
        return "Preclinical"
    else:
        return "Other"
