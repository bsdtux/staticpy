from htmlnode import HTMLNode, LeafNode
import unittest


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_one_prop(self):
        node = HTMLNode(props={"class": "test"})
        self.assertEqual(node.props_to_html(), "class=\"test\"")

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(props={"class": "test", "id": "test2"})
        self.assertEqual(node.props_to_html(), "class=\"test\" id=\"test2\"")

    def test_repr_empty(self):
        node = HTMLNode()
        self.assertEqual(repr(node), "HTMLNode('')")

    def test_repr_one_prop(self):
        node = HTMLNode(tag='div', props={"class": "test"})
        self.assertEqual(repr(node), "HTMLNode(<div class=\"test\"> </div>)")

    def test_repr_multiple_props(self):
        node = HTMLNode(tag='div', props={"class": "test", "id": "test2"})
        self.assertEqual(repr(node), "HTMLNode(<div class=\"test\" id=\"test2\"> </div>)")


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode(tag='div', value='test')
        self.assertEqual(node.to_html(), "<div>test</div>")

    def test_repr(self):
        node = LeafNode(tag='div', value='test')
        self.assertEqual(repr(node), "LeafNode(<div>test</div>)")

    def test_to_html_with_props(self):
        node = LeafNode(tag='a', value='test', props={"class": "test", "href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), "<a class=\"test\" href=\"https://www.boot.dev\">test</a>")