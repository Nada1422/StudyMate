import unittest
from datetime import date
from unittest.mock import patch
from notifications import get_notifications


TODAY = date(2026, 11, 25)


def make_task(task_id, title, deadline, status="Pending"):
    return (
        task_id, title, "", 1, "CS101",
        "Computer Science", deadline, "High", status
    )


class TestNotifications(unittest.TestCase):

    def test_overdue(self):
        tasks = [make_task(1, "Assignment", "2026-11-24")]
        with patch("notifications.get_tasks", return_value=tasks):
            result = get_notifications(today=TODAY)
        self.assertEqual(result[0]["type"], "Overdue")

    def test_due_today(self):
        tasks = [make_task(1, "Exam", "2026-11-25")]
        with patch("notifications.get_tasks", return_value=tasks):
            result = get_notifications(today=TODAY)
        self.assertEqual(result[0]["type"], "Due Today")

    def test_upcoming(self):
        tasks = [make_task(1, "Project", "2026-11-28")]
        with patch("notifications.get_tasks", return_value=tasks):
            result = get_notifications(today=TODAY)
        self.assertEqual(result[0]["type"], "Upcoming")
        self.assertEqual(result[0]["days_left"], 3)

    def test_completed_tasks_excluded(self):
        tasks = [make_task(1, "Finished", "2026-11-24", "Completed")]
        with patch("notifications.get_tasks", return_value=tasks):
            result = get_notifications(today=TODAY)
        self.assertEqual(result, [])

    def test_far_deadline_excluded(self):
        tasks = [make_task(1, "Later", "2026-12-20")]
        with patch("notifications.get_tasks", return_value=tasks):
            result = get_notifications(today=TODAY)
        self.assertEqual(result, [])

    def test_invalid_days_ahead(self):
        with self.assertRaises(ValueError):
            get_notifications(days_ahead=-1)


if __name__ == "__main__":
    unittest.main()
