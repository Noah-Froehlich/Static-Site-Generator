from enum import Enum

BlockType = Enum('BlockType',['PARAGRAPH','HEADING','CODE','QUOTE','UNORDEREDLIST','ORDEREDLIST'])

def block_to_block_type(block):
    lines = block.split("\n")