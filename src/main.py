from textnode import TextNode,TextType
from blocks import markdown_to_blocks

def main():
    node = TextNode("This is a node",TextType.BOLD)
    print(node)

main()