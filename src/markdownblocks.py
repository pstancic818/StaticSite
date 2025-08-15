from enum import Enum
from splitnodes import text_to_textnodes
from textnode import text_node_to_html_node
from htmlnode import ParentNode, LeafNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    if not isinstance(markdown, str):
        raise TypeError("markdown_to_blocks only accepts a string as input")
    blocks = []
    for i in markdown.split('\n\n'):
        if not i:
            continue
        blocks.append(i.strip())
    return blocks

def block_to_block_type(markdown_block):
    if markdown_block.startswith("#"):
        if (
            markdown_block.startswith('# ') or 
            markdown_block.startswith('## ') or 
            markdown_block.startswith('### ') or 
            markdown_block.startswith('#### ') or 
            markdown_block.startswith('##### ') or 
            markdown_block.startswith('###### ')
        ):
            return BlockType.HEADING
        return BlockType.PARAGRAPH
    elif markdown_block.startswith('```') and markdown_block.endswith('```'):
        return BlockType.CODE
    tmp = markdown_block.split('\n')
    if markdown_block.startswith('> '):
        for i in range(len(tmp)):
            if not tmp[i].startswith('>'):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif markdown_block.startswith('- '):
        for i in range(len(tmp)):
            if not tmp[i].startswith('- '):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif markdown_block.startswith('1. '):
        tracker = True
        for i in range(len(tmp)):
            if not tmp[i].startswith(f'{i+1}. '):
                tracker = False
            if tracker is not True:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    mainlist = []
    for block in blocks:
        blocktype = block_to_block_type(block)
        mainlist.extend(block_to_children(block, blocktype))
    return ParentNode('div', mainlist)

def block_to_children(block, blocktype):
    if blocktype == BlockType.PARAGRAPH:
        newstr = ' '.join(block.split('\n'))
        return [ParentNode('p', unpack_nodes(newstr))]
    elif blocktype == BlockType.HEADING:
        hnum = len(block) - len(block.lstrip('#'))
        parent = [ParentNode(f'h{hnum}', unpack_nodes(block.lstrip('# ')))]
        return parent
    elif blocktype == BlockType.QUOTE:
        tmp = block.split('\n')
        newstr = ''
        for i in tmp:
            if not i[1:]:
                newstr += '<br>'
                continue
            newstr += i[1:].strip()
        newstr = newstr[:-4]
        parent = [ParentNode('blockquote', unpack_nodes(newstr))]
        return parent
    elif blocktype == BlockType.CODE:
        parent = [ParentNode('pre', [LeafNode('code', block.split('```')[1][1:])])]
        return parent
    elif blocktype == BlockType.UNORDERED_LIST:
        tmp = block.split('\n')
        newlist = []
        for i in tmp:
            newlist.append(ParentNode('li', unpack_nodes(i.lstrip('- '))))
        return [ParentNode('ul', newlist)]
    elif blocktype == BlockType.ORDERED_LIST:
        tmp = block.split('\n')
        newlist = []
        for i in range(len(tmp)):
            newlist.append(ParentNode('li', unpack_nodes(tmp[i].lstrip(f'{i+1}. '))))
        return [ParentNode('ol', newlist)]

def unpack_nodes(block):
    newlist = []
    nodes = text_to_textnodes(block)
    for node in nodes:
        newlist.append(text_node_to_html_node(node))
    return newlist