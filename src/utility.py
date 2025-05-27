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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text == "":
            continue
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        
        text = node.text
        images = extract_markdown_images(text)
        
        if not images:
            new_nodes.append(node)
            continue
        
        for image in images:
            alt_text = image[0]
            url = image[1]

            parts = text.split(f"![{alt_text}]({url})",1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0],TextType.NORMAL))
            new_nodes.append(TextNode(alt_text,TextType.IMAGE,url))
            text = parts[1]

        if text:
            new_nodes.append(TextNode(text,TextType.NORMAL))
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text == "":
            continue
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        
        text = node.text
        links = extract_markdown_links(text)
        
        if not links:
            new_nodes.append(node)
            continue
        
        for link in links:
            link_text = link[0]
            url = link[1]

            parts = text.split(f"[{link_text}]({url})",1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0],TextType.NORMAL))
            new_nodes.append(TextNode(link_text,TextType.LINK,url))
            text = parts[1]

        if text:
            new_nodes.append(TextNode(text,TextType.NORMAL))
    
    return new_nodes  

def text_to_textnodes(text):
    nodes = TextNode(text,TextType.NORMAL)
    nodes = split_nodes_delimiter([nodes], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    block = markdown.split("\n\n")
    new_block = []
    for i in block:
        temp = i.strip()
        striped_lines = temp.split("\n")
        x = []
        for line in striped_lines:
            striped_line = line.strip()
            x.append(striped_line)
        temp = "\n".join(x)
        if temp == "":
            continue
        else:
            new_block.append(temp)
    return new_block