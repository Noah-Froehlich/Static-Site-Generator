import unittest
from htmlnode import HTMLNode, LeafNode, ParrentNode
from textnode import TextNode,TextType
from utility import *

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

class TESTExtraction(unittest.TestCase):
    def test_eq(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(result,expected)

        text2 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result2 = extract_markdown_links(text2)
        expected2 = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(result2,expected2)

        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

class TESTImageNodeSplit(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertEqual([TextNode("This is text with an ", TextType.NORMAL),TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),TextNode(" and another ", TextType.NORMAL),TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")],new_nodes)

    def test_no_image(self):
        node = TextNode("No image here", TextType.NORMAL)
        result = split_nodes_image([node])
        expected = [TextNode("No image here", TextType.NORMAL)]
        self.assertEqual(result, expected)

    def test_text_before_and_after_image(self):
        node = TextNode("Before ![img](http://url.com) after", TextType.NORMAL)
        result = split_nodes_image([node])
        expected = [
            TextNode("Before ", TextType.NORMAL),
            TextNode("img", TextType.IMAGE, "http://url.com"),
            TextNode(" after", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_multiple_node(self):
        node1 = TextNode("Start ![one](https://example.com/1.png) middle ![two](https://example.com/2.png) end",TextType.NORMAL)
        node2 = TextNode("No images here.",TextType.NORMAL)
        node3 = TextNode("![only](https://example.com/only.png) trailing text",TextType.NORMAL)
        result = split_nodes_image([node1,node2,node3])
        expected = [
        TextNode("Start ", TextType.NORMAL),
        TextNode("one", TextType.IMAGE, "https://example.com/1.png"),
        TextNode(" middle ", TextType.NORMAL),
        TextNode("two", TextType.IMAGE, "https://example.com/2.png"),
        TextNode(" end", TextType.NORMAL),

        TextNode("No images here.", TextType.NORMAL),

        TextNode("only", TextType.IMAGE, "https://example.com/only.png"),
        TextNode(" trailing text", TextType.NORMAL),
    ]
        self.assertEqual(expected,result)

class TESTLinksSplitNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a [link](https://example.com) and another [second](https://second.com)",TextType.NORMAL)
        result = split_nodes_link([node])
        excepted = [TextNode("This is a ", TextType.NORMAL),TextNode("link", TextType.LINK, "https://example.com"),TextNode(" and another ", TextType.NORMAL),TextNode("second", TextType.LINK, "https://second.com")]
        self.assertEqual(result,excepted)

    def test_single_link(self):
        node = TextNode("Click [here](https://example.com) for more info",TextType.NORMAL)
        result = split_nodes_link([node])
        expected = [TextNode("Click ", TextType.NORMAL),TextNode("here", TextType.LINK, "https://example.com"),TextNode(" for more info", TextType.NORMAL)]
        self.assertEqual(expected,result)

    def test_no_links(self):
        node = TextNode( "Just a simple sentence without links.",TextType.NORMAL)
        result = split_nodes_link([node])
        expected = [node]
        self.assertEqual(result,expected)
    
    def test_multiple_node(self):
        node1 = TextNode("Visit [Google](https://google.com) now!",TextType.NORMAL)
        node2 = TextNode("No links here.",TextType.NORMAL)
        result = split_nodes_link([node1,node2])
        expected = [TextNode("Visit ", TextType.NORMAL),TextNode("Google", TextType.LINK, "https://google.com"),TextNode(" now!", TextType.NORMAL),TextNode("No links here.", TextType.NORMAL)]
        self.assertEqual(expected,result)

class TESTTexttoNodes(unittest.TestCase):
    def test_eq(self):
        txt = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(txt)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(expected,nodes)

    def test_multiple(self):
        input_text = "**Bold** then normal _italic_ and ![img](url.com) and `code` then [link](url)"
        result = text_to_textnodes(input_text)
        expected = [
        TextNode("Bold", TextType.BOLD),
        TextNode(" then normal ", TextType.NORMAL),
        TextNode("italic", TextType.ITALIC),
        TextNode(" and ", TextType.NORMAL),
        TextNode("img", TextType.IMAGE, "url.com"),
        TextNode(" and ", TextType.NORMAL),
        TextNode("code", TextType.CODE),
        TextNode(" then ", TextType.NORMAL),
        TextNode("link", TextType.LINK, "url"),
    ]
        self.assertEqual(expected,result)

class TESTMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
                This is **bolded** paragraph

                This is another paragraph with _italic_ text and `code` here
                This is the same paragraph on a new line

                - This is a list
                - with items
                """
        blocks = markdown_to_blocks(md)
        expected = [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items"]
        self.assertEqual(expected,blocks)

    def test_markdown_to_blocks(self):
        md = """
            This i good Code

            And I Think that this are 2 Line
            Paragraphs

            - Test Lsite 1
            - Test Leise 2
    """
        blocks = markdown_to_blocks(md)
        
        expected = ["This i good Code","And I Think that this are 2 Line\nParagraphs","- Test Lsite 1\n- Test Leise 2"]
        self.assertEqual(expected,blocks)

    def test_more_Lists(self):
        md = """
            This is a **Text**

            - List 1
            - List 2
            - List 3

            - Neue Liste 1
            - Neue Liste 2
        """
        blocks = markdown_to_blocks(md)
        expected = ["This is a **Text**","- List 1\n- List 2\n- List 3","- Neue Liste 1\n- Neue Liste 2"]
        self.assertEqual(expected,blocks)

if __name__ == "__main__":
    unittest.main() 