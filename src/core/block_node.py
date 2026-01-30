from enum import Enum

from src.core.html_node import LeafNode, ParentNode
from src.core.markdown_node import text_to_textnodes
from src.core.text_node import TextNode, TextType, text_node_to_html_node


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def heading_level(block):
    count = 0
    for char in block:
        if char == "#":
            count += 1
        else:
            break
    return count if 1 <= count <= 6 else None


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    lines = block.split("\n")

    # ---- HEADING ----
    if block.startswith("#"):
        level = heading_level(block)

        if level is not None and block[level : level + 1] == " ":
            return BlockType.HEADING

    # ---- CODE BLOCK ----
    if len(lines) >= 2 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    # ---- QUOTE BLOCK ----
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # ---- UNORDERED LIST ----
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # ---- ORDERED LIST ----
    if all(line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST

    # ---- PARAGRAPH ----
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    # Split on double newlines
    raw_blocks = markdown.split("\n\n")

    blocks = []
    for block in raw_blocks:
        stripped = block.strip()
        if stripped:
            blocks.append(stripped)

    return blocks


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        # ---- PARAGRAPH ----
        if block_type == BlockType.PARAGRAPH:
            # Paragraphs collapse internal newlines into spaces
            text = block.replace("\n", " ")
            children.append(ParentNode("p", text_to_children(text)))

        # ---- HEADING ----
        elif block_type == BlockType.HEADING:
            level = heading_level(block)
            assert level is not None
            content = block[level + 1 :]
            children.append(
                ParentNode(
                    f"h{level}",
                    text_to_children(content),
                )
            )
        # ---- CODE BLOCK ----
        elif block_type == BlockType.CODE:
            # Remove opening and closing ```
            code_text = "\n".join(block.split("\n")[1:-1]) + "\n"
            code_node = text_node_to_html_node(TextNode(code_text, TextType.CODE))
            children.append(ParentNode("pre", [code_node]))

        # ---- QUOTE ----
        elif block_type == BlockType.QUOTE:
            text = "\n".join(line[2:] for line in block.split("\n"))
            children.append(ParentNode("blockquote", [LeafNode(None, text)]))

        # ---- UNORDERED LIST ----
        elif block_type == BlockType.UNORDERED_LIST:
            items = []
            for line in block.split("\n"):
                item_text = line[2:]
                items.append(ParentNode("li", text_to_children(item_text)))
            children.append(ParentNode("ul", items))

        # ---- ORDERED LIST ----
        elif block_type == BlockType.ORDERED_LIST:
            items = []
            for line in block.split("\n"):
                item_text = line.split(". ", 1)[1]
                items.append(ParentNode("li", text_to_children(item_text)))
            children.append(ParentNode("ol", items))

    return ParentNode("div", children)
