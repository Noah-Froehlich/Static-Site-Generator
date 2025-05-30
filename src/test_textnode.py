import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test2_eq(self):
        node = TextNode("This is a text node", TextType.LINKS,"www.Boot.dev")
        node2 = TextNode("This is a text node", TextType.LINKS,"www.Boot.dev")
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main() 