import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.ai_chat import AIChatAssistant

assistant = AIChatAssistant()

answer1 = assistant.ask_question("What is photosynthesis?")
print("--- After asking question 1 ---")
print(answer1)

answer2 = assistant.ask_question("What is Newton's second law?")
print("\n--- After asking question 2 ---")
print(answer2)

print("\n--- Full chat history ---")
for entry in assistant.get_chat_history():
    print(entry)

cleared = assistant.clear_chat_history()
print(f"\n--- Cleared chat history? {cleared} ---")
print(assistant.get_chat_history())

answer3 = assistant.ask_question("What is mitosis?")
print("\n--- After asking a new question post-clear ---")
print(answer3)
print(assistant.get_chat_history())