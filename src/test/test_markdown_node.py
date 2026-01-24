import unittest

from src.markdown_node import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from src.text_node import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_bold(self):
        node = TextNode(
            "This is **bold** text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_italic(self):
        node = TextNode(
            "This is _italic_ text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_non_text_nodes_unchanged(self):
        node = TextNode("bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [node])

    def test_missing_closing_delimiter_raises(self):
        node = TextNode("This is `broken text", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)


class TestMarkdownExtract(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches,
        )

    def test_extract_multiple_images(self):
        text = "Here is ![one](url1.png) and ![two](url2.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("one", "url1.png"), ("two", "url2.jpg")],
            matches,
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is a [link](https://example.com)")
        self.assertListEqual(
            [("link", "https://example.com")],
            matches,
        )

    def test_extract_multiple_links(self):
        text = "Links: [one](url1) and [two](url2)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("one", "url1"), ("two", "url2")],
            matches,
        )

    def test_links_do_not_match_images(self):
        text = "![image](img.png) and [link](site.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("link", "site.com")],
            matches,
        )


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images_basic(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://i.imgur.com/zjjcJKZ.png",
                ),
            ],
            new_nodes,
        )

    def test_split_images_multiple(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
            "and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://i.imgur.com/zjjcJKZ.png",
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

    def test_split_images_only_image(self):
        node = TextNode(
            "![alt](https://example.com/image.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode(
                    "alt",
                    TextType.IMAGE,
                    "https://example.com/image.png",
                )
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("Just plain text", TextType.TEXT)
        self.assertListEqual(
            [node],
            split_nodes_image([node]),
        )

    def test_split_images_ignores_non_text_nodes(self):
        node = TextNode(
            "image",
            TextType.IMAGE,
            "https://example.com/image.png",
        )

        self.assertListEqual(
            [node],
            split_nodes_image([node]),
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links_basic(self):
        node = TextNode(
            "This is a [link](https://example.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode(
                    "link",
                    TextType.LINK,
                    "https://example.com",
                ),
            ],
            new_nodes,
        )

    def test_split_links_multiple(self):
        node = TextNode(
            "Links: [one](https://one.com) and [two](https://two.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Links: ", TextType.TEXT),
                TextNode("one", TextType.LINK, "https://one.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.LINK, "https://two.com"),
            ],
            new_nodes,
        )

    def test_split_links_only_link(self):
        node = TextNode(
            "[bootdev](https://www.boot.dev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode(
                    "bootdev",
                    TextType.LINK,
                    "https://www.boot.dev",
                )
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode("Just plain text", TextType.TEXT)
        self.assertListEqual(
            [node],
            split_nodes_link([node]),
        )

    def test_split_links_does_not_match_images(self):
        node = TextNode(
            "![alt](https://example.com/image.png)",
            TextType.TEXT,
        )

        self.assertListEqual(
            [node],
            split_nodes_link([node]),
        )

    def test_split_links_ignores_non_text_nodes(self):
        node = TextNode(
            "bootdev",
            TextType.LINK,
            "https://www.boot.dev",
        )

        self.assertListEqual(
            [node],
            split_nodes_link([node]),
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_full_example(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )

        nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_textnodes_plain_text(self):
        text = "Just plain text"

        nodes = text_to_textnodes(text)

        self.assertListEqual(
            [TextNode("Just plain text", TextType.TEXT)],
            nodes,
        )

    def test_text_to_textnodes_only_bold(self):
        text = "**bold**"

        nodes = text_to_textnodes(text)

        self.assertListEqual(
            [TextNode("bold", TextType.BOLD)],
            nodes,
        )

    def test_text_to_textnodes_only_italic(self):
        text = "_italic_"

        nodes = text_to_textnodes(text)

        self.assertListEqual(
            [TextNode("italic", TextType.ITALIC)],
            nodes,
        )

    def test_text_to_textnodes_only_code(self):
        text = "`code`"

        nodes = text_to_textnodes(text)

        self.assertListEqual(
            [TextNode("code", TextType.CODE)],
            nodes,
        )

    def test_text_to_textnodes_only_image(self):
        text = "![alt](https://example.com/image.png)"

        nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode(
                    "alt",
                    TextType.IMAGE,
                    "https://example.com/image.png",
                )
            ],
            nodes,
        )

    def test_text_to_textnodes_only_link(self):
        text = "[bootdev](https://www.boot.dev)"

        nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode(
                    "bootdev",
                    TextType.LINK,
                    "https://www.boot.dev",
                )
            ],
            nodes,
        )

    def test_text_to_textnodes_mixed_no_spacing(self):
        text = "**bold**_italic_`code`"

        nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode("code", TextType.CODE),
            ],
            nodes,
        )


if __name__ == "__main__":
    unittest.main()
