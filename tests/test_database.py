import unittest
import database as db
from tempfile import TemporaryDirectory
from pathlib import Path


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.temp = TemporaryDirectory()
        self.original_db = db.DB_NAME
        db.DB_NAME = str(Path(self.temp.name) / "test.db")
        db.init_db()

    def tearDown(self):
        db.DB_NAME = self.original_db
        self.temp.cleanup()

    def test_add_subject(self):
        success, _ = db.add_subject("CS101", "Computer Science")
        self.assertTrue(success)
        self.assertEqual(len(db.get_subjects()), 1)

    def test_add_task(self):
        db.add_subject("CS101", "Computer Science")
        subject_id = db.get_subjects()[0][0]

        success, _ = db.add_task(
            "Study Python", "Chapter 1",
            subject_id, "2026-12-01", "High"
        )

        self.assertTrue(success)
        self.assertEqual(len(db.get_tasks()), 1)

    def test_deadline_validation(self):
        db.add_subject("CS101", "Computer Science")
        subject_id = db.get_subjects()[0][0]

        success, _ = db.add_task(
            "Study Python", "",
            subject_id, "", "High"
        )

        self.assertFalse(success)

    def test_data_persistence(self):
        db.add_subject("CS101", "Computer Science")
        db.init_db()
        self.assertEqual(len(db.get_subjects()), 1)

    def test_update_and_delete(self):
        db.add_subject("CS101", "Computer Science")
        subject_id = db.get_subjects()[0][0]

        db.add_task(
            "Study Python", "",
            subject_id, "2026-12-01", "High"
        )

        task_id = db.get_tasks()[0][0]

        success, _ = db.update_task(
            task_id, "Study SQL", "",
            subject_id, "2026-12-02",
            "Medium", "In Progress"
        )

        self.assertTrue(success)
        self.assertEqual(db.get_tasks()[0][1], "Study SQL")
        self.assertTrue(db.delete_task(task_id)[0])


if __name__ == "__main__":
    unittest.main()
