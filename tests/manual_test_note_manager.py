import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.note_manager import NoteManager
# ==========================================
# Manual Test - NoteManager
# AI Study Assistant
# ==========================================

from modules.note_manager import NoteManager

print("=" * 60)
print("        AI STUDY ASSISTANT - NOTEMANAGER TEST")
print("=" * 60)

# ------------------------------------------
# Create NoteManager Object
# ------------------------------------------

manager = NoteManager()

print("\n✅ NoteManager object created successfully.")

# ------------------------------------------
# TEST 1 - Create Notes
# ------------------------------------------

print("\n" + "=" * 60)
print("TEST 1 - CREATE NOTES")
print("=" * 60)

note1 = manager.create_note(
    "Photosynthesis",
    "Plants convert sunlight into energy.",
    "Biology"
)

note2 = manager.create_note(
    "Newton's Laws",
    "Force equals mass times acceleration.",
    "Physics"
)

print("✅ Two notes created successfully!")

# ------------------------------------------
# TEST 2 - Display Notes
# ------------------------------------------

print("\n" + "=" * 60)
print("TEST 2 - DISPLAY NOTES")
print("=" * 60)

notes = manager.get_notes()

for note in notes:
    print(f"ID      : {note['id']}")
    print(f"Title   : {note['title']}")
    print(f"Subject : {note['subject']}")
    print(f"Content : {note['content']}")
    print("-" * 40)

# ------------------------------------------
# TEST 3 - Update Note
# ------------------------------------------

print("\n" + "=" * 60)
print("TEST 3 - UPDATE NOTE")
print("=" * 60)

updated = manager.update_note(
    note1["id"],
    title="Photosynthesis (Updated)"
)

print("Update Successful:", updated)

print("\nUpdated Notes:\n")

notes = manager.get_notes()

for note in notes:
    print(f"ID      : {note['id']}")
    print(f"Title   : {note['title']}")
    print(f"Subject : {note['subject']}")
    print(f"Content : {note['content']}")
    print("-" * 40)

# ------------------------------------------
# TEST 4 - Delete Note
# ------------------------------------------

print("\n" + "=" * 60)
print("TEST 4 - DELETE NOTE")
print("=" * 60)

deleted = manager.delete_note(note2["id"])

print("Delete Successful:", deleted)

print("\nRemaining Notes:\n")

notes = manager.get_notes()

for note in notes:
    print(f"ID      : {note['id']}")
    print(f"Title   : {note['title']}")
    print(f"Subject : {note['subject']}")
    print(f"Content : {note['content']}")
    print("-" * 40)

# ------------------------------------------
# TEST 5 - Delete Invalid Note
# ------------------------------------------

print("\n" + "=" * 60)
print("TEST 5 - DELETE INVALID NOTE")
print("=" * 60)

deleted = manager.delete_note(999)

print("Delete Successful:", deleted)

# ------------------------------------------
# TEST 6 - Final List of Notes
# ------------------------------------------

print("\n" + "=" * 60)
print("FINAL NOTES")
print("=" * 60)

notes = manager.get_notes()

for note in notes:
    print(f"ID      : {note['id']}")
    print(f"Title   : {note['title']}")
    print(f"Subject : {note['subject']}")
    print(f"Content : {note['content']}")
    print("-" * 40)

# ------------------------------------------
# END OF TEST
# ------------------------------------------

print("\n" + "=" * 60)
print("🎉 ALL MANUAL TESTS COMPLETED SUCCESSFULLY!")
print("=" * 60)
