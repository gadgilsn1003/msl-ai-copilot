"""
📖 PubMed Fetcher - NCBI Entrez API Integration

Handles searching PubMed and fetching article details
using the Biopython Entrez module.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Configure Entrez
from Bio import Entrez

NCBI_EMAIL = os.getenv("NCBI_EMAIL", "msl-copilot@example.com")
NCBI_API_KEY = os.getenv("NCBI_API_KEY", None)

Entrez.email = NCBI_EMAIL
if NCBI_API_KEY:
    Entrez.api_key = NCBI_API_KEY


def search_pubmed(query: str, max_results: int = 15, sort: str = "relevance") -> list:
    """
    Search PubMed and return article details.

    Args:
        query: PubMed search query (supports MeSH syntax)
        max_results: Maximum number of results to return
        sort: Sort order - 'relevance' or 'date'

    Returns:
        List of article dictionaries
    """
    if not query or query.strip() == "":
        return []

    try:
        # Search PubMed for IDs
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

        # Fetch article details
        articles = fetch_article_details(id_list)
        return articles

    except Exception as e:
        raise Exception(f"PubMed search failed: {str(e)}")


def fetch_article_details(pmid_list: list) -> list:
    """
    Fetch detailed article information for a list of PMIDs.

    Args:
        pmid_list: List of PubMed IDs

    Returns:
        List of article dictionaries with full details
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
            article = parse_article(article_data)
            if article:
                articles.append(article)

        return articles

    except Exception as e:
        raise Exception(f"Failed to fetch article details: {str(e)}")


def parse_article(article_data: dict) -> dict:
    """
    Parse a single PubMed article record into a clean dictionary.

    Args:
        article_data: Raw PubMed article data

    Returns:
        Cleaned article dictionary
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
        study_type = classify_study_type(pub_type_list, title, abstract)

        # MeSH terms
        mesh_list = medline.get("MeshHeadingList", [])
        mesh_terms = []
        for mesh in mesh_list:
            descriptor = mesh.get("DescriptorName", "")
            if descriptor:
                mesh_terms.append(str(descriptor))

        # DOI
        doi = ""
        article_ids = article_data.get("PubmedData", {}).get("ArticleIdList", [])
        for aid in article_ids:
            if hasattr(aid, "attributes") and aid.attributes.get("IdType") == "doi":
                doi = str(aid)
                break

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
            "doi": doi,
        }

    except Exception:
        return None


def classify_study_type(pub_types: list, title: str, abstract: str) -> str:
    """
    Classify the study type based on publication types and content.

    Args:
        pub_types: List of publication type strings
        title: Article title
        abstract: Article abstract

    Returns:
        Study type classification string
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
