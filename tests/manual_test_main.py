import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from main import build_app, save_all, restore_data
from modules.file_manager import FileManager

# --- First "session": create data and save it ---
app = build_app()

note = app["note_manager"].create_note(
    "Photosynthesis",
    "Photosynthesis is the process plants use to convert sunlight into energy. "
    "This process mainly takes place inside the chloroplasts of plant cells.",
    "Biology"
)

quiz = app["quiz_generator"].generate_quiz(note["title"], note["content"], num_questions=2)
cards = app["flashcard_generator"].generate_flashcards(note["title"], note["content"], num_cards=2)
app["flashcard_generator"].mark_flashcard(cards[0]["id"], "known")
app["chat_assistant"].ask_question("What is photosynthesis?")

print("--- Dashboard after first session ---")
print(app["dashboard"].get_summary())

save_all(app)
print("\nData saved to disk.")

# --- Second "session": simulate restarting the app ---
new_app = build_app()

print("\n--- Notes reloaded in a fresh session ---")
print(new_app["note_manager"].get_notes())

print("\n--- Quizzes reloaded in a fresh session ---")
print(new_app["quiz_generator"].get_quizzes())

print("\n--- Flashcards reloaded in a fresh session ---")
print(new_app["flashcard_generator"].get_flashcards())

print("\n--- Dashboard summary in the fresh session ---")
print(new_app["dashboard"].get_summary())

# --- Confirm new IDs continue correctly instead of restarting at 1 ---
second_note = new_app["note_manager"].create_note("Newton's Laws", "Force equals mass times acceleration.", "Physics")
print(f"\n--- New note created after reload has ID: {second_note['id']} (should be 2, not 1) ---")

# Note: chat_assistant is intentionally NOT persisted/reloaded here,
# since AIChatAssistant has no save/load wiring yet — that's expected.