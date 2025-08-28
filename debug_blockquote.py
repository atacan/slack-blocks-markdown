#!/usr/bin/env python3
"""Debug script to understand blockquote parsing"""

from mistletoe import Document
from slack_blocks_renderer import SlackBlocksRenderer

# Blockquote test
blockquote_markdown = """## Blockquotes

> This is an important quote that should stand out.
> 
> It can span multiple lines and contain *formatting*.
"""

print("=== Debugging Blockquote Parsing ===")
print("Markdown content:")
print(repr(blockquote_markdown))
print("\n=== Document structure ===")

document = Document(blockquote_markdown)

def print_token_tree(token, indent=0):
    """Recursively print the token tree"""
    spaces = "  " * indent
    print(f"{spaces}{token.__class__.__name__}", end="")
    
    # Print relevant attributes
    if hasattr(token, 'content'):
        print(f": '{token.content}'")
    elif hasattr(token, 'level'):
        print(f" (level {token.level})")
    elif hasattr(token, 'start') and token.start is not None:
        print(f" (start={token.start})")
    else:
        print()
    
    # Recursively print children
    if hasattr(token, 'children') and token.children is not None:
        for child in token.children:
            print_token_tree(child, indent + 1)

print_token_tree(document)

print("\n=== Rendered blocks ===")
with SlackBlocksRenderer() as renderer:
    blocks = renderer.render(document)

for i, block in enumerate(blocks):
    print(f"Block {i+1}: {block.type}")
    if hasattr(block, 'text'):
        print(f"  Text: {repr(block.text.text)}")