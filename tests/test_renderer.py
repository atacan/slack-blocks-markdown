"""
Tests for SlackBlocksRenderer functionality
"""

import pytest
from mistletoe import Document
from slack_sdk.models.blocks import DividerBlock, HeaderBlock, SectionBlock


class TestBasicRendering:
    """Test basic markdown element rendering"""

    def test_heading_renders_to_header_block(self, renderer):
        """Test that headings become HeaderBlocks"""
        markdown = "# Test Heading"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], HeaderBlock)
        assert blocks[0].text.text == "Test Heading"

    def test_heading_with_bold_strips_formatting(self, renderer):
        """Test that bold formatting in headings is stripped (plain text only)"""
        markdown = "### **Chapter 5**"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], HeaderBlock)
        # Should be plain text without asterisks
        assert blocks[0].text.text == "Chapter 5"
        assert "*" not in blocks[0].text.text

    def test_heading_with_italic_strips_formatting(self, renderer):
        """Test that italic formatting in headings is stripped"""
        markdown = "## _Important Section_"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], HeaderBlock)
        assert blocks[0].text.text == "Important Section"
        assert "_" not in blocks[0].text.text

    def test_heading_with_inline_code_strips_formatting(self, renderer):
        """Test that inline code in headings is stripped"""
        markdown = "# Working with `config.json`"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], HeaderBlock)
        assert blocks[0].text.text == "Working with config.json"
        assert "`" not in blocks[0].text.text

    def test_heading_with_mixed_formatting(self, renderer):
        """Test that mixed formatting in headings is all stripped"""
        markdown = "## **Bold** and _italic_ with `code`"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], HeaderBlock)
        assert blocks[0].text.text == "Bold and italic with code"
        assert "*" not in blocks[0].text.text
        assert "_" not in blocks[0].text.text
        assert "`" not in blocks[0].text.text

    def test_paragraph_renders_to_section_block(self, renderer):
        """Test that paragraphs become SectionBlocks"""
        markdown = "This is a paragraph with **bold** text."
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], SectionBlock)
        assert blocks[0].text.text == "This is a paragraph with *bold* text."

    def test_horizontal_rule_renders_to_divider(self, renderer):
        """Test that horizontal rules become DividerBlocks"""
        markdown = "---"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], DividerBlock)


class TestInlineFormatting:
    """Test inline markdown formatting"""

    @pytest.mark.parametrize(
        ("markdown", "expected"),
        [
            ("**bold**", "*bold*"),
            ("_italic_", "_italic_"),
            ("`code`", "`code`"),
            ("~strikethrough~", "~strikethrough~"),
            ("[link](https://example.com)", "<https://example.com|link>"),
        ],
    )
    def test_inline_formatting(self, renderer, markdown, expected):
        """Test various inline formatting conversions"""
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert blocks[0].text.text == expected


class TestLists:
    """Test list rendering functionality"""

    def test_unordered_list_rendering(self, renderer):
        """Test unordered list conversion"""
        markdown = "- Item 1\n- Item 2\n- Item 3"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], SectionBlock)
        assert "• Item 1" in blocks[0].text.text
        assert "• Item 2" in blocks[0].text.text
        assert "• Item 3" in blocks[0].text.text

    def test_ordered_list_rendering(self, renderer):
        """Test ordered list conversion"""
        markdown = "1. First\n2. Second\n3. Third"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], SectionBlock)
        assert "1. First" in blocks[0].text.text
        assert "2. Second" in blocks[0].text.text
        assert "3. Third" in blocks[0].text.text


class TestCodeBlocks:
    """Test code block handling"""

    def test_code_block_rendering(self, renderer):
        """Test code block formatting"""
        markdown = "```python\ndef hello():\n    return 'world'\n```"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], SectionBlock)
        assert blocks[0].text.text.startswith("```")
        assert "def hello():" in blocks[0].text.text
        assert blocks[0].text.text.endswith("```")


class TestBlockquotes:
    """Test blockquote rendering"""

    def test_simple_blockquote(self, renderer):
        """Test basic blockquote formatting"""
        markdown = "> This is a quote"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], SectionBlock)
        assert blocks[0].text.text.startswith(">This is a quote")

    def test_multiline_blockquote(self, renderer):
        """Test multiline blockquote handling"""
        markdown = "> First line\n>\n> Second paragraph"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        text = blocks[0].text.text
        assert ">First line" in text
        assert ">Second paragraph" in text


