"""
Slack Blocks Renderer for Mistletoe

This module provides a custom renderer that converts Markdown to Slack Block Kit blocks.
The renderer inherits from mistletoe's BaseRenderer and outputs a list of Block objects
that can be used with the Slack SDK.
"""

from typing import List, Any, Optional, Dict
from mistletoe.base_renderer import BaseRenderer
from slack_sdk.models.blocks import (
    Block, SectionBlock, HeaderBlock, DividerBlock, 
    MarkdownTextObject, PlainTextObject
)


class TableBlock(Block):
    """
    Custom Table Block implementation for Slack Block Kit.
    
    Since the Slack SDK doesn't include TableBlock, this implements it
    according to the official Slack documentation.
    """
    
    def __init__(self, rows: List[List[Dict[str, Any]]], block_id: Optional[str] = None, 
                 column_settings: Optional[List[Dict[str, Any]]] = None):
        """
        Initialize a Table block.
        
        Args:
            rows: List of rows, where each row is a list of cell objects
            block_id: Optional unique identifier for the block (max 255 chars)
            column_settings: Optional list of column configuration objects
        """
        # Initialize parent Block with correct parameters
        super().__init__(type="table", block_id=block_id)
        
        # Validate constraints
        if len(rows) > 100:
            raise ValueError("Table cannot have more than 100 rows")
        
        for i, row in enumerate(rows):
            if len(row) > 20:
                raise ValueError(f"Row {i} cannot have more than 20 columns")
        
        if block_id and len(block_id) > 255:
            raise ValueError("block_id cannot be longer than 255 characters")
        
        self.rows = rows
        self.column_settings = column_settings
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the TableBlock to a dictionary for JSON serialization.
        """
        result = {
            "type": self.type,
            "rows": self.rows
        }
        
        if self.block_id:
            result["block_id"] = self.block_id
            
        if self.column_settings:
            result["column_settings"] = self.column_settings
            
        return result


class SlackBlocksRenderer(BaseRenderer):
    """
    Renderer that converts Markdown to Slack Block Kit blocks.
    
    Returns a list of Block objects that can be used with Slack's messaging APIs.
    """
    
    def __init__(self, *extras):
        """
        Initialize the Slack blocks renderer.
        
        Args:
            extras: Additional custom tokens to add to the parsing process
        """
        super().__init__(*extras)
        self.blocks: List[Block] = []
        self.current_text_parts: List[str] = []
    
    def render_document(self, token) -> List[Block]:
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
    
    def render_heading(self, token) -> str:
        """
        Render heading as HeaderBlock.
        
        HeaderBlock is limited to 150 characters and only supports plain text.
        """
        text_content = self.render_inner(token).strip()
        # Truncate if too long
        if len(text_content) > 150:
            text_content = text_content[:147] + "..."
        
        header_block = HeaderBlock(
            text=PlainTextObject(text=text_content)
        )
        self.blocks.append(header_block)
        return ""
    
    def render_paragraph(self, token) -> str:
        """
        Render paragraph as SectionBlock with MarkdownTextObject.
        """
        text_content = self.render_inner(token).strip()
        if text_content:
            # Truncate if too long (3000 char limit)
            if len(text_content) > 3000:
                text_content = text_content[:2997] + "..."
            
            section_block = SectionBlock(
                text=MarkdownTextObject(text=text_content)
            )
            self.blocks.append(section_block)
        return ""
    
    def render_block_code(self, token) -> str:
        """
        Render code block as SectionBlock with preformatted text.
        """
        code_content = token.children[0].content if token.children else ""
        
        # Format as code block in Slack markdown
        formatted_code = f"```\n{code_content}\n```"
        
        # Truncate if too long
        if len(formatted_code) > 3000:
            formatted_code = formatted_code[:2997] + "..."
        
        section_block = SectionBlock(
            text=MarkdownTextObject(text=formatted_code)
        )
        self.blocks.append(section_block)
        return ""
    
    def render_quote(self, token) -> str:
        """
        Render blockquote as SectionBlock with quote formatting.
        """
        # Collect content from all paragraphs within the quote
        quote_parts = []
        for child in token.children:
            if hasattr(child, 'children'):
                # This is typically a Paragraph, extract its content
                content_parts = []
                for subchild in child.children:
                    content_parts.append(self.render(subchild))
                paragraph_content = ''.join(content_parts).strip()
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
            formatted_quote = '\n'.join(formatted_parts)
            
            # Truncate if too long
            if len(formatted_quote) > 3000:
                formatted_quote = formatted_quote[:2997] + "..."
            
            section_block = SectionBlock(
                text=MarkdownTextObject(text=formatted_quote)
            )
            self.blocks.append(section_block)
        return ""
    
    def render_list(self, token) -> str:
        """
        Render list as SectionBlock with formatted list items.
        """
        list_items = []
        
        # Collect all list items
        for i, child in enumerate(token.children):
            item_content = self.render_list_item(child).strip()
            if item_content:
                if hasattr(token, 'start') and token.start is not None:
                    # Ordered list
                    list_items.append(f"{i + token.start}. {item_content}")
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
                text=MarkdownTextObject(text=list_text)
            )
            self.blocks.append(section_block)
        
        return ""
    
    def render_list_item(self, token) -> str:
        """
        Render list item content (used by render_list).
        This extracts the text content without creating a new block.
        """
        # List items usually contain a paragraph, get its text content
        content_parts = []
        for child in token.children:
            if hasattr(child, 'children'):
                # This is typically a Paragraph, extract its text
                for subchild in child.children:
                    content_parts.append(self.render(subchild))
            else:
                content_parts.append(self.render(child))
        return ''.join(content_parts)
    
    def render_thematic_break(self, token) -> str:
        """
        Render horizontal rule as DividerBlock.
        """
        divider_block = DividerBlock()
        self.blocks.append(divider_block)
        return ""
    
    def render_table(self, token) -> str:
        """
        Render table as TableBlock with proper cell structure.
        """
        rows = []
        
        # Render header if present
        if hasattr(token, 'header') and token.header:
            header_row = self._render_table_row_as_cells(token.header)
            rows.append(header_row)
        
        # Render body rows
        for row in token.children:
            body_row = self._render_table_row_as_cells(row)
            rows.append(body_row)
        
        if rows:
            # Ensure we don't exceed limits
            if len(rows) > 100:
                rows = rows[:100]
            
            table_block = TableBlock(rows=rows)
            self.blocks.append(table_block)
        return ""
    
    def _render_table_row_as_cells(self, token) -> List[Dict[str, Any]]:
        """
        Render a table row as a list of cell objects for TableBlock.
        
        Returns:
            List of cell objects with type and content
        """
        cells = []
        for cell in token.children:
            cell_content = self.render_table_cell(cell)
            # Limit to 20 columns
            if len(cells) >= 20:
                break
            cells.append({
                "type": "raw_text",
                "text": cell_content or " "
            })
        return cells
    
    def render_table_row(self, token, is_header=False) -> str:
        """
        Render a table row.
        """
        cells = []
        for cell in token.children:
            cell_content = self.render_table_cell(cell)
            cells.append(cell_content or " ")
        
        if is_header:
            return f"*{' | '.join(cells)}*"
        else:
            return " | ".join(cells)
    
    def render_table_cell(self, token) -> str:
        """
        Render a table cell.
        """
        return self.render_inner(token).strip()
    
    # Inline element renderers - these return formatted text
    
    def render_strong(self, token) -> str:
        """
        Render bold text with Slack markdown formatting.
        """
        content = self.render_inner(token)
        return f"*{content}*"
    
    def render_emphasis(self, token) -> str:
        """
        Render italic text with Slack markdown formatting.
        """
        content = self.render_inner(token)
        return f"_{content}_"
    
    def render_strikethrough(self, token) -> str:
        """
        Render strikethrough text with Slack markdown formatting.
        """
        content = self.render_inner(token)
        return f"~{content}~"
    
    def render_inline_code(self, token) -> str:
        """
        Render inline code with Slack markdown formatting.
        """
        content = self.render_inner(token)
        return f"`{content}`"
    
    def render_link(self, token) -> str:
        """
        Render link with Slack markdown formatting.
        """
        url = token.target
        text = self.render_inner(token)
        
        if text and text != url:
            return f"<{url}|{text}>"
        else:
            return f"<{url}>"
    
    def render_auto_link(self, token) -> str:
        """
        Render auto link with Slack markdown formatting.
        """
        return f"<{token.target}>"
    
    def render_image(self, token) -> str:
        """
        Render image as a link (Slack blocks don't support inline images in text).
        """
        alt_text = self.render_inner(token)
        if alt_text:
            return f"<{token.src}|{alt_text}>"
        else:
            return f"<{token.src}>"
    
    def render_line_break(self, token) -> str:
        """
        Render line break.
        """
        return "\n" if token.soft else "\n\n"
    
    def render_raw_text(self, token) -> str:
        """
        Render raw text content.
        """
        return token.content
    
    def render_escape_sequence(self, token) -> str:
        """
        Render escaped characters.
        """
        return self.render_inner(token)
    
    def render(self, token):
        """
        Override the base render method to handle our custom return type.
        """
        if token.__class__.__name__ == 'Document':
            return self.render_document(token)
        else:
            return super().render(token)