#!/usr/bin/env python3
"""
Process extracted CAB help files and create a navigable structure.
"""

import os
import re
import shutil
from pathlib import Path
from html.parser import HTMLParser
from collections import defaultdict

class HTMLTitleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data

def get_html_title(filepath):
    """Extract title from HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(10000)  # Read first 10KB
            parser = HTMLTitleParser()
            parser.feed(content)
            return parser.title.strip() or os.path.basename(filepath)
    except Exception as e:
        return os.path.basename(filepath)

def extract_links(filepath):
    """Extract all href links from HTML file."""
    links = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Find all href links
            pattern = r'href=["\']([^"\']+)["\']'
            links = re.findall(pattern, content)
    except Exception:
        pass
    return links

def main():
    base_dir = Path("/home/user/Kube-help-navigator")
    extracted_dir = base_dir / "extracted_help"
    docs_dir = base_dir / "docs"

    # Create docs directory
    docs_dir.mkdir(exist_ok=True)

    print("Scanning extracted files...")

    # Get all files
    all_files = list(extracted_dir.glob("_*"))

    # Categorize files
    html_files = []
    image_files = []
    other_files = []

    for filepath in all_files:
        if filepath.suffix.lower() in ['.htm', '.html', '']:
            # Check if it's actually HTML
            try:
                with open(filepath, 'rb') as f:
                    start = f.read(500)
                    if b'<html' in start.lower() or b'<!doctype' in start.lower():
                        html_files.append(filepath)
                        continue
            except:
                pass

        suffix = filepath.suffix.lower()
        if suffix in ['.gif', '.jpg', '.jpeg', '.png', '.bmp', '.ico']:
            image_files.append(filepath)
        elif suffix in ['.xml']:
            other_files.append(filepath)
        else:
            # Try to determine if it's an image
            try:
                with open(filepath, 'rb') as f:
                    header = f.read(10)
                    # Check for image magic numbers
                    if header.startswith(b'GIF'):
                        image_files.append(filepath)
                    elif header.startswith(b'\xff\xd8\xff'):  # JPEG
                        image_files.append(filepath)
                    elif header.startswith(b'\x89PNG'):
                        image_files.append(filepath)
                    else:
                        other_files.append(filepath)
            except:
                other_files.append(filepath)

    print(f"Found {len(html_files)} HTML files")
    print(f"Found {len(image_files)} image files")
    print(f"Found {len(other_files)} other files")

    # Create subdirectories
    (docs_dir / "images").mkdir(exist_ok=True)
    (docs_dir / "pages").mkdir(exist_ok=True)
    (docs_dir / "assets").mkdir(exist_ok=True)

    # Copy files
    print("\nCopying files...")

    # Copy images
    for img in image_files:
        shutil.copy2(img, docs_dir / "images" / img.name)

    # Copy HTML files
    html_info = []
    for html_file in html_files:
        title = get_html_title(html_file)
        shutil.copy2(html_file, docs_dir / "pages" / html_file.name)
        html_info.append((html_file.name, title))

    # Copy other files
    for other in other_files:
        shutil.copy2(other, docs_dir / "assets" / other.name)

    # Sort HTML files by title
    html_info.sort(key=lambda x: x[1].lower())

    # Create index page
    print("\nCreating index page...")

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Help Documentation Navigator</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .search-box {{
            padding: 20px 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
        }}

        #searchInput {{
            width: 100%;
            padding: 12px 20px;
            font-size: 16px;
            border: 2px solid #667eea;
            border-radius: 25px;
            outline: none;
            transition: all 0.3s;
        }}

        #searchInput:focus {{
            border-color: #764ba2;
            box-shadow: 0 0 0 3px rgba(118, 75, 162, 0.1);
        }}

        .stats {{
            padding: 15px 30px;
            background: #e9ecef;
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 10px;
        }}

        .stat-item {{
            text-align: center;
        }}

        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}

        .stat-label {{
            color: #6c757d;
            font-size: 0.9em;
        }}

        .content {{
            padding: 30px;
        }}

        .page-list {{
            display: grid;
            gap: 10px;
        }}

        .page-item {{
            padding: 15px 20px;
            background: #f8f9fa;
            border-radius: 8px;
            transition: all 0.3s;
            border-left: 4px solid #667eea;
        }}

        .page-item:hover {{
            background: #e9ecef;
            transform: translateX(5px);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .page-item a {{
            color: #212529;
            text-decoration: none;
            font-size: 1.1em;
            display: block;
        }}

        .page-item a:hover {{
            color: #667eea;
        }}

        .no-results {{
            text-align: center;
            padding: 40px;
            color: #6c757d;
            font-size: 1.2em;
        }}

        footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #6c757d;
            border-top: 1px solid #dee2e6;
        }}

        @media (max-width: 768px) {{
            header h1 {{
                font-size: 1.8em;
            }}

            .stats {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📚 Help Documentation Navigator</h1>
            <p>Browse and search through {len(html_files)} help topics</p>
        </header>

        <div class="search-box">
            <input type="text" id="searchInput" placeholder="🔍 Search documentation..." onkeyup="filterPages()">
        </div>

        <div class="stats">
            <div class="stat-item">
                <div class="stat-number">{len(html_files)}</div>
                <div class="stat-label">Help Pages</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{len(image_files)}</div>
                <div class="stat-label">Images</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{len(other_files)}</div>
                <div class="stat-label">Resources</div>
            </div>
        </div>

        <div class="content">
            <div class="page-list" id="pageList">
"""

    for filename, title in html_info:
        index_html += f"""                <div class="page-item" data-title="{title.lower()}">
                    <a href="pages/{filename}" target="_blank">{title}</a>
                </div>
"""

    index_html += """            </div>
            <div class="no-results" id="noResults" style="display:none;">
                No matching pages found. Try a different search term.
            </div>
        </div>

        <footer>
            <p>Extracted from Help.cab | Total Files: """ + str(len(all_files)) + """</p>
        </footer>
    </div>

    <script>
        function filterPages() {
            const input = document.getElementById('searchInput');
            const filter = input.value.toLowerCase();
            const pageList = document.getElementById('pageList');
            const items = pageList.getElementsByClassName('page-item');
            const noResults = document.getElementById('noResults');
            let visibleCount = 0;

            for (let i = 0; i < items.length; i++) {
                const title = items[i].getAttribute('data-title');
                if (title.includes(filter)) {
                    items[i].style.display = '';
                    visibleCount++;
                } else {
                    items[i].style.display = 'none';
                }
            }

            if (visibleCount === 0) {
                pageList.style.display = 'none';
                noResults.style.display = 'block';
            } else {
                pageList.style.display = 'grid';
                noResults.style.display = 'none';
            }
        }
    </script>
</body>
</html>
"""

    with open(docs_dir / "index.html", 'w', encoding='utf-8') as f:
        f.write(index_html)

    print(f"\n✓ Documentation ready!")
    print(f"✓ Created {len(html_files)} HTML pages")
    print(f"✓ Copied {len(image_files)} images")
    print(f"✓ Copied {len(other_files)} other resources")
    print(f"\nOpen: docs/index.html")

if __name__ == "__main__":
    main()
