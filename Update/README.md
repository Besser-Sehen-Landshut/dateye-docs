# DATEYE Documentation Update System

## Purpose
Generates `summary.txt` from all documentation files linked in `index.md`.

## Usage
```bash
./update.sh
```

## How it works
1. Reads `/docs/index.md` to find all linked `.md` files
2. Collects content from each linked file
3. Generates `summary.txt` with all documentation
4. Opens the file for review (macOS only)

## Files
- `update.sh` - Main script to run
- `generate_summary.py` - Python script that does the work
- This README

## Why this approach?
- **Single Source of Truth**: `index.md` defines what's included
- **No redundancy**: Only files actually linked are included
- **Simple**: One script, one purpose
- **Maintainable**: Update `index.md`, run script, done

## Session Continuity
After running the update, upload the generated `summary.txt` to your Claude Project to maintain context across sessions.
