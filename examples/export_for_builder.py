#!/usr/bin/env python3
"""
Export blocks in a format ready for Slack Block Kit Builder

This script reads the generated example_output.json and prints
the blocks array in a format that can be directly pasted into
the Block Kit Builder.
"""

import json
import sys


def export_blocks(example_name: str = "advanced_example") -> None:
    """
    Export blocks for the specified example.

    Args:
        example_name: Either "advanced_example" or "simple_example"
    """
    try:
        with open("examples/example_output.json") as f:
            data = json.load(f)

        if example_name not in data:
            print(f"❌ Error: '{example_name}' not found in example_output.json")
            print(f"Available examples: {', '.join(data.keys())}")
            sys.exit(1)

        blocks = data[example_name]

        print(f"✓ Exporting '{example_name}' blocks")
        print("=" * 70)
        print("\nCopy the JSON below and paste it into Block Kit Builder:")
        print("🔗 https://app.slack.com/block-kit-builder")
        print("=" * 70)
        print()

        # Pretty print the blocks
        print(json.dumps(blocks, indent=2))

        print()
        print("=" * 70)
        print(f"✓ Total blocks: {len(blocks['blocks'])}")
        print("=" * 70)

        # Show summary of block types
        block_types: dict[str, int] = {}
        for block in blocks["blocks"]:
            block_type = block["type"]
            block_types[block_type] = block_types.get(block_type, 0) + 1

        print("\n📊 Block type summary:")
        for block_type, count in sorted(block_types.items()):
            print(f"  - {block_type}: {count}")

    except FileNotFoundError:
        print("❌ Error: example_output.json not found")
        print("Run 'uv run python examples/basic_usage.py' first to generate it")
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ Error: Invalid JSON in example_output.json")
        sys.exit(1)


if __name__ == "__main__":
    # Check command line arguments
    example = sys.argv[1] if len(sys.argv) > 1 else "advanced_example"

    print()
    print("📤 Slack Block Kit Builder Export Tool")
    print()

    export_blocks(example)

    print()
    print("💡 Tip: Run with 'simple_example' to export the simpler version:")
    print("   uv run python examples/export_for_builder.py simple_example")
    print()
