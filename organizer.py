#!/usr/bin/env python3
"""AI File Organizer — sort a messy folder into tidy category subfolders.

Usage:
    python organizer.py ~/Downloads            # organize ~/Downloads
    python organizer.py ~/Downloads --dry-run  # preview without moving anything
    python organizer.py . --verbose            # show every move

Zero third-party dependencies — standard library only.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

EXTENSIONS = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".svg", ".ico", ".heic"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".webm", ".flv", ".wmv"],
    "Music": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".pptx", ".ppt", ".xlsx", ".xls",
                  ".csv", ".md", ".odt", ".rtf", ".epub"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
    "Code": [".py", ".js", ".ts", ".html", ".css", ".cpp", ".c", ".h", ".java",
             ".json", ".xml", ".yml", ".yaml", ".sh", ".sql", ".rs", ".go"],
    "Apps": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm", ".apk", ".appimage"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
}

# Reverse lookup: ".png" -> "Images"
_EXTENSION_MAP = {ext: cat for cat, exts in EXTENSIONS.items() for ext in exts}

DEFAULT_CATEGORY = "Others"


def categorize(path: Path) -> str:
    """Return the category folder name for a file."""
    return _EXTENSION_MAP.get(path.suffix.lower(), DEFAULT_CATEGORY)


def unique_target(directory: Path, name: str) -> Path:
    """Return a non-colliding target path (appends _1, _2, … if needed)."""
    candidate = directory / name
    if not candidate.exists():
        return candidate
    stem, suffix = Path(name).stem, Path(name).suffix
    counter = 1
    while (candidate := directory / f"{stem}_{counter}{suffix}").exists():
        counter += 1
    return candidate


def organize(folder: str | Path, *, dry_run: bool = False,
             include_hidden: bool = False, verbose: bool = False) -> dict[str, int]:
    """Move every file in *folder* (top level only) into category subfolders.

    Returns a mapping of category -> number of files moved.
    """
    folder = Path(folder).expanduser().resolve()
    if not folder.is_dir():
        raise NotADirectoryError(f"Not a folder: {folder}")

    stats: dict[str, int] = {}
    script = Path(__file__).resolve()

    for item in sorted(folder.iterdir()):
        if not item.is_file() or item.resolve() == script:
            continue  # skip directories and this script itself
        if not include_hidden and item.name.startswith("."):
            continue

        category = categorize(item)
        target_dir = folder / category
        if not dry_run:
            target_dir.mkdir(exist_ok=True)
        target = unique_target(target_dir, item.name) if not dry_run else target_dir / item.name

        if verbose or dry_run:
            print(f"  {'[dry-run] ' if dry_run else ''}{item.name} -> {category}/{target.name}")
        if not dry_run:
            shutil.move(str(item), str(target))
        stats[category] = stats.get(category, 0) + 1

    return stats


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Organize files into categorized folders based on extension.")
    parser.add_argument("folder", nargs="?", help="Folder to organize (default: prompt)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview the moves without changing anything")
    parser.add_argument("--include-hidden", action="store_true",
                        help="Also organize dotfiles")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print every move")
    args = parser.parse_args(argv)

    folder = args.folder or input("Folder Path: ").strip().strip('"')
    try:
        stats = organize(folder, dry_run=args.dry_run,
                         include_hidden=args.include_hidden, verbose=args.verbose)
    except NotADirectoryError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    total = sum(stats.values())
    if args.dry_run:
        print(f"Dry run: {total} file(s) would be organized.")
    else:
        print(f"Done! {total} file(s) organized.")
    if total and (args.verbose or args.dry_run):
        for category, count in sorted(stats.items()):
            print(f"  {category}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
