import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_href(self):
        node = LeafNode("a", "Hello, world!", {"href": "http://example.com"})
        self.assertEqual(node.to_html(), '<a href="http://example.com">Hello, world!</a>')

    def test_repr(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(repr(node), "HTMLNode(p, Hello, world!, None)")