class TestTables:
    """Test table rendering functionality"""

    def test_simple_table_rendering(self, renderer):
        """Test basic table conversion to TableBlock"""
        markdown = """| Name | Value |
|------|--------|
| Test | 123 |
| Demo | 456 |"""

        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        # Should be our custom TableBlock
        assert blocks[0].type == "table"
        assert len(blocks[0].rows) == 3  # Header + 2 data rows

    def test_table_with_bold_text_strips_formatting(self, renderer):
        """Test that bold formatting in table cells is stripped (raw_text only)"""
        markdown = """| Name | Status |
|------|--------|
| **Important** | Done |
| Task | **Complete** |"""

        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert blocks[0].type == "table"

        # Check header row (first row)
        header_row = blocks[0].rows[0]
        assert header_row[0]["text"] == "Name"
        assert header_row[1]["text"] == "Status"

        # Check data rows - should not have asterisks
        row1 = blocks[0].rows[1]
        assert row1[0]["text"] == "Important"
        assert "*" not in row1[0]["text"]
        assert row1[1]["text"] == "Done"

        row2 = blocks[0].rows[2]
        assert row2[0]["text"] == "Task"
        assert row2[1]["text"] == "Complete"
        assert "*" not in row2[1]["text"]

    def test_table_with_italic_text_strips_formatting(self, renderer):
        """Test that italic formatting in table cells is stripped"""
        markdown = """| Item | _Priority_ |
|------|------------|
| Fix | _High_ |"""

        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        header_row = blocks[0].rows[0]
        assert header_row[1]["text"] == "Priority"
        assert "_" not in header_row[1]["text"]

        row1 = blocks[0].rows[1]
        assert row1[1]["text"] == "High"
        assert "_" not in row1[1]["text"]

    def test_table_with_code_text_strips_formatting(self, renderer):
        """Test that inline code in table cells is stripped"""
        markdown = """| Config | Value |
|--------|-------|
| `debug` | true |"""

        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        row1 = blocks[0].rows[1]
        assert row1[0]["text"] == "debug"
        assert "`" not in row1[0]["text"]

    def test_table_with_mixed_formatting(self, renderer):
        """Test that mixed formatting in table cells is all stripped"""
        markdown = """| Feature | Status |
|---------|--------|
| **Auth** with `API` | _Ready_ |"""

        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        row1 = blocks[0].rows[1]
        assert row1[0]["text"] == "Auth with API"
        assert "*" not in row1[0]["text"]
        assert "`" not in row1[0]["text"]
        assert row1[1]["text"] == "Ready"
        assert "_" not in row1[1]["text"]


class TestConstraints:
    """Test Slack Block Kit constraint handling"""

    def test_long_heading_truncation(self, renderer):
        """Test that long headings are truncated to 150 chars"""
        long_title = "A" * 200
        markdown = f"# {long_title}"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert len(blocks[0].text.text) <= 150
        assert blocks[0].text.text.endswith("...")

    def test_long_paragraph_truncation(self, renderer):
        """Test that long paragraphs are truncated to 3000 chars"""
        long_text = "This is a very long paragraph. " * 200
        document = Document(long_text)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert len(blocks[0].text.text) <= 3000
        assert blocks[0].text.text.endswith("...")


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_empty_document(self, renderer):
        """Test handling of empty markdown"""
        markdown = ""
        document = Document(markdown)
        blocks = renderer.render(document)

        assert blocks == []

    def test_whitespace_only(self, renderer):
        """Test handling of whitespace-only content"""
        markdown = (
            "   \n\n   \n"  # Just spaces, no tabs (which would create code block)
        )
        document = Document(markdown)
        blocks = renderer.render(document)

        assert blocks == []

    def test_mixed_complex_content(self, renderer):
        """Test complex mixed content document"""
        markdown = """# Main Title

This paragraph has **bold**, _italic_, and `code` formatting.

## Subsection

- First item with [link](https://example.com)
- Second item with *emphasis*

```javascript
console.log('hello world');
```

> Important note about the code above

| Feature | Status | Notes |
|---------|--------|-------|
| Auth | Done | Ready |
| API | Progress | Testing |

---

Final paragraph after divider.
"""

        document = Document(markdown)
        blocks = renderer.render(document)

        # Should generate multiple blocks of different types
        assert len(blocks) > 5

        # Check we have different block types
        block_types = [block.type for block in blocks]
        assert "header" in block_types
        assert "section" in block_types
        assert "divider" in block_types
        assert "table" in block_types
