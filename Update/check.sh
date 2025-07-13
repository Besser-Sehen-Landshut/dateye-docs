#!/bin/bash
# DATEYE Documentation Consistency Check Only
# Quick check without generating summary.txt

cd "$(dirname "$0")"

echo "🔍 DATEYE Documentation Consistency Check"
echo "========================================="
echo ""

python3 check_consistency.py

if [ $? -eq 0 ]; then
    echo "🎉 All good! Documentation is consistent."
    echo ""
    echo "Run 'dateye' to update summary.txt"
else
    echo ""
    echo "🔧 Fix the issues above, then run 'dateye' to update summary.txt"
fi
