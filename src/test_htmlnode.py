import unittest
from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode(tag="div", value="Hello, World!", props={"class": "greeting"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello, World!")
        self.assertEqual(node.props, {"class": "greeting"})
        self.assertEqual(node.children, [])

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), 'href="https://example.com" target="_blank"')

    def test_empty_node(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_with_attributes(self):
        node = LeafNode("a", "Click here", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Click here</a>')
    
    def test_leaf_to_html_img_tag(self):
        node = LeafNode("img", "", {"src": "/images/logo.png", "alt": "Logo", "width": "100"})
        self.assertEqual(node.to_html(), '<img src="/images/logo.png" alt="Logo" width="100"></img>')
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


    