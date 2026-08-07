# User Manual — AI Study Assistant

Welcome! This guide explains how to use the AI Study Assistant, step by step. No programming knowledge is needed — you'll interact with the app by typing simple menu numbers and answers into your terminal.

---

## 1. Getting Started

The AI Study Assistant runs in a terminal (a text window on your computer). To start it, someone with the project set up will run:

```
python main.py
```

Once started, you'll see a numbered menu like this:

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

**How to use the menu:** type the number of the option you want, then press **Enter**. After each action, the menu reappears so you can choose your next step.

**Important:** your notes, quizzes, and flashcards are only permanently saved when you choose option **9 (Save and exit)**. If you close the terminal window without choosing option 9, anything you did in that session may not be saved — see Section 10 (Troubleshooting) for more on this.

---

## 2. Creating Notes

**What it does:** Lets you type in a study note — a title, the content, and (optionally) a subject — which the app stores so you can generate quizzes and flashcards from it later.

**Steps:**

1. From the main menu, type `1` and press Enter.
2. When prompted `Note title:`, type a short title (e.g., `Photosynthesis`) and press Enter.
3. When prompted `Note content:`, type the actual content of your note — this can be a few sentences or a full paragraph — and press Enter.
4. When prompted `Subject (optional):`, type a subject (e.g., `Biology`) if you want one, or just press Enter to skip it.

**What you should see:**

```
Note created with ID 1.
```

The number shown is your note's unique ID — you'll use this ID later when generating quizzes or flashcards from this note.

---

## 3. Viewing Notes

**What it does:** Shows a list of every note you've created so far, along with each note's ID and subject.

**Steps:**

1. From the main menu, type `2` and press Enter.

**What you should see:**

```
[1] Photosynthesis (Biology)
[2] Newton's Laws (Physics)
```

Each line shows the note's ID in brackets, its title, and its subject. If you haven't created any notes yet, you'll instead see:

```
No notes yet.
```

**Note:** this view shows only the title and subject — not the full note content.

---

## 4. Updating Notes

**Current status: not available from the menu.**

The application is capable of updating a note's title, content, or subject internally, but this feature has **not yet been connected to the main menu** — there is no numbered option for it. If you need to change a note, the current workaround is to delete the note (see Section 5's note below) and create a new one with the corrected information — though note that deleting is also not currently available from the menu either.

If this is a feature you need, it should be added as a new menu option before it can be used.

---

## 5. Deleting Notes

**Current status: not available from the menu.**

Similarly, the application can delete a note internally, but **no menu option currently exposes this** to you as a user. Right now, once a note is created, there is no way to remove it through the menu.

If this is a feature you need, it should be added as a new menu option before it can be used.

---

## 6. Creating Quizzes

**What it does:** Uses AI to generate a multiple-choice quiz based on one of your existing notes, and immediately displays the questions, answer choices, and correct answers.

**Steps:**

1. First, make sure you know the ID of the note you want a quiz from (check with option 2 if needed).
2. From the main menu, type `3` and press Enter.
3. When prompted `Note ID to generate a quiz from:`, type the note's ID number and press Enter.

**What you should see:**

- A short pause while the AI generates your quiz (this calls an AI service and can take a few seconds).
- Then output like:

```
Quiz created with 3 questions.

Quiz for note: Photosynthesis (Quiz ID: 1)

  Q1: What do plants primarily use to convert into energy?
     - Sunlight
     - Water
     - Soil
     - Air
     Answer: Sunlight

  Q2: ...
```

Each question shows its answer choices and the correct answer directly beneath it.

**If you entered a note ID that doesn't exist**, you'll see:

```
Note not found.
```

**Note:** answers are shown immediately below each question — this feature currently displays answers right away rather than letting you answer first and reveal them after.

---

## 7. Creating Flashcards

**What it does:** Uses AI to generate flashcards (a front/back pair) based on one of your existing notes, and immediately displays them.

**Steps:**

1. Know the ID of the note you want flashcards from (check with option 2 if needed).
2. From the main menu, type `4` and press Enter.
3. When prompted `Note ID to generate flashcards from:`, type the note's ID number and press Enter.

**What you should see:**

- A short pause while the AI generates your flashcards.
- Then output like:

```
3 flashcards created.

  [1] Status: unknown
     Front: What is the powerhouse of the cell?
     Back:  Mitochondria

  [2] Status: unknown
  ...
```

Each flashcard shows its ID, a status (new flashcards always start as `unknown`), the front (the prompt/question side), and the back (the answer side).

**If you entered a note ID that doesn't exist**, you'll see:

