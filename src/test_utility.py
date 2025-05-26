import unittest
from htmlnode import HTMLNode, LeafNode, ParrentNode
from textnode import TextNode,TextType
from utility import text_node_to_html_node,split_nodes_delimiter

class TESTTextNodeConverion(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        node2 = TextNode("This is a Link",TextType.LINK,"www.google.com")
        html_node2 = text_node_to_html_node(node2)
        self.assertEqual(html_node2.tag,"a")
        self.assertEqual(html_node2.props,{"href": "www.google.com"})
        node3 = TextNode("Bold Text",TextType.BOLD)
        html_node3 = text_node_to_html_node(node3)
        self.assertEqual(html_node3.tag,"b")
        node4 = TextNode("Hello World",TextType.IMAGE,"www.boot.dev")
        html_node4 = text_node_to_html_node(node4)
        self.assertEqual(html_node4.tag,"img")
        self.assertEqual(html_node4.props,{"src": "www.boot.dev","alt":"Hello World"})

class TESTSplitNodes(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes,[TextNode("This is text with a ", TextType.NORMAL),TextNode("code block", TextType.CODE),TextNode(" word", TextType.NORMAL)])
        
        input_nodes = [TextNode("This is just plain text", TextType.NORMAL)]
        output = split_nodes_delimiter(input_nodes, "`", TextType.CODE)
        expected = [TextNode("This is just plain text", TextType.NORMAL)]
        self.assertEqual(output,expected)

        input_nodes2 = [TextNode("This is `broken code block", TextType.NORMAL)]
        output2 = split_nodes_delimiter(input_nodes2, "`", TextType.CODE)
        expected2 = [TextNode("This is `broken code block", TextType.NORMAL)]
        self.assertEqual(output2,expected2)

        input_nodes3 = [TextNode("Here is `code1` and `code2`", TextType.NORMAL)]
        output3 = split_nodes_delimiter(input_nodes3, "`", TextType.CODE)
        expected3 = [TextNode("Here is ", TextType.NORMAL),TextNode("code1", TextType.CODE),TextNode(" and ", TextType.NORMAL),TextNode("code2", TextType.CODE)]
        self.assertEqual(output3,expected3)

        input_nodes4 = [TextNode("Some **bold** and _italic_ text", TextType.NORMAL)]
        after_bold = split_nodes_delimiter(input_nodes4, "**", TextType.BOLD)
        after_italic = split_nodes_delimiter(after_bold, "_", TextType.ITALIC)
        expected4 = [TextNode("Some ", TextType.NORMAL),TextNode("bold", TextType.BOLD),TextNode(" and ", TextType.NORMAL),TextNode("italic", TextType.ITALIC),TextNode(" text", TextType.NORMAL),]
        self.assertEqual(expected4,after_italic)

if __name__ == "__main__":
    unittest.main() 