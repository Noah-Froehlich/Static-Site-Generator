from utility import *
from htmlnode import *
from textnode import *
from blocks import *

def handle_quote(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParrentNode("blockquote", children)

def handle_Ul(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParrentNode("li", children))
    return ParrentNode("ul", html_items)

def handle_Ol(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParrentNode("li", children))
    return ParrentNode("ol", html_items)

def handle_code(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParrentNode("code", [child])
    return ParrentNode("pre", [code])

def handle_Headline(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParrentNode(f"h{level}", children)

def handle_Paragraphs(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParrentNode("p", children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        match BlockType:
            case BlockType.PARAGRAPH:
                children.append(handle_Paragraphs(block))
            case BlockType.QUOTE:
                children.append(handle_quote(block))
            case BlockType.CODE:
                children.append(handle_code(block))
            case BlockType.UNORDEREDLIST:
                children.append(handle_Ul(block))
            case BlockType.ORDEREDLIST:
                children.append(handle_Ol(block))
            case BlockType.HEADING:
                children.append(handle_Headline(block))
    return ParrentNode("div",children,None)