#!/usr/bin/env python3
"""
Development script to test the Slack Blocks Renderer.

This script demonstrates how to use the SlackBlocksRenderer to convert
various Markdown examples to Slack Block Kit JSON format.
"""

import json
from mistletoe import Document
from slack_blocks_renderer import SlackBlocksRenderer


def test_markdown_samples():
    """
    Test the renderer with various markdown samples and output JSON.
    """
    
    # Sample markdown content covering different elements
    markdown_samples = {
        "basic_formatting": """# Welcome to Slack Blocks!

This is a **bold** statement with some _italic_ text and `inline code`.

You can also have ~strikethrough~ text and [links to external sites](https://example.com).

---

## Code Blocks

Here's a Python code example:

```python
def hello_world():
    print("Hello, Slack!")
    return True
```

## Lists

### Unordered List:
- First item
- Second item with **bold** text  
- Third item with a [link](https://slack.com)

### Ordered List:
1. Step one
2. Step two
3. Step three

## Blockquotes

> This is an important quote that should stand out.
> 
> It can span multiple lines and contain *formatting*.

## Tables

| Feature | Supported | Notes |
|---------|-----------|-------|
| Headers | ✅ | Limited to 150 chars |
| Paragraphs | ✅ | Uses SectionBlock |
| Code blocks | ✅ | Preformatted text |
| Lists | ✅ | Bullet and numbered |
""",
        
        "simple_message": """# Project Update

The new feature is ready for testing! 

Key highlights:
- ✅ Authentication system
- ✅ User dashboard  
- 🚧 Admin panel (in progress)

Check out the [demo site](https://demo.example.com) and let me know your thoughts.
""",
        
        "technical_doc": """## API Documentation

### Authentication

All API requests must include an authentication header:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \\
     https://api.example.com/v1/users
```

**Important**: Keep your API tokens secure and never commit them to version control.

### Rate Limits

| Endpoint | Limit | Window |
|----------|-------|---------|
| /users | 100 req/min | 60 seconds |
| /data | 50 req/min | 60 seconds |

> **Note**: Rate limits are enforced per API key. Contact support if you need higher limits.
"""
    }
    
    print("🚀 Testing Slack Blocks Renderer")
    print("=" * 50)
    
    for name, markdown_content in markdown_samples.items():
        print(f"\n📝 Testing: {name}")
        print("-" * 30)
        
        try:
            # Parse markdown and render to Slack blocks
            with SlackBlocksRenderer() as renderer:
                document = Document(markdown_content)
                blocks = renderer.render(document)
            
            # Convert blocks to JSON format for Block Kit Builder
            blocks_json = [block.to_dict() for block in blocks]
            
            # Save to file
            filename = f"output_{name}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    "blocks": blocks_json
                }, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Generated {len(blocks)} blocks")
            print(f"💾 Saved to: {filename}")
            
            # Print first few blocks for preview
            print("\n🔍 Preview (first 2 blocks):")
            for i, block in enumerate(blocks[:2]):
                print(f"  Block {i+1}: {block.type}")
                block_dict = block.to_dict()
                if 'text' in block_dict:
                    text_preview = block_dict['text'].get('text', '')[:100]
                    print(f"    Text: {text_preview}{'...' if len(text_preview) >= 100 else ''}")
            
            if len(blocks) > 2:
                print(f"    ... and {len(blocks) - 2} more blocks")
                
        except Exception as e:
            print(f"❌ Error processing {name}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("🎉 Testing complete!")
    print("\n📋 To test in Slack's Block Kit Builder:")
    print("1. Go to https://app.slack.com/block-kit-builder")
    print("2. Copy the JSON from any output_*.json file") 
    print("3. Paste it into the Block Kit Builder")
    print("4. See how your markdown looks in Slack!")


def test_edge_cases():
    """
    Test edge cases and limits.
    """
    print("\n🧪 Testing Edge Cases")
    print("-" * 30)
    
    # Test very long heading (should be truncated)
    long_heading = "# " + "A" * 200
    
    # Test very long paragraph (should be truncated) 
    long_paragraph = "This is a very long paragraph. " * 200
    
    # Test empty content
    empty_content = ""
    
    edge_cases = {
        "long_heading": long_heading,
        "long_paragraph": long_paragraph, 
        "empty_content": empty_content,
        "mixed_content": f"{long_heading}\n\n{long_paragraph}"
    }
    
    for name, content in edge_cases.items():
        try:
            with SlackBlocksRenderer() as renderer:
                document = Document(content)
                blocks = renderer.render(document)
            
            blocks_json = [block.to_dict() for block in blocks]
            filename = f"edge_case_{name}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({"blocks": blocks_json}, f, indent=2)
                
            print(f"✅ {name}: {len(blocks)} blocks generated")
            
        except Exception as e:
            print(f"❌ {name} failed: {e}")


if __name__ == "__main__":
    test_markdown_samples()
    test_edge_cases()