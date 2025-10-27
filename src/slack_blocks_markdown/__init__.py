"""
Slack Blocks Markdown - Convert Markdown to Slack Block Kit blocks
"""

from .blocks import TableBlock
from .renderer import SlackBlocksRenderer


# Convenience function for simple usage
def markdown_to_blocks(markdown_text: str) -> list:
    """Convert markdown text to Slack blocks"""
    from mistletoe import Document  # type: ignore[import-untyped]

    with SlackBlocksRenderer() as renderer:
        document = Document(markdown_text)
        blocks = renderer.render(document)
    return [block.to_dict() for block in blocks]


__all__ = ["SlackBlocksRenderer", "TableBlock", "markdown_to_blocks"]
__version__ = "0.1.0"
