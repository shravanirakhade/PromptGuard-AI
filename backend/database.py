"""
PromptGuard AI - Database Management
"""

import sqlite3

DATABASE_NAME = "promptguard.db"


def get_connection():
    """Create a database connection."""

    return sqlite3.connect(DATABASE_NAME)


def create_table():
    """Create prompt history table."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prompt_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_prompt TEXT NOT NULL,
            improved_prompt TEXT NOT NULL,
            ai_response TEXT NOT NULL,
            score INTEGER,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_prompt(original, improved, response, score, status):
    """Save prompt testing results."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO prompt_history
        (original_prompt, improved_prompt, ai_response, score, status)
        VALUES (?, ?, ?, ?, ?)
    """, (original, improved, response, score, status))

    connection.commit()
    connection.close()


def get_all_history():
    """Retrieve all previous testing records."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM prompt_history
        ORDER BY id DESC
    """)

    history = cursor.fetchall()

    connection.close()

    return history