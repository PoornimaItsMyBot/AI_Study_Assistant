
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import os
import shutil
from main import build_app, save_all, restore_data


class TestMain(unittest.TestCase):

    def setUp(self):
        # Use a separate, temporary folder so tests never touch real app data.
        # build_app() now accepts data_folder directly, so nothing is loaded
        # from the real "data" folder at any point during this test.
        self.test_folder = "data_test_main"
        self.app = build_app(data_folder=self.test_folder)

        self.sample_content = (
            "Photosynthesis is the process plants use to convert sunlight into energy. "
            "This process mainly takes place inside the chloroplasts of plant cells."
        )

    def tearDown(self):
        # Runs after every test, deleting the temporary test folder and everything in it
        if os.path.exists(self.test_folder):
            shutil.rmtree(self.test_folder)

    def test_restore_data_sets_list_and_next_id(self):
        sample_notes = [{"id": 5, "title": "A", "content": "B", "subject": None}]
        restore_data(self.app["note_manager"], sample_notes, "notes")

        self.assertEqual(self.app["note_manager"].get_notes(), sample_notes)
        self.assertEqual(self.app["note_manager"].next_id, 6)

    def test_restore_data_with_empty_list_resets_next_id_to_one(self):
        restore_data(self.app["note_manager"], [], "notes")
        self.assertEqual(self.app["note_manager"].next_id, 1)

    def test_full_session_save_and_reload(self):
        note = self.app["note_manager"].create_note("Photosynthesis", self.sample_content, "Biology")
        self.app["quiz_generator"].generate_quiz(note["title"], note["content"], num_questions=2)
        self.app["flashcard_generator"].generate_flashcards(note["title"], note["content"], num_cards=2)

        save_all(self.app)

        # Simulate restarting the app by loading data straight from the same file manager
        fm = self.app["file_manager"]
        reloaded_notes = fm.load_notes()
        reloaded_quizzes = fm.load_quizzes()
        reloaded_flashcards = fm.load_flashcards()

        self.assertEqual(len(reloaded_notes), 1)
        self.assertEqual(len(reloaded_quizzes), 1)
        self.assertEqual(len(reloaded_flashcards), 2)
        self.assertEqual(reloaded_notes[0]["title"], "Photosynthesis")

    def test_full_session_creates_fresh_app_instance_correctly(self):
        # Create and save data in the first "session"
        note = self.app["note_manager"].create_note("Newton's Laws", "Force equals mass times acceleration.", "Physics")
        self.app["quiz_generator"].generate_quiz(note["title"], note["content"], num_questions=1)
        save_all(self.app)

        # Build a completely new app instance pointed at the same test folder,
        # simulating the app being restarted
        new_app = build_app(data_folder=self.test_folder)

        self.assertEqual(len(new_app["note_manager"].get_notes()), 1)
        self.assertEqual(new_app["note_manager"].get_notes()[0]["title"], "Newton's Laws")

        # Confirm the ID counter continued correctly instead of resetting to 1
        second_note = new_app["note_manager"].create_note("Second Note", "Some content")
        self.assertEqual(second_note["id"], 2)


if __name__ == "__main__":
    unittest.main()