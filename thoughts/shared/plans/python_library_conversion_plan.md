# Python Library Conversion Implementation Plan

## Overview

Convert the slack-blocks-markdown project from a simple Python project into a professional library suitable for PyPI publication. The project currently has solid technical foundations with a functional markdown-to-Slack-blocks converter using mistletoe and slack-sdk, but needs significant restructuring for professional library distribution.

## Current State Analysis

**Existing Strengths:**
- Solid technical implementation in `slack_blocks_renderer.py:1-519` with `SlackBlocksRenderer` class
- Custom `TableBlock` implementation extending Slack SDK
- Comprehensive markdown element support (headers, paragraphs, lists, tables, code blocks)
- Proper Slack Block Kit constraint handling (3000 char limits, truncation, validation)
- Working examples and development testing scripts

**Current Limitations:**
- Flat project layout instead of modern `src/` structure
- Minimal `pyproject.toml:1-10` missing essential metadata and build configuration
- Development testing scripts rather than proper pytest framework
- Missing standard library files (LICENSE, CHANGELOG, proper documentation structure)
- No entry points defined for package usage
- Mixed development/production files in root directory

## Desired End State

**A professional Python library that:**
- Can be installed via `pip install slack-blocks-markdown`
- Follows modern Python packaging standards with `src/` layout
- Has comprehensive test suite with >80% coverage
- Includes proper documentation and examples
- Supports semantic versioning and changelog tracking
- Passes all quality gates (linting, type checking, tests)
- Is ready for PyPI publication

**Verification Method:**
- Package builds successfully: `uv build`
- Installs correctly: `pip install -e .`
- Tests pass: `pytest`
- API works as expected: Import and use in separate project

### Key Discoveries:
- Core `SlackBlocksRenderer` implementation follows mistletoe's `BaseRenderer` pattern correctly (`slack_blocks_renderer.py:84-97`)
- Custom `TableBlock` class properly inherits from `slack_sdk.models.blocks.Block` (`slack_blocks_renderer.py:23-71`)
- Current usage pattern is clean and ready for library export (`example_usage.py:10-25`)
- Testing approach provides good coverage but needs pytest conversion (`test_renderer.py:14-153`)

## What We're NOT Doing

