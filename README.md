# KUBE Help Navigator

A navigable web interface for legacy software help documentation extracted from a `.cab` file.

## Overview

This project converts Microsoft Cabinet (CAB) archive help documentation into a modern, searchable web interface. The original help file has been extracted, organized, and made accessible through an easy-to-use navigation system.

## Structure

```
.
├── Help.cab                  # Original CAB archive
├── extracted_help/           # Raw extracted files (733 files with GUID names)
├── docs/                     # Organized documentation
│   ├── index.html           # Main navigation page (START HERE)
│   ├── pages/               # 906 HTML help pages
│   ├── images/              # 1557 image files (GIF, JPEG, etc.)
│   └── assets/              # 74 other resources (XML, icons, etc.)
└── process_help.py          # Python script used to organize the documentation
```

## Features

- **🔍 Search Functionality**: Real-time search across all 906 help topics
- **📊 Statistics Dashboard**: Overview of available documentation
- **🎨 Modern Interface**: Clean, responsive design that works on all devices
- **⚡ Fast Navigation**: Alphabetically sorted topics with instant filtering
- **📱 Mobile Friendly**: Works seamlessly on phones, tablets, and desktops

## Getting Started

### Viewing the Documentation

Simply open `docs/index.html` in any modern web browser:

```bash
# On Linux/Mac
open docs/index.html

# Or with a specific browser
firefox docs/index.html
chrome docs/index.html
```

### Contents

The documentation contains 906 help pages covering topics including:
- Scanning and hardware setup
- User interface references
- Troubleshooting guides
- Inspection mode documentation
- Macro commands
- Working with data
- And much more!

## Technical Details

### Original Format

The help documentation was originally stored in a Microsoft Compiled HTML Help (CHM) format, packaged as a CAB archive. The files were extracted using `cabextract`.

### Extraction Process

1. **Extract CAB**: Used `cabextract` to decompress Help.cab (25.6 MB)
2. **File Analysis**: Identified 2537 files with GUID-based names
3. **Categorization**: Separated HTML (906), images (1557), and other files (74)
4. **Organization**: Copied files into logical directory structure
5. **Index Generation**: Created searchable navigation interface

### File Types

- **HTML Pages**: 906 documentation pages
- **Images**: 1557 files (GIF, JPEG, PNG, icons)
- **Resources**: 74 XML configuration files and other assets

## Usage Tips

1. **Search**: Use the search box to quickly find topics
2. **Browse**: Scroll through the alphabetically sorted list
3. **Open in New Tab**: All help pages open in a new tab for easy reference
4. **Multiple Topics**: Keep multiple help pages open for cross-referencing

## Requirements

- Any modern web browser (Chrome, Firefox, Safari, Edge)
- No server or special software needed - works offline!

## License

This documentation belongs to the original software vendor. This project only provides a convenient navigation interface for the existing help content.

## Acknowledgments

- Original documentation created with RoboHelp WebHelp 5.50
- Extraction performed using `cabextract`
- Navigation interface built with vanilla HTML/CSS/JavaScript
