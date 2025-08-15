from enum import Enum
from htmlnode import LeafNode, HTMLNode

class TextType(Enum):
    PLAIN = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        if isinstance(text_type, str) and text_type in TextType._value2member_map_:
            self.text_type = TextType(text_type)
        elif isinstance(text_type, TextType) and text_type.value in TextType._value2member_map_:
            self.text_type = text_type
        else:
            raise ValueError("not a valid TextType")
        self.url = url

    def __eq__(self, value):
        if not isinstance(value, TextNode):
            return False
        return (self.text == value.text 
                and self.text_type == value.text_type 
                and self.url == value.url)
    
    def __repr__(self):
        if not self.url:
            return f'TextNode("{self.text}", {self.text_type})'
        return f'TextNode("{self.text}", {self.text_type}, "{self.url}")'
    
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.PLAIN:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError("not a valid TextType")