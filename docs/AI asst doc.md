# AI Study Assistant — Project Documentation

**Type:** Student-built educational application
**Language:** Python 3
**Status:** Functional MVP with real AI integration (Google Gemini API)

---

## 1. Project Overview

AI Study Assistant is a command-line Python application that helps students study more effectively. It allows a user to:

- Create, view, update, and delete study notes
- Generate AI-powered multiple-choice quizzes from a note
- Generate AI-powered flashcards from a note, and track which ones are "known" vs. "unknown"
- Ask free-form study questions to an AI assistant
- View a dashboard summarizing study activity (note/quiz/flashcard counts, flashcard progress, recent chats)
- Persist notes, quizzes, and flashcards to disk as JSON, so data survives between runs

The application runs as an interactive text menu in the terminal.

---

## 2. Project Structure

```
AI_Study_Assistant/
├── main.py                      # Application entry point
├── ai/
│   ├── __init__.py              # Exposes GeminiClient, prompt builders, parser
│   ├── gemini_client.py         # Wraps the Gemini API connection (includes retry logic)
│   ├── prompts.py               # Prompt templates for chat, quiz, flashcards
│   └── parser.py                # Parses Gemini's JSON responses
├── modules/
│   ├── note_manager.py          # NoteManager class
│   ├── quiz_generator.py        # QuizGenerator class
│   ├── flashcard_generator.py   # FlashcardGenerator class
│   ├── ai_chat.py               # AIChatAssistant class
│   ├── dashboard.py             # Dashboard class
│   └── file_manager.py          # FileManager class (JSON persistence)
├── tests/                       # Test suite — see Section 7
├── data/                        # Created automatically at runtime; stores JSON data
├── assets/                      # Currently empty — reserved for future use
├── config/                      # Currently empty — reserved for future use
├── docs/                        # Currently empty — reserved for future use
├── .env                         # Stores GOOGLE_API_KEY (not committed to version control)
├── .gitignore
├── requirements.txt
└── README.md
```

`assets/`, `config/`, and `docs/` were created during initial project scaffolding but currently contain no files.

---

## 3. Modules, Classes, and Methods

### 3.1 `modules/note_manager.py` — `NoteManager`

Manages study notes in memory as a list of dictionaries. No AI dependency.

| Method                                                         | Purpose                                                               |
| -------------------------------------------------------------- | --------------------------------------------------------------------- |
| `create_note(title, content, subject=None)`                    | Creates a note with an auto-incrementing `id`; `subject` is optional. |
| `get_notes()`                                                  | Returns all stored notes.                                             |
| `delete_note(note_id)`                                         | Removes a note by ID. Returns `True`/`False`.                         |
| `update_note(note_id, title=None, content=None, subject=None)` | Updates only the fields explicitly provided. Returns `True`/`False`.  |

---

### 3.2 `modules/quiz_generator.py` — `QuizGenerator`

Generates multiple-choice quizzes from note content using the Gemini API.

| Method                                                     | Purpose                                                                                                                                                                                |
| ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `generate_quiz(note_title, note_content, num_questions=3)` | Builds a prompt via `build_quiz_prompt()`, sends it to Gemini via `GeminiClient.generate_text()`, parses the JSON response via `parse_json_response()`, and stores the resulting quiz. |
| `get_quizzes()`                                            | Returns all generated quizzes.                                                                                                                                                         |
| `delete_quiz(quiz_id)`                                     | Removes a quiz by ID. Returns `True`/`False`.                                                                                                                                          |

Accepts an optional `ai_client` constructor parameter (defaults to a real `GeminiClient()`), allowing test code to inject a fake client instead of calling the real API.

---

### 3.3 `modules/flashcard_generator.py` — `FlashcardGenerator`

Generates flashcards from note content using the Gemini API.

| Method                                                       | Purpose                                                                                                                                                         |
| ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `generate_flashcards(note_title, note_content, num_cards=5)` | Builds a prompt via `build_flashcard_prompt()`, sends it to Gemini, parses the JSON response, and stores each flashcard with a default `status` of `"unknown"`. |
| `get_flashcards()`                                           | Returns all generated flashcards.                                                                                                                               |
| `delete_flashcard(flashcard_id)`                             | Removes a flashcard by ID. Returns `True`/`False`.                                                                                                              |
| `mark_flashcard(flashcard_id, status)`                       | Sets a flashcard's status to `"known"` or `"unknown"`. Rejects any other value, returning `False`.                                                              |

