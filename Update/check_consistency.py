#!/usr/bin/env python3
"""
DATEYE Documentation Consistency Checker
Verifies that index.md links match existing documentation files
"""

import re
from pathlib import Path

def extract_links_from_index():
    """Extract all .md file links from index.md"""
    index_path = Path("../index.md")
    if not index_path.exists():
        return [], ["ERROR: index.md not found!"]
    
    content = index_path.read_text(encoding='utf-8')
    
    # Find all markdown links: [text](file.md)
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
    
    return files, []

def find_all_markdown_files():
    """Find all .md files in the docs directory"""
    doc_root = Path("..")
    md_files = []
    
    # Define directories to scan
    scan_dirs = [
        ".",
        "adapters",
        "architecture", 
        "ui-design",
        "ui-design/dashboard",
        "ui-design/connections",
        "ui-design/history",
        "ui-design/settings",
        "ui-design/eye-office-setup",
        "ui-design/identity-key-dialog",
        "ui-design/logo",
        "external-apis",
        "external-apis/eye-office",
        "external-apis/mediworks", 
        "external-apis/zeiss",
        "../development"
    ]
    
    for scan_dir in scan_dirs:
        dir_path = doc_root / scan_dir
        if dir_path.exists():
            for md_file in dir_path.glob("*.md"):
                # Get relative path from docs root
                try:
                    if scan_dir == "../development":
                        rel_path = f"../development/{md_file.name}"
                    elif scan_dir == ".":
                        rel_path = md_file.name
                    else:
                        rel_path = f"{scan_dir}/{md_file.name}"
                    
                    # Skip generated files
                    if md_file.name not in ["summary.txt"]:
                        md_files.append(rel_path)
                except Exception as e:
                    print(f"Warning: Could not process {md_file}: {e}")
    
    return sorted(list(set(md_files)))

def check_consistency():
    """Check consistency between index.md and existing files"""
    print("🔍 DATEYE Documentation Consistency Check")
    print("=" * 45)
    print()
    
    # Get linked files from index.md
    linked_files, errors = extract_links_from_index()
    if errors:
        for error in errors:
            print(f"❌ {error}")
        return False
    
    # Get all existing .md files
    existing_files = find_all_markdown_files()
    
    print(f"📋 Found {len(linked_files)} files linked in index.md")
    print(f"📁 Found {len(existing_files)} .md files in filesystem")
    print()
    
    # Check for broken links (linked but not existing)
    doc_root = Path("..")
    broken_links = []
    for linked_file in linked_files:
        file_path = doc_root / linked_file
        if not file_path.exists():
            broken_links.append(linked_file)
    
    # Check for missing links (existing but not linked)
    missing_links = []
    for existing_file in existing_files:
        # Skip excluded patterns
        should_exclude = False
        
        # Check specific exclusions
        if existing_file in ["README.md", "index.md"]:
            should_exclude = True
        # Check directory patterns  
        elif "/README.md" in existing_file or "Update/" in existing_file:
            should_exclude = True
        # Exclude Chinese duplicates (we link English versions)
        elif existing_file.endswith("-ZH.md") or existing_file.endswith("-zh.md"):
            should_exclude = True
            
        if should_exclude:
            continue
            
        if existing_file not in linked_files:
            missing_links.append(existing_file)
    
    # Report results
    all_good = True
    
    if broken_links:
        print("❌ BROKEN LINKS (in index.md but file doesn't exist):")
        for link in broken_links:
            print(f"   • {link}")
        print()
        all_good = False
    
    if missing_links:
        print("⚠️  MISSING LINKS (file exists but not in index.md):")
        for link in missing_links:
            print(f"   • {link}")
        print()
        all_good = False
    
    if all_good:
        print("✅ All documentation files are properly linked!")
        print()
        return True
    else:
        print("🔧 ACTION REQUIRED:")
        if broken_links:
            print("   1. Remove broken links from index.md or create missing files")
        if missing_links:
            print("   2. Add missing files to appropriate sections in index.md")
        print("   3. Run 'dateye' again to update summary.txt")
        print()
        return False

if __name__ == "__main__":
    success = check_consistency()
    exit(0 if success else 1)
