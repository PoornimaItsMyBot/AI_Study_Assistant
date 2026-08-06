"""
Handles turning Gemini's raw text responses into usable Python data.
Kept separate from gemini_client.py so parsing logic — and its own tests —
don't get tangled up with the actual API call logic.
"""

import json


def parse_json_response(raw_text):
    """
    Takes Gemini's raw text response, strips markdown code fences if
    present (Gemini sometimes wraps JSON in ```json ... ```), and parses
    it into a Python list/dict. Raises ValueError if it isn't valid JSON.
    """
    cleaned = raw_text.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as error:
        raise ValueError(f"Gemini did not return valid JSON: {error}\nRaw response: {raw_text}")