Same `ai_client` injection pattern as `QuizGenerator`.

---

### 3.4 `modules/ai_chat.py` — `AIChatAssistant`

Handles free-form study question answering via the Gemini API.

| Method                        | Purpose                                                                                                                          |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `ask_question(question)`      | Builds a prompt via `build_chat_prompt()`, sends it to Gemini via `generate_text()`, saves the Q&A pair, and returns the answer. |
| `save_chat(question, answer)` | Stores a question/answer pair with an auto-incrementing `id`.                                                                    |
| `get_chat_history()`          | Returns all stored Q&A pairs.                                                                                                    |
| `clear_chat_history()`        | Empties the chat history and resets the ID counter to 1.                                                                         |

Same `ai_client` injection pattern as the two generators above. Chat history exists only in memory during a session — see Section 5.

---

### 3.5 `modules/dashboard.py` — `Dashboard`

Aggregates statistics from the other modules. Stores no data of its own — constructed with references to `NoteManager`, `QuizGenerator`, `FlashcardGenerator`, and `AIChatAssistant`, and reads live from them.

| Method                      | Purpose                                                                                                   |
| --------------------------- | --------------------------------------------------------------------------------------------------------- |
| `get_summary()`             | Returns total notes, total quizzes, total flashcards, flashcards known/unknown, and total chat questions. |
| `get_flashcard_progress()`  | Returns the percentage of flashcards marked "known" (0.0 if there are no flashcards).                     |
| `get_recent_chats(limit=5)` | Returns the most recent chat entries, up to `limit`.                                                      |

---

### 3.6 `modules/file_manager.py` — `FileManager`

Handles saving/loading data as JSON files on disk.

| Method                                              | Purpose                             |
| --------------------------------------------------- | ----------------------------------- |
| `save_notes(notes)` / `load_notes()`                | Saves/loads `data/notes.json`.      |
| `save_quizzes(quizzes)` / `load_quizzes()`          | Saves/loads `data/quizzes.json`.    |
| `save_flashcards(flashcards)` / `load_flashcards()` | Saves/loads `data/flashcards.json`. |

Constructor accepts `data_folder` (default `"data"`), and creates the folder automatically if it doesn't exist. Loading returns an empty list `[]` if the corresponding file doesn't exist yet.

**There is no `save_chat_history()` or `load_chat_history()` method** — chat history is not persisted between runs.

---

## 4. The `ai/` Package (Gemini Integration Layer)

This package isolates all AI-provider-specific logic so the feature modules above never talk to Gemini directly.

### 4.1 `ai/gemini_client.py` — `GeminiClient`

```python
GeminiClient(model="gemini-3.5-flash", max_retries=3, retry_delay_seconds=5)
```

- Loads `GOOGLE_API_KEY` from `.env` via `python-dotenv`. Raises `ValueError` immediately if the key is missing.
- Creates a `google.genai.Client` instance.
- `generate_text(prompt)` — calls `client.models.generate_content(model=..., contents=prompt)` and returns the response text, stripped of whitespace.
- **Includes automatic retry logic:** if Gemini returns a `ServerError` (e.g., HTTP 503 "model currently experiencing high demand"), the client retries up to `max_retries` times, waiting `retry_delay_seconds` between attempts, before raising a clear `RuntimeError` if all attempts fail.

> **Discrepancy to be aware of:** the project's `README.md` shows an example `.env` with a `GEMINI_MODEL` variable, but `GeminiClient` does not currently read this variable — the model name is set via the `model` constructor parameter (hardcoded default: `"gemini-3.5-flash"`). If you want `.env` to actually control the model, `GeminiClient.__init__()` would need to read `os.getenv("GEMINI_MODEL")` as a fallback; this is not yet implemented.

### 4.2 `ai/prompts.py`

Pure functions that build prompt strings — no API calls:

- `build_chat_prompt(question)` — currently returns the question unmodified.
- `build_quiz_prompt(note_title, note_content, num_questions)` — instructs Gemini to return a JSON array of multiple-choice questions.
- `build_flashcard_prompt(note_title, note_content, num_cards)` — instructs Gemini to return a JSON array of front/back flashcard pairs.

### 4.3 `ai/parser.py`

- `parse_json_response(raw_text)` — strips markdown code fences (e.g. ` ```json ... ``` `) if present, then parses the remaining text with `json.loads()`. Raises `ValueError` (including the raw response) if parsing fails.

### 4.4 `ai/__init__.py`

