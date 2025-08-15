import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not isinstance(old_nodes, list):
        raise TypeError("old_nodes should be a list")
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        tmp = node.text.split(delimiter)
        if len(tmp) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(tmp)):
            if tmp[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(tmp[i], "text"))
            else:
                new_nodes.append(TextNode(tmp[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r'!\[(.+?)\]\((.+?)\)', text)

def extract_markdown_links(text):
    return re.findall(r'\[(.+?)\]\((.+?)\)', text)

def split_nodes_image(old_nodes):
    if not isinstance(old_nodes, list):
        raise TypeError("old_nodes should be a list")
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        tmp = extract_markdown_images(node.text)
        if not tmp:
            new_nodes.append(TextNode(node.text, TextType.PLAIN))
            continue
        current_text = node.text
        for i in range(len(tmp)):
            list_text = current_text.split(f'![{tmp[i][0]}]({tmp[i][1]})', 1)
            if list_text[0]:
                new_nodes.append(TextNode(list_text[0], TextType.PLAIN))
            new_nodes.append(TextNode(tmp[i][0], TextType.IMAGE, tmp[i][1]))
            current_text = list_text[1]
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.PLAIN))
    return new_nodes

def split_nodes_link(old_nodes):
    if not isinstance(old_nodes, list):
        raise TypeError("old_nodes should be a list")
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        tmp = extract_markdown_links(node.text)
        if not tmp:
            new_nodes.append(TextNode(node.text, TextType.PLAIN))
            continue
        current_text = node.text
        for i in range(len(tmp)):
            list_text = current_text.split(f'[{tmp[i][0]}]({tmp[i][1]})', 1)
            if list_text[0]:
                new_nodes.append(TextNode(list_text[0], TextType.PLAIN))
            new_nodes.append(TextNode(tmp[i][0], TextType.LINK, tmp[i][1]))
            current_text = list_text[1]
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.PLAIN))
    return new_nodes

def text_to_textnodes(text):
    if not isinstance(text, str):
        raise TypeError("text should be a string")
    new_nodes = [TextNode(text, TextType.PLAIN)]
    new_nodes = split_nodes_delimiter(new_nodes, '**', TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, '_', TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, '`', TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes