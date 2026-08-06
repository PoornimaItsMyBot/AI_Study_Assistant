
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from modules.ai_chat import AIChatAssistant


class TestAIChatAssistant(unittest.TestCase):

    def setUp(self):
        self.assistant = AIChatAssistant()

    def test_ask_question_returns_an_answer(self):
        answer = self.assistant.ask_question("What is photosynthesis?")
        self.assertIn("What is photosynthesis?", answer)

    def test_ask_question_saves_to_history(self):
        self.assistant.ask_question("What is photosynthesis?")
        history = self.assistant.get_chat_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["question"], "What is photosynthesis?")

    def test_multiple_questions_increment_ids(self):
        self.assistant.ask_question("Question 1")
        self.assistant.ask_question("Question 2")
        history = self.assistant.get_chat_history()
        self.assertEqual(history[0]["id"], 1)
        self.assertEqual(history[1]["id"], 2)

    def test_save_chat_directly(self):
        entry = self.assistant.save_chat("Manual question", "Manual answer")
        self.assertEqual(entry["question"], "Manual question")
        self.assertEqual(entry["answer"], "Manual answer")
        self.assertEqual(len(self.assistant.get_chat_history()), 1)

    def test_clear_chat_history_empties_list(self):
        self.assistant.ask_question("Some question")
        result = self.assistant.clear_chat_history()
        self.assertTrue(result)
        self.assertEqual(self.assistant.get_chat_history(), [])

    def test_clear_chat_history_resets_id_counter(self):
        self.assistant.ask_question("Question 1")
        self.assistant.ask_question("Question 2")
        self.assistant.clear_chat_history()

        new_answer_entry = self.assistant.save_chat("New question", "New answer")
        self.assertEqual(new_answer_entry["id"], 1)


if __name__ == "__main__":
    unittest.main()