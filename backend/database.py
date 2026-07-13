"""
🗄️ Database Module - SQLite CRUD & Analytics
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "msl_copilot.db")


def _get_connection():
    """Get SQLite database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables."""
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kol_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            institution TEXT,
            specialty TEXT,
            therapeutic_area TEXT,
            tier TEXT,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kol_name TEXT NOT NULL,
            type TEXT,
            date TEXT,
            therapeutic_area TEXT,
            notes TEXT,
            followup TEXT,
            logged_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pmid TEXT,
            title TEXT,
            authors TEXT,
            journal TEXT,
            year TEXT,
            abstract TEXT,
            study_type TEXT,
            saved_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# Initialize on import
init_db()


def add_kol(profile: dict) -> int:
    """Save a KOL profile."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO kol_profiles (name, institution, specialty, therapeutic_area, tier, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        profile.get("name", ""),
        profile.get("institution", ""),
        profile.get("specialty", ""),
        profile.get("therapeutic_area", ""),
        profile.get("tier", ""),
        profile.get("notes", ""),
    ))
    conn.commit()
    profile_id = cursor.lastrowid
    conn.close()
    return profile_id


def get_all_kols() -> list:
    """Get all KOL profiles."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kol_profiles ORDER BY name")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def search_kols(query: str) -> list:
    """Search KOL profiles by name."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kol_profiles WHERE name LIKE ?", (f"%{query}%",))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def log_interaction(interaction: dict) -> int:
    """Save an interaction."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO interactions (kol_name, type, date, therapeutic_area, notes, followup)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        interaction.get("kol_name", ""),
        interaction.get("type", ""),
        interaction.get("date", ""),
        interaction.get("therapeutic_area", ""),
        interaction.get("notes", ""),
        interaction.get("followup", ""),
    ))
    conn.commit()
    interaction_id = cursor.lastrowid
    conn.close()
    return interaction_id


def get_all_interactions() -> list:
    """Get all interactions."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM interactions ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_interaction_stats() -> dict:
    """Get aggregated stats."""
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as count FROM interactions")
    total = cursor.fetchone()["count"]

    cursor.execute("SELECT COUNT(DISTINCT kol_name) as count FROM interactions")
    unique_kols = cursor.fetchone()["count"]

    cursor.execute("SELECT COUNT(*) as count FROM saved_articles")
    saved = cursor.fetchone()["count"]

    conn.close()
    return {"total_interactions": total, "unique_kols": unique_kols, "saved_articles": saved}


def save_article(article: dict) -> int:
    """Save an article to the library."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO saved_articles (pmid, title, authors, journal, year, abstract, study_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        article.get("pmid", ""),
        article.get("title", ""),
        article.get("authors", ""),
        article.get("journal", ""),
        article.get("year", ""),
        article.get("abstract", ""),
        article.get("study_type", ""),
    ))
    conn.commit()
    article_id = cursor.lastrowid
    conn.close()
    return article_id


def get_saved_articles() -> list:
    """Get all saved articles."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM saved_articles ORDER BY saved_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
