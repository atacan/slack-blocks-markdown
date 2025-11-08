# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2025-11-08

### Breaking
- Lists, block quotes, and fenced code blocks now render as Slack `rich_text` blocks instead of `section` blocks; update any consumers that expected only `section` blocks from the renderer or `markdown_to_blocks`

### Added
- `markdown_to_block_objects` convenience helper for retrieving editable Slack `Block` instances before serialization
- Optional `expand_sections` parameter on both convenience helpers and the renderer to control Slack's section expansion behaviour
- New examples and documentation showing how to edit generated blocks, mix manual blocks, and use the renderer directly
- Extended test coverage for the new APIs, rich text outputs, and expand behaviour

### Changed
- List rendering now produces proper Slack rich text lists with nesting, ordered-list offsets, and inline styling
- Code blocks and block quotes emit rich text elements that match Slack's native formatting

## [0.1.1] - 2024-10-26

### Fixed
- Corrected CHANGELOG date for initial release
- Updated package metadata

## [0.1.0] - 2024-10-26

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

[Unreleased]: https://github.com/atacan/slack-blocks-markdown/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/atacan/slack-blocks-markdown/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/atacan/slack-blocks-markdown/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/atacan/slack-blocks-markdown/releases/tag/v0.1.0
