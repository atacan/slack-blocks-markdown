# Slack Blocks Markdown

[![PyPI version](https://badge.fury.io/py/slack-blocks-markdown.svg)](https://badge.fury.io/py/slack-blocks-markdown)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/atacan/slack-blocks-markdown/workflows/tests/badge.svg)](https://github.com/atacan/slack-blocks-markdown/actions)

Convert Markdown to Slack Block Kit blocks using Python. This library provides a clean, efficient way to transform your Markdown content into Slack's interactive Block Kit format.

## Features

- 🚀 **Complete Markdown Support**: Headers, paragraphs, lists, code blocks, quotes, tables, links, and inline formatting
- 📱 **Slack Block Kit Compatible**: All blocks follow official Slack specifications with proper constraints
- 🎯 **Custom Table Support**: Full implementation of Slack's table blocks with validation
- 🔧 **Easy to Use**: Simple API with both direct renderer and convenience function
- ⚡ **High Performance**: Efficient processing of large documents
- 🧪 **Well Tested**: Comprehensive test suite with 88% coverage
- 📝 **Type Safe**: Full type hints for better development experience

## Installation

```bash
pip install slack-blocks-markdown
```

## Quick Start

### Simple Usage

```python
from slack_blocks_markdown import markdown_to_blocks

# Convert markdown to Slack blocks
markdown = """# Project Update

This is a **bold** announcement about our new features:

- ✅ User authentication
- ✅ Real-time updates
- 🚧 Mobile app (coming soon)

> **Note**: This is still in beta, so please report any issues!
"""

blocks = markdown_to_blocks(markdown)
print(f"Generated {len(blocks)} blocks")

# Use blocks with Slack SDK
from slack_sdk import WebClient

client = WebClient(token="your-token")
client.chat_postMessage(
    channel="#general",
    blocks=blocks
)
```

### Advanced Usage

```python
from mistletoe import Document
from slack_blocks_markdown import SlackBlocksRenderer

# For more control over the rendering process
with SlackBlocksRenderer() as renderer:
    document = Document(markdown)
    blocks = renderer.render(document)

# Convert to dictionaries for JSON serialization
blocks_json = [block.to_dict() for block in blocks]
```

## Supported Markdown Elements

| Markdown Element | Slack Block Type | Notes |
|-----------------|------------------|-------|
| `# Headers` | HeaderBlock | Truncated to 150 chars |
| Paragraphs | SectionBlock | With mrkdwn formatting |
| `**Bold**` → `*Bold*` | Inline formatting | Slack markdown style |
| `_Italic_` → `_Italic_` | Inline formatting | Slack markdown style |
| `` `Code` `` → `` `Code` `` | Inline formatting | Preserved |
| `~~Strike~~` → `~Strike~` | Inline formatting | Slack markdown style |
| `[Link](url)` → `<url\|Link>` | Inline formatting | Slack link format |
| Code blocks | SectionBlock | With triple backticks |
| > Blockquotes | SectionBlock | With > prefix |
| Lists | SectionBlock | Bullet (•) or numbered |
| Tables | TableBlock | Custom implementation |
| `---` | DividerBlock | Horizontal rules |

## Examples

### Basic Formatting

```python
markdown = "This is **bold** and _italic_ with `code` and [links](https://example.com)"
blocks = markdown_to_blocks(markdown)
# Result: [{"type": "section", "text": {"type": "mrkdwn", "text": "This is *bold* and _italic_ with `code` and <https://example.com|links>"}}]
```

### Lists and Code

```python
markdown = """
## Features

- Easy to use
- Fast processing
- Great documentation

```python
def hello():
    return "world"
```
"""
blocks = markdown_to_blocks(markdown)
# Generates HeaderBlock, SectionBlock (list), and SectionBlock (code)
```

### Tables

```python
markdown = """
| Feature | Status |
|---------|--------|
| Auth | ✅ Done |
| API | 🚧 Progress |
"""
blocks = markdown_to_blocks(markdown)
# Generates custom TableBlock with proper cell structure
```

## API Reference

### `markdown_to_blocks(markdown_text: str) -> list`

Convenience function to convert markdown to Slack blocks.

**Parameters:**
- `markdown_text`: Markdown formatted string

**Returns:**
- List of Slack block dictionaries ready for API use

### `SlackBlocksRenderer`

Main renderer class inheriting from mistletoe's BaseRenderer.

**Methods:**
- `render(document)`: Convert mistletoe Document to list of Block objects
- Context manager support for proper resource handling

### `TableBlock`

Custom table block implementation for Slack Block Kit.

**Parameters:**
- `rows`: List of rows (each row is list of cell objects)
- `block_id`: Optional unique identifier (max 255 chars)
- `column_settings`: Optional column configuration

## Slack Block Kit Constraints

This library automatically handles Slack's Block Kit constraints:

- **Headers**: Maximum 150 characters (truncated with "..." if longer)
- **Text blocks**: Maximum 3000 characters (truncated with "..." if longer)
- **Tables**: Maximum 100 rows, 20 columns per row
- **Block IDs**: Maximum 255 characters

## Development

```bash
# Clone repository
git clone https://github.com/atacan/slack-blocks-markdown.git
cd slack-blocks-markdown

# Install with development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check src/ tests/
black src/ tests/

# Run type checking
mypy src/
```

## Testing

The library includes comprehensive tests covering:

- All markdown element types
- Slack constraint validation
- Edge cases and error handling
- Integration with Slack API format
- Performance with large documents

```bash
# Run with coverage
pytest --cov=slack_blocks_markdown --cov-report=html
```

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Related Projects

- [mistletoe](https://github.com/miyuchina/mistletoe) - The markdown parser we use
- [slack-sdk](https://github.com/slackapi/python-slack-sdk) - Official Slack SDK for Python
- [Slack Block Kit Builder](https://app.slack.com/block-kit-builder) - Visual tool for building Slack blocks
