"""
backend/pubmed_fetcher.py
PubMed / NCBI Entrez API integration for MSL AI Copilot.
"""

import os
import time
from typing import Optional
from Bio import Entrez
from dataclasses import dataclass, field

Entrez.email = os.getenv("NCBI_EMAIL", "msl-copilot@example.com")
Entrez.api_key = os.getenv("NCBI_API_KEY", "")


@dataclass
class PubMedArticle:
    pmid: str
    title: str
    abstract: str
    authors: list
    journal: str
    pub_date: str
    doi: str
    url: str
    keywords: list = field(default_factory=list)
    mesh_terms: list = field(default_factory=list)

    def to_dict(self):
        return {
            "pmid": self.pmid,
            "title": self.title,
            "abstract": self.abstract,
            "authors": ", ".join(self.authors[:3]) + (" et al." if len(self.authors) > 3 else ""),
            "journal": self.journal,
            "pub_date": self.pub_date,
            "doi": self.doi,
            "url": self.url,
            "keywords": self.keywords,
            "mesh_terms": self.mesh_terms,
        }


def search_pubmed(query: str, max_results: int = 20,
                 date_range: Optional[tuple] = None, sort_by: str = "relevance") -> list:
    if date_range:
        start, end = date_range
    mindate, maxdate = str(start), str(end)
                     else:
        mindate, maxdate = None, None
    sort_map = {"relevance": "relevance", "pub_date": "pub+date"}
    try:
        handle = Entrez.esearch(db="pubmed", term=query,
                                retmax=min(max_results, 100),
                                sort=sort_map.get(sort_by, "relevance"))
                                    datetype="pdat",
                                    mindate=mindate, maxdate=maxdate
        record = Entrez.read(handle)
        handle.close()
        return record.get("IdList", [])
    except Exception as e:
        print(f"[PubMed Search Error] {e}")
        return []


def fetch_articles(pmids: list) -> list:
    if not pmids:
        return []
    articles = []
    for i in range(0, len(pmids), 20):
        chunk = pmids[i:i + 20]
        try:
            handle = Entrez.efetch(db="pubmed", id=",".join(chunk),
                                   rettype="xml", retmode="xml")
            records = Entrez.read(handle)
            handle.close()
            for record in records.get("PubmedArticle", []):
                article = _parse_article(record)
                if article:
                    articles.append(article)
            time.sleep(0.1 if Entrez.api_key else 0.34)
        except Exception as e:
            print(f"[PubMed Fetch Error] {e}")
    return articles


def _parse_article(record: dict) -> Optional[PubMedArticle]:
    try:
        medline = record["MedlineCitation"]
        article = medline["Article"]
        pmid = str(medline["PMID"])
        title = str(article.get("ArticleTitle", "No title"))
        abstract_data = article.get("Abstract", {})
        abstract_texts = abstract_data.get("AbstractText", [])
        if isinstance(abstract_texts, list):
            abstract = " ".join(str(t) for t in abstract_texts)
        else:
            abstract = str(abstract_texts)
        author_list = article.get("AuthorList", [])
        authors = []
        for a in author_list:
            last = a.get("LastName", "")
            fore = a.get("ForeName", "")
            if last:
                authors.append(f"{last} {fore}".strip())
        journal_info = article.get("Journal", {})
        journal = str(journal_info.get("Title", "Unknown Journal"))
        pub_date_raw = journal_info.get("JournalIssue", {}).get("PubDate", {})
        year = pub_date_raw.get("Year", pub_date_raw.get("MedlineDate", "N/A"))
        month = pub_date_raw.get("Month", "")
        pub_date = f"{month} {year}".strip()
        doi = ""
        for id_item in record.get("PubmedData", {}).get("ArticleIdList", []):
            if str(id_item.attributes.get("IdType")) == "doi":
                doi = str(id_item)
                break
        kw_list = medline.get("KeywordList", [])
        keywords = [str(k) for k in kw_list[0]] if kw_list else []
        mesh_terms = [str(m["DescriptorName"]) for m in medline.get("MeshHeadingList", [])]
        return PubMedArticle(pmid=pmid, title=title, abstract=abstract,
                             authors=authors, journal=journal, pub_date=pub_date,
                             doi=doi, url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                             keywords=keywords, mesh_terms=mesh_terms)
    except Exception as e:
        print(f"[Parse Error] {e}")
        return None


def search_and_fetch(query: str, max_results: int = 20,
                     date_range: Optional[tuple] = None,
                     sort_by: str = "relevance") -> list:
    """Convenience wrapper: search then fetch."""
    pmids = search_pubmed(query, max_results, date_range, sort_by)
    return fetch_articles(pmids)


# Pre-built MSL therapeutic area queries
THERAPEUTIC_AREA_QUERIES = {
    "Oncology": "cancer[MeSH] OR tumor[MeSH] OR neoplasm[MeSH]",
    "Neurology": "neurology[MeSH] OR neurological disorders[MeSH]",
    "Cardiology": "cardiovascular diseases[MeSH] OR heart failure[MeSH]",
    "Immunology": "immunology[MeSH] OR autoimmune diseases[MeSH]",
    "Rare Disease": "rare diseases[MeSH] OR orphan drug[tiab]",
    "GBM / Neuro-Oncology": "glioblastoma[MeSH] OR glioma[MeSH] OR brain neoplasms[MeSH]",
}
