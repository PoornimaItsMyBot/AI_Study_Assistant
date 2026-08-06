
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from ai.parser import parse_json_response


class TestParser(unittest.TestCase):

    def test_parses_plain_json(self):
        raw = '[{"front": "Q", "back": "A"}]'
        result = parse_json_response(raw)
        self.assertEqual(result, [{"front": "Q", "back": "A"}])

    def test_strips_markdown_code_fences(self):
        raw = '```json\n[{"front": "Q", "back": "A"}]\n```'
        result = parse_json_response(raw)
        self.assertEqual(result, [{"front": "Q", "back": "A"}])

    def test_raises_error_on_invalid_json(self):
        raw = "This is not JSON at all."
        with self.assertRaises(ValueError):
            parse_json_response(raw)


if __name__ == "__main__":
    unittest.main()