#!/bin/bash

# Package verification script
# Run this script to verify your package before publishing

set -e

echo "🔍 Verifying slack-blocks-markdown package..."

# Check if package is built
if [ ! -d "dist" ] || [ -z "$(ls -A dist 2>/dev/null)" ]; then
    echo "❌ No built package found in dist/"
    echo "   Run ./scripts/build.sh first"
    exit 1
fi

echo ""
echo "📋 Checking built distributions..."
ls -la dist/

echo ""
echo "🔧 Running twine check..."
python -m twine check dist/*

echo ""
echo "📦 Package contents:"
echo "--- Wheel contents ---"
python -m zipfile -l dist/*.whl 2>/dev/null || echo "No wheel file found"

echo ""
echo "--- Tarball contents ---" 
tar -tzf dist/*.tar.gz 2>/dev/null || echo "No tarball file found"

echo ""
echo "🧪 Testing package installation..."

# Create a temporary virtual environment
TEMP_VENV=$(mktemp -d)
echo "Creating temporary venv at: $TEMP_VENV"

python -m venv "$TEMP_VENV"
source "$TEMP_VENV/bin/activate"

# Install the built package
echo "Installing built package..."
pip install --upgrade pip
pip install dist/*.whl

echo ""
echo "🧪 Testing basic imports..."
python -c "
import slack_blocks_markdown
print('✅ slack_blocks_markdown import successful')

from slack_blocks_markdown import markdown_to_blocks, SlackBlocksRenderer  
print('✅ Main imports successful')

# Test basic functionality
blocks = markdown_to_blocks('# Test\\n\\nThis is a **test**.')
print(f'✅ Basic functionality works (generated {len(blocks)} blocks)')
"

# Test with dependencies
echo ""
echo "🧪 Testing dependencies..."
python -c "
import mistletoe
import slack_sdk.models.blocks
print('✅ All dependencies available')
"

# Cleanup
deactivate
rm -rf "$TEMP_VENV"

echo ""
echo "🎉 Package verification complete!"
echo ""
echo "📋 Summary:"
echo "  ✅ Package builds successfully"
echo "  ✅ Package structure is correct"  
echo "  ✅ Package installs without errors"
echo "  ✅ Basic functionality works"
echo "  ✅ All dependencies are available"
echo ""
echo "🚀 Your package is ready for publishing!"
echo ""
echo "📋 Next steps:"
echo "  • Test publish: ./scripts/publish-test.sh"
echo "  • Publish to PyPI: ./scripts/publish.sh"