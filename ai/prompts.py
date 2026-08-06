"""
Stores every AI prompt template in one place. Each feature module builds
its prompt by calling a function here instead of writing prompt text
inline — this makes prompts easy to find, compare, and improve without
touching feature logic in modules/.
"""


def build_chat_prompt(question):
    """For now, the chat prompt is just the question itself. Kept as its
    own function so we can later add instructions, tone, or context
    (e.g., 'answer like a helpful tutor') without changing ai_chat.py."""
    return question


def build_quiz_prompt(note_title, note_content, num_questions):
    return (
        f"Create {num_questions} multiple-choice quiz questions based on the "
        f"following study notes titled '{note_title}'.\n\n"
        f"Notes:\n{note_content}\n\n"
        "Return ONLY valid JSON, with no extra text, in exactly this format:\n"
        '[{"question": "...", "options": ["A", "B", "C", "D"], "answer": "..."}]'
    )


def build_flashcard_prompt(note_title, note_content, num_cards):
    return (
        f"Create {num_cards} flashcards based on the following study notes "
        f"titled '{note_title}'.\n\n"
        f"Notes:\n{note_content}\n\n"
        "Return ONLY valid JSON, with no extra text, in exactly this format:\n"
        '[{"front": "question or prompt", "back": "answer"}]'
    )