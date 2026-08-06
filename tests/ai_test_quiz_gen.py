

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import json
from unittest.mock import MagicMock
from modules.quiz_generator import QuizGenerator


class TestQuizGenerator(unittest.TestCase):

    def setUp(self):
        self.mock_ai_client = MagicMock()
        self.mock_ai_client.generate_text.return_value = json.dumps([
            {"question": "What do plants convert into energy?",
             "options": ["Sunlight", "Water", "Soil", "Air"],
             "answer": "Sunlight"},
            {"question": "Where does photosynthesis mainly occur?",
             "options": ["Roots", "Chloroplasts", "Stem", "Flowers"],
             "answer": "Chloroplasts"}
        ])
        self.generator = QuizGenerator(ai_client=self.mock_ai_client)

    def test_generate_quiz_returns_ai_generated_questions(self):
        quiz = self.generator.generate_quiz("Photosynthesis", "Plants convert sunlight into energy.", num_questions=2)
        self.assertEqual(len(quiz["questions"]), 2)
        self.assertEqual(quiz["questions"][0]["answer"], "Sunlight")

    def test_generate_quiz_stores_note_title(self):
        quiz = self.generator.generate_quiz("Photosynthesis", "Some content")
        self.assertEqual(quiz["note_title"], "Photosynthesis")

    def test_generate_quiz_calls_ai_client(self):
        self.generator.generate_quiz("Photosynthesis", "Some content", num_questions=2)
        self.mock_ai_client.generate_text.assert_called_once()

    def test_get_quizzes_returns_all_created_quizzes(self):
        self.generator.generate_quiz("Quiz 1", "Content 1")
        self.generator.generate_quiz("Quiz 2", "Content 2")
        self.assertEqual(len(self.generator.get_quizzes()), 2)

    def test_delete_quiz_removes_it(self):
        quiz = self.generator.generate_quiz("Photosynthesis", "Some content")
        result = self.generator.delete_quiz(quiz["id"])
        self.assertTrue(result)
        self.assertEqual(len(self.generator.get_quizzes()), 0)

    def test_delete_quiz_with_invalid_id_returns_false(self):
        result = self.generator.delete_quiz(999)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()