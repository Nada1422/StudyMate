
import sqlite3

DB_NAME = "studymate.db"


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL UNIQUE
            )
        """)


def add_subject(code, name):
    code = code.strip().upper()
    name = name.strip()

    if not code or not name:
        return False, "Please enter both subject code and name."

    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute(
                """
                INSERT INTO subjects (code, name)
                VALUES (?, ?)
                """,
                (code, name)
            )

        return True, f"{code} - {name} added successfully!"

    except sqlite3.IntegrityError:
        return False, "Subject code or name already exists!"


def get_subjects():
    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute(
            """
            SELECT id, code, name
            FROM subjects
            ORDER BY code
            """
        ).fetchall()

    return rows


def update_subject(subject_id, code, name):
    code = code.strip().upper()
    name = name.strip()

    if not code or not name:
        return False, "Please enter both subject code and name."

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.execute(
                """
                UPDATE subjects
                SET code = ?, name = ?
                WHERE id = ?
                """,
                (code, name, subject_id)
            )

            if cursor.rowcount == 0:
                return False, "Subject not found."

        return True, "Subject updated successfully!"

    except sqlite3.IntegrityError:
        return False, "Subject code or name already exists!"


def delete_subject(subject_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute(
            """
            DELETE FROM subjects
            WHERE id = ?
            """,
            (subject_id,)
        )

        if cursor.rowcount == 0:
            return False, "Subject not found."

    return True, "Subject deleted successfully!"
