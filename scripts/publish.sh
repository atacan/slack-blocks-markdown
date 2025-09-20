#!/bin/bash

# Publish to PyPI (production)
# ⚠️  WARNING: This publishes to the real PyPI! Make sure you've tested with TestPyPI first.

set -e

echo "🚀 Publishing to PyPI (PRODUCTION)..."
echo ""
echo "⚠️  WARNING: You are about to publish to the REAL PyPI!"
echo "   Make sure you have tested your package with TestPyPI first."
echo ""
read -p "Are you sure you want to continue? (y/n): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    exit 1
fi

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

# Upload to PyPI
echo "⬆️  Uploading to PyPI..."
python -m twine upload $INTERACTIVE_FLAG dist/*

echo ""
echo "🎉 Package published to PyPI!"
echo ""
echo "🔗 View your package at:"
echo "   https://pypi.org/project/slack-blocks-markdown/"
echo ""
echo "✅ Users can now install with:"
echo "   pip install slack-blocks-markdown"