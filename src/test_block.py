import unittest

from block import BlockType, block_to_block_type, markdown_to_blocks


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

    def test_heading_paragraph_list(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_excessive_newlines_are_removed(self):
        md = "First block\n\n\n\nSecond block\n\n\nThird block"
        self.assertEqual(
            markdown_to_blocks(md),
            ["First block", "Second block", "Third block"],
        )

    def test_whitespace_only_blocks_are_removed(self):
        md = "First block\n\n   \n\nSecond block"
        self.assertEqual(
            markdown_to_blocks(md),
            ["First block", "Second block"],
        )

    def test_leading_and_trailing_whitespace_is_stripped(self):
        md = "\n\n   First block   \n\n   Second block   \n\n"
        self.assertEqual(
            markdown_to_blocks(md),
            ["First block", "Second block"],
        )

    def test_single_block(self):
        self.assertEqual(
            markdown_to_blocks("Just one block"),
            ["Just one block"],
        )

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_whitespace_only_string(self):
        self.assertEqual(markdown_to_blocks("   \n\n   "), [])


class TestBlockToBlockType(unittest.TestCase):
    def test_headings(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading"), BlockType.HEADING)

    def test_too_many_hashes_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("####### Heading"),
            BlockType.PARAGRAPH,
        )

    def test_heading_without_space_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("#Heading"),
            BlockType.PARAGRAPH,
        )

    def test_code_block(self):
        block = '```\nx = 1\nprint(x)\n```'
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_without_newline_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("```code```"),
            BlockType.PARAGRAPH,
        )

    def test_quote_block(self):
        self.assertEqual(block_to_block_type("> quoted text"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">no space"), BlockType.QUOTE)

    def test_multiline_quote_block(self):
        self.assertEqual(
            block_to_block_type("> first line\n> second line"),
            BlockType.QUOTE,
        )

    def test_quote_with_line_not_starting_with_quote_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("> first line\nsecond line"),
            BlockType.PARAGRAPH,
        )

    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- first\n- second\n- third"),
            BlockType.UNORDERED_LIST,
        )

    def test_unordered_list_without_space_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("-first\n-second"),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. first\n2. second\n3. third"),
            BlockType.ORDERED_LIST,
        )

    def test_ordered_list_starting_at_one_only(self):
        self.assertEqual(
            block_to_block_type("2. first\n3. second"),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_must_increment_by_one(self):
        self.assertEqual(
            block_to_block_type("1. first\n3. second"),
            BlockType.PARAGRAPH,
        )

    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("This is just a normal paragraph."),
            BlockType.PARAGRAPH,
        )


if __name__ == "__main__":
    unittest.main()
