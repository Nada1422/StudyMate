
import sqlite3

DB_NAME = "studymate.db"


def get_connection():

    conn = sqlite3.connect(DB_NAME)

    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def init_db():

    with get_connection() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL UNIQUE
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                subject_id INTEGER NOT NULL,
                deadline TEXT NOT NULL,

                priority TEXT NOT NULL
                    CHECK(priority IN ('Low', 'Medium', 'High')),

                status TEXT NOT NULL DEFAULT 'Pending'
                    CHECK(status IN (
                        'Pending',
                        'In Progress',
                        'Completed'
                    )),

                FOREIGN KEY (subject_id)
                    REFERENCES subjects(id)
                    ON DELETE RESTRICT
            )
        """)


# =========================
# SUBJECT MANAGEMENT
# =========================

def add_subject(code, name):

    code = code.strip().upper()
    name = name.strip()

    if not code or not name:

        return False, "Please enter both subject code and name."

    try:

        with get_connection() as conn:

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

    with get_connection() as conn:

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

        with get_connection() as conn:

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

    try:

        with get_connection() as conn:

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

    except sqlite3.IntegrityError:

        return False, (
            "Cannot delete this subject because it has "
            "associated tasks. Delete its tasks first."
        )


# =========================
# TASK MANAGEMENT
# =========================

def add_task(title, description, subject_id, deadline, priority):

    title = title.strip()
    description = description.strip()

    if not title:

        return False, "Task title is required."

    if not deadline:

        return False, "Deadline is required."

    try:

        with get_connection() as conn:

            conn.execute(
                """
                INSERT INTO tasks
                (title, description, subject_id, deadline, priority)
                VALUES (?, ?, ?, ?, ?)
                """,
                (title, description, subject_id, deadline, priority)
            )

        return True, "Task added successfully!"

    except sqlite3.IntegrityError:

        return False, "Invalid subject or task data."


def get_tasks():

    with get_connection() as conn:

        rows = conn.execute(
            """
            SELECT
                tasks.id,
                tasks.title,
                tasks.description,
                tasks.subject_id,
                subjects.code,
                subjects.name,
                tasks.deadline,
                tasks.priority,
                tasks.status

            FROM tasks

            JOIN subjects
                ON tasks.subject_id = subjects.id

            ORDER BY
                tasks.deadline ASC,

                CASE tasks.priority
                    WHEN 'High' THEN 1
                    WHEN 'Medium' THEN 2
                    WHEN 'Low' THEN 3
                END ASC
            """
        ).fetchall()

    return rows


def update_task(
    task_id,
    title,
    description,
    subject_id,
    deadline,
    priority,
    status
):

    title = title.strip()
    description = description.strip()

    if not title:

        return False, "Task title is required."

    try:

        with get_connection() as conn:

            cursor = conn.execute(
                """
                UPDATE tasks

                SET
                    title = ?,
                    description = ?,
                    subject_id = ?,
                    deadline = ?,
                    priority = ?,
                    status = ?

                WHERE id = ?
                """,

                (
                    title,
                    description,
                    subject_id,
                    deadline,
                    priority,
                    status,
                    task_id
                )
            )

            if cursor.rowcount == 0:

                return False, "Task not found."

        return True, "Task updated successfully!"

    except sqlite3.IntegrityError:

        return False, "Invalid task data."


def delete_task(task_id):

    with get_connection() as conn:

        cursor = conn.execute(
            """
            DELETE FROM tasks
            WHERE id = ?
            """,
            (task_id,)
        )

        if cursor.rowcount == 0:

            return False, "Task not found."

    return True, "Task deleted successfully!"