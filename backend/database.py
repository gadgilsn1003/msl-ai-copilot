"""
🗄️ Database Module - SQLite CRUD & Analytics

Handles persistent storage for:
- KOL interactions
- KOL profiles
- Saved articles
- Dashboard analytics queries
"""

import sqlite3
import os
import json
from datetime import datetime


# =================================================================================
# DATABASE SETUP
# =================================================================================
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "msl_copilot.db")


def get_connection():
    """Get SQLite database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialize database tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # KOL Profiles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kol_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            institution TEXT,
            specialty TEXT,
            therapeutic_area TEXT,
            tier TEXT,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Interactions table
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

    # Saved articles table
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
init_database()


# =================================================================================
# KOL PROFILES
# =================================================================================
def save_kol_profile(profile: dict) -> int:
    """Save a KOL profile to the database."""
    conn = get_connection()
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


def get_all_kol_profiles() -> list:
    """Get all KOL profiles."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM kol_profiles ORDER BY name")
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_kol_profile(name: str) -> dict:
    """Get a specific KOL profile by name."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM kol_profiles WHERE name LIKE ?", (f"%{name}%",))
    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None


# =================================================================================
# INTERACTIONS
# =================================================================================
def save_interaction(interaction: dict) -> int:
    """Save an interaction to the database."""
    conn = get_connection()
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
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM interactions ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_interactions_by_kol(kol_name: str) -> list:
    """Get all interactions for a specific KOL."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM interactions WHERE kol_name LIKE ? ORDER BY date DESC",
        (f"%{kol_name}%",)
    )
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


# =================================================================================
# SAVED ARTICLES
# =================================================================================
def save_article(article: dict) -> int:
    """Save an article to the library."""
    conn = get_connection()
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
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM saved_articles ORDER BY saved_at DESC")
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


# =================================================================================
# DASHBOARD ANALYTICS
# =================================================================================
def get_dashboard_stats() -> dict:
    """Get aggregated stats for the dashboard."""
    conn = get_connection()
    cursor = conn.cursor()

    # Total interactions
    cursor.execute("SELECT COUNT(*) as count FROM interactions")
    total_interactions = cursor.fetchone()["count"]

    # Unique KOLs
    cursor.execute("SELECT COUNT(DISTINCT kol_name) as count FROM interactions")
    unique_kols = cursor.fetchone()["count"]

    # Saved articles
    cursor.execute("SELECT COUNT(*) as count FROM saved_articles")
    saved_articles = cursor.fetchone()["count"]

    # Interactions by type
    cursor.execute("""
        SELECT type, COUNT(*) as count
        FROM interactions
        GROUP BY type
        ORDER BY count DESC
    """)
    by_type = [dict(row) for row in cursor.fetchall()]

    # Interactions by therapeutic area
    cursor.execute("""
        SELECT therapeutic_area, COUNT(*) as count
        FROM interactions
        GROUP BY therapeutic_area
        ORDER BY count DESC
    """)
    by_ta = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return {
        "total_interactions": total_interactions,
        "unique_kols": unique_kols,
        "saved_articles": saved_articles,
        "by_type": by_type,
        "by_therapeutic_area": by_ta,
    }
