import os
import sys

# Add the project root to Python's path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from modules.quiz_generator import QuizGenerator

generator = QuizGenerator()

sample_note_content = (
    "Photosynthesis is the process plants use to convert sunlight into energy. "
    "This process mainly takes place inside the chloroplasts of plant cells. "
    "Oxygen is released into the atmosphere as a byproduct of photosynthesis."
)

quiz1 = generator.generate_quiz("Photosynthesis", sample_note_content, num_questions=3)

print("--- After generating a quiz ---")
print(quiz1)

print("\n--- All quizzes stored ---")
print(generator.get_quizzes())

deleted = generator.delete_quiz(quiz1["id"])
print(f"\n--- Deleted quiz 1? {deleted} ---")
print(generator.get_quizzes())

deleted_again = generator.delete_quiz(999)
print(f"\n--- Tried deleting a quiz that doesn't exist. Success? {deleted_again} ---")