import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import unittest
import json
from unittest.mock import MagicMock
from modules.flashcard_generator import FlashcardGenerator

class TestFlashcardGenerator(unittest.TestCase):

    def setUp(self):
        self.mock_ai_client = MagicMock()
        self.mock_ai_client.generate_text.return_value = json.dumps([
            {"front": "What is the powerhouse of the cell?", "back": "Mitochondria"},
            {"front": "What molecule stores cellular energy?", "back": "ATP"}
        ])
        self.generator = FlashcardGenerator(ai_client=self.mock_ai_client)

    def test_generate_flashcards_returns_expected_number(self):
        cards = self.generator.generate_flashcards("Cell Biology", "Some content", num_cards=2)
        self.assertEqual(len(cards), 2)

    def test_generate_flashcards_uses_ai_generated_content(self):
        cards = self.generator.generate_flashcards("Cell Biology", "Some content", num_cards=2)
        self.assertEqual(cards[0]["front"], "What is the powerhouse of the cell?")
        self.assertEqual(cards[0]["back"], "Mitochondria")

    def test_new_flashcards_default_to_unknown_status(self):
        cards = self.generator.generate_flashcards("Cell Biology", "Some content", num_cards=1)
        self.assertEqual(cards[0]["status"], "unknown")

    def test_get_flashcards_returns_all_created_cards(self):
        self.generator.generate_flashcards("Cell Biology", "Some content", num_cards=2)
        self.assertEqual(len(self.generator.get_flashcards()), 2)

    def test_mark_flashcard_updates_status(self):
        cards = self.generator.generate_flashcards("Cell Biology", "Some content", num_cards=1)
        result = self.generator.mark_flashcard(cards[0]["id"], "known")
        self.assertTrue(result)
        self.assertEqual(self.generator.get_flashcards()[0]["status"], "known")

    def test_mark_flashcard_rejects_invalid_status(self):
        cards = self.generator.generate_flashcards("Cell Biology", "Some content", num_cards=1)
        result = self.generator.mark_flashcard(cards[0]["id"], "maybe")
        self.assertFalse(result)

    def test_delete_flashcard_removes_it(self):
        cards = self.generator.generate_flashcards("Cell Biology", "Some content", num_cards=1)
        result = self.generator.delete_flashcard(cards[0]["id"])
        self.assertTrue(result)
        self.assertEqual(len(self.generator.get_flashcards()), 0)

    def test_delete_flashcard_with_invalid_id_returns_false(self):
        result = self.generator.delete_flashcard(999)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()