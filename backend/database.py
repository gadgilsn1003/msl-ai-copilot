"""
backend/database.py
SQLite-based local database for MSL AI Copilot.
Stores KOL profiles, field interaction logs, saved articles, and insights.
Falls back to SQLite if Supabase is not configured.
"""

import os
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

DB_PATH = Path("msl_copilot.db")


def get_connection() -> sqlite3.Connection:
    """Get SQLite connection with row factory for dict-like access."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize all database tables. Run once on app startup."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS kol_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialty TEXT,
            institution TEXT,
            therapeutic_area TEXT,
            email TEXT,
            notes TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS field_interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kol_id INTEGER REFERENCES kol_profiles(id),
            kol_name TEXT,
            interaction_date TEXT,
            interaction_type TEXT,
            notes TEXT,
            topics_discussed TEXT,
            unmet_needs TEXT,
            action_items TEXT,
            insight_analysis TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS saved_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pmid TEXT UNIQUE,
            title TEXT,
            abstract TEXT,
            authors TEXT,
            journal TEXT,
            pub_date TEXT,
            doi TEXT,
            url TEXT,
            ai_summary TEXT,
            compliance_status TEXT,
            therapeutic_area TEXT,
            saved_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS kol_briefings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kol_id INTEGER REFERENCES kol_profiles(id),
            kol_name TEXT,
            briefing_content TEXT,
            meeting_date TEXT,
            therapeutic_area TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS msl_insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_interaction_id INTEGER,
            insight_type TEXT,
            insight_text TEXT,
            therapeutic_area TEXT,
            kol_name TEXT,
            flagged_for_review INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()


# ── KOL Profile CRUD ───────────────────────────────────────────────────────────────────

def add_kol(name: str, specialty: str, institution: str,
            therapeutic_area: str, notes: str = "", email: str = "") -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO kol_profiles (name, specialty, institution, therapeutic_area, email, notes)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (name, specialty, institution, therapeutic_area, email, notes)
    )
    conn.commit()
    kol_id = cursor.lastrowid
    conn.close()
    return kol_id


def get_all_kols() -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kol_profiles ORDER BY name")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_kol_by_id(kol_id: int) -> Optional[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kol_profiles WHERE id = ?", (kol_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def search_kols(query: str) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM kol_profiles WHERE name LIKE ? OR institution LIKE ? OR specialty LIKE ?",
        (f"%{query}%", f"%{query}%", f"%{query}%")
    )
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


# ── Field Interaction CRUD ───────────────────────────────────────────────────────────

def log_interaction(kol_name: str, interaction_date: str, interaction_type: str,
                    notes: str, topics: list = None, unmet_needs: str = "",
                    action_items: str = "", insight_analysis: str = "",
                    kol_id: Optional[int] = None) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO field_interactions
           (kol_id, kol_name, interaction_date, interaction_type, notes,
            topics_discussed, unmet_needs, action_items, insight_analysis)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (kol_id, kol_name, interaction_date, interaction_type, notes,
         json.dumps(topics or []), unmet_needs, action_items, insight_analysis)
    )
    conn.commit()
    interaction_id = cursor.lastrowid
    conn.close()
    return interaction_id


def get_interactions_by_kol(kol_name: str) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM field_interactions WHERE kol_name LIKE ? ORDER BY interaction_date DESC",
        (f"%{kol_name}%",)
    )
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_all_interactions(limit: int = 100) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM field_interactions ORDER BY interaction_date DESC LIMIT ?", (limit,)
    )
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


# ── Saved Articles CRUD ──────────────────────────────────────────────────────────────

def save_article(article_dict: dict, ai_summary: str = "",
                compliance_status: str = "UNCHECKED",
                therapeutic_area: str = "") -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT OR REPLACE INTO saved_articles
               (pmid, title, abstract, authors, journal, pub_date, doi, url,
                ai_summary, compliance_status, therapeutic_area)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (article_dict.get("pmid"), article_dict.get("title"),
             article_dict.get("abstract"), article_dict.get("authors"),
             article_dict.get("journal"), article_dict.get("pub_date"),
             article_dict.get("doi"), article_dict.get("url"),
             ai_summary, compliance_status, therapeutic_area)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"[DB Error] save_article: {e}")
        return False
    finally:
        conn.close()


def get_saved_articles(therapeutic_area: Optional[str] = None) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    if therapeutic_area:
        cursor.execute(
            "SELECT * FROM saved_articles WHERE therapeutic_area = ? ORDER BY saved_at DESC",
            (therapeutic_area,)
        )
    else:
        cursor.execute("SELECT * FROM saved_articles ORDER BY saved_at DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


# ── Analytics Queries for Impact Dashboard ─────────────────────────────────────────

def get_interaction_stats() -> dict:
    """Aggregate stats for the Impact Dashboard."""
    conn = get_connection()
    cursor = conn.cursor()

    stats = {}

    cursor.execute("SELECT COUNT(*) as total FROM field_interactions")
    stats["total_interactions"] = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(DISTINCT kol_name) as total FROM field_interactions")
    stats["unique_kols"] = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as total FROM saved_articles")
    stats["saved_articles"] = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT kol_name, COUNT(*) as count
        FROM field_interactions
        GROUP BY kol_name
        ORDER BY count DESC
        LIMIT 10
    """)
    stats["top_kols"] = [{"kol": row["kol_name"], "count": row["count"]}
                         for row in cursor.fetchall()]

    cursor.execute("""
        SELECT interaction_type, COUNT(*) as count
        FROM field_interactions
        GROUP BY interaction_type
    """)
    stats["by_type"] = [{"type": row["interaction_type"], "count": row["count"]}
                        for row in cursor.fetchall()]

    cursor.execute("""
        SELECT strftime('%Y-%m', interaction_date) as month, COUNT(*) as count
        FROM field_interactions
        GROUP BY month
        ORDER BY month DESC
        LIMIT 12
    """)
    stats["by_month"] = [{"month": row["month"], "count": row["count"]}
                         for row in cursor.fetchall()]

    conn.close()
    return stats
