import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import unittest
from modules.note_manager import NoteManager


class TestNoteManager(unittest.TestCase):

    def setUp(self):
        # Runs before every test method, giving each test a fresh, clean NoteManager
        self.manager = NoteManager()

    def test_create_note(self):
        note = self.manager.create_note("Photosynthesis", "Plants convert light into energy.", "Biology")
        self.assertEqual(note["title"], "Photosynthesis")
        self.assertEqual(note["content"], "Plants convert light into energy.")
        self.assertEqual(note["subject"], "Biology")
        self.assertEqual(note["id"], 1)

    def test_create_note_without_subject(self):
        note = self.manager.create_note("Untitled", "Some content")
        self.assertIsNone(note["subject"])

    def test_get_notes_returns_all_created_notes(self):
        self.manager.create_note("Note 1", "Content 1")
        self.manager.create_note("Note 2", "Content 2")
        notes = self.manager.get_notes()
        self.assertEqual(len(notes), 2)

    def test_ids_increment_correctly(self):
        note1 = self.manager.create_note("Note 1", "Content 1")
        note2 = self.manager.create_note("Note 2", "Content 2")
        self.assertEqual(note1["id"], 1)
        self.assertEqual(note2["id"], 2)

    def test_update_note_changes_only_given_fields(self):
        note = self.manager.create_note("Old Title", "Old Content", "Old Subject")
        result = self.manager.update_note(note["id"], title="New Title")

        updated_note = self.manager.get_notes()[0]
        self.assertTrue(result)
        self.assertEqual(updated_note["title"], "New Title")
        self.assertEqual(updated_note["content"], "Old Content")  # unchanged
        self.assertEqual(updated_note["subject"], "Old Subject")  # unchanged

    def test_update_note_with_invalid_id_returns_false(self):
        result = self.manager.update_note(999, title="Doesn't matter")
        self.assertFalse(result)

    def test_delete_note_removes_it(self):
        note = self.manager.create_note("To Delete", "Content")
        result = self.manager.delete_note(note["id"])
        self.assertTrue(result)
        self.assertEqual(len(self.manager.get_notes()), 0)

    def test_delete_note_with_invalid_id_returns_false(self):
        result = self.manager.delete_note(999)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()