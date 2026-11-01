
import sqlite3

DB_NAME = "studymate.db"


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)


def add_subject(name):
    name = name.strip()

    if not name:
        return False, "Please enter a subject."

    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute(
                "INSERT INTO subjects (name) VALUES (?)",
                (name,)
            )
        return True, f"{name} added successfully!"

    except sqlite3.IntegrityError:
        return False, f"{name} already exists!"


def get_subjects():
    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute(
            "SELECT id, name FROM subjects ORDER BY name"
        ).fetchall()

    return rows
