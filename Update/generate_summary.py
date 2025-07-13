#!/usr/bin/env python3
"""
DATEYE Documentation Summary Generator
Reads all files linked in index.md and generates summary.txt
"""

import re
from pathlib import Path
from datetime import datetime

def extract_links_from_index():
    """Extract all .md file links from index.md"""
    index_path = Path("../index.md")
    if not index_path.exists():
        raise FileNotFoundError("index.md not found!")
    
    content = index_path.read_text(encoding='utf-8')
    
    # Find all markdown links: [text](file.md)
    # Also find relative paths like adapters/file.md
    pattern = r'\[([^\]]+)\]\(([^)]+\.md)\)'
    matches = re.findall(pattern, content)
    
    files = []
    for text, link in matches:
        # Skip external URLs
        if link.startswith('http'):
            continue
        # Skip anchors
        if '#' in link:
            link = link.split('#')[0]
        # Clean up link
        link = link.strip()
        if link and link not in files:
            files.append(link)
    
    return files

def clean_content(content):
    """Basic cleaning: remove excessive whitespace, normalize line endings"""
    # Normalize line endings
    content = content.replace('\r\n', '\n')
    # Remove trailing whitespace
    lines = [line.rstrip() for line in content.split('\n')]
    # Join back
    return '\n'.join(lines)

def main():
    print("DATEYE Documentation Summary Generator")
    print("-" * 40)
    
    # Get all linked files from index.md
    try:
        linked_files = extract_links_from_index()
        print(f"Found {len(linked_files)} files in index.md")
    except Exception as e:
        print(f"Error reading index.md: {e}")
        return 1
    
    # Collect content
    doc_root = Path("..")
    all_content = []
    
    # Header
    all_content.append("DATEYE DOCUMENTATION SUMMARY")
    all_content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    all_content.append("=" * 50)
    
    # Process each file
    processed = 0
    for file_path in linked_files:
        full_path = doc_root / file_path
        
        if full_path.exists():
            try:
                content = full_path.read_text(encoding='utf-8')
                content = clean_content(content)
                
                all_content.append("")
                all_content.append("")
                all_content.append(f"FILE: {file_path}")
                all_content.append("=" * 50)
                all_content.append("")
                all_content.append(content)
                
                processed += 1
                print(f"  ✓ {file_path} ({len(content)//1024}KB)")
            except Exception as e:
                print(f"  ✗ {file_path} - Error: {e}")
        else:
            print(f"  ✗ {file_path} - Not found")
    
    # Footer
    all_content.append("")
    all_content.append("")
    all_content.append("=" * 50)
    all_content.append("END OF DOCUMENTATION")
    all_content.append(f"Total files: {processed}")
    all_content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Write summary
    summary_content = '\n'.join(all_content)
    output_path = doc_root / "summary.txt"
    
    try:
        output_path.write_text(summary_content, encoding='utf-8')
        size_kb = len(summary_content) // 1024
        print(f"\n✓ Created: summary.txt ({size_kb}KB)")
        print(f"  Tokens: ~{len(summary_content)//4}")
    except Exception as e:
        print(f"\n✗ Error writing summary.txt: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
