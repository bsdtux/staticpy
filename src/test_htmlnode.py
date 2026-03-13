from src.htmlnode import HTMLNode, LeafNode, ParentNode
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
    
    def test_to_html_no_tag(self):
        node = LeafNode(None, "test")
        self.assertEqual(node.to_html(), "test")


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(tag='p', children=[ LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text")])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

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
