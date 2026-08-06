import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.file_manager import FileManager

manager = FileManager()

sample_notes = [
    {"id": 1, "title": "Photosynthesis", "content": "Plants convert light into energy.", "subject": "Biology"},
    {"id": 2, "title": "Newton's Laws", "content": "Force equals mass times acceleration.", "subject": "Physics"}
]

sample_quizzes = [
    {"id": 1, "note_title": "Photosynthesis", "questions": [
        {"question": "Plants convert _____ into energy.", "answer": "light"}
    ]}
]

sample_flashcards = [
    {"id": 1, "note_title": "Cell Biology", "front": "What is the powerhouse of the cell?", "back": "Mitochondria", "status": "known"}
]

# --- Notes ---
manager.save_notes(sample_notes)
loaded_notes = manager.load_notes()
print("--- Loaded notes ---")
print(loaded_notes)
print(f"Match original? {loaded_notes == sample_notes}")

# --- Quizzes ---
manager.save_quizzes(sample_quizzes)
loaded_quizzes = manager.load_quizzes()
print("\n--- Loaded quizzes ---")
print(loaded_quizzes)
print(f"Match original? {loaded_quizzes == sample_quizzes}")

# --- Flashcards ---
manager.save_flashcards(sample_flashcards)
loaded_flashcards = manager.load_flashcards()
print("\n--- Loaded flashcards ---")
print(loaded_flashcards)
print(f"Match original? {loaded_flashcards == sample_flashcards}")

# --- Test loading when no file exists yet ---
import os
empty_test_folder = "data_empty_test"
temp_manager = FileManager(data_folder=empty_test_folder)
print("\n--- Loading notes from a fresh, empty data folder ---")
print(temp_manager.load_notes())  # should print []

# Clean up the temporary test folder
if os.path.exists(os.path.join(empty_test_folder, "notes.json")):
    os.remove(os.path.join(empty_test_folder, "notes.json"))
os.rmdir(empty_test_folder)