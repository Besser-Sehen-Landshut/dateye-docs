#!/bin/bash
# DATEYE Global Command
# Usage: dateye [command]
#
# Commands:
#   docs    - Update documentation summary (default)
#   help    - Show this help

DATEYE_ROOT="/Users/culfin/Documents/Projekte/Dateye"
DOCS_UPDATE="$DATEYE_ROOT/docs/Update"

case "${1:-docs}" in
    docs|update)
        echo "🔄 Updating DATEYE documentation..."
        cd "$DOCS_UPDATE" && ./update.sh
        ;;
    help|--help|-h)
        echo "DATEYE Command Line Tool"
        echo ""
        echo "Usage: dateye [command]"
        echo ""
        echo "Commands:"
        echo "  docs    Update documentation summary (default)"
        echo "  help    Show this help"
        ;;
    *)
        echo "Unknown command: $1"
        echo "Run 'dateye help' for available commands"
        exit 1
        ;;
esac