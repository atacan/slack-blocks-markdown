"""
Slack Blocks Renderer for Mistletoe

This module provides a custom renderer that converts Markdown to Slack Block Kit blocks.
"""

from typing import Any, cast

from mistletoe import block_token, span_token  # type: ignore[import-untyped]
from mistletoe.base_renderer import BaseRenderer  # type: ignore[import-untyped]
from slack_sdk.models.blocks import (
    Block,
    DividerBlock,
    HeaderBlock,
    MarkdownTextObject,
    PlainTextObject,
    SectionBlock,
)

from .blocks import TableBlock


class SlackBlocksRenderer(BaseRenderer):
    """
    Renderer that converts Markdown to Slack Block Kit blocks.

    Returns a list of Block objects that can be used with Slack's messaging APIs.
    """

    def __init__(self, *extras: type[Any], expand_sections: bool | None = None) -> None:
        """
        Initialize the Slack blocks renderer.

        Args:
            extras: Additional custom tokens to add to the parsing process
            expand_sections: Whether to expand all section blocks by default.
                If True, section blocks will always be fully expanded.
                If False, Slack may show "Show more" button for long content.
                If None (default), uses Slack's default behavior.
        """
        super().__init__(*extras)
        self.blocks: list[Block] = []
        self.current_text_parts: list[str] = []
        self.expand_sections = expand_sections

    def _extract_plain_text(self, token: Any) -> str:
        """
        Extract plain text from a token without any markdown formatting.

        This is used for contexts where only plain text is allowed (e.g., HeaderBlock).

        Args:
            token: The token to extract text from

        Returns:
            Plain text string without markdown formatting
        """
        # Handle raw text directly
        if isinstance(token, span_token.RawText):
            return str(token.content)

        # For formatting tokens (bold, italic, code, etc.), extract inner text
        if isinstance(
            token,
            span_token.Strong
            | span_token.Emphasis
            | span_token.Strikethrough
            | span_token.InlineCode,
        ):
            return self._extract_plain_text_from_children(token)

        # For links, extract the link text
        if isinstance(token, span_token.Link | span_token.AutoLink):
            if hasattr(token, "children") and token.children:
                return self._extract_plain_text_from_children(token)
            # For autolinks, return the URL
            return getattr(token, "target", "")

        # For images, return alt text or empty string
        if isinstance(token, span_token.Image):
            if hasattr(token, "children") and token.children:
                return self._extract_plain_text_from_children(token)
            return ""

        # For escape sequences, extract content
        if isinstance(token, span_token.EscapeSequence):
            return self._extract_plain_text_from_children(token)

        # For line breaks, return space
        if isinstance(token, span_token.LineBreak):
            return " " if token.soft else " "

        # Default: try to extract from children
        if hasattr(token, "children") and token.children:
            return self._extract_plain_text_from_children(token)

        return ""

    def _extract_plain_text_from_children(self, token: Any) -> str:
        """
        Extract plain text from all children of a token.

        Args:
            token: The token whose children to process

        Returns:
            Combined plain text from all children
        """
        parts = []
        if hasattr(token, "children") and token.children:
            for child in token.children:
                parts.append(self._extract_plain_text(child))
        return "".join(parts)

    def render_document(self, token: block_token.Document) -> list[Block]:  # type: ignore[override]
        """
        Render the entire document and return the list of blocks.

        Args:
            token: The document token

        Returns:
            List of Slack Block objects
        """
        self.blocks = []
        self.render_inner(token)
        return self.blocks

    def render_heading(self, token: block_token.Heading) -> str:
        """
        Render heading as HeaderBlock.

        HeaderBlock is limited to 150 characters and only supports plain text.
        Markdown formatting is stripped since HeaderBlock doesn't support it.
        """
        # Extract plain text without markdown formatting
        text_content = self._extract_plain_text_from_children(token).strip()
        # Truncate if too long
        if len(text_content) > 150:
            text_content = text_content[:147] + "..."

        header_block = HeaderBlock(
            text=PlainTextObject(text=text_content),
        )
        self.blocks.append(header_block)
        return ""

    def render_paragraph(self, token: block_token.Paragraph) -> str:
        """
        Render paragraph as SectionBlock with MarkdownTextObject.
        """
        text_content = self.render_inner(token).strip()
        if text_content:
            # Truncate if too long (3000 char limit)
            if len(text_content) > 3000:
                text_content = text_content[:2997] + "..."

            section_block = SectionBlock(
                text=MarkdownTextObject(text=text_content),
                expand=self.expand_sections,
            )
            self.blocks.append(section_block)
        return ""

    def render_block_code(self, token: block_token.BlockCode) -> str:
        """
        Render code block as SectionBlock with preformatted text.
        """
        children_list = list(token.children) if token.children else []
        code_content = getattr(children_list[0], "content", "") if children_list else ""

        # Format as code block in Slack markdown
        formatted_code = f"```\n{code_content}\n```"

        # Truncate if too long
        if len(formatted_code) > 3000:
            formatted_code = formatted_code[:2997] + "..."

        section_block = SectionBlock(
            text=MarkdownTextObject(text=formatted_code),
            expand=self.expand_sections,
        )
        self.blocks.append(section_block)
        return ""

    def render_quote(self, token: block_token.Quote) -> str:
        """
        Render blockquote as SectionBlock with quote formatting.
        """
        # Collect content from all paragraphs within the quote
        quote_parts = []
        if token.children:
            for child in token.children:
                if hasattr(child, "children") and child.children:
                    # This is typically a Paragraph, extract its content
                    content_parts = []
                    for subchild in child.children:
                        content_parts.append(cast(str, self.render(subchild)))
                    paragraph_content = "".join(content_parts).strip()
                    if paragraph_content:
                        quote_parts.append(paragraph_content)

        if quote_parts:
            # Format each part as a quote line with > prefix
            # When there are multiple paragraphs, insert empty quote line between them
            formatted_parts = []
            for i, part in enumerate(quote_parts):
                formatted_parts.append(f">{part}")
                # Add empty quote line between paragraphs (except after the last one)
                if i < len(quote_parts) - 1:
                    formatted_parts.append(">")
            formatted_quote = "\n".join(formatted_parts)

            # Truncate if too long
            if len(formatted_quote) > 3000:
                formatted_quote = formatted_quote[:2997] + "..."

            section_block = SectionBlock(
                text=MarkdownTextObject(text=formatted_quote),
                expand=self.expand_sections,
            )
            self.blocks.append(section_block)
        return ""

    def render_list(self, token: block_token.List) -> str:
        """
        Render list as SectionBlock with formatted list items.
        """
        list_items = []

        # Collect all list items
        if token.children:
            for i, child in enumerate(token.children):
                item_content = self.render_list_item(
                    cast(block_token.ListItem, child),
                ).strip()
                if item_content:
                    # Check if this is an ordered list with a start attribute
                    if hasattr(token, "start") and token.start is not None:
                        # Ordered list
                        start_num = int(str(token.start))
                        list_items.append(f"{i + start_num}. {item_content}")
                    else:
                        # Unordered list
                        list_items.append(f"• {item_content}")

        # Create a single block with all list items
        if list_items:
            list_text = "\n".join(list_items)

            # Truncate if too long
            if len(list_text) > 3000:
                list_text = list_text[:2997] + "..."

            section_block = SectionBlock(
                text=MarkdownTextObject(text=list_text),
                expand=self.expand_sections,
            )
            self.blocks.append(section_block)

        return ""

    def render_list_item(self, token: block_token.ListItem) -> str:
        """
        Render list item content (used by render_list).
        This extracts the text content without creating a new block.
        """
        # List items usually contain a paragraph, get its text content
        content_parts = []
        if token.children:
            for child in token.children:
                if hasattr(child, "children") and child.children:
                    # This is typically a Paragraph, extract its text
                    for subchild in child.children:
                        content_parts.append(cast(str, self.render(subchild)))
                else:
                    content_parts.append(cast(str, self.render(child)))
        return "".join(content_parts)

    def render_thematic_break(self, token: block_token.ThematicBreak) -> str:
        """
        Render horizontal rule as DividerBlock.
        """
        divider_block = DividerBlock()
        self.blocks.append(divider_block)
        return ""

    def render_table(self, token: block_token.Table) -> str:
        """
        Render table as TableBlock with proper cell structure.
        """
        rows = []

        # Render header if present
        if hasattr(token, "header") and token.header:
            header_row = self._render_table_row_as_cells(
                cast(block_token.TableRow, token.header),
            )
            rows.append(header_row)

        # Render body rows
        if token.children:
            for row in token.children:
                body_row = self._render_table_row_as_cells(
                    cast(block_token.TableRow, row),
                )
                rows.append(body_row)

        if rows:
            # Ensure we don't exceed limits
            if len(rows) > 100:
                rows = rows[:100]

            table_block = TableBlock(rows=rows)
            self.blocks.append(table_block)
        return ""

    def _render_table_row_as_cells(
        self,
        token: block_token.TableRow,
    ) -> list[dict[str, Any]]:
        """
        Render a table row as a list of cell objects for TableBlock.

        Returns:
            List of cell objects with type and content
        """
        cells: list[dict[str, Any]] = []
        if token.children:
            for cell in token.children:
                cell_content = self.render_table_cell(cast(block_token.TableCell, cell))
                # Limit to 20 columns
                if len(cells) >= 20:
                    break
                cells.append(
                    {
                        "type": "raw_text",
                        "text": cell_content or " ",
                    },
                )
        return cells

    def render_table_row(
        self,
        token: block_token.TableRow,
        is_header: bool = False,
    ) -> str:
        """
        Render a table row.
        """
        cells = []
        if token.children:
            for cell in token.children:
                cell_content = self.render_table_cell(cast(block_token.TableCell, cell))
                cells.append(cell_content or " ")

        if is_header:
            return f"*{' | '.join(cells)}*"
        return " | ".join(cells)

    def render_table_cell(self, token: block_token.TableCell) -> str:
        """
        Render a table cell.

        Table cells use raw_text type which doesn't support markdown formatting,
        so we strip all formatting to display plain text only.
        """
        return self._extract_plain_text_from_children(token).strip()

    # Inline element renderers - these return formatted text

    def render_strong(self, token: span_token.Strong) -> str:
        """
        Render bold text with Slack markdown formatting.
        """
        content = self.render_inner(token)
        return f"*{content}*"

    def render_emphasis(self, token: span_token.Emphasis) -> str:
        """
        Render italic text with Slack markdown formatting.
        """
        content = self.render_inner(token)
        return f"_{content}_"

    def render_strikethrough(self, token: span_token.Strikethrough) -> str:
        """
        Render strikethrough text with Slack markdown formatting.
        """
        content = self.render_inner(token)
        return f"~{content}~"

    def render_inline_code(self, token: span_token.InlineCode) -> str:
        """
        Render inline code with Slack markdown formatting.
        """
        content = self.render_inner(token)
        return f"`{content}`"

    def render_link(self, token: span_token.Link) -> str:
        """
        Render link with Slack markdown formatting.
        """
        url = token.target
        text = self.render_inner(token)

        if text and text != url:
            return f"<{url}|{text}>"
        return f"<{url}>"

    def render_auto_link(self, token: span_token.AutoLink) -> str:
        """
        Render auto link with Slack markdown formatting.
        """
        return f"<{token.target}>"

    def render_image(self, token: span_token.Image) -> str:
        """
        Render image as a link (Slack blocks don't support inline images in text).
        """
        alt_text = self.render_inner(token)
        if alt_text:
            return f"<{token.src}|{alt_text}>"
        return f"<{token.src}>"

    def render_line_break(self, token: span_token.LineBreak) -> str:
        """
        Render line break.
        """
        return "\n" if token.soft else "\n\n"

    def render_raw_text(self, token: span_token.RawText) -> str:
        """
        Render raw text content.
        """
        return token.content  # type: ignore[no-any-return]

    def render_escape_sequence(self, token: span_token.EscapeSequence) -> str:
        """
        Render escaped characters.
        """
        return self.render_inner(token)  # type: ignore[no-any-return]

    def render(self, token: Any) -> list[Block] | str:
        """
        Override the base render method to handle our custom return type.
        """
        if token.__class__.__name__ == "Document":
            return self.render_document(token)
        return super().render(token)  # type: ignore[no-any-return]
