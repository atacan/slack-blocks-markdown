# Examples

This directory contains examples showcasing the slack-blocks-markdown renderer, including the new **RichTextBlock** features with native Slack formatting.

## Files

- **`basic_usage.py`** - Main example script demonstrating both simple and advanced usage
- **`export_for_builder.py`** - Helper script to export JSON for Slack Block Kit Builder
- **`example_output.json`** - Generated output with two example conversions
- **`TESTING.md`** - Detailed guide for testing in Slack Block Kit Builder

## Quick Start

### 1. Run the Example

```bash
uv run python examples/basic_usage.py
```

This will:
- Show two markdown examples (advanced and simple)
- Convert them to Slack blocks
- Display block type summaries
- Save output to `example_output.json`

### 2. Test in Block Kit Builder

**Option A: Using the export script**
```bash
uv run python examples/export_for_builder.py
```

This will print the JSON in a ready-to-copy format.

**Option B: Manual copy**
1. Open `examples/example_output.json`
2. Copy the `blocks` array from either example
3. Paste into https://app.slack.com/block-kit-builder

### 3. See the Results

You'll see:
- ✅ **Native bullet points** (not • character)
- ✅ **Proper numbered lists** with formatting
- ✅ **Nested lists** with indentation
- ✅ **Rich text in quotes** with bold, italic, code
- ✅ **Preformatted code blocks**
- ✅ **Inline formatting** preserved everywhere

## What's New

### RichTextBlock Features

The examples showcase the newly implemented RichTextBlock features:

#### 1. Native Lists
```markdown
- **Bold item** with emphasis
- _Italic item_ for subtle text
- Item with `inline code`
- Item with [links](https://example.com)
```

Renders as native Slack bullets with full rich text support.

#### 2. Nested Lists
```markdown
- Top level
  - Nested level 1
    - Nested level 2
```

Proper indentation using Slack's `indent` property.

#### 3. Ordered Lists
```markdown
1. First step
2. Second step with **bold**
3. Third step with _italic_
```

Native numbering with rich text formatting.

#### 4. Code Blocks
````markdown
```python
def hello():
    return "world"
```
````

Uses `rich_text_preformatted` element for better rendering.

#### 5. Blockquotes
```markdown
> **Bold quote** with _italic_ and `code`
```

Uses `rich_text_quote` element with full formatting support.

## Advanced Example Content

The advanced example (`basic_usage.py`) demonstrates:

- Multiple heading levels (h1, h2, h3)
- Paragraphs with inline formatting
- Unordered lists with rich formatting
- Ordered lists with rich formatting
- Deeply nested lists (3 levels)
- Python code blocks
- Bash code blocks
- Blockquotes with multiple paragraphs
- Mixed content combinations
- Horizontal dividers
- Tables (in integration examples)

## Simple Example Content

The simple example provides:

- Quick start guide
- Installation instructions
- Numbered steps with inline code
- Feature list with nested items
- Code examples
- Tips in blockquotes

## Customization

### Modifying Examples

Edit the markdown strings in `basic_usage.py`:

```python
def advanced_usage_example():
    sample_markdown = """# Your Custom Content

Your markdown here...
"""
```

Then re-run to generate new output.

### Creating Your Own Example

```python
from slack_blocks_markdown import markdown_to_blocks
import json

markdown = """
# Your Content

Your markdown here with:
- Lists
- **Formatting**
- `Code`
"""

blocks = markdown_to_blocks(markdown)

# Save for Block Kit Builder
with open("my_example.json", "w") as f:
    json.dump({"blocks": blocks}, f, indent=2)
```

## Block Types Reference

| Markdown | Slack Block Type | Rich Text Element |
|----------|-----------------|-------------------|
| `# Heading` | `header` | - |
| Paragraph | `section` | - |
| `- List` | `rich_text` | `rich_text_list` (bullet) |
| `1. List` | `rich_text` | `rich_text_list` (ordered) |
| ` ```code``` ` | `rich_text` | `rich_text_preformatted` |
| `> Quote` | `rich_text` | `rich_text_quote` |
| `---` | `divider` | - |
| Tables | `table` | - |

## Next Steps

1. ✅ Run the examples
2. ✅ Test in Block Kit Builder
3. ✅ Customize the markdown
4. ✅ Use in your Slack app!

For detailed testing instructions, see [TESTING.md](./TESTING.md).

## Links

- [Slack Block Kit Builder](https://app.slack.com/block-kit-builder)
- [Slack Block Kit Documentation](https://api.slack.com/block-kit)
- [Rich Text Block Reference](https://api.slack.com/reference/block-kit/blocks#rich_text)
