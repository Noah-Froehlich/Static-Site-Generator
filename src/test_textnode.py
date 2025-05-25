import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node3 = TextNode("Hello World",TextType.ITALIC,"Goolge.com")
        self.assertNotEqual(node2,node3)
        node4 = TextNode("This is a text node", TextType.BOLD,"www.Boot.dev")
        self.assertNotEqual(node,node4)


if __name__ == "__main__":
    unittest.main()