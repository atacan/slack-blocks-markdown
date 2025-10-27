# Release 0.1.1 - Pre-Release Checklist

This document outlines the changes needed before publishing version 0.1.1 to PyPI.

## Critical Changes Required

### 1. Update Version Number
**File**: `pyproject.toml`
- **Line 7**: Change `version = "0.1.0"` to `version = "0.1.1"`

### 2. Fix CHANGELOG Date
**File**: `CHANGELOG.md`
- **Line 10**: Change `## [0.1.0] - 2025-08-29` to `## [0.1.0] - 2024-10-26`
- Add new section for 0.1.1:
  ```markdown
  ## [0.1.1] - 2024-10-26

  ### Fixed
  - Corrected CHANGELOG date for initial release
  - Updated package metadata

  ## [0.1.0] - 2024-10-26
  ```
- Update version links at bottom of file:
  ```markdown
  [Unreleased]: https://github.com/atacan/slack-blocks-markdown/compare/v0.1.1...HEAD
  [0.1.1]: https://github.com/atacan/slack-blocks-markdown/releases/tag/v0.1.1
  [0.1.0]: https://github.com/atacan/slack-blocks-markdown/releases/tag/v0.1.0
  ```

## Optional Improvements

### 3. Update License Format in pyproject.toml
**File**: `pyproject.toml`
- **Line 10-11**: Replace:
  ```toml
  license = "MIT"
  license-files = ["LICENSE"]
  ```
  With:
  ```toml
  license = {file = "LICENSE"}
  ```
  This uses the newer PEP 621 format and prevents the full license text from appearing in PyPI metadata.

### 4. Add Type Checking Support (Optional)
**Action**: Create a new file `src/slack_blocks_markdown/py.typed` (empty file)
- This signals to type checkers that your package includes type hints
- Command: `touch src/slack_blocks_markdown/py.typed`

### 5. Fix GitHub Actions Workflow
**File**: `.github/workflows/publish.yml`
- **Line 84**: The `actions/create-release@v1` action is deprecated
- **Recommended**: Replace with `softprops/action-gh-release@v1` for better maintenance:
  ```yaml
  - name: Create GitHub Release
    if: github.event_name == 'push' && steps.target.outputs.repository == 'pypi'
    uses: softprops/action-gh-release@v1
    with:
      name: Release ${{ github.ref_name }}
      body: |
        ## Changes

        See [CHANGELOG.md](https://github.com/atacan/slack-blocks-markdown/blob/main/CHANGELOG.md) for details.

        ## Installation

        ```bash
        pip install slack-blocks-markdown==${{ github.ref_name }}
        ```
      draft: false
      prerelease: false
    env:
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  ```

## Testing Before Release

### Test Installation from Test PyPI
Before publishing to production, test that the package installs correctly:

```bash
# Create a test environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from Test PyPI with production PyPI as fallback for dependencies
pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ \
            slack-blocks-markdown

# Test the package
python -c "from slack_blocks_markdown import markdown_to_blocks; print(markdown_to_blocks('# Test'))"

# Cleanup
deactivate
rm -rf test_env
```

### Verify Package Build
```bash
# Clean previous builds
rm -rf dist/ build/ src/*.egg-info

# Build new package
python -m build

# Check distribution
python -m twine check dist/*

# Verify contents
tar -tzf dist/slack_blocks_markdown-0.1.1.tar.gz
```

## Release Process

### Option 1: Manual Release via GitHub Actions
1. Go to Actions tab in GitHub
2. Select "Publish to PyPI" workflow
3. Click "Run workflow"
4. Select branch: `main`
5. Select environment: `pypi`
6. Click "Run workflow"

### Option 2: Tag-Based Release (Recommended)
```bash
# Commit all changes
git add .
git commit -m "chore: prepare for v0.1.1 release"
git push origin main

# Create and push tag
git tag v0.1.1
git push origin v0.1.1
```
This will automatically trigger the publish workflow.

## Post-Release Verification

1. **Check PyPI page**: Visit https://pypi.org/project/slack-blocks-markdown/
2. **Verify badges work**: Check that README badges display correctly
3. **Test installation**: `pip install slack-blocks-markdown==0.1.1`
4. **Check GitHub Release**: Verify release was created at https://github.com/atacan/slack-blocks-markdown/releases

## Summary Checklist

- [ ] Update version to 0.1.1 in `pyproject.toml`
- [ ] Fix CHANGELOG date and add 0.1.1 entry
- [ ] (Optional) Update license format in `pyproject.toml`
- [ ] (Optional) Add `py.typed` file
- [ ] (Optional) Fix deprecated GitHub Action
- [ ] Clean and rebuild package
- [ ] Test package with `twine check`
- [ ] Test installation from Test PyPI
- [ ] Commit and push changes
- [ ] Create and push v0.1.1 tag
- [ ] Verify release on PyPI
- [ ] Verify GitHub Release created

## Notes

- Version 0.1.0 is already published to PyPI, so we cannot republish that version
- All changes above are backward compatible
- The package structure and code are production-ready
- No code changes are required, only metadata updates
