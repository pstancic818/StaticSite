import unittest
#from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


class TestSplitNodes(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.PLAIN
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.PLAIN),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.PLAIN
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_invalid_markdown(self):
        node = TextNode("This is text with a `code block word", TextType.PLAIN)
        with self.assertRaises(ValueError) as context:
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
            self.assertEqual(str(context.exception), "invalid markdown, formatted section not closed")

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_empty(self):
        matches = extract_markdown_images("Hello World!")
        self.assertListEqual([], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_beginning(self):
        node = TextNode("[link to a cool thing](https://srbija.do.tokija)Znas sta", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link to a cool thing", TextType.LINK, "https://srbija.do.tokija"),
                TextNode("Znas sta", TextType.PLAIN)
            ],
            new_nodes
        )

    def test_split_ending(self):
        node = TextNode("Znas sta[link to a cool thing](https://srbija.do.tokija)", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Znas sta", TextType.PLAIN),
                TextNode("link to a cool thing", TextType.LINK, "https://srbija.do.tokija")
            ],
            new_nodes
        )

    def test_textnode_nobold(self):
        text = 'This is text with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        node = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN), 
                TextNode("italic", TextType.ITALIC), 
                TextNode(" word and a ", TextType.PLAIN), 
                TextNode("code block", TextType.CODE), 
                TextNode(" and an ", TextType.PLAIN), 
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), 
                TextNode(" and a ", TextType.PLAIN), 
                TextNode("link", TextType.LINK, "https://boot.dev")
            ],
            node
        )

    def test_textnode_noimage(self):
        text = "This is **bold** text with an _italic_ word and a [link](https://boot.dev) whachu think?"
        node = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" text with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC), 
                TextNode(" word and a ", TextType.PLAIN), 
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" whachu think?", TextType.PLAIN),
            ],
            node
        )

    def test_textnode_nolink(self):
        text = "This is **bold** text with an _italic_ word and a `code block` whachu think?"
        node = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" text with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC), 
                TextNode(" word and a ", TextType.PLAIN), 
                TextNode("code block", TextType.CODE),
                TextNode(" whachu think?", TextType.PLAIN),
            ],
            node
        )

    def test_textnode_nodelimiters(self):
        text = "This is text with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) whachu think?"
        node = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), 
                TextNode(" and a ", TextType.PLAIN), 
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" whachu think?", TextType.PLAIN),
            ],
            node
        )

if __name__ == "__main__":
    unittest.main()