import unittest

from inline import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


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
        node = TextNode("This is **bold** text", TextType.TEXT)
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
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_multiple_sections(self):
        node = TextNode("`a` and `b`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("a", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("b", TextType.CODE),
            ],
        )

    def test_non_text_nodes_are_kept(self):
        nodes = [
            TextNode("plain", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("a link", TextType.LINK, "https://www.boot.dev"),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, nodes)

    def test_no_delimiter_in_text(self):
        node = TextNode("just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("just plain text", TextType.TEXT)])

    def test_unmatched_delimiter_raises(self):
        node = TextNode("This is `unclosed code", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_empty_text_returns_empty_list(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [])

    def test_split_only_delimited_text(self):
        node = TextNode("`code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("code", TextType.CODE)])


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], matches
        )

    def test_extract_multiple_images(self):
        text = (
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) "
            "and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual(
            [("to boot dev", "https://www.boot.dev")], matches
        )

    def test_extract_multiple_links(self):
        text = (
            "This is text with a link [to boot dev](https://www.boot.dev) "
            "and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            extract_markdown_links(text),
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_images_are_not_extracted_as_links(self):
        text = "![alt text](https://example.com/image.png)"
        self.assertListEqual(extract_markdown_links(text), [])
        self.assertListEqual(
            extract_markdown_images(text),
            [("alt text", "https://example.com/image.png")],
        )

    def test_extract_from_text_with_both(self):
        text = (
            "An image ![alt](https://example.com/img.png) and a "
            "link [anchor](https://example.com)"
        )
        self.assertListEqual(
            extract_markdown_images(text),
            [("alt", "https://example.com/img.png")],
        )
        self.assertListEqual(
            extract_markdown_links(text),
            [("anchor", "https://example.com")],
        )

    def test_no_matches(self):
        text = "This text has neither images nor links."
        self.assertListEqual(extract_markdown_images(text), [])
        self.assertListEqual(extract_markdown_links(text), [])


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
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

    def test_split_image_at_start(self):
        node = TextNode(
            "![image](https://example.com/img.png) trailing text",
            TextType.TEXT,
        )
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" trailing text", TextType.TEXT),
            ],
        )

    def test_split_image_at_end(self):
        node = TextNode(
            "leading text ![image](https://example.com/img.png)",
            TextType.TEXT,
        )
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("leading text ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            ],
        )

    def test_split_adjacent_images(self):
        node = TextNode(
            "![one](https://example.com/1.png)![two](https://example.com/2.png)",
            TextType.TEXT,
        )
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("one", TextType.IMAGE, "https://example.com/1.png"),
                TextNode("two", TextType.IMAGE, "https://example.com/2.png"),
            ],
        )

    def test_split_images_no_images(self):
        node = TextNode("just plain text", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [TextNode("just plain text", TextType.TEXT)],
        )

    def test_split_images_keeps_non_text_nodes(self):
        nodes = [
            TextNode("bold", TextType.BOLD),
            TextNode("![image](https://example.com/img.png)", TextType.TEXT),
        ]
        self.assertListEqual(
            split_nodes_image(nodes),
            [
                TextNode("bold", TextType.BOLD),
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            ],
        )

    def test_split_images_empty_text(self):
        self.assertListEqual(split_nodes_image([TextNode("", TextType.TEXT)]), [])

    def test_split_images_leaves_links_alone(self):
        node = TextNode("[link](https://example.com)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [TextNode("[link](https://example.com)", TextType.TEXT)],
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube",
                    TextType.LINK,
                    "https://www.youtube.com/@bootdotdev",
                ),
            ],
            new_nodes,
        )

    def test_split_link_at_start(self):
        node = TextNode("[anchor](https://example.com) trailing", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("anchor", TextType.LINK, "https://example.com"),
                TextNode(" trailing", TextType.TEXT),
            ],
        )

    def test_split_link_at_end(self):
        node = TextNode("leading [anchor](https://example.com)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("leading ", TextType.TEXT),
                TextNode("anchor", TextType.LINK, "https://example.com"),
            ],
        )

    def test_split_adjacent_links(self):
        node = TextNode(
            "[one](https://example.com/1)[two](https://example.com/2)",
            TextType.TEXT,
        )
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("one", TextType.LINK, "https://example.com/1"),
                TextNode("two", TextType.LINK, "https://example.com/2"),
            ],
        )

    def test_split_links_no_links(self):
        node = TextNode("just plain text", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [TextNode("just plain text", TextType.TEXT)],
        )

    def test_split_links_keeps_non_text_nodes(self):
        nodes = [
            TextNode("italic", TextType.ITALIC),
            TextNode("[link](https://example.com)", TextType.TEXT),
        ]
        self.assertListEqual(
            split_nodes_link(nodes),
            [
                TextNode("italic", TextType.ITALIC),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
        )

    def test_split_links_empty_text(self):
        self.assertListEqual(split_nodes_link([TextNode("", TextType.TEXT)]), [])

    def test_split_links_ignores_images(self):
        node = TextNode(
            "![image](https://example.com/img.png) and [link](https://example.com)",
            TextType.TEXT,
        )
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode(
                    "![image](https://example.com/img.png) and ",
                    TextType.TEXT,
                ),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_full_example(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and "
            "an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
            "[link](https://boot.dev)"
        )
        self.assertListEqual(
            text_to_textnodes(text),
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
        )

    def test_plain_text(self):
        self.assertListEqual(
            text_to_textnodes("just plain text"),
            [TextNode("just plain text", TextType.TEXT)],
        )

    def test_only_bold(self):
        self.assertListEqual(
            text_to_textnodes("**bold**"),
            [TextNode("bold", TextType.BOLD)],
        )

    def test_only_image(self):
        self.assertListEqual(
            text_to_textnodes("![alt](https://example.com/img.png)"),
            [TextNode("alt", TextType.IMAGE, "https://example.com/img.png")],
        )

    def test_only_link(self):
        self.assertListEqual(
            text_to_textnodes("[anchor](https://example.com)"),
            [TextNode("anchor", TextType.LINK, "https://example.com")],
        )

    def test_multiple_same_type(self):
        self.assertListEqual(
            text_to_textnodes("**one** and **two**"),
            [
                TextNode("one", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
            ],
        )


if __name__ == "__main__":
    unittest.main()
