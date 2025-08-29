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