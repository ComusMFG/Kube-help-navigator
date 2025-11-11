#!/usr/bin/env python3
"""
Fix image display issues by:
1. Adding proper extensions to image files
2. Attempting to map GUID filenames to original names referenced in HTML
"""

import os
import re
import subprocess
from pathlib import Path
from collections import defaultdict

def get_file_extension(filepath):
    """Determine file extension based on file type."""
    try:
        result = subprocess.run(['file', '--mime-type', '-b', filepath],
                              capture_output=True, text=True)
        mime_type = result.stdout.strip()

        mime_to_ext = {
            'image/gif': '.gif',
            'image/jpeg': '.jpg',
            'image/png': '.png',
            'image/bmp': '.bmp',
            'image/x-icon': '.ico',
            'image/vnd.microsoft.icon': '.ico'
        }

        return mime_to_ext.get(mime_type, '')
    except Exception as e:
        print(f"Error checking {filepath}: {e}")
        return ''

def extract_image_references(html_dir):
    """Extract all image references from HTML files."""
    image_refs = set()
    pattern = re.compile(r'src=["\']\.\.\/images\/([^"\']+)["\']', re.IGNORECASE)

    for html_file in Path(html_dir).glob('*.html'):
        try:
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                matches = pattern.findall(content)
                image_refs.update(matches)
        except Exception as e:
            print(f"Error reading {html_file}: {e}")

    return image_refs

def main():
    base_dir = Path("/home/user/Kube-help-navigator")
    images_dir = base_dir / "docs" / "images"
    pages_dir = base_dir / "docs" / "pages"

    print("Step 1: Adding file extensions to images based on file type...")
    print("-" * 60)

    # First, add extensions to all image files
    extension_counts = defaultdict(int)
    renamed_files = {}

    for img_file in sorted(images_dir.glob("_*")):
        if '.' in img_file.name:  # Already has extension
            continue

        ext = get_file_extension(img_file)
        if ext:
            new_name = img_file.name + ext
            new_path = img_file.parent / new_name

            # Store the renaming
            renamed_files[img_file.name] = new_name

            # Rename the file
            img_file.rename(new_path)
            extension_counts[ext] += 1

    print(f"✓ Added extensions to {sum(extension_counts.values())} image files:")
    for ext, count in sorted(extension_counts.items()):
        print(f"  - {count} {ext} files")

    print("\nStep 2: Analyzing image references in HTML files...")
    print("-" * 60)

    # Extract all image references from HTML
    html_refs = extract_image_references(pages_dir)
    print(f"Found {len(html_refs)} unique image references in HTML files")
    print("\nSample references:")
    for ref in sorted(list(html_refs))[:10]:
        print(f"  - {ref}")

    # Count how many now exist
    existing_count = 0
    missing_refs = []
    for ref in html_refs:
        ref_path = images_dir / ref
        if ref_path.exists():
            existing_count += 1
        else:
            missing_refs.append(ref)

    print(f"\n✓ {existing_count} referenced images exist")
    print(f"✗ {len(missing_refs)} referenced images are missing (GUID mapping issue)")

    if missing_refs and len(missing_refs) <= 20:
        print("\nMissing images:")
        for ref in sorted(missing_refs)[:20]:
            print(f"  - {ref}")

    print("\n" + "=" * 60)
    print("Image file extensions have been added.")
    print(f"However, {len(missing_refs)} images cannot be displayed because")
    print("they are referenced by original names in HTML but stored with GUID names.")
    print("\nThe RoboHelp project was compiled without preserving filename mappings.")

if __name__ == "__main__":
    main()