```
Note not found.
```

**Note:** flashcards can, internally, be marked as `"known"` once you've studied them — but like updating/deleting notes, **there is currently no menu option to mark a flashcard as known**. Every flashcard you view will show `Status: unknown`, regardless of how many times you've reviewed it, until this feature is added to the menu.

---

## 8. Using the AI Study Assistant (Ask a Question)

**What it does:** Lets you type any study-related question in plain English and get an AI-generated answer.

**Steps:**

1. From the main menu, type `5` and press Enter.
2. When prompted `Your question:`, type your question (e.g., `Why is photosynthesis important for life on Earth?`) and press Enter.

**What you should see:**

- A short pause while the AI generates a response.
- Then:

```
Answer: Photosynthesis is important because...
```

**Note:** each question is answered independently — the assistant does not currently reference your saved notes when answering, and it does not remember earlier questions as conversational context within the same session (each question/answer pair is simply logged, not used to inform the next answer).

---

## 9. Viewing the Dashboard

**What it does:** Shows a quick summary of your overall study activity — how many notes, quizzes, and flashcards you've created, and how many questions you've asked the AI assistant.

**Steps:**

1. From the main menu, type `6` and press Enter.

**What you should see:**

```
{'total_notes': 2, 'total_quizzes': 1, 'total_flashcards': 3, 'flashcards_known': 0, 'flashcards_unknown': 3, 'total_chat_questions': 2}
```

This is a summary of counts: total notes, total quizzes, total flashcards, how many flashcards are known vs. unknown, and total questions asked. Since there's currently no way to mark a flashcard as "known" (see Section 7), `flashcards_known` will always show `0`.

**Related options — reviewing generated content:**

- **Option 7 (View all quizzes)** — displays every quiz you've generated so far, in the same format shown when a quiz is first created.
- **Option 8 (View all flashcards)** — displays every flashcard you've generated so far, in the same format shown when flashcards are first created.

---

## 10. Troubleshooting

| What you see                                                             | What it means                                                                                         | What to do                                                                                                                        |
| ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `No notes yet.` (when viewing notes)                                     | You haven't created any notes in this session or in previously saved data                             | Choose option 1 to create your first note                                                                                         |
| `Note not found.` (when generating a quiz or flashcards)                 | The note ID you typed doesn't match any existing note                                                 | Choose option 2 to view your notes and confirm the correct ID                                                                     |
| A long pause after choosing option 3, 4, or 5                            | The app is waiting on a response from the AI service — this is normal and usually takes a few seconds | Wait for it to finish; if it takes unusually long, there may be a connectivity issue (see below)                                  |
| An error message mentioning the AI service being "unavailable" or "busy" | The AI service is temporarily overloaded                                                              | Try the same action again in a minute or two — this is temporary and not something you did wrong                                  |
| An error message about a missing or invalid answer format from the AI    | The AI occasionally returns content that isn't in the expected format                                 | Try generating the quiz or flashcards again — this is an occasional AI response quirk                                             |
| Your notes/quizzes/flashcards from a previous session are missing        | You likely closed the app without choosing option 9 (Save and exit) last time                         | Always choose option 9 to save before closing; unfortunately, data from a session that wasn't saved cannot be recovered           |
| You want to update or delete a note, or mark a flashcard as known        | These actions exist in the app's underlying logic but are **not yet available** as menu options       | This isn't something you can currently do — it would need to be added as a new menu feature                                       |
| The app closes unexpectedly or shows a technical error (a "traceback")   | An unexpected problem occurred                                                                        | Note down what you were doing when it happened and report it, including the full error text, to whoever maintains the application |

---

## Summary of What's Available Today

| Feature                           | Available from the menu? |
| --------------------------------- | ------------------------ |
| Create a note                     | ✅ Yes (Option 1)        |
| View all notes                    | ✅ Yes (Option 2)        |
| Update a note                     | ❌ Not yet               |
| Delete a note                     | ❌ Not yet               |
| Generate a quiz                   | ✅ Yes (Option 3)        |
| View all quizzes                  | ✅ Yes (Option 7)        |
| Delete a quiz                     | ❌ Not yet               |
| Generate flashcards               | ✅ Yes (Option 4)        |
| View all flashcards               | ✅ Yes (Option 8)        |
| Mark a flashcard as known/unknown | ❌ Not yet               |
| Delete a flashcard                | ❌ Not yet               |
| Ask the AI a study question       | ✅ Yes (Option 5)        |
| View dashboard summary            | ✅ Yes (Option 6)        |
| Save data and exit                | ✅ Yes (Option 9)        |
