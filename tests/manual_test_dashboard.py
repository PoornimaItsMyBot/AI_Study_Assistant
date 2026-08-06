import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.note_manager import NoteManager
from modules.quiz_generator import QuizGenerator
from modules.flashcard_generator import FlashcardGenerator
from modules.ai_chat import AIChatAssistant
from modules.dashboard import Dashboard

# Set up all the modules the Dashboard depends on
note_manager = NoteManager()
quiz_generator = QuizGenerator()
flashcard_generator = FlashcardGenerator()
chat_assistant = AIChatAssistant()

dashboard = Dashboard(note_manager, quiz_generator, flashcard_generator, chat_assistant)

# Add some sample data across the different modules
note_manager.create_note("Photosynthesis", "Plants convert light into energy.", "Biology")
note_manager.create_note("Newton's Laws", "Force equals mass times acceleration.", "Physics")

quiz_generator.generate_quiz(
    "Photosynthesis",
    "Photosynthesis is the process plants use to convert sunlight into energy. "
    "This process mainly takes place inside the chloroplasts of plant cells.",
    num_questions=2
)

cards = flashcard_generator.generate_flashcards(
    "Cell Biology",
    "Mitochondria are the powerhouse of the cell. "
    "They generate most of the cell's supply of adenosine triphosphate.",
    num_cards=2
)
flashcard_generator.mark_flashcard(cards[0]["id"], "known")

chat_assistant.ask_question("What is photosynthesis?")
chat_assistant.ask_question("What is mitosis?")
chat_assistant.ask_question("What is Newton's second law?")

# Now check the Dashboard reflects all of it
print("--- Dashboard summary ---")
print(dashboard.get_summary())

print("\n--- Flashcard progress ---")
print(f"{dashboard.get_flashcard_progress()}% known")

print("\n--- Recent chats (limit 2) ---")
for chat in dashboard.get_recent_chats(limit=2):
    print(chat)