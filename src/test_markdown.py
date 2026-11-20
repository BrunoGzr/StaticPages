import unittest

from markdown import extract_title, markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):
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

    def test_headings(self):
        md = "# Heading 1\n\n## Heading **2**\n\n###### Heading 6"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><h1>Heading 1</h1><h2>Heading <b>2</b></h2><h6>Heading 6</h6></div>",
        )

    def test_quote(self):
        md = "> This is a quote\n> with **bold** text"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>This is a quote with <b>bold</b> text</blockquote></div>",
        )

    def test_quote_without_space_after_gt(self):
        md = ">no space here"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>no space here</blockquote></div>",
        )

    def test_unordered_list(self):
        md = "- first item\n- second **item**\n- third item"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>first item</li><li>second <b>item</b></li><li>third item</li></ul></div>",
        )

    def test_ordered_list(self):
        md = "1. first item\n2. second _item_\n3. third item"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>first item</li><li>second <i>item</i></li><li>third item</li></ol></div>",
        )

    def test_multiple_block_types(self):
        md = """
# Heading

A paragraph with a [link](https://boot.dev).

- one
- two

1. first
2. second

> a quote

```
code
```
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><h1>Heading</h1>"
            '<p>A paragraph with a <a href="https://boot.dev">link</a>.</p>'
            "<ul><li>one</li><li>two</li></ul>"
            "<ol><li>first</li><li>second</li></ol>"
            "<blockquote>a quote</blockquote>"
            "<pre><code>code\n</code></pre></div>",
        )

    def test_empty_markdown(self):
        node = markdown_to_html_node("")
        self.assertEqual(node.to_html(), "<div></div>")


class TestExtractTitle(unittest.TestCase):
    def test_simple_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_title_with_whitespace(self):
        self.assertEqual(extract_title("#   Hello World   "), "Hello World")

    def test_ignores_other_headings(self):
        md = "## Not the title\n\n### Also not\n\n# The Title\n\n## After"
        self.assertEqual(extract_title(md), "The Title")

    def test_first_h1_is_used(self):
        md = "# First\n\n# Second"
        self.assertEqual(extract_title(md), "First")

    def test_no_h1_raises(self):
        with self.assertRaises(ValueError):
            extract_title("## Only an h2\n\nSome text")

    def test_hash_without_space_is_not_a_title(self):
        with self.assertRaises(ValueError):
            extract_title("#NoSpace")


if __name__ == "__main__":
    unittest.main()
