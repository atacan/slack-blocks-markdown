#!/bin/bash

# Publish to TestPyPI (testing environment)
# Use this script to test your package before publishing to the real PyPI

set -e

echo "🧪 Publishing to TestPyPI..."

# Check if TWINE_USERNAME and TWINE_PASSWORD are set
if [[ -z "$TWINE_USERNAME" && -z "$TWINE_PASSWORD" ]]; then
    echo "⚠️  Environment variables not set. You can either:"
    echo "   1. Set TWINE_USERNAME and TWINE_PASSWORD environment variables"
    echo "   2. Use --interactive flag to enter credentials manually"
    echo ""
    read -p "Do you want to proceed interactively? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Cancelled"
        exit 1
    fi
    INTERACTIVE_FLAG="--interactive"
else
    echo "✅ Using environment variables for authentication"
    INTERACTIVE_FLAG=""
fi

# Build first if no dist folder exists
if [ ! -d "dist" ] || [ -z "$(ls -A dist)" ]; then
    echo "📦 No built package found. Building first..."
    ./scripts/build.sh
fi

# Upload to TestPyPI
echo "⬆️  Uploading to TestPyPI..."
python -m twine upload $INTERACTIVE_FLAG --repository testpypi dist/*

echo ""
echo "✅ Package published to TestPyPI!"
echo ""
echo "🔗 View your package at:"
echo "   https://test.pypi.org/project/slack-blocks-markdown/"
echo ""
echo "🧪 Test installation with:"
echo "   pip install --index-url https://test.pypi.org/simple/ slack-blocks-markdown"
echo ""
echo "📋 If everything works, publish to real PyPI with:"
echo "   ./scripts/publish.sh"