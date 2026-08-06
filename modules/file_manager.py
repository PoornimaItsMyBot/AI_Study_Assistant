import os
import json


class FileManager:
    def __init__(self, data_folder="data"):
        self.data_folder = data_folder
        os.makedirs(self.data_folder, exist_ok=True)

        self.notes_path = os.path.join(self.data_folder, "notes.json")
        self.quizzes_path = os.path.join(self.data_folder, "quizzes.json")
        self.flashcards_path = os.path.join(self.data_folder, "flashcards.json")

    def save_notes(self, notes):
        with open(self.notes_path, "w") as f:
            json.dump(notes, f, indent=2)
        return True

    def load_notes(self):
        if not os.path.exists(self.notes_path):
            return []
        with open(self.notes_path, "r") as f:
            return json.load(f)

    def save_quizzes(self, quizzes):
        with open(self.quizzes_path, "w") as f:
            json.dump(quizzes, f, indent=2)
        return True

    def load_quizzes(self):
        if not os.path.exists(self.quizzes_path):
            return []
        with open(self.quizzes_path, "r") as f:
            return json.load(f)

    def save_flashcards(self, flashcards):
        with open(self.flashcards_path, "w") as f:
            json.dump(flashcards, f, indent=2)
        return True

    def load_flashcards(self):
        if not os.path.exists(self.flashcards_path):
            return []
        with open(self.flashcards_path, "r") as f:
            return json.load(f)