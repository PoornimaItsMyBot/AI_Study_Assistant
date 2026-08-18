import streamlit as st

from modules.note_manager import NoteManager
from modules.quiz_generator import QuizGenerator
from modules.flashcard_generator import FlashcardGenerator
from modules.ai_chat import AIChatAssistant
from modules.dashboard import Dashboard
from ai.gemini_client import GeminiClient


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# CREATE APPLICATION OBJECTS
# ============================================================

@st.cache_resource
def create_app():

    # Create the core managers
    note_manager = NoteManager()

    quiz_generator = QuizGenerator()

    flashcard_generator = FlashcardGenerator()

    # Gemini client
    gemini = GeminiClient()

    # AI chat assistant
    chat_assistant = AIChatAssistant()

    # Dashboard needs all four components
    dashboard = Dashboard(
        note_manager,
        quiz_generator,
        flashcard_generator,
        chat_assistant
    )

    return (
        note_manager,
        quiz_generator,
        flashcard_generator,
        gemini,
        chat_assistant,
        dashboard
    )


(
    note_manager,
    quiz_generator,
    flashcard_generator,
    gemini,
    chat_assistant,
    dashboard
) = create_app()


# ============================================================
# TITLE
# ============================================================

st.title("🤖 AI Study Assistant")

st.write(
    "Your personal AI-powered study companion."
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

option = st.sidebar.selectbox(
    "Choose an option",
    [
        "🏠 Home",
        "📝 Create a Note",
        "📚 View Notes",
        "🧠 Generate Quiz",
        "🎴 Generate Flashcards",
        "💬 Ask AI",
        "📊 Dashboard"
    ]
)


# ============================================================
# HOME
# ============================================================

if option == "🏠 Home":

    st.header("Welcome to AI Study Assistant! 👋")

    st.write(
        """
        Use the menu on the left to:
        
        - 📝 Create study notes
        - 📚 View your notes
        - 🧠 Generate quizzes
        - 🎴 Generate flashcards
        - 💬 Ask your AI tutor
        - 📊 View your study dashboard
        """
    )


# ============================================================
# CREATE NOTE
# ============================================================

elif option == "📝 Create a Note":

    st.header("📝 Create a Note")

    title = st.text_input(
        "Note title"
    )

    content = st.text_area(
        "Note content",
        height=250
    )

    subject = st.text_input(
        "Subject"
    )

    if st.button("Save Note"):

        if not title.strip():

            st.warning(
                "Please enter a note title."
            )

        elif not content.strip():

            st.warning(
                "Please enter some note content."
            )

        else:

            note = note_manager.create_note(
                title,
                content,
                subject or None
            )

            st.success(
                f"Note created successfully! "
                f"Note ID: {note['id']}"
            )

            st.rerun()


# ============================================================
# VIEW NOTES
# ============================================================

elif option == "📚 View Notes":

    st.header("📚 My Notes")

    notes = note_manager.get_notes()

    if not notes:

        st.info(
            "No notes found. Create a note first."
        )

    else:

        st.write(
            f"You have **{len(notes)} note(s)**."
        )

        for note in notes:

            with st.expander(
                f"📖 [{note['id']}] {note['title']}"
            ):

                if note.get("subject"):

                    st.write(
                        f"**Subject:** {note['subject']}"
                    )

                st.write(
                    note["content"]
                )


# ============================================================
# GENERATE QUIZ
# ============================================================

elif option == "🧠 Generate Quiz":

    st.header("🧠 Generate a Quiz")

    notes = note_manager.get_notes()

    if not notes:

        st.warning(
            "You need to create a note first."
        )

    else:

        note = st.selectbox(
            "Choose a note",
            notes,
            format_func=lambda n:
                f"[{n['id']}] {n['title']}"
        )

        if st.button("Generate Quiz"):

            with st.spinner(
                "🤖 Gemini is creating your quiz..."
            ):

                try:

                    quiz = quiz_generator.generate_quiz(
                        note["title"],
                        note["content"]
                    )

                    st.success(
                        "Quiz generated successfully!"
                    )

                    st.write(
                        f"**{len(quiz['questions'])} "
                        f"questions generated.**"
                    )

                    for i, question in enumerate(
                        quiz["questions"],
                        start=1
                    ):

                        st.subheader(
                            f"Question {i}"
                        )

                        st.write(
                            question["question"]
                        )

                        options = question.get(
                            "options"
                        )

                        if options:

                            st.radio(
                                "Choose your answer:",
                                options,
                                key=f"quiz_{note['id']}_{i}"
                            )

                        st.write(
                            f"**Answer:** "
                            f"{question['answer']}"
                        )

                except Exception as error:

                    st.error(
                        f"Quiz generation failed: "
                        f"{error}"
                    )


# ============================================================
# GENERATE FLASHCARDS
# ============================================================

elif option == "🎴 Generate Flashcards":

    st.header("🎴 Generate Flashcards")

    notes = note_manager.get_notes()

    if not notes:

        st.warning(
            "You need to create a note first."
        )

    else:

        note = st.selectbox(
            "Choose a note",
            notes,
            format_func=lambda n:
                f"[{n['id']}] {n['title']}",
            key="flashcard_note"
        )

        if st.button("Generate Flashcards"):

            with st.spinner(
                "🤖 Gemini is creating your flashcards..."
            ):

                try:

                    cards = (
                        flashcard_generator
                        .generate_flashcards(
                            note["title"],
                            note["content"]
                        )
                    )

                    st.success(
                        f"{len(cards)} flashcards generated!"
                    )

                    for card in cards:

                        with st.expander(
                            f"🎴 {card['front']}"
                        ):

                            st.write(
                                card["back"]
                            )

                except Exception as error:

                    st.error(
                        f"Flashcard generation failed: "
                        f"{error}"
                    )


# ============================================================
# ASK AI
# ============================================================

elif option == "💬 Ask AI":

    st.header(
        "💬 Ask Your AI Study Assistant"
    )

    question = st.text_area(
        "What would you like to know?",
        height=150
    )

    if st.button("Ask AI"):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "🤖 Thinking..."
            ):

                try:

                    answer = gemini.generate_text(
                        question
                    )

                    st.subheader(
                        "AI Answer"
                    )

                    st.write(answer)

                except Exception as error:

                    st.error(
                        f"AI request failed: {error}"
                    )


# ============================================================
# DASHBOARD
# ============================================================

elif option == "📊 Dashboard":

    st.header("📊 Study Dashboard")

    try:

        summary = dashboard.get_summary()

        st.write(summary)

    except Exception as error:

        st.error(
            f"Dashboard could not be loaded: {error}"
        )