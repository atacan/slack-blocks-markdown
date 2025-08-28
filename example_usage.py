#!/usr/bin/env python3
"""
Simple example showing how to use the SlackBlocksRenderer
"""

import json
from mistletoe import Document
from slack_blocks_renderer import SlackBlocksRenderer

def markdown_to_slack_blocks(markdown_text: str) -> list:
    """
    Convert markdown text to Slack blocks
    
    Args:
        markdown_text: Markdown formatted string
        
    Returns:
        List of Slack block dictionaries
    """
    with SlackBlocksRenderer() as renderer:
        document = Document(markdown_text)
        blocks = renderer.render(document)
    
    # Convert to dictionaries for JSON serialization
    return [block.to_dict() for block in blocks]

# Example usage
if __name__ == "__main__":
    # Sample markdown
    sample_markdown = """# Welcome to our project! 

This is a **bold** announcement about our new features:

- ✅ User authentication 
- ✅ Real-time updates
- 🚧 Mobile app (coming soon)

Check out our [documentation](https://docs.example.com) for more details.

> **Note**: This is still in beta, so please report any issues!
"""

    print("📝 Converting Markdown to Slack Blocks")
    print("=" * 40)
    print(f"Input markdown:\n{sample_markdown}")
    
    # Convert to blocks
    blocks = markdown_to_slack_blocks(sample_markdown)
    
    print(f"\n🎉 Generated {len(blocks)} blocks:")
    for i, block in enumerate(blocks):
        print(f"  {i+1}. {block['type']}")
        if 'text' in block:
            text_preview = block['text']['text'][:50]
            print(f"     Text: {text_preview}{'...' if len(text_preview) >= 50 else ''}")
    
    # Save for testing in Block Kit Builder
    output = {"blocks": blocks}
    with open("example_output.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\n💾 Saved to example_output.json")
    print("🔗 Test in Slack's Block Kit Builder: https://app.slack.com/block-kit-builder")