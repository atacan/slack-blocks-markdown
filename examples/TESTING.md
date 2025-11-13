# Testing in Slack Block Kit Builder

This guide shows you how to test the generated Slack blocks in Slack's Block Kit Builder web UI.

## Quick Start

1. **Run the example script** to generate the JSON output:
   ```bash
   uv run python examples/basic_usage.py
   ```

2. **Open Slack's Block Kit Builder**:
   - Visit: https://app.slack.com/block-kit-builder

3. **Copy the JSON**:
   - Open `examples/example_output.json`
   - Copy the content of either:
     - `advanced_example` - Comprehensive showcase of all features
     - `simple_example` - Quick start guide

4. **Paste into Block Kit Builder**:
   - In the Block Kit Builder, paste the JSON into the left panel
   - You'll see a live preview on the right

## What to Look For

### Native List Rendering ✓
- Lists should display with **native Slack bullet points** (not the • character)
- Ordered lists should show proper numbering (1, 2, 3...)
- Nested lists should be properly indented

### Rich Text Formatting ✓
- **Bold text** should appear bold
- _Italic text_ should appear in italics
- `Inline code` should appear in monospace with background
- [Links](https://example.com) should be clickable

### Code Blocks ✓
- Code blocks should appear in a preformatted container
- Syntax and indentation should be preserved

### Blockquotes ✓
- Quotes should appear in Slack's native quote style (with vertical bar)
- Formatting within quotes should be preserved

## Example JSON Structure

The output file contains two examples:

```json
{
  "advanced_example": {
    "blocks": [...]  // Comprehensive feature showcase
  },
  "simple_example": {
    "blocks": [...]  // Quick start guide
  }
}
```

## Features Demonstrated

### Advanced Example
- ✅ Headers (h1, h2, h3)
- ✅ Paragraphs with inline formatting
- ✅ Unordered lists with rich formatting
- ✅ Ordered lists with rich formatting
- ✅ Nested lists (2-3 levels deep)
- ✅ Code blocks with syntax
- ✅ Blockquotes with rich formatting
- ✅ Mixed content combinations
- ✅ Horizontal dividers

### Simple Example
- ✅ Quick start instructions
- ✅ Installation steps
- ✅ Ordered lists with inline code
- ✅ Nested lists
- ✅ Blockquotes with tips
- ✅ Code examples

## Key Improvements

### Before (Old Implementation)
```
• Item 1
• Item 2
• Item 3
```
Lists used the bullet character (•) in plain text.

### After (New RichTextBlock Implementation)
- Native Slack bullet points
- Proper indentation for nested lists
- Full rich text support (bold, italic, code, links)
- Better visual appearance in Slack

## Troubleshooting

### If blocks don't appear correctly:
1. Make sure you copied the entire JSON object
2. Verify the JSON is valid (Block Kit Builder will show syntax errors)
3. Check that you're copying the "blocks" array, not the wrapper object

### To modify examples:
1. Edit the markdown strings in `examples/basic_usage.py`
2. Run the script again to regenerate `example_output.json`
3. Reload in Block Kit Builder

## Block Types Generated

The renderer creates these Slack block types:

| Markdown Element | Slack Block Type | Details |
|-----------------|------------------|---------|
| Headings (#) | `header` | Plain text, max 150 chars |
| Paragraphs | `section` | Markdown text with inline formatting |
| Bullet lists | `rich_text` | Native bullets with `rich_text_list` |
| Ordered lists | `rich_text` | Native numbering with `rich_text_list` |
| Code blocks | `rich_text` | Preformatted with `rich_text_preformatted` |
| Blockquotes | `rich_text` | Quote formatting with `rich_text_quote` |
| Horizontal rules | `divider` | Visual separator |
| Tables | `table` | Custom table block |

## Next Steps

After verifying in Block Kit Builder:
1. Use the same JSON in your Slack app
2. Send via `chat.postMessage` API
3. Enjoy native rich text rendering! 🚀
