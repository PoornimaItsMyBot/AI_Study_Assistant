import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import os
import shutil
from modules.file_manager import FileManager


class TestFileManager(unittest.TestCase):

    def setUp(self):
        # Use a separate, temporary folder so tests never touch real app data
        self.test_folder = "data_test"
        self.manager = FileManager(data_folder=self.test_folder)

        self.sample_notes = [
            {"id": 1, "title": "Photosynthesis", "content": "Plants convert light into energy.", "subject": "Biology"}
        ]
        self.sample_quizzes = [
            {"id": 1, "note_title": "Photosynthesis", "questions": [{"question": "...", "answer": "light"}]}
        ]
        self.sample_flashcards = [
            {"id": 1, "note_title": "Cell Biology", "front": "...", "back": "Mitochondria", "status": "known"}
        ]

    def tearDown(self):
        # Runs after every test, deleting the temporary test folder and everything in it
        if os.path.exists(self.test_folder):
            shutil.rmtree(self.test_folder)

    def test_save_and_load_notes(self):
        self.manager.save_notes(self.sample_notes)
        loaded = self.manager.load_notes()
        self.assertEqual(loaded, self.sample_notes)

    def test_save_and_load_quizzes(self):
        self.manager.save_quizzes(self.sample_quizzes)
        loaded = self.manager.load_quizzes()
        self.assertEqual(loaded, self.sample_quizzes)

    def test_save_and_load_flashcards(self):
        self.manager.save_flashcards(self.sample_flashcards)
        loaded = self.manager.load_flashcards()
        self.assertEqual(loaded, self.sample_flashcards)

    def test_load_notes_when_file_does_not_exist(self):
        loaded = self.manager.load_notes()
        self.assertEqual(loaded, [])

    def test_load_quizzes_when_file_does_not_exist(self):
        loaded = self.manager.load_quizzes()
        self.assertEqual(loaded, [])

    def test_load_flashcards_when_file_does_not_exist(self):
        loaded = self.manager.load_flashcards()
        self.assertEqual(loaded, [])

    def test_data_folder_is_created_automatically(self):
        self.assertTrue(os.path.isdir(self.test_folder))


if __name__ == "__main__":
    unittest.main()