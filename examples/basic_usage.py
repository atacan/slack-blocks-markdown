#!/usr/bin/env python3
"""
Simple example showing how to use the SlackBlocksRenderer
"""

import json

from mistletoe import Document

from slack_blocks_markdown import SlackBlocksRenderer, markdown_to_blocks


def advanced_usage_example():
    """
    Example showing advanced usage with SlackBlocksRenderer directly

    This example showcases the new RichTextBlock features:
    - Native bullet and ordered lists
    - Nested lists with proper indentation
    - Rich text quotes
    - Preformatted code blocks
    - Inline formatting (bold, italic, code, links) within lists
    """
    sample_markdown = """# Slack Blocks Markdown Renderer

This renderer now supports **native Slack rich text blocks** with proper formatting!

## Features

### Lists with Native Bullets

Unordered lists now use native Slack bullets (not • character):

- **Bold item** with emphasis
- _Italic item_ for subtle text
- Item with `inline code` formatting
- Item with [a link](https://github.com/slack-blocks-markdown)

### Ordered Lists

1. First step in the process
2. Second step with **bold text**
3. Third step with _italic emphasis_
4. Final step with `code example`

### Nested Lists

Multi-level lists with proper indentation:

- Top level item
  - Nested item 1.1
  - Nested item 1.2 with **bold**
    - Deep nested item
- Another top level
  - Nested under second item

### Code Blocks

Code blocks use rich text preformatted elements:

```python
def greet(name):
    return f"Hello, {name}!"

result = greet("Slack")
print(result)
```

### Blockquotes

Quotes now use native rich text formatting:

> This is a **powerful** feature that supports _rich formatting_ within quotes!
>
> You can have multiple paragraphs in quotes with `inline code` too.

### Mixed Content

Combine everything for complex messages:

1. Start with setup instructions
2. Review the [documentation](https://docs.example.com)
3. Run the following command:

```bash
npm install slack-blocks-markdown
```

> **Pro tip**: Use `markdown_to_blocks()` for quick conversions!

---

## Summary

All formatting is preserved with native Slack rendering! 🚀
"""

    print("📝 Advanced Usage: Using SlackBlocksRenderer directly")
    print("=" * 50)
    print(f"Input markdown:\n{sample_markdown}")

    # Advanced usage with direct renderer control
    with SlackBlocksRenderer() as renderer:
        document = Document(sample_markdown)
        blocks = renderer.render(document)

    # Convert to dictionaries for JSON serialization
    blocks_json = [block.to_dict() for block in blocks]

    print(f"\n🎉 Generated {len(blocks)} blocks:")
    for i, block in enumerate(blocks_json):
        print(f"  {i+1}. {block['type']}")
        if "text" in block:
            text_preview = block["text"]["text"][:50]
            print(
                f"     Preview: {text_preview}{'...' if len(text_preview) >= 50 else ''}",
            )
        elif block["type"] == "rich_text" and "elements" in block:
            # Show what type of rich text element it is
            if block["elements"]:
                element_type = block["elements"][0]["type"]
                print(f"     Contains: {element_type}")
                if element_type == "rich_text_list":
                    list_style = block["elements"][0].get("style", "bullet")
                    item_count = len(block["elements"][0].get("elements", []))
                    print(f"     Style: {list_style}, Items: {item_count}")

    return blocks_json


def simple_usage_example():
    """
    Example showing simple usage with convenience function
    """
    sample_markdown = """# Quick Start Guide

Get started with **slack-blocks-markdown** in seconds!

## Installation

```bash
pip install slack-blocks-markdown
```

## Basic Usage

Follow these steps:

1. Import the function: `from slack_blocks_markdown import markdown_to_blocks`
2. Convert your markdown: `blocks = markdown_to_blocks(markdown_text)`
3. Send to Slack API: `client.chat_postMessage(channel=channel, blocks=blocks)`

## Features

Native support for:

- **Bold** and _italic_ text
- `Inline code` snippets
- [Links](https://api.slack.com) to external sites
- Nested lists
  - With proper indentation
  - And rich formatting

> **Tip**: All Slack-compatible markdown is automatically converted to native blocks!

## Example Code

```python
from slack_blocks_markdown import markdown_to_blocks

markdown = "# Hello **Slack**!"
blocks = markdown_to_blocks(markdown)
# Ready to send! 🚀
```

---

That's it! You're ready to go! ✨
"""

    print("\n📝 Simple Usage: Using convenience function")
    print("=" * 50)
    print(f"Input markdown:\n{sample_markdown}")

    # Simple usage with convenience function
    blocks = markdown_to_blocks(sample_markdown)

    print(f"\n🎉 Generated {len(blocks)} blocks:")
    for i, block in enumerate(blocks):
        print(f"  {i+1}. {block['type']}")
        if "text" in block:
            text_preview = block["text"]["text"][:50]
            print(
                f"     Preview: {text_preview}{'...' if len(text_preview) >= 50 else ''}",
            )
        elif block["type"] == "rich_text" and "elements" in block:
            # Show what type of rich text element it is
            if block["elements"]:
                element_type = block["elements"][0]["type"]
                print(f"     Contains: {element_type}")

    return blocks


# Example usage
if __name__ == "__main__":
    # Demonstrate both usage patterns
    advanced_blocks = advanced_usage_example()
    simple_blocks = simple_usage_example()

    # Save for testing in Block Kit Builder
    output = {
        "advanced_example": {"blocks": advanced_blocks},
        "simple_example": {"blocks": simple_blocks},
    }

    with open("examples/example_output.json", "w") as f:
        json.dump(output, f, indent=2)

    print("\n💾 Saved to example_output.json")
    print(
        "🔗 Test in Slack's Block Kit Builder: https://app.slack.com/block-kit-builder",
    )
