import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from modules.quiz_generator import QuizGenerator


class TestQuizGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = QuizGenerator()
        self.sample_content = (
            "Photosynthesis is the process plants use to convert sunlight into energy. "
            "This process mainly takes place inside the chloroplasts of plant cells. "
            "Oxygen is released into the atmosphere as a byproduct of photosynthesis."
        )

    def test_generate_quiz_creates_expected_number_of_questions(self):
        quiz = self.generator.generate_quiz("Photosynthesis", self.sample_content, num_questions=2)
        self.assertEqual(len(quiz["questions"]), 2)

    def test_generate_quiz_stores_note_title(self):
        quiz = self.generator.generate_quiz("Photosynthesis", self.sample_content)
        self.assertEqual(quiz["note_title"], "Photosynthesis")

    def test_each_question_has_question_and_answer_keys(self):
        quiz = self.generator.generate_quiz("Photosynthesis", self.sample_content, num_questions=1)
        question = quiz["questions"][0]
        self.assertIn("question", question)
        self.assertIn("answer", question)

    def test_answer_is_blanked_out_in_question_text(self):
        quiz = self.generator.generate_quiz("Photosynthesis", self.sample_content, num_questions=1)
        question = quiz["questions"][0]
        self.assertIn("_____", question["question"])
        self.assertNotIn(question["answer"], question["question"])

    def test_get_quizzes_returns_all_created_quizzes(self):
        self.generator.generate_quiz("Quiz 1", self.sample_content)
        self.generator.generate_quiz("Quiz 2", self.sample_content)
        self.assertEqual(len(self.generator.get_quizzes()), 2)

    def test_delete_quiz_removes_it(self):
        quiz = self.generator.generate_quiz("Photosynthesis", self.sample_content)
        result = self.generator.delete_quiz(quiz["id"])
        self.assertTrue(result)
        self.assertEqual(len(self.generator.get_quizzes()), 0)

    def test_delete_quiz_with_invalid_id_returns_false(self):
        result = self.generator.delete_quiz(999)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()