import unittest

from textnode import TextNode, TextType, text_node_to_html_node



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
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")




if __name__ == "__main__":
    unittest.main()