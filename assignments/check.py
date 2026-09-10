"""
Does this repository meet the assignment spec?

Run it inside your assignment repo — the folder with README.md in it:

    uv run https://raw.githubusercontent.com/sd5913/pfad/2026/assignments/check.py

or, if you have the course repo cloned next to yours:

    uv run ../pfad/assignments/check.py

It prints a checklist and exits with an error if anything on it fails. The same
script runs on GitHub every time you push once you have added the workflow from
`assignments/check.yml` to your repo — that is where the green tick comes from.

It checks what a script can check: the files are there, the essay is the right
length, the process note says something, the history shows the essay was written
over more than one sitting, nothing that does not belong is committed. It cannot
tell whether the essay is any good. That part is still a person.

Nothing to install — this uses only what ships with Python.
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

MIN_WORDS, MAX_WORDS = 500, 1000
MIN_COMMITS, MIN_DAYS = 3, 2

JUNK = re.compile(r"(^|/)(\.DS_Store|Thumbs\.db|desktop\.ini|\.vscode/|\.idea/|__pycache__/|node_modules/|.*\.docx?$|.*\.pdf$|.*\.zip$)", re.I)
ALLOWED = {"README.md", "PROCESS.md", ".gitignore", ".gitattributes", "LICENSE", "LICENSE.md"}
ALLOWED_DIRS = ("assets/", "images/", "img/", ".github/")

OK, FAIL, WARN = "  ok  ", "  FAIL", "  note"
failed = 0


def report(status, text):
    global failed
    if status == FAIL:
        failed += 1
    print(f"{status}  {text}")


def words(text):
    """A rough word count that treats markdown as prose and Chinese text fairly."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)      # [text](url) -> text
    text = re.sub(r"<[^>]+>", " ", text)                       # html tags
    text = re.sub(r"[#*_>`|]", " ", text)
    latin = len(text.split())
    cjk = len(re.findall(r"[㐀-鿿]", text))
    return latin + cjk // 2


def git(repo, *args):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def check_readme(repo):
    path = repo / "README.md"
    if not path.is_file():
        report(FAIL, "README.md is missing at the top level — the essay is the README")
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    body = re.split(r"(?im)^#+\s*(references|bibliography|sources|works cited|reference list)\b.*$", text)[0]
    n = words(body)
    if n < 40:
        report(FAIL, f"README.md is a placeholder ({n} words) — the essay goes here")
    elif n < MIN_WORDS:
        report(FAIL, f"README.md is {n} words; the essay is {MIN_WORDS}–{MAX_WORDS} (bibliography not counted)")
    elif n > MAX_WORDS * 1.1:
        report(FAIL, f"README.md is {n} words; the essay is {MIN_WORDS}–{MAX_WORDS} (bibliography not counted)")
    else:
        report(OK, f"README.md: {n} words")
    if re.search(r"(?im)^#+\s*(references|bibliography|sources|works cited|reference list)\b", text):
        report(OK, "README.md has a References section")
    else:
        report(FAIL, "README.md has no References heading — cite what you drew on, APA, at the bottom")
    brackets = len(re.findall(r"\[[^\]\n]{6,}\](?!\()", text))
    if brackets >= 4:
        report(FAIL, f"README.md still has {brackets} [bracketed prompts] — this is an outline, not the essay")
    if not re.search(r"(?m)^#{1,3}\s+\S", text):
        report(WARN, "README.md has no headings — markdown is there to be used")
    if not re.search(r"https?://", text):
        report(WARN, "README.md has no links — if you cite something, link it")


