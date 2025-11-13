# Publishing Guide for slack-blocks-markdown

This guide covers everything you need to know about publishing the `slack-blocks-markdown` package to PyPI.

## Table of Contents

1. [Initial PyPI Setup](#initial-pypi-setup)
2. [Local Publishing](#local-publishing)
3. [GitHub Actions Publishing](#github-actions-publishing)
4. [Version Management](#version-management)
5. [Troubleshooting](#troubleshooting)

## Initial PyPI Setup

### 1. Create PyPI Accounts

You'll need accounts on both PyPI and TestPyPI:

1. **TestPyPI** (for testing): https://test.pypi.org/account/register/
2. **PyPI** (production): https://pypi.org/account/register/

### 2. Generate API Tokens

For security, use API tokens instead of passwords:

#### For TestPyPI:
1. Go to https://test.pypi.org/manage/account/token/
2. Click "Add API token"
3. Name: `slack-blocks-markdown-token`
4. Scope: "Entire account" (or limit to your project once published)
5. Copy the token (starts with `pypi-...`)

#### For PyPI:
1. Go to https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Name: `slack-blocks-markdown-token`
4. Scope: "Entire account" (or limit to your project once published)
5. Copy the token (starts with `pypi-...`)

### 3. Install Required Tools

```bash
# Install build and publishing tools
pip install build twine
```

## Local Publishing

### Method 1: Using Scripts (Recommended)

We've provided convenient scripts for local publishing:

#### Step 1: Build the Package
```bash
./scripts/build.sh
```

#### Step 2: Test on TestPyPI
```bash
./scripts/publish-test.sh
```

#### Step 3: Publish to PyPI
```bash
./scripts/publish.sh
```

### Method 2: Manual Commands

If you prefer manual control:

#### Build
```bash
# Clean previous builds
rm -rf dist/ build/ src/*.egg-info/

# Build the package
python -m build
```

#### Publish to TestPyPI
```bash
python -m twine upload --repository testpypi dist/*
```

#### Publish to PyPI
```bash
python -m twine upload dist/*
```

### Authentication Options

#### Option 1: Environment Variables (Recommended)
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-token-here

# Add to your ~/.bashrc or ~/.zshrc for persistence
echo 'export TWINE_USERNAME=__token__' >> ~/.bashrc
echo 'export TWINE_PASSWORD=pypi-your-token-here' >> ~/.bashrc
```

#### Option 2: Interactive Mode
The scripts will prompt for credentials if environment variables aren't set.

#### Option 3: Configuration File
Create `~/.pypirc`:
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-production-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-token-here
```

## GitHub Actions Publishing

### Setup GitHub Secrets

Add these secrets to your GitHub repository:

1. Go to your repository on GitHub
2. Settings → Secrets and variables → Actions
3. Add the following secrets:
   - `PYPI_API_TOKEN`: Your production PyPI token
   - `TESTPYPI_API_TOKEN`: Your TestPyPI token

### Publishing Methods

#### Method 1: Manual Dispatch
1. Go to Actions tab in your GitHub repository
2. Select "Publish to PyPI" workflow
3. Click "Run workflow"
4. Choose environment (testpypi or pypi)

#### Method 2: Automatic on Tags (Recommended for Releases)
1. **Ensure version is bumped** in `pyproject.toml`
2. **Create and push a git tag**:
```bash
git tag v0.2.0
git push origin v0.2.0
```
3. GitHub Actions will automatically:
   - Publish to PyPI (production)
   - Create a GitHub release

> **📝 Note**: This is the standard way to release. The workflow ONLY triggers on tags, not on commits or PR merges. After merging a PR with a version bump, remember to create and push the corresponding tag.

### Testing the Workflow

1. First, test with TestPyPI:
   - Use manual dispatch with "testpypi" environment
   - Verify package appears at https://test.pypi.org/project/slack-blocks-markdown/

2. Then publish to PyPI:
   - Use manual dispatch with "pypi" environment, or
   - Create a version tag for automatic publishing

## Version Management

### Updating Version

1. **Edit pyproject.toml**:
```toml
[project]
version = "0.2.0"  # Update this
```

2. **Update CHANGELOG.md** with new features/fixes

3. **Commit changes**:
```bash
git add pyproject.toml CHANGELOG.md
git commit -m "Bump version to 0.2.0"
```

4. **Create and push tag** (for automatic publishing):
```bash
git tag v0.2.0
git push origin main
git push origin v0.2.0
```

> **⚠️ IMPORTANT**: After merging a PR with a version bump, you MUST create and push a git tag to trigger the PyPI publish workflow. Simply bumping the version number and merging is NOT enough - the workflow only triggers on tags matching the pattern `v*`.
>
> If you forget to create the tag, the package will not be published to PyPI automatically. You'll need to create and push the tag manually (as shown above) to trigger the workflow.

### Version Numbering Guidelines

Follow [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH` (e.g., 1.2.3)
- `MAJOR`: Breaking changes
- `MINOR`: New features (backward compatible)
- `PATCH`: Bug fixes (backward compatible)

## Troubleshooting

### Common Issues

#### PyPI Publish Workflow Didn't Trigger After Merging PR
**Symptom**: You merged a PR with a version bump, but the PyPI publish workflow didn't run.

**Cause**: The workflow only triggers on git tags matching `v*` pattern, not on regular commits or merges.

**Solution**:
```bash
# Create the tag for the version in pyproject.toml
git tag v0.2.0
# Push the tag to trigger the workflow
git push origin v0.2.0
```

The workflow will then:
- Build the package
- Publish to PyPI
- Create a GitHub release

#### "File already exists" Error
- PyPI doesn't allow re-uploading the same version
- Increment the version number in `pyproject.toml`
- Build and upload again

#### Authentication Errors
- Check that your API token is correct
- Ensure token has the right scope
- For TestPyPI, make sure you're using the TestPyPI token

#### Build Errors
```bash
# Clean everything and rebuild
rm -rf dist/ build/ src/*.egg-info/
pip install --upgrade build twine
python -m build
```

#### Permission Denied on Scripts
```bash
chmod +x scripts/*.sh
```

### Verification Steps

#### Verify Package Before Publishing
```bash
# Check the built package
python -m twine check dist/*

# Install and test locally
pip install dist/slack_blocks_markdown-*.whl
python -c "from slack_blocks_markdown import markdown_to_blocks; print('✅ Import works')"
```

#### Test Installation from TestPyPI
```bash
pip install --index-url https://test.pypi.org/simple/ slack-blocks-markdown
```

#### Test Installation from PyPI
```bash
pip install slack-blocks-markdown
```

### Getting Help

- **PyPI Help**: https://pypi.org/help/
- **Packaging Guide**: https://packaging.python.org/
- **GitHub Actions**: https://docs.github.com/en/actions

### Security Best Practices

1. **Never commit API tokens** to version control
2. **Use scoped tokens** when possible
3. **Regularly rotate tokens**
4. **Use GitHub secrets** for CI/CD
5. **Test on TestPyPI first** before production

## Quick Reference

### Local Publishing Workflow
```bash
# 1. Update version in pyproject.toml
# 2. Build and test
./scripts/build.sh
./scripts/publish-test.sh

# 3. Verify on TestPyPI, then publish
./scripts/publish.sh
```

### GitHub Actions Workflow
```bash
# For testing
# Use manual dispatch → testpypi

# For release (REQUIRED after version bump)
# 1. Update version in pyproject.toml and merge PR
# 2. Create and push tag:
git tag v0.2.0
git push origin v0.2.0
# → Automatic PyPI publish + GitHub release
```

**Remember**: The tag is what triggers the publish workflow, not the PR merge!

### Important URLs
- **PyPI Project**: https://pypi.org/project/slack-blocks-markdown/
- **TestPyPI Project**: https://test.pypi.org/project/slack-blocks-markdown/
- **GitHub Repository**: https://github.com/atacan/slack-blocks-markdown
