#!/usr/bin/env python3
"""
Completely fix HTML files - remove broken references, add proper styling.
"""

import os
import re
from pathlib import Path

def fix_html_file(html_content, filename):
    """Fix HTML content to work in new structure."""

    # Remove broken CSS link references
    html_content = re.sub(
        r'<link[^>]*href=["\'][^"\']*\.css["\'][^>]*>',
        '',
        html_content,
        flags=re.IGNORECASE
    )

    # Remove broken JavaScript references
    html_content = re.sub(
        r'<script[^>]*src=["\'][^"\']*\.js["\'][^>]*></script>',
        '',
        html_content,
        flags=re.IGNORECASE
    )

    # Remove inline script blocks that reference missing JS
    html_content = re.sub(
        r'<script[^>]*>.*?</script>',
        '',
        html_content,
        flags=re.IGNORECASE | re.DOTALL
    )

    # Remove base tags
    html_content = re.sub(
        r'<base[^>]*>',
        '',
        html_content,
        flags=re.IGNORECASE
    )

    # Fix image paths - change any relative path to ../images/basename
    html_content = re.sub(
        r'src=["\'](?:\.\./)*([^"\']*?/)([^/\'"]+\.(gif|jpg|jpeg|png|bmp|ico))["\']',
        r'src="../images/\2"',
        html_content,
        flags=re.IGNORECASE
    )

    # Also handle images without directory structure
    html_content = re.sub(
        r'src=["\'](?:\.\./)+([^/\'"]+\.(gif|jpg|jpeg|png|bmp|ico))["\']',
        r'src="../images/\1"',
        html_content,
        flags=re.IGNORECASE
    )

    # Add our CSS and a back link in the head section
    head_addition = '''
    <link rel="stylesheet" href="../style.css" type="text/css">
    <style>
        .back-to-index {
            position: fixed;
            top: 10px;
            right: 10px;
            background: #667eea;
            color: white;
            padding: 8px 15px;
            border-radius: 5px;
            text-decoration: none;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            z-index: 1000;
            font-size: 14px;
        }
        .back-to-index:hover {
            background: #764ba2;
            color: white;
        }
    </style>
</head>'''

    html_content = re.sub(
        r'</head>',
        head_addition,
        html_content,
        flags=re.IGNORECASE,
        count=1
    )

    # Add back button after opening body tag
    body_addition = '''<body>
    <a href="../index.html" class="back-to-index">← Back to Index</a>
'''

    html_content = re.sub(
        r'<body[^>]*>',
        body_addition,
        html_content,
        flags=re.IGNORECASE,
        count=1
    )

    return html_content

def main():
    base_dir = Path("/home/user/Kube-help-navigator")
    pages_dir = base_dir / "docs" / "pages"

    print("Fixing HTML files for proper display...")
    print("Removing broken CSS/JS references...")
    print("Adding proper styling and navigation...")

    fixed_count = 0
    error_count = 0

    for html_file in pages_dir.glob("_*"):
        try:
            # Read the file
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Only process if it looks like HTML
            if '<html' not in content.lower():
                continue

            # Fix the HTML
            fixed_content = fix_html_file(content, html_file.name)

            # Write back
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(fixed_content)

            fixed_count += 1

            if fixed_count % 100 == 0:
                print(f"  Processed {fixed_count} files...")

        except Exception as e:
            print(f"Error processing {html_file.name}: {e}")
            error_count += 1

    print(f"\n✓ Successfully fixed {fixed_count} HTML files")
    if error_count > 0:
        print(f"✗ {error_count} files had errors")

    print("\nChanges made:")
    print("  ✓ Removed broken CSS/JS references")
    print("  ✓ Added new style.css stylesheet")
    print("  ✓ Fixed image paths to ../images/")
    print("  ✓ Added 'Back to Index' button to each page")
    print("  ✓ Removed problematic script tags")

if __name__ == "__main__":
    main()