def check_process(repo):
    path = repo / "PROCESS.md"
    if not path.is_file():
        near = [p for p in repo.rglob("*") if p.is_file() and p.name.lower() == "process.md" and ".git" not in p.parts]
        if near and near[0].parent == repo:
            # Right file, wrong case. Windows and macOS would not notice; GitHub does.
            report(WARN, f"{near[0].name} should be spelled PROCESS.md exactly — git mv it")
            path = near[0]
        else:
            where = f" (found {near[0].relative_to(repo)} — move it to the top level, exact name)" if near else ""
            report(FAIL, "PROCESS.md is missing" + where)
            return
    text = path.read_text(encoding="utf-8", errors="replace")
    n = words(text)
    none = re.search(r"(?i)\b(did not|didn't|no|without)\b.{0,30}\b(ai|assistant|chatgpt|copilot|llm)\b", text)
    if n < 5:
        report(FAIL, "PROCESS.md is empty — tools used, one thing kept, one thing rejected, and why")
    elif n < 40 and not none:
        report(FAIL, f"PROCESS.md is {n} words — tools used, one thing kept, one thing rejected, and why")
    elif re.search(r"(?i)\b(kept|keep|rejected|reject|discard|threw away|deleted|cut)\b", text) or none:
        report(OK, f"PROCESS.md: {n} words")
    else:
        report(WARN, "PROCESS.md does not say what you kept or rejected — that is the part that carries the marks")


def check_history(repo):
    log = git(repo, "log", "--format=%ad%x09%an%x09%s", "--date=short")
    if log is None:
        report(FAIL, "not a git repository, or git is not installed")
        return
    lines = [ln for ln in log.splitlines() if ln.strip()]
    days = {ln.split("\t")[0] for ln in lines}
    if len(lines) < MIN_COMMITS:
        report(FAIL, f"{len(lines)} commit(s) — the history should show the essay being written, not pasted")
    elif len(days) < MIN_DAYS:
        report(FAIL, f"{len(lines)} commits, all on one day — spread the work over more than one sitting")
    else:
        report(OK, f"{len(lines)} commits over {len(days)} days")
    vague = [ln for ln in lines if re.fullmatch(r"(?i)(initial commit|first commit|update|update readme\.md|commit|test|.)?", ln.split("\t")[-1].strip())]
    if lines and len(vague) > len(lines) // 2:
        report(WARN, "most commit messages say nothing — 'cut 200 words' beats 'Update README.md'")


def check_files(repo):
    tracked = git(repo, "ls-files")
    files = tracked.split("\n") if tracked else [str(p.relative_to(repo)) for p in repo.rglob("*") if p.is_file() and ".git" not in p.parts]
    files = [f for f in files if f]
    junk = [f for f in files if JUNK.search(f)]
    extra = [f for f in files if f.upper() not in {a.upper() for a in ALLOWED} and not f.startswith(ALLOWED_DIRS) and not JUNK.search(f)]
    if junk:
        report(FAIL, f"files that do not belong in a repo: {', '.join(junk[:4])} — remove them and add them to .gitignore")
    if extra:
        report(WARN, f"{len(extra)} file(s) beyond README.md and PROCESS.md: {', '.join(extra[:4])} — the Schotter sketch is a different repo")
    if not junk and not extra:
        report(OK, "just the files that belong")


def check_visibility():
    private = os.environ.get("ASSIGNMENT_REPO_PRIVATE", "").lower()
    if private == "true":
        report(FAIL, "the repository is private — a private repo cannot be marked")
    elif private == "false":
        report(OK, "the repository is public")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("path", nargs="?", default=".", help="the repo to check (default: here)")
    ap.add_argument("--assignment", default="1", help="which assignment's spec (only 1 so far)")
    args = ap.parse_args()
    if args.assignment != "1":
        sys.exit(f"no spec for assignment {args.assignment} yet")
    repo = Path(args.path).resolve()
    print(f"Assignment {args.assignment} — {repo.name}\n")
    check_readme(repo)
    check_process(repo)
    check_history(repo)
    check_files(repo)
    check_visibility()
    print()
    if failed:
        print(f"{failed} thing(s) to fix. Push again when you have, and the check runs again.")
        sys.exit(1)
    print("Everything a script can check is in place. Whether the essay is good is up to you.")


if __name__ == "__main__":
    main()
