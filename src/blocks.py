
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        block.strip()
        if block == "":
            continue
        stripped_blocks = block.split("\n")
        
        for b in stripped_blocks:
            text = ""
            if b == "":
                continue
            text += f"\n{b}"
            new_blocks.append(text)
        new_blocks.append(block)
    return new_blocks
