import re

from src.text_node import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        # Only split TEXT nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        # If delimiter count is odd → invalid markdown
        if len(parts) % 2 == 0:
            raise Exception(f"Invalid markdown syntax: missing closing '{delimiter}'")

        for i, part in enumerate(parts):
            if part == "":
                continue

            if i % 2 == 0:
                # Even index → normal text
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # Odd index → delimited text
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def extract_markdown_images(text):
    """
    Extract markdown images of the form:
    ![alt text](url)

    Returns a list of (alt_text, url) tuples
    """
    pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    """
    Extract markdown links of the form:
    [anchor text](url)

    Returns a list of (anchor_text, url) tuples
    """
    # Negative lookbehind to ensure we don't match images
    pattern = r"(?<!\!)\[([^\]]*)\]\(([^)]+)\)"
    return re.findall(pattern, text)


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        # Only split TEXT nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)

        # No images → keep node as-is
        if not images:
            new_nodes.append(node)
            continue

        for alt, url in images:
            markdown = f"![{alt}]({url})"
            before, text = text.split(markdown, 1)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        # Only split TEXT nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)

        # No links → keep node as-is
        if not links:
            new_nodes.append(node)
            continue

        for link_text, url in links:
            markdown = f"[{link_text}]({url})"
            before, text = text.split(markdown, 1)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(link_text, TextType.LINK, url))

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    # Start with a single TEXT node
    nodes = [TextNode(text, TextType.TEXT)]

    # Split by inline markdown delimiters
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    # Split images and links last
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
