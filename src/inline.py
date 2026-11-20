import re

from textnode import TextNode, TextType

IMAGE_PATTERN = re.compile(r"!\[([^\[\]]*)\]\(([^()]*)\)")
LINK_PATTERN = re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^()]*)\)")


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return IMAGE_PATTERN.findall(text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return LINK_PATTERN.findall(text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_by_pattern(old_nodes, IMAGE_PATTERN, TextType.IMAGE)


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_by_pattern(old_nodes, LINK_PATTERN, TextType.LINK)


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def _split_nodes_by_pattern(
    old_nodes: list[TextNode],
    pattern: re.Pattern[str],
    text_type: TextType,
) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        last_index = 0
        for match in pattern.finditer(text):
            before = text[last_index : match.start()]
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            label, url = match.group(1), match.group(2)
            new_nodes.append(TextNode(label, text_type, url))
            last_index = match.end()

        remaining = text[last_index:]
        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType,
) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        parts = old_node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(
                f"invalid markdown: missing closing delimiter {delimiter!r} "
                f"in {old_node.text!r}"
            )

        for i, part in enumerate(parts):
            if part == "":
                continue
            node_type = text_type if i % 2 == 1 else TextType.TEXT
            new_nodes.append(TextNode(part, node_type))

    return new_nodes
