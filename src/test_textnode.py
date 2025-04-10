import unittest

from textnode import TextNode, TextType, text_node_to_html_node, text_to_textnodes, markdown_to_blocks



class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)
    
    def test_not_equal_different_types(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.NORMAL_TEXT)
        self.assertNotEqual(node, node2)
    
    def test_with_url(self):
        node = TextNode("Link", TextType.LINK_TEXT, "https://example.com")
        node2 = TextNode("Link", TextType.LINK_TEXT, "https://example.com")
        self.assertEqual(node, node2)

    def test_none_url(self):
        node = TextNode("Some text", TextType.BOLD_TEXT)
        self.assertIsNone(node.url)
    
    def test_not_equal_different_urls(self):
        node1 = TextNode("Link text", TextType.LINK_TEXT, "https://example.com")
        node2 = TextNode("Link text", TextType.LINK_TEXT, "https://different.com")
        self.assertNotEqual(node1, node2)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_to_text_node(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        self.assertEqual(3, len(nodes))
        self.assertEqual("This is ", nodes[0].text)
        self.assertEqual(TextType.NORMAL_TEXT, nodes[0].text_type)
        self.assertEqual("bold", nodes[1].text)
        self.assertEqual(TextType.BOLD_TEXT, nodes[1].text_type)

def test_markdown_to_blocks(self):
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )


if __name__ == "__main__":
    unittest.main()