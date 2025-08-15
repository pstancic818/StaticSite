import unittest
from markdownblocks import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node

class TestMarkdownBlocks(unittest.TestCase):
    def test_md_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
            blocks
        )

    def test_md_extra_blocks(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item



4hehe




5hehe
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            [
                '# This is a heading',
                'This is a paragraph of text. It has some **bold** and _italic_ words inside of it.',
                '- This is the first list item in a list block\n- This is a list item\n- This is another list item',
                '4hehe', 
                '5hehe'
            ],
            blocks
        )

    def test_md_head(self):
        md = "# This is a heading"
        block = block_to_block_type(md)
        self.assertEqual(BlockType.HEADING, block)

    def test_md_nothead(self):
        md = "#This is a heading"
        block = block_to_block_type(md)
        self.assertEqual(BlockType.PARAGRAPH, block)

    def test_md_code(self):
        md = '```\nThis is a code block\n```'
        block = block_to_block_type(md)
        self.assertEqual(BlockType.CODE, block)

    def test_md_notcode(self):
        md = '```\nThis is a code block\n'
        block = block_to_block_type(md)
        self.assertEqual(BlockType.PARAGRAPH, block)

    def test_md_quote(self):
        md = '>green text\n>mfw'
        block = block_to_block_type(md)
        self.assertEqual(BlockType.QUOTE, block)

    def test_md_notquote(self):
        md = '>green text\nmfw'
        block = block_to_block_type(md)
        self.assertEqual(BlockType.PARAGRAPH, block)

    def test_md_unlist(self):
        md = '- item 1\n- item 2\n- item 3'
        block = block_to_block_type(md)
        self.assertEqual(BlockType.UNORDERED_LIST, block)

    def test_md_notunlist(self):
        md = '- item 1\nitem 2\n- item 3'
        block = block_to_block_type(md)
        self.assertEqual(BlockType.PARAGRAPH, block)

    def test_md_odlist(self):
        md = '1. item 1\n2. item 2\n3. item 3'
        block = block_to_block_type(md)
        self.assertEqual(BlockType.ORDERED_LIST, block)

    def test_md_notodlist(self):
        md = '1. item 1\nitem 2\n3. item 3'
        block = block_to_block_type(md)
        self.assertEqual(BlockType.PARAGRAPH, block)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_blockquote(self):
        md = """
>lol
>lmao even
>mfw

Then we do reddit spacing because that's how they _roll_ my **dude**
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>lol\nlmao even\nmfw</blockquote><p>Then we do reddit spacing because that's how they <i>roll</i> my <b>dude</b></p></div>"
        )

    def test_bothlists(self):
        md = """
# Countries

- Slovenia
- Croatia
- Serbia
- Montenegro
- Bosnia

## Song

1. here comes the
2. to the
3. to the
4. something something floor
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Countries</h1><ul><li>Slovenia</li><li>Croatia</li><li>Serbia</li><li>Montenegro</li><li>Bosnia</li></ul><h2>Song</h2><ol><li>here comes the</li><li>to the</li><li>to the</li><li>something something floor</li></ol></div>"
        )