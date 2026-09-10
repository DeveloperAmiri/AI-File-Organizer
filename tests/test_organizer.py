"""Tests for organizer.py — run with: pytest"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from organizer import categorize, organize, unique_target


def test_categorize_known_extensions():
    assert categorize(Path("photo.PNG")) == "Images"
    assert categorize(Path("movie.mkv")) == "Videos"
    assert categorize(Path("song.flac")) == "Music"
    assert categorize(Path("report.pdf")) == "Documents"
    assert categorize(Path("backup.zip")) == "Archives"
    assert categorize(Path("app.py")) == "Code"
    assert categorize(Path("setup.exe")) == "Apps"


def test_categorize_unknown_goes_to_others():
    assert categorize(Path("weird.xyz")) == "Others"
    assert categorize(Path("noextension")) == "Others"


def test_organize_moves_files(tmp_path):
    (tmp_path / "a.png").write_text("x")
    (tmp_path / "b.mp3").write_text("x")
    (tmp_path / "c.pdf").write_text("x")
    stats = organize(tmp_path)
    assert stats == {"Images": 1, "Music": 1, "Documents": 1}
    assert (tmp_path / "Images" / "a.png").exists()
    assert (tmp_path / "Music" / "b.mp3").exists()
    assert (tmp_path / "Documents" / "c.pdf").exists()


def test_organize_dry_run_changes_nothing(tmp_path):
    (tmp_path / "a.png").write_text("x")
    stats = organize(tmp_path, dry_run=True)
    assert stats == {"Images": 1}
    assert (tmp_path / "a.png").exists()
    assert not (tmp_path / "Images").exists()


def test_organize_skips_directories_and_hidden(tmp_path):
    (tmp_path / "sub").mkdir()
    (tmp_path / ".secret").write_text("x")
    (tmp_path / "ok.txt").write_text("x")
    assert organize(tmp_path) == {"Documents": 1}
    assert (tmp_path / ".secret").exists()
    assert organize(tmp_path, include_hidden=True) == {"Others": 1}


def test_organize_never_overwrites(tmp_path):
    dest = tmp_path / "Images"
    dest.mkdir()
    (dest / "a.png").write_text("original")
    (tmp_path / "a.png").write_text("new")
    organize(tmp_path)
    assert (dest / "a.png").read_text() == "original"
    assert (dest / "a_1.png").read_text() == "new"


def test_unique_target_increments(tmp_path):
    (tmp_path / "f.txt").write_text("x")
    assert unique_target(tmp_path, "f.txt").name == "f_1.txt"
    assert unique_target(tmp_path, "g.txt").name == "g.txt"
