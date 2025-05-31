from enum import Enum
from htmlnode import ParrentNode,LeafNode
from textnode import text_node_to_html_node,TextNode,TextType
from utlility import text_to_textnodes


class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unorderdList"
    OLIST = "orderdList"
    PARAGRAPH = "Paragraph"

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH

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


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                children.append(handle_Paragraphs(block))
            case BlockType.QUOTE:
                children.append(handle_Quote(block))
            case BlockType.CODE:
                children.append(handle_Code(block))
            case BlockType.ULIST:
                children.append(handle_Ul(block))
            case BlockType.OLIST:
                children.append(handle_Ol(block))
            case BlockType.HEADING:
                children.append(handle_Headline(block))
    return ParrentNode("div",children,None)

def handle_Paragraphs(block):
    lines = block.split("\n")
    text = " ".join(lines)
    child = text_to_node(text)
    return ParrentNode("p",child)

def handle_Quote(block):    
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_node(content)
    return ParrentNode("blockquote", children)

def handle_Code(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid Code")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParrentNode("code", [child])
    return ParrentNode("pre", [code])

def handle_Ul(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_node(text)
        html_items.append(ParrentNode("li", children))
    return ParrentNode("ul", html_items)

def handle_Ol(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_node(text)
        html_items.append(ParrentNode("li", children))
    return ParrentNode("ol", html_items)

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
    children = text_to_node(text)
    return ParrentNode(f"h{level}", children)

#return a Childnode from Text
def text_to_node(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children