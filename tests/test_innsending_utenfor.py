"""docs/innsending holdes utenfor git: følgebrev og skjemasvar til tidsskriftet publiseres ikke (eier, 10.10.2026)."""
import subprocess
from pathlib import Path

ROT = Path(__file__).resolve().parents[1]


def test_ingen_sporet_fil_under_docs_innsending():
    ut = subprocess.run(["git", "-C", str(ROT), "ls-files", "--", "docs/innsending"], check=True, capture_output=True, text=True)
    assert ut.stdout.strip() == ""


def test_gitignore_holder_katalogen_ute():
    assert "docs/innsending/" in (ROT / ".gitignore").read_text(encoding="utf-8").splitlines()
