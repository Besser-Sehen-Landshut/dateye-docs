#!/bin/bash
# DATEYE Documentation Update Script
# Checks consistency and generates summary.txt

cd "$(dirname "$0")"

echo "DATEYE Documentation Update"
echo "---------------------------"
echo ""

# First check consistency
echo "🔍 Checking documentation consistency..."
python3 check_consistency.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Consistency check failed!"
    echo "   Please fix the issues above before updating summary.txt"
    echo ""
    exit 1
fi

echo "✅ Consistency check passed!"
echo ""

# Run the summary generator
echo "📝 Generating summary.txt..."
python3 generate_summary.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Update complete!"
    echo ""
    echo "Next steps:"
    echo "1. Review summary.txt"
    echo "2. Upload to Claude Projects for session continuity"
    
    # Open the file (macOS)
    if [ -f ../summary.txt ] && [[ "$OSTYPE" == "darwin"* ]]; then
        open ../summary.txt
    fi
else
    echo ""
    echo "✗ Summary generation failed! Check the errors above."
    exit 1
fi
