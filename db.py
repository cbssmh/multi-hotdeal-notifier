import sqlite3
from contextlib import closing

DB_PATH = "posts.db"


def init_db():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    site_name TEXT NOT NULL,
                    post_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (site_name, post_id)
                )
            """)


def has_any_posts(site_name):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cursor = conn.execute("""
            SELECT 1
            FROM posts
            WHERE site_name = ?
            LIMIT 1
        """, (site_name,))
        return cursor.fetchone() is not None


def has_post(site_name, post_id):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cursor = conn.execute("""
            SELECT 1
            FROM posts
            WHERE site_name = ? AND post_id = ?
            LIMIT 1
        """, (site_name, post_id))
        return cursor.fetchone() is not None


def save_post(site_name, post):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute("""
                INSERT OR IGNORE INTO posts (site_name, post_id, title, url)
                VALUES (?, ?, ?, ?)
            """, (site_name, post["id"], post["title"], post["url"]))


def save_posts(site_name, posts):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.executemany("""
                INSERT OR IGNORE INTO posts (site_name, post_id, title, url)
                VALUES (?, ?, ?, ?)
            """, [
                (site_name, post["id"], post["title"], post["url"])
                for post in posts
            ])