- Changing core functionality or API design (it's already well-designed)
- Adding new features or markdown elements
- Creating CLI interface (not requested, can be added later)
- Setting up CI/CD pipeline (focus on package structure first)
- Deploying to PyPI (preparation only)

## Implementation Approach

**Strategy:** Incremental transformation maintaining working code at each step
**Risk Mitigation:** Test after each phase to ensure functionality is preserved
**Quality Focus:** Modern packaging standards with comprehensive testing

## Phase 1: Project Structure Reorganization

### Overview
Create modern `src/` layout and properly organize existing code into a structured package format.

### Changes Required:

#### 1. Create Source Package Structure
**Directory Creation:**
```bash
mkdir -p src/slack_blocks_markdown
mkdir -p tests
mkdir -p examples
mkdir -p docs
```

#### 2. Core Module Reorganization
**File**: `src/slack_blocks_markdown/renderer.py`
**Changes**: Move core renderer class from root, excluding TableBlock

```python
"""
Slack Blocks Renderer for Mistletoe

This module provides a custom renderer that converts Markdown to Slack Block Kit blocks.
"""

from typing import List, Any
from mistletoe.base_renderer import BaseRenderer
from slack_sdk.models.blocks import (
    Block, SectionBlock, HeaderBlock, DividerBlock,
    MarkdownTextObject, PlainTextObject
)
from .blocks import TableBlock

class SlackBlocksRenderer(BaseRenderer):
    # Move existing implementation from slack_blocks_renderer.py:84-519
    # Update imports to use relative import for TableBlock
    pass
```

#### 3. Custom Blocks Module
**File**: `src/slack_blocks_markdown/blocks.py`
**Changes**: Extract TableBlock class with proper isolation

```python
"""
Custom Slack Block implementations
"""

from typing import List, Any, Optional, Dict
from slack_sdk.models.blocks import Block

class TableBlock(Block):
    # Move existing TableBlock implementation from slack_blocks_renderer.py:23-71
    pass
```

#### 4. Package API Definition
**File**: `src/slack_blocks_markdown/__init__.py`
**Changes**: Create clean public API

```python
"""
Slack Blocks Markdown - Convert Markdown to Slack Block Kit blocks
"""

from .renderer import SlackBlocksRenderer
from .blocks import TableBlock

# Convenience function for simple usage
def markdown_to_blocks(markdown_text: str) -> list:
    """Convert markdown text to Slack blocks"""
    from mistletoe import Document
    with SlackBlocksRenderer() as renderer:
        document = Document(markdown_text)
        blocks = renderer.render(document)
    return [block.to_dict() for block in blocks]

__all__ = ['SlackBlocksRenderer', 'TableBlock', 'markdown_to_blocks']
__version__ = '0.1.0'
```

#### 5. Move Examples
**File**: `examples/basic_usage.py`
**Changes**: Update imports and move from root

```python
# Update import to use new package structure
from slack_blocks_markdown import SlackBlocksRenderer, markdown_to_blocks
```

### Success Criteria:

#### Automated Verification:
- [ ] Package structure created correctly: `ls src/slack_blocks_markdown/`
- [ ] Python can import new modules: `python -c "from src.slack_blocks_markdown import SlackBlocksRenderer"`
- [ ] No syntax errors in refactored code: `python -m py_compile src/slack_blocks_markdown/*.py`
- [ ] Original functionality preserved: `python examples/basic_usage.py`

#### Manual Verification:
- [ ] All core functionality works identical to original
- [ ] Import paths are clean and intuitive
- [ ] Code organization feels logical and maintainable
- [ ] No functionality regressions compared to original

---

## Phase 2: Enhanced Configuration & Metadata

### Overview
Upgrade project configuration to meet professional library standards and add all required metadata files.

### Changes Required:

#### 1. Comprehensive pyproject.toml
**File**: `pyproject.toml`
**Changes**: Complete rewrite with full metadata and build configuration

```toml
[build-system]
requires = ["setuptools>=68", "setuptools-scm[toml]>=8"]
build-backend = "setuptools.build_meta"

[project]
name = "slack-blocks-markdown"
version = "0.1.0"
description = "Convert Markdown to Slack Block Kit blocks using mistletoe"
readme = "README.md"
license = {file = "LICENSE"}
authors = [
    {name = "atacan", email = "info@actondon.com"}
]
maintainers = [
    {name = "atacan", email = "info@actondon.com"}
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Communications :: Chat",
    "Topic :: Text Processing :: Markup",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
keywords = ["slack", "markdown", "blocks", "mistletoe", "converter", "block-kit"]
requires-python = ">=3.11"
dependencies = [
    "mistletoe>=1.4.0",
    "slack-sdk>=3.36.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.5.0",
]
test = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0"
]

[project.urls]
Homepage = "https://github.com/atacan/slack-blocks-markdown"
Repository = "https://github.com/atacan/slack-blocks-markdown"
Issues = "https://github.com/atacan/slack-blocks-markdown/issues"
Documentation = "https://github.com/atacan/slack-blocks-markdown/blob/main/README.md"

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--cov=slack_blocks_markdown --cov-report=html --cov-report=term-missing"

[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'

[tool.ruff]
line-length = 88
target-version = "py311"
select = ["E", "F", "W", "C90", "I", "N", "UP", "YTT", "S", "BLE", "B", "A", "COM", "C4", "DTZ", "T10", "EM", "EXE", "ISC", "ICN", "G", "INP", "PIE", "T20", "PYI", "PT", "Q", "RSE", "RET", "SLF", "SIM", "TID", "TCH", "ARG", "PTH", "ERA", "PD", "PGH", "PL", "TRY", "NPY", "RUF"]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

#### 2. License File
**File**: `LICENSE`
**Changes**: Add MIT License

```text
MIT License

Copyright (c) 2025 [@atacan](https://github.com/atacan)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

#### 3. Changelog File
**File**: `CHANGELOG.md`
**Changes**: Initialize version tracking

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-08-29

### Added
- Initial release of slack-blocks-markdown library
- Support for converting Markdown to Slack Block Kit blocks
- Custom TableBlock implementation for Slack tables
- Comprehensive markdown element support (headers, paragraphs, lists, code blocks, quotes)
- Proper Slack Block Kit constraint handling and validation
- Example usage documentation and scripts

### Features
- Headers converted to HeaderBlock with PlainTextObject
- Paragraphs converted to SectionBlock with MarkdownTextObject
- Code blocks with preformatted text formatting
- Lists with bullet points and numbered items
- Blockquotes with proper quote formatting
- Horizontal rules as DividerBlock
- Tables as custom TableBlock with proper cell structure
- Inline formatting (bold, italic, code, links) in Slack markdown format
- Automatic content truncation for Slack limits (150 chars for headers, 3000 for text)

[Unreleased]: https://github.com/atacan/slack-blocks-markdown/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/atacan/slack-blocks-markdown/releases/tag/v0.1.0
```

#### 4. Enhanced README
**File**: `README.md`
**Changes**: Update for library installation and usage

```markdown
# Slack Blocks Markdown

[![PyPI version](https://badge.fury.io/py/slack-blocks-markdown.svg)](https://badge.fury.io/py/slack-blocks-markdown)
[![Python Support](https://img.shields.io/pypi/pyversions/slack-blocks-markdown.svg)](https://pypi.org/project/slack-blocks-markdown/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python library that converts Markdown to [Slack Block Kit](https://api.slack.com/block-kit) blocks using [mistletoe](https://github.com/miyuchina/mistletoe).

## Installation

Install from PyPI:

```bash
pip install slack-blocks-markdown
```

Install for development:

```bash
git clone https://github.com/atacan/slack-blocks-markdown.git
cd slack-blocks-markdown
pip install -e .[dev]
```

## Quick Start

```python
from slack_blocks_markdown import markdown_to_blocks

markdown = """
# Project Update

This is a **bold** announcement!

- Feature A completed
- Feature B in progress

Check out our [documentation](https://example.com) for details.
"""

blocks = markdown_to_blocks(markdown)
print(blocks)  # Ready for Slack API
```

## Advanced Usage

```python
from mistletoe import Document
from slack_blocks_markdown import SlackBlocksRenderer

# For more control over the rendering process
with SlackBlocksRenderer() as renderer:
    document = Document(markdown_text)
    blocks = renderer.render(document)

# Convert to JSON for Slack API
blocks_json = [block.to_dict() for block in blocks]
```

[Continue with rest of existing README content, updated for library usage]
```

### Success Criteria:

#### Automated Verification:
- [ ] Package builds successfully: `python -m build`
- [ ] Metadata is valid: `twine check dist/*`
- [ ] Dependencies install correctly: `pip install -e .[dev]`
- [ ] Linting passes: `ruff check src/`
- [ ] Type checking passes: `mypy src/`

#### Manual Verification:
- [ ] README clearly explains installation and usage
- [ ] License terms are appropriate and clear
- [ ] Changelog format follows standard conventions
- [ ] Package metadata appears correct in build artifacts
- [ ] Development dependencies work as expected

---

## Phase 3: Testing Infrastructure Conversion

### Overview
Convert development testing scripts into a comprehensive pytest-based test suite with proper fixtures, coverage, and automation.

### Changes Required:

#### 1. Test Configuration
**File**: `tests/conftest.py`
**Changes**: Create pytest fixtures and configuration

```python
"""
Pytest configuration and fixtures for slack-blocks-markdown tests
"""

import pytest
from mistletoe import Document
from slack_blocks_markdown import SlackBlocksRenderer


@pytest.fixture
def renderer():
    """Provide a SlackBlocksRenderer instance for tests"""
    return SlackBlocksRenderer()


@pytest.fixture
def sample_markdown():
    """Provide standard markdown samples for testing"""
    return {
        "simple": "# Hello\n\nThis is **bold** text.",
        "complex": """# Project Update

This is a **bold** announcement with _italic_ text and `inline code`.

## Features:
- Item 1
- Item 2 with [link](https://example.com)

```python
def hello():
    return "world"
```

> Important note here

| Feature | Status |
|---------|---------|
| Auth | ✅ Done |
| API | 🚧 Progress |
""",
        "edge_cases": {
            "long_heading": "# " + "A" * 200,
            "long_paragraph": "This is very long. " * 200,
            "empty": "",
            "special_chars": "# Title with *special* ~chars~ and `code`"
        }
    }


@pytest.fixture
def expected_blocks():
    """Expected block structures for validation"""
    return {
        "header": {
            "type": "header",
            "text": {"type": "plain_text", "text": "Hello"}
        },
        "section": {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "This is *bold* text."}
        }
    }
```

#### 2. Core Renderer Tests
**File**: `tests/test_renderer.py`
**Changes**: Comprehensive test coverage based on current `test_renderer.py`

```python
"""
Tests for SlackBlocksRenderer functionality
"""

import pytest
from mistletoe import Document
from slack_blocks_markdown import SlackBlocksRenderer
from slack_sdk.models.blocks import HeaderBlock, SectionBlock, DividerBlock


class TestBasicRendering:
    """Test basic markdown element rendering"""

    def test_heading_renders_to_header_block(self, renderer):
        """Test that headings become HeaderBlocks"""
        markdown = "# Test Heading"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], HeaderBlock)
        assert blocks[0].text.text == "Test Heading"

    def test_paragraph_renders_to_section_block(self, renderer):
        """Test that paragraphs become SectionBlocks"""
        markdown = "This is a paragraph with **bold** text."
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], SectionBlock)
        assert blocks[0].text.text == "This is a paragraph with *bold* text."

    def test_horizontal_rule_renders_to_divider(self, renderer):
        """Test that horizontal rules become DividerBlocks"""
        markdown = "---"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], DividerBlock)


class TestInlineFormatting:
    """Test inline markdown formatting"""

    @pytest.mark.parametrize("markdown,expected", [
        ("**bold**", "*bold*"),
        ("_italic_", "_italic_"),
        ("`code`", "`code`"),
        ("~strikethrough~", "~strikethrough~"),
        ("[link](https://example.com)", "<https://example.com|link>"),
    ])
    def test_inline_formatting(self, renderer, markdown, expected):
        """Test various inline formatting conversions"""
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert blocks[0].text.text == expected


class TestLists:
    """Test list rendering functionality"""

    def test_unordered_list_rendering(self, renderer):
        """Test unordered list conversion"""
        markdown = "- Item 1\n- Item 2\n- Item 3"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], SectionBlock)
        assert "• Item 1" in blocks[0].text.text
        assert "• Item 2" in blocks[0].text.text
        assert "• Item 3" in blocks[0].text.text

    def test_ordered_list_rendering(self, renderer):
        """Test ordered list conversion"""
        markdown = "1. First\n2. Second\n3. Third"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], SectionBlock)
        assert "1. First" in blocks[0].text.text
        assert "2. Second" in blocks[0].text.text
        assert "3. Third" in blocks[0].text.text


class TestCodeBlocks:
    """Test code block handling"""

    def test_code_block_rendering(self, renderer):
        """Test code block formatting"""
        markdown = "```python\ndef hello():\n    return 'world'\n```"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], SectionBlock)
        assert blocks[0].text.text.startswith("```")
        assert "def hello():" in blocks[0].text.text
        assert blocks[0].text.text.endswith("```")


class TestBlockquotes:
    """Test blockquote rendering"""

    def test_simple_blockquote(self, renderer):
        """Test basic blockquote formatting"""
        markdown = "> This is a quote"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert isinstance(blocks[0], SectionBlock)
        assert blocks[0].text.text.startswith(">This is a quote")

    def test_multiline_blockquote(self, renderer):
        """Test multiline blockquote handling"""
        markdown = "> First line\n>\n> Second paragraph"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        text = blocks[0].text.text
        assert ">First line" in text
        assert ">Second paragraph" in text


class TestTables:
    """Test table rendering functionality"""

    def test_simple_table_rendering(self, renderer):
        """Test basic table conversion to TableBlock"""
        markdown = """| Name | Value |
|------|--------|
| Test | 123 |
| Demo | 456 |"""

        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        # Should be our custom TableBlock
        assert blocks[0].type == "table"
        assert len(blocks[0].rows) == 3  # Header + 2 data rows


class TestConstraints:
    """Test Slack Block Kit constraint handling"""

    def test_long_heading_truncation(self, renderer):
        """Test that long headings are truncated to 150 chars"""
        long_title = "A" * 200
        markdown = f"# {long_title}"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert len(blocks[0].text.text) <= 150
        assert blocks[0].text.text.endswith("...")

    def test_long_paragraph_truncation(self, renderer):
        """Test that long paragraphs are truncated to 3000 chars"""
        long_text = "This is a very long paragraph. " * 200
        document = Document(long_text)
        blocks = renderer.render(document)

        assert len(blocks) == 1
        assert len(blocks[0].text.text) <= 3000
        assert blocks[0].text.text.endswith("...")


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_empty_document(self, renderer):
        """Test handling of empty markdown"""
        markdown = ""
        document = Document(markdown)
        blocks = renderer.render(document)

        assert blocks == []

    def test_whitespace_only(self, renderer):
        """Test handling of whitespace-only content"""
        markdown = "   \n\n\t  \n"
        document = Document(markdown)
        blocks = renderer.render(document)

        assert blocks == []

    def test_mixed_complex_content(self, renderer):
        """Test complex mixed content document"""
        markdown = """# Main Title

This paragraph has **bold**, _italic_, and `code` formatting.

## Subsection

- First item with [link](https://example.com)
- Second item with *emphasis*

```javascript
console.log('hello world');
```

> Important note about the code above

| Feature | Status | Notes |
|---------|--------|-------|
| Auth | Done | Ready |
| API | Progress | Testing |

---

Final paragraph after divider.
"""

        document = Document(markdown)
        blocks = renderer.render(document)

        # Should generate multiple blocks of different types
        assert len(blocks) > 5

        # Check we have different block types
        block_types = [block.type for block in blocks]
        assert "header" in block_types
        assert "section" in block_types
        assert "divider" in block_types
        assert "table" in block_types
```

#### 3. Custom Blocks Tests
**File**: `tests/test_blocks.py`
**Changes**: Test custom TableBlock implementation

```python
"""
Tests for custom Slack Block implementations
"""

import pytest
from slack_blocks_markdown.blocks import TableBlock


class TestTableBlock:
    """Test custom TableBlock functionality"""

    def test_table_block_creation(self):
        """Test basic TableBlock creation"""
        rows = [
            [{"type": "raw_text", "text": "Header 1"}],
            [{"type": "raw_text", "text": "Cell 1"}]
        ]

        table = TableBlock(rows=rows)

        assert table.type == "table"
        assert len(table.rows) == 2
        assert table.rows[0][0]["text"] == "Header 1"

    def test_table_block_to_dict(self):
        """Test TableBlock serialization"""
        rows = [
            [{"type": "raw_text", "text": "Name"}, {"type": "raw_text", "text": "Value"}],
            [{"type": "raw_text", "text": "Test"}, {"type": "raw_text", "text": "123"}]
        ]

        table = TableBlock(rows=rows, block_id="test_table")
        table_dict = table.to_dict()

        assert table_dict["type"] == "table"
        assert table_dict["block_id"] == "test_table"
        assert len(table_dict["rows"]) == 2
        assert table_dict["rows"][0][0]["text"] == "Name"

    def test_table_constraints(self):
        """Test TableBlock constraint validation"""
        # Test row limit
        too_many_rows = [[{"type": "raw_text", "text": f"Row {i}"}] for i in range(101)]

        with pytest.raises(ValueError, match="cannot have more than 100 rows"):
            TableBlock(rows=too_many_rows)

        # Test column limit
        too_many_cols = [{"type": "raw_text", "text": f"Col {i}"} for i in range(21)]

        with pytest.raises(ValueError, match="cannot have more than 20 columns"):
            TableBlock(rows=[too_many_cols])

        # Test block_id length limit
        long_id = "x" * 256

        with pytest.raises(ValueError, match="cannot be longer than 255 characters"):
            TableBlock(rows=[[{"type": "raw_text", "text": "test"}]], block_id=long_id)
```

#### 4. Integration Tests
**File**: `tests/test_integration.py`
**Changes**: End-to-end testing scenarios

```python
"""
Integration tests for complete markdown to Slack blocks conversion
"""

import json
import pytest
from slack_blocks_markdown import markdown_to_blocks, SlackBlocksRenderer
from mistletoe import Document


class TestIntegrationScenarios:
    """Test complete conversion scenarios"""

    def test_readme_example(self):
        """Test the example from README works correctly"""
        markdown = """# Project Update

This is a **bold** announcement!

- Feature A completed
- Feature B in progress

Check out our [documentation](https://example.com) for details."""

        blocks = markdown_to_blocks(markdown)

        assert len(blocks) >= 3  # Header, paragraph, list
        assert blocks[0]["type"] == "header"
        assert blocks[0]["text"]["text"] == "Project Update"
        assert "*bold*" in blocks[1]["text"]["text"]

    def test_complex_document_conversion(self):
        """Test conversion of complex technical document"""
        markdown = """# API Documentation

## Authentication

All requests require authentication:

```bash
curl -H "Authorization: Bearer TOKEN" https://api.example.com
```

### Rate Limits

| Endpoint | Limit |
|----------|-------|
| /users   | 100/min |
| /data    | 50/min |

> **Important**: Store tokens securely

For more info, see our [docs](https://docs.example.com).

---

© 2025 Example Corp"""

        blocks = markdown_to_blocks(markdown)

        # Should have multiple different block types
        block_types = [block["type"] for block in blocks]
        assert "header" in block_types
        assert "section" in block_types
        assert "table" in block_types
        assert "divider" in block_types

        # Verify JSON serialization works
        json_str = json.dumps({"blocks": blocks}, indent=2)
        assert len(json_str) > 100

        # Should be valid JSON
        parsed = json.loads(json_str)
        assert "blocks" in parsed

    def test_slack_api_compatibility(self):
        """Test that output is compatible with Slack API format"""
        markdown = "# Test\n\nThis is a test message with **formatting**."

        blocks = markdown_to_blocks(markdown)

        # Each block should have required fields for Slack API
        for block in blocks:
            assert "type" in block

            if block["type"] == "header":
                assert "text" in block
                assert block["text"]["type"] == "plain_text"

            elif block["type"] == "section":
                assert "text" in block
                assert block["text"]["type"] == "mrkdwn"

    def test_error_handling_gracefully(self):
        """Test that malformed input doesn't crash"""
        test_cases = [
            "",  # Empty
            "   ",  # Whitespace only
            "# \n\n",  # Empty header
            "[]() invalid link",  # Malformed link
        ]

        for markdown in test_cases:
            # Should not raise exceptions
            blocks = markdown_to_blocks(markdown)
            assert isinstance(blocks, list)

    def test_performance_with_large_documents(self):
        """Test performance with reasonably large documents"""
        import time

        # Generate large but reasonable markdown
        large_markdown = "# Large Document\n\n"
        for i in range(100):
            large_markdown += f"## Section {i}\n\nThis is paragraph {i} with **bold** text.\n\n"
            large_markdown += f"- Item {i}a\n- Item {i}b\n\n"

        start_time = time.time()
        blocks = markdown_to_blocks(large_markdown)
        end_time = time.time()

        # Should complete reasonably quickly (under 5 seconds)
        assert (end_time - start_time) < 5.0
        assert len(blocks) > 200  # Should generate many blocks
```

### Success Criteria:

#### Automated Verification:
- [ ] All tests pass: `pytest`
- [ ] Test coverage >80%: `pytest --cov=slack_blocks_markdown --cov-report=term-missing`
- [ ] No test failures or errors: `pytest --tb=short`
- [ ] Performance tests complete within limits: `pytest tests/test_integration.py::TestIntegrationScenarios::test_performance_with_large_documents`

#### Manual Verification:
- [ ] Test suite covers all major functionality
- [ ] Edge cases are properly handled
- [ ] Error conditions fail gracefully
- [ ] Test output is clear and informative
- [ ] Coverage report identifies any gaps

---

## Phase 4: Final Polish & Verification

### Overview
Complete the library preparation with final verification, cleanup, and readiness checks for PyPI publication.

### Changes Required:

#### 1. Development Dependency Management
**File**: `requirements-dev.txt` (Optional, for development)
**Changes**: Pin development dependencies for reproducible builds

```text
# Development dependencies
pytest>=7.4.0
pytest-cov>=4.1.0
black>=23.0.0
ruff>=0.1.0
mypy>=1.5.0
build>=1.0.0
twine>=4.0.0
```

#### 2. Improved .gitignore
**File**: `.gitignore`
**Changes**: Add comprehensive Python project ignores

```text
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Testing
.tox/
.nox/
.coverage
.coverage.*
.cache
.pytest_cache/
cover/
htmlcov/

# Development
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
debug_*.py
output_*.json
edge_case_*.json
```

#### 3. Package Verification Scripts
**File**: `scripts/verify_package.py`
**Changes**: Create verification script for package quality

```python
#!/usr/bin/env python3
"""
Package verification script to ensure library is ready for publication
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, description):
    """Run a command and report results"""
    print(f"\n🔍 {description}")
    print(f"Running: {cmd}")

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ {description} - PASSED")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"❌ {description} - FAILED")
        if result.stderr:
            print(result.stderr)
        if result.stdout:
            print(result.stdout)
        return False

    return True


def main():
    """Run all verification checks"""
    checks = [
        ("python -c 'import slack_blocks_markdown; print(\"Import successful\")'", "Package Import"),
        ("python -m pytest tests/ -v", "Test Suite"),
        ("python -m pytest --cov=slack_blocks_markdown --cov-report=term-missing", "Test Coverage"),
        ("python -m ruff check src/", "Linting"),
        ("python -m black --check src/ tests/", "Code Formatting"),
        ("python -m mypy src/", "Type Checking"),
        ("python -m build", "Package Building"),
        ("python -m twine check dist/*", "Package Validation"),
    ]

    print("🚀 Starting package verification...")
    print("=" * 50)

    failed_checks = []

    for cmd, description in checks:
        if not run_command(cmd, description):
            failed_checks.append(description)

    print("\n" + "=" * 50)
    if failed_checks:
        print(f"❌ {len(failed_checks)} checks failed:")
        for check in failed_checks:
            print(f"  - {check}")
        print("\nPlease fix the issues above before publishing.")
        sys.exit(1)
    else:
        print("🎉 All checks passed! Package is ready for publication.")
        print("\nNext steps:")
        print("1. Review the built package in dist/")
        print("2. Test installation: pip install dist/*.whl")
        print("3. Publish to TestPyPI first: twine upload --repository testpypi dist/*")
        print("4. Publish to PyPI: twine upload dist/*")


if __name__ == "__main__":
    main()
```

#### 4. Documentation Enhancements
**File**: `docs/CONTRIBUTING.md`
**Changes**: Add contribution guidelines

```markdown
# Contributing to Slack Blocks Markdown

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/atacan/slack-blocks-markdown.git
cd slack-blocks-markdown
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install in development mode:
```bash
pip install -e .[dev]
```

## Running Tests

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=slack_blocks_markdown --cov-report=html
```

## Code Quality

Format code:
```bash
black src/ tests/
```

Lint code:
```bash
ruff check src/ tests/
```

Type checking:
```bash
mypy src/
```

## Making Changes

1. Create a feature branch
2. Make your changes
3. Add tests for new functionality
4. Ensure all tests pass
5. Update documentation as needed
6. Submit a pull request

## Release Process

1. Update version in `pyproject.toml` and `__init__.py`
2. Update `CHANGELOG.md`
3. Run verification script: `python scripts/verify_package.py`
4. Create a release tag
5. Publish to PyPI
```

#### 5. Clean Up Development Files
**Remove Files**: Clean up development artifacts

```bash
# Files to remove or move
rm debug_*.py
rm output_*.json
rm edge_case_*.json
```

### Success Criteria:

#### Automated Verification:
- [ ] Package builds successfully: `python -m build`
- [ ] All tests pass with coverage >80%: `pytest --cov=slack_blocks_markdown`
- [ ] Linting passes: `ruff check src/`
- [ ] Type checking passes: `mypy src/`
- [ ] Code formatting is correct: `black --check src/ tests/`
- [ ] Package validation passes: `twine check dist/*`
- [ ] Package installs from wheel: `pip install dist/*.whl`
- [ ] Verification script passes: `python scripts/verify_package.py`

#### Manual Verification:
- [ ] README instructions are accurate and complete
- [ ] Package can be imported and used as documented
- [ ] All example code works correctly
- [ ] Documentation is clear and comprehensive
- [ ] Package meets PyPI quality standards
- [ ] Version numbers are consistent across files
- [ ] License and copyright information is correct

---

## Testing Strategy

### Unit Tests:
- Individual renderer method functionality
- Custom block implementations
- Constraint validation and error handling
- Edge cases and boundary conditions

### Integration Tests:
- End-to-end markdown to blocks conversion
- Complex document scenarios
- Slack API compatibility verification
- Performance with reasonable document sizes

### Manual Testing Steps:
1. Install package in fresh environment: `pip install -e .`
2. Test basic usage from README examples
3. Test with complex markdown documents
4. Verify output in Slack Block Kit Builder
5. Check package builds and installs correctly
6. Confirm all development tools work as expected

## Performance Considerations

- Single-pass processing maintains efficiency
- Constraint enforcement prevents resource issues
- Memory usage scales linearly with document size
- Processing time remains reasonable for typical documents

## Migration Notes

**Backward Compatibility:**
- Public API remains identical to current implementation
- Import paths change but old usage patterns still work via convenience functions
- All existing functionality preserved

**Development Workflow Changes:**
- Replace `python test_renderer.py` with `pytest`
- Replace manual testing with automated test suite
- Use build tools instead of direct file copying

## References

- Original research: `thoughts/shared/research/2025-08-29_08-55-13_python_library_conversion.md`
- Core implementation: `slack_blocks_renderer.py:1-519`
- Current usage examples: `example_usage.py:10-25`
- Development testing approach: `test_renderer.py:14-153`
- PyPI packaging guide: https://packaging.python.org/
- Slack Block Kit documentation: https://api.slack.com/block-kit
