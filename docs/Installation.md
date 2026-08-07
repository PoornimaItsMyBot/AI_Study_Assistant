# Installation Guide — AI Study Assistant

This guide walks a first-time user through setting up and running the **AI Study Assistant** project from scratch. It assumes no prior setup exists on your computer.

Every command below tells you:

- **Where** to run it (which folder, which tool)
- **What** it does
- **What you should see** afterward

---

## 1. Prerequisites

Before starting, you need:

- A computer running Windows, macOS, or Linux
- An internet connection (required to install packages and to call the Gemini API)
- A Google account (required to get a free Gemini API key)
- [Visual Studio Code](https://code.visualstudio.com/) installed
- The project files (either cloned from GitHub or downloaded as a folder)

You do **not** need: a database, Docker, Node.js, or any other language runtime — this is a pure Python project with two external packages (`google-genai` and `python-dotenv`).

---

## 2. Installing Python

The project requires **Python 3**. If you're not sure whether Python is already installed, check first.

**Where to run this:** any terminal (Windows: Command Prompt or PowerShell; macOS/Linux: Terminal)

```bash
python --version
```

**What it does:** Asks your computer to report the installed Python version.

**What to expect:**

- If Python is already installed, you'll see something like `Python 3.12.x`. If the version is `3.9` or higher, you're set — skip to Section 3.
- If you see an error like `'python' is not recognized...` (Windows) or `command not found: python` (macOS/Linux), Python isn't installed yet.

**If Python is not installed:**

1. Go to [python.org/downloads](https://www.python.org/downloads/) and download the latest Python 3 installer for your operating system.
2. Run the installer.
   - **Windows only:** on the first installer screen, check the box **"Add Python to PATH"** before clicking Install. This step is easy to miss and causes the `python --version` command to fail later if skipped.
3. After installing, close and reopen your terminal, then run `python --version` again to confirm it now shows a version number.

---

## 3. Opening the Project in VS Code

**Where to run this:** VS Code application, or a terminal

**Option A — from VS Code:**

1. Open VS Code.
2. Go to **File → Open Folder...**
3. Select your `AI_Study_Assistant` project folder and click **Select Folder**.

**Option B — from a terminal**, navigate into the project folder first, then launch VS Code from there:

```bash
cd path/to/AI_Study_Assistant
code .
```

**What it does:** `cd` moves your terminal into the project folder; `code .` opens the current folder in VS Code.

**What to expect:** VS Code opens with the project's file tree visible on the left — you should see `main.py`, the `ai/` folder, `modules/` folder, `tests/` folder, `requirements.txt`, and `README.md`.

**Important:** for every command in the rest of this guide, make sure your terminal's current folder is the **project root** (`AI_Study_Assistant/`, the folder containing `main.py`) — not `modules/`, not `ai/`, not `tests/`. You can open a terminal inside VS Code itself via **Terminal → New Terminal**, which automatically starts in the project root.

---

## 4. Creating and Activating a Virtual Environment

A virtual environment keeps this project's Python packages separate from other projects on your computer, so installing `google-genai` here won't affect anything else you have installed. This is optional but strongly recommended.

**Where to run this:** terminal, in the project root

**Create it:**

```bash
python -m venv venv
```

**What it does:** Creates a new folder called `venv/` inside your project containing a private copy of Python and its package tools.

**What to expect:** A new `venv/` folder appears in your project (visible in VS Code's file tree). No output is printed if it succeeds.

**Activate it:**

_Windows (Command Prompt):_

```bash
venv\Scripts\activate
```

_Windows (PowerShell):_

```bash
venv\Scripts\Activate.ps1
```

_macOS/Linux:_

```bash
source venv/bin/activate
```

**What it does:** Switches your terminal to use the Python and packages inside `venv/` instead of your system-wide Python.

**What to expect:** Your terminal prompt changes to show `(venv)` at the beginning, e.g.:

```
(venv) C:\Users\you\AI_Study_Assistant>
```

**Note:** you'll need to activate the virtual environment (repeat this step) every time you open a new terminal to work on this project. `venv/` is already excluded via `.gitignore`, so it won't be committed to Git.

---

## 5. Installing Requirements

**Where to run this:** terminal, in the project root (with `venv` activated, if you created one)

```bash
pip install -r requirements.txt
```

**What it does:** Reads `requirements.txt` and installs the two packages this project depends on:

```
google-genai>=1.0.0
python-dotenv>=1.0.0
```

- `google-genai` — lets Python talk to the Gemini API.
- `python-dotenv` — lets the app read your API key from a `.env` file instead of hardcoding it in source code.

**What to expect:** Several lines of installation progress, ending with something like:

```
Successfully installed google-genai-1.x.x python-dotenv-1.x.x ...
```

If a package is already installed, `pip` will note that instead of reinstalling it — that's normal.

---

## 6. Creating the `.env` File

The application reads your Gemini API key from a file named `.env` in the project root. This file is intentionally excluded from Git (see `.gitignore`) since it holds a private credential.

**Where to create this:** project root (same folder as `main.py`) — **not** inside `modules/` or `ai/`

**In VS Code:**

1. Right-click the project root folder in the file explorer.
2. Select **New File**.
3. Name it exactly `.env` (with the leading dot, no file extension after it).

**Contents to add:**

```
GOOGLE_API_KEY=
```

You'll fill in the actual key in Section 8, after obtaining it in Section 7.

---

## 7. Obtaining a Google Gemini API Key

**Where to do this:** your web browser (not VS Code or the terminal)

1. Go to **[aistudio.google.com](https://aistudio.google.com/)**.
2. Sign in with your Google account.
3. In the left sidebar, click **Get API key**.
4. Click **Create API key**.
5. If prompted, select or create a Google Cloud project to associate the key with — this does not require adding a billing account for free-tier use.
6. Copy the generated key immediately and store it somewhere safe (e.g., a password manager) — you'll paste it into `.env` next.

**What to expect:** A long string of letters and numbers is generated and displayed once. Google AI Studio offers a free usage tier suitable for a student project like this one, though exact free-tier limits are account-specific and viewable in your AI Studio dashboard.

**Never commit this key to Git, share it in screenshots, or paste it into a chat.** Treat it like a password.

---

## 8. Adding `GOOGLE_API_KEY` to `.env`

**Where to do this:** back in VS Code, editing the `.env` file you created in Section 6

Open `.env` and paste your key after the `=` sign, with no spaces and no quotation marks:

```
GOOGLE_API_KEY=paste_your_real_key_here
```

Save the file (Ctrl+S / Cmd+S).

**What to expect:** No visible confirmation — this is just a text file being saved. You can verify it worked once you run the app in Section 9: if the key is missing or malformed, `GeminiClient` will raise a clear error (`ValueError: GOOGLE_API_KEY not found...`) rather than failing silently.

**Note:** the example `.env` shown in some earlier project notes also included a `GEMINI_MODEL` line. The current code does not read that variable — only `GOOGLE_API_KEY` is required. You can safely omit `GEMINI_MODEL` from `.env`.

---

## 9. Running the Application

**Where to run this:** terminal, in the project root (with `venv` activated, if used)

```bash
python main.py
```

**What it does:** Starts the interactive AI Study Assistant. Internally, this calls `build_app()`, which loads any previously saved notes/quizzes/flashcards from the `data/` folder (created automatically on first run), then displays a text menu.

**What to expect:**

```
===== AI Study Assistant =====
1. Create a note
2. View all notes
3. Generate a quiz from a note
4. Generate flashcards from a note
5. Ask a study question
6. View dashboard summary
7. View all quizzes
8. View all flashcards
9. Save and exit
Choose an option:
```

Type a number and press Enter to use a feature. Options 3, 4, and 5 call the real Gemini API, so they require a working internet connection and a valid `GOOGLE_API_KEY` — expect a short pause (typically a few seconds) while Gemini generates a response.

To stop the app safely (saving your data first), choose option **9**.

---

## 10. Running the Tests

The project uses Python's built-in **`unittest`** framework (not `pytest`). Tests use mocked AI responses, so they run instantly and do **not** call the real Gemini API or require an internet connection or valid API key.

**Where to run this:** terminal, in the project root (with `venv` activated, if used)

**Run the full test suite:**

```bash
python -m unittest discover -s tests
```

**What it does:** Automatically finds and runs every test file inside the `tests/` folder.

**What to expect:**

```
..........................
----------------------------------------------------------------------
Ran 26 tests in 0.048s

OK
```

Each dot represents one passing test. If a test fails, you'll see an `F` instead of a dot, followed by details about which test failed and why.

**Run a single test file** (useful when working on one module at a time):

```bash
python -m unittest tests.test_note_manager
```

---

## 11. Common Errors and Solutions

| Error / Symptom                                                                            | Cause                                                                                                        | Solution                                                                                                                                                                     |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `'python' is not recognized...` or `command not found: python`                             | Python isn't installed, or wasn't added to PATH                                                              | Reinstall Python from python.org, making sure to check "Add Python to PATH" (Windows), then reopen your terminal                                                             |
| `ModuleNotFoundError: No module named 'google'` or `'dotenv'`                              | Dependencies haven't been installed, or you're not in the activated virtual environment                      | Run `pip install -r requirements.txt` from the project root; if using a virtual environment, make sure it's activated (prompt shows `(venv)`)                                |
| `ValueError: GOOGLE_API_KEY not found. Add it to your .env file.`                          | `.env` file is missing, misnamed, in the wrong folder, or the key wasn't saved                               | Confirm `.env` exists directly in the project root (same level as `main.py`), is named exactly `.env`, and contains `GOOGLE_API_KEY=your_key` with no quotes or extra spaces |
| `ModuleNotFoundError: No module named 'ai'` or `'modules'` when running tests or `main.py` | Command was run from the wrong folder (e.g., inside `tests/` or `modules/` instead of the project root)      | `cd` back to the project root (the folder containing `main.py`) before running any `python` command                                                                          |
| `google.genai.errors.ServerError: 503 UNAVAILABLE`                                         | Gemini's servers are temporarily overloaded — not a problem with your code                                   | `GeminiClient` automatically retries a few times before giving up; if it still fails, wait a minute and try again                                                            |
| `ValueError: Gemini did not return valid JSON...` (when generating a quiz or flashcards)   | Gemini occasionally returns extra text alongside the requested JSON                                          | Try generating again — this is a known, occasional AI response quirk rather than a bug in your setup                                                                         |
| Tests fail with file/permission errors related to a `data_test` or similar folder          | A previous test run didn't clean up properly (rare)                                                          | Manually delete any leftover `data_test*` folders in the project root, then rerun the tests                                                                                  |
| `pip install` fails with a permissions error                                               | Trying to install packages globally without sufficient permissions, especially outside a virtual environment | Use a virtual environment (Section 4) — this avoids needing elevated permissions entirely                                                                                    |
