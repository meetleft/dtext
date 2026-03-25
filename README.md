# TextEditMac

A Notepad++-like text editor for macOS, built with Python, PyQt6, and QScintilla.

## Features

- **Multi-tab editing** — open multiple files in tabs, drag to reorder, right-click context menu
- **Syntax highlighting** — 15+ languages including Python, JavaScript, HTML, CSS, Java, C/C++, SQL, JSON, XML, Markdown, Bash, YAML, Ruby, Perl, Lua
- **JSON tools** — format (pretty-print), compress (minify), and validate JSON with error location
- **File comparison** — side-by-side diff viewer with color-coded differences and synchronized scrolling
- **Find / Replace** — regex support, case-sensitive, whole-word matching, replace all
- **Code editing** — line numbers, code folding, bracket matching, auto-indent, indentation guides
- **Themes** — light and dark themes, follow macOS system appearance
- **Encoding detection** — automatic encoding detection via chardet (UTF-8, GBK, Latin-1, etc.)
- **Drag and drop** — drop files onto the window to open them

## Requirements

- Python 3.10+
- macOS (tested on macOS 15)

## Installation

```bash
pip install -r requirements.txt
```

## Build macOS App

Build a standalone `.app` bundle (no Python required to run):

```bash
pip install pyinstaller
bash build_app.sh
```

The app will be created at `dist/TextEditMac.app`. You can:
- Double-click it to launch
- Drag it to `/Applications` to install
- Or copy via terminal: `cp -r dist/TextEditMac.app /Applications/`

## Run from Source

```bash
python main.py
```

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| Cmd+N | New file |
| Cmd+O | Open file |
| Cmd+S | Save |
| Cmd+Shift+S | Save As |
| Cmd+W | Close tab |
| Cmd+Z | Undo |
| Cmd+Shift+Z | Redo |
| Cmd+F | Find / Replace |
| Cmd+Shift+J | Format JSON |
| Cmd+D | Compare files |
| Cmd+A | Select all |
| Cmd+X / C / V | Cut / Copy / Paste |
