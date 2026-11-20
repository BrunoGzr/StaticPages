from block import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import LeafNode, ParentNode
from inline import text_to_textnodes
from textnode import text_node_to_html_node


def text_to_children(text: str) -> list[LeafNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]


def code_block_to_html_node(block: str) -> ParentNode:
    code_text = block[4:-3]
    code_node = ParentNode("code", [LeafNode(None, code_text)])
    return ParentNode("pre", [code_node])


def quote_block_to_text(block: str) -> str:
    lines = []
    for line in block.split("\n"):
        line = line.removeprefix(">").removeprefix(" ")
        lines.append(line)
    return " ".join(lines)


def list_items_to_html_nodes(block: str, prefix_length: int) -> list[ParentNode]:
    items = []
    for line in block.split("\n"):
        item_text = line[prefix_length:]
        items.append(ParentNode("li", text_to_children(item_text)))
    return items


def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        paragraph = " ".join(block.split("\n"))
        return ParentNode("p", text_to_children(paragraph))

    if block_type == BlockType.HEADING:
        level = len(block.split(" ", 1)[0])
        return ParentNode(f"h{level}", text_to_children(block[level + 1 :]))

    if block_type == BlockType.CODE:
        return code_block_to_html_node(block)

    if block_type == BlockType.QUOTE:
        return ParentNode("blockquote", text_to_children(quote_block_to_text(block)))

    if block_type == BlockType.UNORDERED_LIST:
        return ParentNode("ul", list_items_to_html_nodes(block, 2))

    if block_type == BlockType.ORDERED_LIST:
        return ParentNode("ol", list_items_to_html_nodes(block, 3))

    raise ValueError(f"unknown block type: {block_type}")


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)


def extract_title(markdown: str) -> str:
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("markdown has no h1 heading")
