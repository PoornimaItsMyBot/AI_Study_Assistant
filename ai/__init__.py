"""
Exposes the most commonly used pieces of the `ai` package directly, so
other modules can write:

    from ai import GeminiClient, build_quiz_prompt, parse_json_response

instead of reaching into each individual file.
"""

from .gemini_client import GeminiClient
from .prompts import build_chat_prompt, build_quiz_prompt, build_flashcard_prompt
from .parser import parse_json_response
#testing Git