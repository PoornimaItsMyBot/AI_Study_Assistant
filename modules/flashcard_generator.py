from ai import GeminiClient, build_flashcard_prompt, parse_json_response


class FlashcardGenerator:
    def __init__(self, ai_client=None):
        self.flashcards = []
        self.next_id = 1
        self.ai_client = ai_client or GeminiClient()

    def generate_flashcards(self, note_title, note_content, num_cards=5):
        prompt = build_flashcard_prompt(note_title, note_content, num_cards)
        raw_response = self.ai_client.generate_text(prompt)
        card_data = parse_json_response(raw_response)

        new_cards = []
        for item in card_data:
            flashcard = {
                "id": self.next_id,
                "note_title": note_title,
                "front": item["front"],
                "back": item["back"],
                "status": "unknown"
            }
            self.flashcards.append(flashcard)
            new_cards.append(flashcard)
            self.next_id += 1

        return new_cards

    def get_flashcards(self):
        return self.flashcards

    def delete_flashcard(self, flashcard_id):
        for card in self.flashcards:
            if card["id"] == flashcard_id:
                self.flashcards.remove(card)
                return True
        return False

    def mark_flashcard(self, flashcard_id, status):
        if status not in ("known", "unknown"):
            return False

        for card in self.flashcards:
            if card["id"] == flashcard_id:
                card["status"] = status
                return True
        return False