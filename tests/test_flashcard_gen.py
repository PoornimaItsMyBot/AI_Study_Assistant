import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import unittest
from modules.flashcard_generator import FlashcardGenerator


class TestFlashcardGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = FlashcardGenerator()
        self.sample_content = (
            "Mitochondria are the powerhouse of the cell. "
            "They generate most of the cell's supply of adenosine triphosphate. "
            "This energy is used to power various cellular processes."
        )

    def test_generate_flashcards_creates_expected_number(self):
        cards = self.generator.generate_flashcards("Cell Biology", self.sample_content, num_cards=2)
        self.assertEqual(len(cards), 2)

    def test_new_flashcards_default_to_unknown_status(self):
        cards = self.generator.generate_flashcards("Cell Biology", self.sample_content, num_cards=1)
        self.assertEqual(cards[0]["status"], "unknown")

    def test_flashcard_has_front_and_back(self):
        cards = self.generator.generate_flashcards("Cell Biology", self.sample_content, num_cards=1)
        self.assertIn("front", cards[0])
        self.assertIn("back", cards[0])

    def test_get_flashcards_returns_all_created_cards(self):
        self.generator.generate_flashcards("Cell Biology", self.sample_content, num_cards=2)
        self.assertEqual(len(self.generator.get_flashcards()), 2)

    def test_mark_flashcard_updates_status(self):
        cards = self.generator.generate_flashcards("Cell Biology", self.sample_content, num_cards=1)
        result = self.generator.mark_flashcard(cards[0]["id"], "known")
        self.assertTrue(result)
        self.assertEqual(self.generator.get_flashcards()[0]["status"], "known")

    def test_mark_flashcard_rejects_invalid_status(self):
        cards = self.generator.generate_flashcards("Cell Biology", self.sample_content, num_cards=1)
        result = self.generator.mark_flashcard(cards[0]["id"], "maybe")
        self.assertFalse(result)

    def test_mark_flashcard_with_invalid_id_returns_false(self):
        result = self.generator.mark_flashcard(999, "known")
        self.assertFalse(result)

    def test_delete_flashcard_removes_it(self):
        cards = self.generator.generate_flashcards("Cell Biology", self.sample_content, num_cards=1)
        result = self.generator.delete_flashcard(cards[0]["id"])
        self.assertTrue(result)
        self.assertEqual(len(self.generator.get_flashcards()), 0)

    def test_delete_flashcard_with_invalid_id_returns_false(self):
        result = self.generator.delete_flashcard(999)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()