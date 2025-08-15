import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_types(self):
        node = TextNode("this is a text node", "italic")
        node2 = TextNode("this is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("this is a text node", "italic", "https://boot.dev")
        node2 = TextNode("this is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", "bold", "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_invalid_type(self):
        with self.assertRaises(ValueError) as context:
            node = TextNode("This is an invalid tag", 1)
            self.assertEqual(str(context.exception), "not a valid TextType")

    def test_invalid_tag(self):
        with self.assertRaises(ValueError) as context:
            node = TextNode("This is an invalid tag", "random")
            self.assertEqual(str(context.exception), "not a valid TextType")
            
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", "italic")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is alt text", "image", "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "https://google.com", "alt": "This is alt text"})

    def test_link(self):
        node = TextNode("This is link text", "link", "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is link text")
        self.assertEqual(html_node.props, {"href": "https://google.com"})



if __name__ == "__main__":
    unittest.main()