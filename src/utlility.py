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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        images = extract_markdown_images(text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            section = text.split(f"![{image[0]}]({image[1]})", 1)
            if len(section) != 2:
                raise ValueError("invalid markdown")
            if section[0] != "":
                new_nodes.append(TextNode(section[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0],TextType.IMAGE,image[1]))
            text = section[1]
        if text != "":
            new_nodes.append(TextNode(text,TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        images = extract_markdown_links(text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            section = text.split(f"[{image[0]}]({image[1]})", 1)
            if len(section) != 2:
                raise ValueError("invalid markdown")
            if section[0] != "":
                new_nodes.append(TextNode(section[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0],TextType.LINK,image[1]))
            text = section[1]
        if text != "":
            new_nodes.append(TextNode(text,TextType.TEXT))
    return new_nodes
