import unittest
from main import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_basic(self):
        markdown = "# This is a title\nSome content"
        self.assertEqual(extract_title(markdown), "This is a title")
    
    def test_extract_title_whitespace(self):
        markdown = "#    Lots of space    \nSome content"
        self.assertEqual(extract_title(markdown), "Lots of space")
    
    def test_extract_title_no_h1(self):
        markdown = "## This is h2\nSome content"
        with self.assertRaises(Exception):
            extract_title(markdown)
    
    def test_extract_title_empty(self):
        markdown = "No headers here"
        with self.assertRaises(Exception):
            extract_title(markdown)
    
    def test_extract_title_hash_no_space(self):
        markdown = "#This is not a header\nSome content"
        with self.assertRaises(Exception):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()

