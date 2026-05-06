import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode('div', 'Hello World', None, {'class': 'my-class'})
        self.assertEqual(repr(node), "HTMLNode(div, Hello World, None, {'class': 'my-class'})")

    def test_props_to_html(self):
        node = HTMLNode('div', 'Hello World', None, {'class': 'my-class'})
        self.assertEqual(node.props_to_html(), 'class="my-class"')

    def test_props_to_html2(self):
        node = HTMLNode('div', 'Hello World', None)
        self.assertEqual(node.props_to_html(), '')

