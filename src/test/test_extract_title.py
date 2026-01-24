import unittest

from src.extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_strips_whitespace(self):
        self.assertEqual(
            extract_title("#   Hello World   "),
            "Hello World",
        )

    def test_extract_title_first_h1_only(self):
        markdown = """# Title
## Subtitle
# Another"""
        self.assertEqual(extract_title(markdown), "Title")

    def test_extract_title_raises_if_missing(self):
        with self.assertRaises(Exception):
            extract_title("## No H1 here")


if __name__ == "__main__":
    unittest.main()