Re-exports `GeminiClient`, `build_chat_prompt`, `build_quiz_prompt`, `build_flashcard_prompt`, and `parse_json_response`, so other modules import from `ai` directly:

```python
from ai import GeminiClient, build_quiz_prompt, parse_json_response
```

---

## 5. Data Persistence

| Data         | Persisted to disk? | File                                                         |
| ------------ | ------------------ | ------------------------------------------------------------ |
| Notes        | Yes                | `data/notes.json`                                            |
| Quizzes      | Yes                | `data/quizzes.json`                                          |
| Flashcards   | Yes                | `data/flashcards.json`                                       |
| Chat history | **No**             | Not saved — exists only in memory during the running session |

**Save/restore flow (from `main.py`):**

- `build_app(data_folder="data")` creates all module instances, then calls `FileManager.load_notes()/load_quizzes()/load_flashcards()` and feeds the results into each manager via a helper function, `restore_data()`, which also recalculates each manager's ID counter from the highest existing ID (so new items don't reuse old IDs after a reload).
- `save_all(app)` pulls current data from each manager via its `get_*()` method and writes it to disk via the corresponding `FileManager.save_*()` method.
- `data_folder` is a parameter (not hardcoded), which allows tests to redirect storage to a temporary folder, keeping real application data untouched during test runs.

---

## 6. How the Application Starts

Entry point: **`main.py`**, run via:

```bash
python main.py
```

Execution flow:

1. `if __name__ == "__main__": run()` triggers `run()`.
2. `run()` calls `build_app()`, wiring together `NoteManager`, `QuizGenerator`, `FlashcardGenerator`, `AIChatAssistant`, `Dashboard`, and `FileManager`, and restoring any previously saved notes/quizzes/flashcards.
3. `run()` enters a loop: `show_menu()` prints a numbered menu, `input()` reads the user's choice, and the corresponding action executes.

### Menu options

| #   | Action                                                                                 |
| --- | -------------------------------------------------------------------------------------- |
| 1   | Create a note                                                                          |
| 2   | View all notes                                                                         |
| 3   | Generate a quiz from a note (calls Gemini; prints the generated questions immediately) |
| 4   | Generate flashcards from a note (calls Gemini; prints the generated cards immediately) |
| 5   | Ask a study question (calls Gemini)                                                    |
| 6   | View dashboard summary                                                                 |
| 7   | View all quizzes generated so far                                                      |
| 8   | View all flashcards generated so far                                                   |
| 9   | Save all data to disk and exit                                                         |

Helper functions `print_quiz(quiz)` and `print_flashcard(card)` format quiz/flashcard output consistently wherever it's displayed (options 3, 4, 7, 8).

---

## 7. Testing

