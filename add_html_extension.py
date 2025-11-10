#!/usr/bin/env python3
"""
Rename all HTML files to have .html extension and update all links.
"""

import os
import re
from pathlib import Path

def main():
    base_dir = Path("/home/user/Kube-help-navigator")
    pages_dir = base_dir / "docs" / "pages"

    print("Renaming HTML files to add .html extension...")

    # Step 1: Rename all files to add .html extension
    renamed_files = {}
    for file in pages_dir.glob("_*"):
        if not file.name.endswith('.html'):
            new_name = file.name + ".html"
            new_path = file.parent / new_name
            file.rename(new_path)
            renamed_files[file.name] = new_name

    print(f"✓ Renamed {len(renamed_files)} files")

    # Step 2: Update index.html to use .html extensions
    print("\nUpdating index.html...")
    index_path = base_dir / "docs" / "index.html"

    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update links: pages/GUID to pages/GUID.html
    content = re.sub(
        r'href="pages/(_[^"]+)"',
        r'href="pages/\1.html"',
        content
    )

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✓ Updated index.html links")

    # Step 3: Update internal links in HTML files
    print("\nUpdating internal links in HTML files...")
    fixed_count = 0

    for html_file in pages_dir.glob("*.html"):
        try:
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            original = content

            # Update any links to other pages that don't have .html
            # Pattern: href="GUID" or href="../pages/GUID" where GUID starts with _
            content = re.sub(
                r'href="(_[A-F0-9]+)"',
                r'href="\1.html"',
                content
            )

            if content != original:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_count += 1

        except Exception as e:
            print(f"Error processing {html_file.name}: {e}")

    print(f"✓ Updated {fixed_count} HTML files with internal links")

    print("\n" + "="*60)
    print("✓ All files renamed with .html extension")
    print("✓ Index links updated")
    print("✓ Internal links updated")
    print("\nThe documentation should now render properly in browsers!")

if __name__ == "__main__":
    main()
