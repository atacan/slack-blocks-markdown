#!/bin/bash

# Build script for slack-blocks-markdown package
# This script builds the package for distribution

set -e

echo "🔨 Building slack-blocks-markdown package..."

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ src/*.egg-info/

# Create dist directory
mkdir -p dist

# Build the package
echo "📦 Building package..."
python -m build

# List built files
echo "✅ Build complete! Files created:"
ls -la dist/

echo ""
echo "📋 Next steps:"
echo "  • Test your package: scripts/verify-package.sh"
echo "  • Publish to TestPyPI: scripts/publish-test.sh"
echo "  • Publish to PyPI: scripts/publish.sh"
