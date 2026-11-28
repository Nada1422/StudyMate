import sqlite3
import unittest
from contextlib import nullcontext
from datetime import date
from unittest.mock import patch

import database as db
from notifications import get_notifications


class TestNotificationIntegration(unittest.TestCase):

    def test_notifications_with_sqlite(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("PRAGMA foreign_keys = ON")

        try:
            with patch.object(
                db, "get_connection",
                lambda: nullcontext(conn)
            ):
                db.init_db()

                success, _ = db.add_subject(
                    "CS101", "Computer Science"
                )
                self.assertTrue(success)

                subject_id = db.get_subjects()[0][0]

                sample_tasks = [
                    ("Late", "2026-11-24"),
                    ("Today", "2026-11-25"),
                    ("Soon", "2026-11-27"),
                    ("Later", "2026-12-20"),
                    ("Done", "2026-11-24"),
                ]

                for title, deadline in sample_tasks:
                    success, _ = db.add_task(
                        title, "", subject_id,
                        deadline, "High"
                    )
                    self.assertTrue(success)

                done_id = next(
                    task[0] for task in db.get_tasks()
                    if task[1] == "Done"
                )

                success, _ = db.update_task(
                    done_id, "Done", "", subject_id,
                    "2026-11-24", "High", "Completed"
                )
                self.assertTrue(success)

                alerts = get_notifications(
                    today=date(2026, 11, 25)
                )

                actual = {
                    alert["title"]: alert["type"]
                    for alert in alerts
                }

                self.assertEqual(actual, {
                    "Late": "Overdue",
                    "Today": "Due Today",
                    "Soon": "Upcoming",
                })

        finally:
            conn.close()


if __name__ == "__main__":
    unittest.main()