**Framework used: `unittest`** (Python's built-in testing framework). `pytest` is **not** used, despite appearing in early project planning notes — this has been confirmed and should not be listed as a dependency.

The `tests/` folder contains two categories of files:

1. **Automated `unittest`-based tests** — one file per module, using `unittest.TestCase`, with `unittest.mock.patch`/`MagicMock` used to substitute a fake AI client wherever real modules would otherwise call the Gemini API. These run instantly, without needing a real API key or internet access, and never touch the real `data/` folder.
2. **Manual test scripts** (e.g., `manual_test_*.py`) — earlier, exploratory scripts that print output for visual inspection rather than asserting correctness automatically. These predate the `unittest` suite and are not run as part of automated testing.

**Recommendation:** since the automated `unittest` suite now covers the same functionality as the manual scripts (and more), consider either removing the manual scripts or clearly separating them (e.g., into a `tests/manual/` subfolder) so it's unambiguous which files are the actual test suite versus exploratory scratch scripts.

Run command:

```bash
python -m unittest discover -s tests
```

Modules with confirmed test coverage: `NoteManager`, `QuizGenerator`, `FlashcardGenerator`, `AIChatAssistant`, `Dashboard`, `FileManager`, `main.py`'s glue logic (`build_app`, `save_all`, `restore_data`), `GeminiClient`, `parser.py`, and `prompts.py`.

---

## 8. Dependencies

From `requirements.txt`:

```
google-genai>=1.0.0
python-dotenv>=1.0.0
```

| Package                              | Used for                                                                |
| ------------------------------------ | ----------------------------------------------------------------------- |
| `google-genai`                       | Connecting to the Gemini API (`from google import genai`)               |
| `python-dotenv`                      | Loading `GOOGLE_API_KEY` from `.env` (`from dotenv import load_dotenv`) |
| `json` _(standard library)_          | Reading/writing saved data and parsing AI responses                     |
| `os` _(standard library)_            | File paths, environment variables, folder creation                      |
| `time` _(standard library)_          | Retry delay logic in `GeminiClient`                                     |
| `unittest` _(standard library)_      | Automated testing                                                       |
| `unittest.mock` _(standard library)_ | Mocking the Gemini client in tests                                      |

No external test framework (e.g., `pytest`) is required — `unittest` ships with Python.

---

## 9. Environment Configuration

`.env` file (project root) must contain:

```
GOOGLE_API_KEY=your_actual_api_key_here
```

The README also documents an optional `GEMINI_MODEL` variable, but per the discrepancy noted in Section 4.1, this is not currently read by the code — including it in `.env` today has no effect.

`GeminiClient.__init__()` raises `ValueError("GOOGLE_API_KEY not found. Add it to your .env file.")` if `GOOGLE_API_KEY` is missing or empty.

---

## 10. Version Control

The project is version-controlled with Git and hosted on GitHub at:
**https://github.com/PoornimaItsMyBot/AI_Study_Assistant**

**Branches:**

| Branch               | Notes                                                                                                                                                        |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `main`               | Primary branch. Tracked by `origin/main`.                                                                                                                    |
| `feature-ai-summary` | Contains the initial project setup commit. Not currently pushed to `origin` (no `remotes/origin/feature-ai-summary` listed).                                 |
| `feature-ai-changes` | Currently checked out (`HEAD`). Tracked by `origin/feature-ai-changes`. Contains the AI/Gemini integration work documented in Sections 3–5 of this document. |

**Commit history** (`git log --oneline`, most recent first):

| Commit    | Branch(es)                                               | Message               |
| --------- | -------------------------------------------------------- | --------------------- |
| `732217a` | `feature-ai-changes`, `origin/feature-ai-changes` (HEAD) | ReTesting Pull        |
| `2d7caed` | `main`, `origin/main`                                    | Testing Pull          |
| `724b91b` | `feature-ai-summary`                                     | Initial project setup |

**Observations:**

- Development is currently happening on `feature-ai-changes`, which has not yet been merged into `main`. `main` is still at the "Testing Pull" commit and does not yet include the Gemini API integration, retry logic, or updated `main.py` menu described elsewhere in this document.
- `feature-ai-summary` exists locally but has no corresponding remote branch — it hasn't been pushed to GitHub.
- Commit messages (`"Testing Pull"`, `"ReTesting Pull"`) are placeholder-style rather than descriptive. Consider using more specific messages going forward (e.g., `"Integrate Gemini API into quiz and flashcard generators"`) to make history more useful for anyone reviewing the project later.
- To make the documented functionality available on `main`, `feature-ai-changes` will need to be merged (via pull request or direct merge) at some point.

`.gitignore` currently excludes: `.env`, all `__pycache__/` folders, `*.pyc`/`*.pyo` files, `.venv/`/`venv/`, `.vscode/`, `.pytest_cache/`, and OS files (`Thumbs.db`, `.DS_Store`). Note: `.pytest_cache/` is excluded even though `pytest` isn't actually used — harmless, but worth knowing it's a leftover from earlier planning.

---

## 11. Known Limitations (Observed, not assumed)

- Chat history is not saved between sessions (see Section 5).
- AI-generated quiz/flashcard content depends on Gemini returning well-formed JSON; `parse_json_response()` raises a `ValueError` (with the raw response included) if Gemini's output can't be parsed. This has been observed in practice and may require prompt refinement over time.
- Gemini API calls can occasionally fail with a transient `503 UNAVAILABLE` server error during periods of high demand; `GeminiClient` now retries automatically before failing (see Section 4.1).
- No user authentication or multi-user support exists — the app manages a single shared set of notes/quizzes/flashcards per `data/` folder.
- `assets/`, `config/`, and `docs/` folders exist but are currently unused.
- The `.env` example in the README references a `GEMINI_MODEL` variable that the code does not currently read (see Section 4.1 and Section 9).

---

## Open Items

None. All sections of this documentation have been confirmed directly against your source files, `requirements.txt`, `.gitignore`, `README.md`, and Git history.

**One thing worth deciding, not a documentation gap:** whether to merge `feature-ai-changes` into `main` now that the Gemini integration is working, since `main` currently does not reflect the AI-integrated version of the app (see Section 10).
