from ai import GeminiClient, build_chat_prompt


class AIChatAssistant:
    def __init__(self, ai_client=None):
        self.chat_history = []
        self.next_id = 1
        self.ai_client = ai_client or GeminiClient()

    def ask_question(self, question):
        prompt = build_chat_prompt(question)
        answer = self.ai_client.generate_text(prompt)
        self.save_chat(question, answer)
        return answer

    def save_chat(self, question, answer):
        chat_entry = {
            "id": self.next_id,
            "question": question,
            "answer": answer
        }
        self.chat_history.append(chat_entry)
        self.next_id += 1
        return chat_entry

    def get_chat_history(self):
        return self.chat_history

    def clear_chat_history(self):
        self.chat_history = []
        self.next_id = 1
        return True