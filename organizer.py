import os
import shutil
from pathlib import Path

EXTENSIONS = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov"],
    "Music": [".mp3", ".wav", ".flac", ".aac"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".pptx", ".xlsx"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".cpp", ".c", ".java", ".json"],
}

def organize(folder):
    folder = Path(folder)

    if not folder.exists():
        print("Folder not found.")
        return

    moved = 0

    for item in folder.iterdir():

        if item.is_dir():
            continue

        suffix = item.suffix.lower()

        category = "Others"

        for key, exts in EXTENSIONS.items():
            if suffix in exts:
                category = key
                break

        target = folder / category
        target.mkdir(exist_ok=True)

        shutil.move(str(item), str(target / item.name))
        moved += 1

    print(f"Done! {moved} files organized.")

if __name__ == "__main__":
    path = input("Folder Path: ").strip('"')
    organize(path)