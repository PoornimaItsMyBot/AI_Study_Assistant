
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import unittest
from ai.prompts import build_chat_prompt, build_quiz_prompt, build_flashcard_prompt


class TestPrompts(unittest.TestCase):

    def test_build_chat_prompt_returns_the_question(self):
        prompt = build_chat_prompt("What is photosynthesis?")
        self.assertEqual(prompt, "What is photosynthesis?")

    def test_build_quiz_prompt_includes_key_details(self):
        prompt = build_quiz_prompt("Photosynthesis", "Plants convert light.", 3)
        self.assertIn("Photosynthesis", prompt)
        self.assertIn("Plants convert light.", prompt)
        self.assertIn("3", prompt)
        self.assertIn("JSON", prompt)

    def test_build_flashcard_prompt_includes_key_details(self):
        prompt = build_flashcard_prompt("Cell Biology", "Mitochondria info.", 5)
        self.assertIn("Cell Biology", prompt)
        self.assertIn("Mitochondria info.", prompt)
        self.assertIn("5", prompt)
        self.assertIn("JSON", prompt)


if __name__ == "__main__":
    unittest.main()