from textnode import TextNode,TextType
import re

# Splits Text into TextNodes
def split_nodes_delimiter(old_nodes,delimiter,text_type):

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = []
        split_node = node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise ValueError("Invalid Markdown")
        for n in range(len(split_node)):
            if split_node[n] == "":
                continue
            if n % 2 == 0:
                split_nodes.append(TextNode(split_node[n],TextType.TEXT))
            else:
                split_nodes.append(TextNode(split_node[n],text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall( r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches