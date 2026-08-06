class Dashboard:
    def __init__(self, note_manager, quiz_generator, flashcard_generator, chat_assistant):
        self.note_manager = note_manager
        self.quiz_generator = quiz_generator
        self.flashcard_generator = flashcard_generator
        self.chat_assistant = chat_assistant

    def get_summary(self):
        notes = self.note_manager.get_notes()
        quizzes = self.quiz_generator.get_quizzes()
        flashcards = self.flashcard_generator.get_flashcards()
        chat_history = self.chat_assistant.get_chat_history()

        known_cards = [c for c in flashcards if c["status"] == "known"]

        summary = {
            "total_notes": len(notes),
            "total_quizzes": len(quizzes),
            "total_flashcards": len(flashcards),
            "flashcards_known": len(known_cards),
            "flashcards_unknown": len(flashcards) - len(known_cards),
            "total_chat_questions": len(chat_history)
        }
        return summary

    def get_flashcard_progress(self):
        flashcards = self.flashcard_generator.get_flashcards()

        if len(flashcards) == 0:
            return 0.0

        known_cards = [c for c in flashcards if c["status"] == "known"]
        progress_percent = (len(known_cards) / len(flashcards)) * 100
        return round(progress_percent, 1)

    def get_recent_chats(self, limit=5):
        chat_history = self.chat_assistant.get_chat_history()
        return chat_history[-limit:]