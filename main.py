from modules.note_manager import NoteManager
from modules.quiz_generator import QuizGenerator
from modules.flashcard_generator import FlashcardGenerator
from modules.ai_chat import AIChatAssistant
from modules.dashboard import Dashboard
from modules.file_manager import FileManager


def restore_data(manager, data_list, list_attr_name):
    """
    Restores previously saved data (loaded from JSON) back into a manager's
    internal list, and makes sure its ID counter continues from the highest
    existing ID instead of restarting at 1.
    """
    setattr(manager, list_attr_name, data_list)

    if data_list:
        max_id = max(item["id"] for item in data_list)
        manager.next_id = max_id + 1
    else:
        manager.next_id = 1


def build_app(data_folder="data"):
    """
    Creates every module, loads any previously saved data from disk,
    and restores it into the right managers. Returns all the wired-up
    objects, ready to use.

    data_folder can be overridden (e.g., in tests) so a test run never
    touches the real application's saved data.
    """
    file_manager = FileManager(data_folder=data_folder)

    note_manager = NoteManager()
    quiz_generator = QuizGenerator()
    flashcard_generator = FlashcardGenerator()
    chat_assistant = AIChatAssistant()

    restore_data(note_manager, file_manager.load_notes(), "notes")
    restore_data(quiz_generator, file_manager.load_quizzes(), "quizzes")
    restore_data(flashcard_generator, file_manager.load_flashcards(), "flashcards")

    dashboard = Dashboard(note_manager, quiz_generator, flashcard_generator, chat_assistant)

    return {
        "file_manager": file_manager,
        "note_manager": note_manager,
        "quiz_generator": quiz_generator,
        "flashcard_generator": flashcard_generator,
        "chat_assistant": chat_assistant,
        "dashboard": dashboard
    }


def save_all(app):
    """Saves the current state of notes, quizzes, and flashcards to disk."""
    app["file_manager"].save_notes(app["note_manager"].get_notes())
    app["file_manager"].save_quizzes(app["quiz_generator"].get_quizzes())
    app["file_manager"].save_flashcards(app["flashcard_generator"].get_flashcards())


def print_quiz(quiz):
    """Nicely formats and prints a single quiz's questions and answers."""
    print(f"\nQuiz for note: {quiz['note_title']} (Quiz ID: {quiz['id']})")
    for i, q in enumerate(quiz["questions"], start=1):
        print(f"\n  Q{i}: {q['question']}")
        options = q.get("options")
        if options:
            for option in options:
                print(f"     - {option}")
        print(f"     Answer: {q['answer']}")


def print_flashcard(card):
    """Nicely formats and prints a single flashcard."""
    print(f"\n  [{card['id']}] Status: {card['status']}")
    print(f"     Front: {card['front']}")
    print(f"     Back:  {card['back']}")


def show_menu():
    print("\n===== AI Study Assistant =====")
    print("1. Create a note")
    print("2. View all notes")
    print("3. Generate a quiz from a note")
    print("4. Generate flashcards from a note")
    print("5. Ask a study question")
    print("6. View dashboard summary")
    print("7. View all quizzes")
    print("8. View all flashcards")
    print("9. Save and exit")


def run():
    app = build_app()

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            title = input("Note title: ")
            content = input("Note content: ")
            subject = input("Subject (optional): ") or None
            note = app["note_manager"].create_note(title, content, subject)
            print(f"Note created with ID {note['id']}.")

        elif choice == "2":
            notes = app["note_manager"].get_notes()
            if not notes:
                print("No notes yet.")
            for note in notes:
                print(f"[{note['id']}] {note['title']} ({note['subject']})")

        elif choice == "3":
            note_id = int(input("Note ID to generate a quiz from: "))
            note = next((n for n in app["note_manager"].get_notes() if n["id"] == note_id), None)
            if note is None:
                print("Note not found.")
            else:
                quiz = app["quiz_generator"].generate_quiz(note["title"], note["content"])
                print(f"\nQuiz created with {len(quiz['questions'])} questions.")
                print_quiz(quiz)

        elif choice == "4":
            note_id = int(input("Note ID to generate flashcards from: "))
            note = next((n for n in app["note_manager"].get_notes() if n["id"] == note_id), None)
            if note is None:
                print("Note not found.")
            else:
                cards = app["flashcard_generator"].generate_flashcards(note["title"], note["content"])
                print(f"\n{len(cards)} flashcards created.")
                for card in cards:
                    print_flashcard(card)

        elif choice == "5":
            question = input("Your question: ")
            answer = app["chat_assistant"].ask_question(question)
            print(f"Answer: {answer}")

        elif choice == "6":
            print(app["dashboard"].get_summary())

        elif choice == "7":
            quizzes = app["quiz_generator"].get_quizzes()
            if not quizzes:
                print("No quizzes yet.")
            for quiz in quizzes:
                print_quiz(quiz)

        elif choice == "8":
            flashcards = app["flashcard_generator"].get_flashcards()
            if not flashcards:
                print("No flashcards yet.")
            for card in flashcards:
                print_flashcard(card)

        elif choice == "9":
            save_all(app)
            print("All data saved. Goodbye!")
            break

        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    run()