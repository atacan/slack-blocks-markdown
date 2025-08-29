"""
Pytest configuration and fixtures for slack-blocks-markdown tests
"""

import pytest

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
            "special_chars": "# Title with *special* ~chars~ and `code`",
        },
    }


@pytest.fixture
def expected_blocks():
    """Expected block structures for validation"""
    return {
        "header": {
            "type": "header",
            "text": {"type": "plain_text", "text": "Hello"},
        },
        "section": {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "This is *bold* text."},
        },
    }
