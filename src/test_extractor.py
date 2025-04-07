import unittest
from extractor import extract_markdown_images, extract_markdown_links

class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = "Here is an image ![alt text](http://example.com/image.png)."
        matches = extract_markdown_images(text)
        self.assertListEqual(matches, [("alt text", "http://example.com/image.png")])

    def test_multiple_images(self):
        text = "Here is one image ![image1](http://example.com/1.png) and another ![image2](http://example.com/2.png)."
        matches = extract_markdown_images(text)
        self.assertListEqual(matches, [
            ("image1", "http://example.com/1.png"),
            ("image2", "http://example.com/2.png")
        ])

    def test_no_images(self):
        text = "This text has no images!"
        matches = extract_markdown_images(text)
        self.assertListEqual(matches, [])

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        # A single markdown link
        text = "Here is a link [example](http://example.com)."
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [("example", "http://example.com")])

    def test_multiple_links(self):
        # Multiple markdown links
        text = "Here are [link1](http://example1.com) and [link2](http://example2.com)."
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [
            ("link1", "http://example1.com"),
            ("link2", "http://example2.com")
        ])

    def test_no_links(self):
        # No links in the input text
        text = "This text has no links at all."
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [])

    def test_links_with_extra_text(self):
        # Markdown links surrounded by other text
        text = "You can find more on [Boot.dev](https://www.boot.dev) or explore [GitHub](https://github.com)."
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [
            ("Boot.dev", "https://www.boot.dev"),
            ("GitHub", "https://github.com")
        ])

    def test_ignores_image_syntax(self):
        # Ensures that markdown links are matched, but images are ignored
        text = "Here is a text link [link](http://example.com) and an image ![alt text](http://example.com/image.png)."
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [("link", "http://example.com")])