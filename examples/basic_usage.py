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
    """
    sample_markdown = """# Welcome to our project! 

This is a **bold** announcement about our new features:

- ✅ User authentication 
- ✅ Real-time updates
- 🚧 Mobile app (coming soon)

Check out our [documentation](https://docs.example.com) for more details.

> **Note**: This is still in beta, so please report any issues!
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
        if 'text' in block:
            text_preview = block['text']['text'][:50]
            print(f"     Text: {text_preview}{'...' if len(text_preview) >= 50 else ''}")
    
    return blocks_json

def simple_usage_example():
    """
    Example showing simple usage with convenience function
    """
    sample_markdown = """# Quick Demo

This is the **easiest way** to convert markdown to Slack blocks!

- Just call `markdown_to_blocks()`
- Get back a list of block dictionaries
- Ready for the Slack API!
"""

    print("\n📝 Simple Usage: Using convenience function")
    print("=" * 50)
    print(f"Input markdown:\n{sample_markdown}")
    
    # Simple usage with convenience function
    blocks = markdown_to_blocks(sample_markdown)
    
    print(f"\n🎉 Generated {len(blocks)} blocks:")
    for i, block in enumerate(blocks):
        print(f"  {i+1}. {block['type']}")
        if 'text' in block:
            text_preview = block['text']['text'][:50]
            print(f"     Text: {text_preview}{'...' if len(text_preview) >= 50 else ''}")
    
    return blocks

# Example usage
if __name__ == "__main__":
    # Demonstrate both usage patterns
    advanced_blocks = advanced_usage_example()
    simple_blocks = simple_usage_example()
    
    # Save for testing in Block Kit Builder
    output = {
        "advanced_example": {"blocks": advanced_blocks},
        "simple_example": {"blocks": simple_blocks}
    }
    
    with open("examples/example_output.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\n💾 Saved to example_output.json")
    print("🔗 Test in Slack's Block Kit Builder: https://app.slack.com/block-kit-builder")