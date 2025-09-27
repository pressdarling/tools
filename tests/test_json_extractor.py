import unittest
import sys
import os

# Add the python directory to the path so we can import the script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python')))

from json_extractor import extract_json_structures

class TestJsonExtractor(unittest.TestCase):
    def test_extract_json_object(self):
        text = 'Some text {"key": "value"} and some more text'
        expected = [{"key": "value"}]
        self.assertEqual(extract_json_structures(text), expected)

    def test_extract_json_array(self):
        text = 'Some text with a JSON array [1, 2, {"key": "value"}]'
        expected = [[1, 2, {"key": "value"}]]
        self.assertEqual(extract_json_structures(text), expected)

if __name__ == '__main__':
    unittest.main()