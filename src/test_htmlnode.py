import unittest
from htmlnode import HTMLNode, LeafNode, ParrentNode
from textnode import TextNode,TextType
from utility import text_node_to_html_node

class TESTHTMLNode(unittest.TestCase):
     def test_eq(self):
        node1 = HTMLNode(props={"class": "container", "id": "main"})
        expected = ' class="container" id="main"'
        actual = node1.props_to_html()
        self.assertEqual(expected,actual)
        node2 = HTMLNode("a","Hello")
        actual2 = node2.props_to_html()
        except2 = ""
        self.assertEqual(except2,actual2)         

class TESTLeafNode(unittest.TestCase):
     def test_eq(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        node2 = LeafNode("a", "Click me!", props={"href": "https://www.google.com"})
        self.assertEqual('<a href="https://www.google.com">Click me!</a>',node2.to_html())
        node3 = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual("<p>This is a paragraph of text.</p>",node3.to_html())

class TESTParrentNode(unittest.TestCase):
    def test_eq(self):
        node = ParrentNode("p",[LeafNode("b", "Bold text"),LeafNode(None, "Normal text"),LeafNode("i", "italic text"),LeafNode(None, "Normal text")])
        self.assertEqual("<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",node.to_html())
        node2 = ParrentNode("p",[LeafNode("b", "Bold text"),LeafNode(None, "Normal text"),ParrentNode("f",[LeafNode(None, "Normal text"),LeafNode("i", "italic text")])])
        
        self.assertEqual("<p><b>Bold text</b>Normal text<f>Normal text<i>italic text</i></f></p>",node2.to_html())
        child_node = LeafNode("span", "child")
        parent_node = ParrentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParrentNode("span", [grandchild_node])
        parent_node = ParrentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>",)







if __name__ == "__main__":
    unittest.main() 