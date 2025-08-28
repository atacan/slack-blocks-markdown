# Slack Blocks Markdown Renderer

A custom renderer for [Mistletoe](https://github.com/miyuchina/mistletoe) that converts Markdown to [Slack Block Kit](https://api.slack.com/block-kit) blocks.

## Features

This renderer converts Markdown elements to appropriate Slack blocks:

### Block Elements
- **Headers (H1-H6)** ’ `HeaderBlock` with PlainTextObject
- **Paragraphs** ’ `SectionBlock` with MarkdownTextObject  
- **Code Blocks** ’ `SectionBlock` with preformatted text
- **Lists** ’ `SectionBlock` with bullet points (") or numbered items
- **Blockquotes** ’ `SectionBlock` with `>` formatting
- **Horizontal Rules** ’ `DividerBlock`
- **Tables** ’ `SectionBlock` with preformatted table layout

### Inline Elements (within MarkdownTextObject)
- **Bold** ’ `*bold*`
- **Italic** ’ `_italic_`
- **Inline Code** ’ `` `code` ``
- **Strikethrough** ’ `~strikethrough~`
- **Links** ’ `<url|text>` or `<url>`
- **Images** ’ `<url|alt_text>` (as links)

## Installation

Install the required dependencies:

```bash
pip install mistletoe slack_sdk
```

## Usage

```python
from mistletoe import Document
from slack_blocks_renderer import SlackBlocksRenderer

# Your markdown content
markdown_text = """
# Project Update

This is a **bold** announcement!

-  Feature A completed
-  Feature B completed  
- =§ Feature C in progress

Check out our [docs](https://example.com) for more info.
"""

# Convert to Slack blocks
with SlackBlocksRenderer() as renderer:
    document = Document(markdown_text)
    blocks = renderer.render(document)

# Convert to JSON for Slack API
blocks_json = [block.to_dict() for block in blocks]
```

## Testing

Run the test script to see examples:

```bash
python test_renderer.py
```

This will generate several JSON files that you can test in [Slack's Block Kit Builder](https://app.slack.com/block-kit-builder).

## Example Output

The markdown:
```markdown
# Welcome!

This is **bold** text with a [link](https://example.com).

- Item 1
- Item 2
```

Becomes:
```json
{
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "Welcome!"
      }
    },
    {
      "type": "section", 
      "text": {
        "type": "mrkdwn",
        "text": "This is *bold* text with a <https://example.com|link>."
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn", 
        "text": "" Item 1\\n" Item 2"
      }
    }
  ]
}
```

## Limitations

- **Headers** are limited to 150 characters (Slack constraint)
- **Text blocks** are limited to 3000 characters (Slack constraint)  
- **Images** are converted to links since Slack blocks don't support inline images in text
- **Tables** are rendered as preformatted text for better readability
- Content that exceeds limits is automatically truncated with "..."

## Files

- `slack_blocks_renderer.py` - The main renderer class
- `test_renderer.py` - Comprehensive test script with examples
- `example_usage.py` - Simple usage example
- `debug_test.py` - Debug script for understanding token parsing

## Block Kit Builder Testing

1. Run `python test_renderer.py` to generate JSON files
2. Go to https://app.slack.com/block-kit-builder
3. Copy the JSON from any `output_*.json` file
4. Paste it into the Block Kit Builder to preview

## Contributing

Feel free to extend the renderer for additional Markdown elements or customize the Slack block formatting to suit your needs.