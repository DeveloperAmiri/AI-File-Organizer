<div align="center">

# 📂 AI File Organizer

**Turn a messy folder into tidy categories in one command.** Images, Videos, Music, Documents, Archives, Code & more — pure Python, zero dependencies.

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/dependencies-0-success)
![Tests](https://img.shields.io/badge/tests-7%20passed-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)
[![CI](https://github.com/DeveloperAmiri/AI-File-Organizer/actions/workflows/ci.yml/badge.svg)](https://github.com/DeveloperAmiri/AI-File-Organizer/actions/workflows/ci.yml)

</div>

---

## ✨ Features

- 🚀 **One-command cleanup** — `python organizer.py ~/Downloads` and you're done
- 👀 **Dry-run mode** — preview every move before anything changes (`--dry-run`)
- 🛡️ **Never overwrites** — collisions become `file_1.ext`, `file_2.ext`, …
- 🙈 **Smart skips** — ignores subfolders, hidden files (unless `--include-hidden`) and itself
- 🌍 **Cross-platform** — Windows, Linux, macOS
- 🐍 **Stdlib only** — no `pip install` needed, ever

## 📦 Categories

| Folder | Extensions |
|---|---|
| Images | png, jpg, jpeg, gif, bmp, webp, svg, ico, heic |
| Videos | mp4, mkv, avi, mov, webm, flv, wmv |
| Music | mp3, wav, flac, aac, ogg, m4a |
| Documents | pdf, docx, txt, pptx, xlsx, csv, md, epub, … |
| Archives | zip, rar, 7z, tar, gz, bz2, xz |
| Code | py, js, ts, html, css, java, json, sh, sql, … |
| Apps | exe, msi, dmg, pkg, deb, apk, … |
| Fonts | ttf, otf, woff, woff2 |
| Others | everything else |

## 🚀 Quickstart

```bash
git clone https://github.com/DeveloperAmiri/AI-File-Organizer.git
cd AI-File-Organizer

# preview first (recommended)
python organizer.py ~/Downloads --dry-run

# actually organize
python organizer.py ~/Downloads --verbose
```

No arguments? It will simply ask for a folder path.

```
usage: organizer.py [--dry-run] [--include-hidden] [--verbose] [folder]
```

## 🧪 Tests

```bash
python -m pytest tests/ -q   # 7 tests, no extra deps (uses tmp_path)
```

## 🗂️ Project structure

```
AI-File-Organizer/
├── organizer.py        CLI + organize() / categorize() logic
├── tests/              pytest suite (tmp_path based)
├── requirements.txt    empty — stdlib only
└── README.md
```

## 🤝 Contributing

Pull requests welcome — fork, branch, PR. Please keep it dependency-free.

## 📄 License

MIT — see [LICENSE](LICENSE).
