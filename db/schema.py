# db/schema.py

import sqlite3
import os
from config.config_loader import get_config
from utils.logger import setup_logger
from utils.helpers import ensure_directory_exists

log = setup_logger()
config = get_config()
DB_PATH = config["database"]["path"]

def create_tables():
    """Create the SQLite tables if they don't exist."""
    ensure_directory_exists(os.path.dirname(DB_PATH))
    log.info(f"Initializing database at {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id TEXT PRIMARY KEY,
        url TEXT,
        title TEXT,
        body TEXT,
        subreddit TEXT,
        created_utc REAL,
        last_active REAL,
        processed_at TEXT,
        relevance_score REAL,
        emotion_score REAL,
        pain_score REAL,
        lead_type TEXT,
        tags TEXT,
        roi_weight INTEGER,
        community_type TEXT,
        type TEXT,  -- 'post' or 'comment'
        insight_processed INTEGER DEFAULT 0
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS offers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        network TEXT NOT NULL,
        payout INTEGER NOT NULL,
        url TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS content (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        offer_id INTEGER NOT NULL,
        linkedin_article TEXT NOT NULL,
        reddit_post TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (offer_id) REFERENCES offers (id)
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id TEXT PRIMARY KEY,
        processed_at TEXT
    );
    """)

    c.execute("CREATE INDEX IF NOT EXISTS idx_posts_processed_at ON posts(processed_at);")
    c.execute("CREATE INDEX IF NOT EXISTS idx_posts_relevance ON posts(relevance_score);")
    c.execute("CREATE INDEX IF NOT EXISTS idx_posts_roi ON posts(roi_weight);")
    c.execute("CREATE INDEX IF NOT EXISTS idx_posts_subreddit ON posts(subreddit);")

    conn.commit()
    conn.close()
    log.info("Database tables created successfully")

if __name__ == "__main__":
    create_tables()
    print(f"Database initialized at {DB_PATH}")
