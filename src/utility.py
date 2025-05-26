from htmlnode import LeafNode
from textnode import TextType,TextNode
import re

def text_node_to_html_node(text_node):
        match text_node.text_type:
            case TextType.NORMAL:
                return LeafNode(None,text_node.text,None)
            case TextType.BOLD:
                return LeafNode("b",text_node.text,None)
            case TextType.ITALIC:
                return LeafNode("i",text_node.text,None)
            case TextType.CODE:
                return LeafNode("code",text_node.text,None)
            case TextType.LINK:
                return LeafNode("a",text_node.text,{"href": text_node.url})
            case TextType.IMAGE:
                return LeafNode("img","",{"src": text_node.url,"alt": text_node.text})
            case _:
                raise Exception
            
def split_nodes_delimiter(old_nodes,delimiter,text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        text_parts = node.text.split(delimiter)
        
        if len(text_parts) < 3 or len(text_parts) % 2 == 0:
            new_nodes.append(node)
            continue
        
        for i,part in enumerate(text_parts):
            if part == "":
                continue
            if i % 2 ==0:
                new_nodes.append(TextNode(part,TextType.NORMAL))
            else:
                new_nodes.append(TextNode(part,text_type))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall( r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches

