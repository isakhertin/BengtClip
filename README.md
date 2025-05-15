# BengtClip

**BengtClip** is a minimal macOS menubar clipboard manager built with Python and Rumps. It stores your clipboard history, lets you quickly access recent items, and supports persistent history across reboots.

<img src="app/resources/Bengt_Logo_rainbow.png" alt="drawing" width="200"/>

---

## Features

- Clipboard history (customizable: 5–30 items)
- One-click to copy previous items
- Persistent storage between reboots
- macOS menubar integration (no Dock icon)
- Toggle history size via menu

---

## Requirements

- macOS 12 or newer (Ventura or later recommended)
- Python 3.9+
- [`py2app`](https://github.com/ronaldoussoren/py2app) (for building .app)

---

## Run from Source

```bash
git clone https://github.com/isakhertin/BengtClip.git
cd BengtClip
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app/BengtClip.py
```
---

## Build app
1. Build app
```bash
python setup.py py2app
open dist/BengtClip.app
```

2. Move Bengtclipp.app to applications folder
