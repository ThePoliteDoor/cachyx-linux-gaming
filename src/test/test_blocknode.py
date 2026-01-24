import unittest

from src.block_node import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

        def test_markdown_to_blocks_single_block(self):
            md = "Just one paragraph"
            self.assertEqual(
                markdown_to_blocks(md),
                ["Just one paragraph"],
            )

        def test_markdown_to_blocks_excessive_newlines(self):
            md = "\n\n\nParagraph one\n\n\nParagraph two\n\n"
            self.assertEqual(
                markdown_to_blocks(md),
                ["Paragraph one", "Paragraph two"],
            )

        def test_markdown_to_blocks_preserves_internal_newlines(self):
            md = "Line one\nLine two\nLine three"
            self.assertEqual(
                markdown_to_blocks(md),
                ["Line one\nLine two\nLine three"],
            )

        def test_markdown_to_blocks_empty_input(self):
            md = ""
            self.assertEqual(
                markdown_to_blocks(md),
                [],
            )


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is just a paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading(self):
        block = "## This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_invalid_heading_no_space(self):
        block = "##Invalid heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> This is a quote\n> that spans lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_start(self):
        block = "2. first\n3. second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_wrong_increment(self):
        block = "1. first\n3. second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_mixed_list_not_valid(self):
        block = "- item one\n2. item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


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
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p>"
        "<p>This is another paragraph with <i>italic</i> text and "
        "<code>code</code> here</p></div>",
    )


def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
"""

    node = markdown_to_html_node(md)
    html = node.to_html()

    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\n"
        "the **same** even with inline stuff\n</code></pre></div>",
    )


def test_heading(self):
    md = "# Hello **world**"
    html = markdown_to_html_node(md).to_html()
    self.assertEqual(
        html,
        "<div><h1>Hello <b>world</b></h1></div>",
    )


def test_unordered_list(self):
    md = """
- one
- two
- **three**
"""
    html = markdown_to_html_node(md).to_html()
    self.assertEqual(
        html,
        "<div><ul><li>one</li><li>two</li><li><b>three</b></li></ul></div>",
    )


if __name__ == "__main__":
    unittest.main()
