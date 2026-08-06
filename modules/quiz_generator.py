from ai import GeminiClient, build_quiz_prompt, parse_json_response


class QuizGenerator:
    def __init__(self, ai_client=None):
        self.quizzes = []
        self.next_id = 1
        self.ai_client = ai_client or GeminiClient()

    def generate_quiz(self, note_title, note_content, num_questions=3):
        prompt = build_quiz_prompt(note_title, note_content, num_questions)
        raw_response = self.ai_client.generate_text(prompt)
        questions = parse_json_response(raw_response)

        quiz = {
            "id": self.next_id,
            "note_title": note_title,
            "questions": questions
        }

        self.quizzes.append(quiz)
        self.next_id += 1
        return quiz

    def get_quizzes(self):
        return self.quizzes

    def delete_quiz(self, quiz_id):
        for quiz in self.quizzes:
            if quiz["id"] == quiz_id:
                self.quizzes.remove(quiz)
                return True
        return False