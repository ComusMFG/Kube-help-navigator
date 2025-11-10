#!/usr/bin/env python3
"""
Fix relative paths in extracted HTML help files.
"""

import os
import re
from pathlib import Path

def fix_html_paths(html_content, filename):
    """Fix relative paths in HTML content."""

    # Fix image references - patterns like ../images/file or ../../images/file
    # Change to ../images/filename
    html_content = re.sub(
        r'(src|href)=["\'](\.\./)+([^"\']*\.(gif|jpg|jpeg|png|bmp|ico))["\']',
        lambda m: f'{m.group(1)}="../images/{os.path.basename(m.group(3))}"',
        html_content,
        flags=re.IGNORECASE
    )

    # Fix references to other HTML files in subdirectories
    # Pattern: ../SomeFolder/file.htm -> _GUID.htm (we need to find the right file)
    # For now, we'll keep them as relative but strip the directory structure

    # Fix links to HTML files - change ../Folder/file.htm to ../pages/_GUID
    # This is tricky because we don't have the mapping. Let's just fix the obvious ones

    # Fix base tag if present - remove or update it
    html_content = re.sub(
        r'<base\s+target=["\'][^"\']*["\']>',
        '',
        html_content,
        flags=re.IGNORECASE
    )

    return html_content

def main():
    base_dir = Path("/home/user/Kube-help-navigator")
    pages_dir = base_dir / "docs" / "pages"

    print("Fixing HTML file paths...")

    fixed_count = 0
    for html_file in pages_dir.glob("_*"):
        try:
            # Read the file
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Fix paths
            fixed_content = fix_html_paths(content, html_file.name)

            # Write back
            if fixed_content != content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                fixed_count += 1

        except Exception as e:
            print(f"Error processing {html_file.name}: {e}")

    print(f"\n✓ Fixed {fixed_count} HTML files")
    print("✓ Image paths updated to ../images/")
    print("✓ Removed problematic base tags")

if __name__ == "__main__":
    main()
