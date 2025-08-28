#!/usr/bin/env python3
"""Detailed debug of quote parsing"""

from mistletoe import Document
from mistletoe.block_token import Quote

# Test different quote formats
test_cases = [
    ("simple", "> Simple quote"),
    ("multiline_no_empty", "> Line 1\n> Line 2"), 
    ("multiline_with_empty", "> Line 1\n> \n> Line 2"),
    ("actual_case", "> This is an important quote that should stand out.\n> \n> It can span multiple lines and contain *formatting*."),
]

for name, markdown in test_cases:
    print(f"\n=== {name.upper()} ===")
    print(f"Input: {repr(markdown)}")
    
    document = Document(markdown)
    
    def find_quotes(token):
        if isinstance(token, Quote):
            print(f"Quote found with {len(token.children)} children:")
            for i, child in enumerate(token.children):
                print(f"  Child {i}: {child.__class__.__name__}")
                if hasattr(child, 'content'):
                    print(f"    Content: {repr(child.content)}")
                elif hasattr(child, 'children'):
                    for j, subchild in enumerate(child.children):
                        if hasattr(subchild, 'content'):
                            print(f"    Subchild {j}: {subchild.__class__.__name__} = {repr(subchild.content)}")
        elif hasattr(token, 'children'):
            for child in token.children:
                find_quotes(child)
    
    find_quotes(document)