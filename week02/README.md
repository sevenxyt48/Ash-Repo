# Week 02 — Your repo passes the check, then: predict, break, fix

Two hours, two jobs.

**Job one, the important one.** Your assignment 1 repository gets the right shape,
GitHub checks it on every push, and the URL is on Canvas before you leave the room.
You can keep writing the essay until Sunday. The *repo* is done today.

**Job two.** You will be handed programs that run, and asked three questions about
them, over and over:

1. **What does it print?** — before you run it.
2. **Where is the fault?** — it runs, and it is wrong.
3. **Does it meet the spec?** — here is the brief, here are three attempts.

Those three questions are the job for the rest of the semester, because the code
you will be handed from now on is mostly going to be written by a machine, and
someone has to be able to tell whether it is any good.

The short drills are in the slides, and they run in your browser:
<https://sd5913.github.io/teaching/week02/>. This folder is the longer version,
on your own machine, with real windows.

---

## 0:00 — `uv run`, and nothing else

```bash
cd pfad          # your clone from week 1
git pull         # this folder arrives
cd week02
uv run schotter.py
```

A window opens with a Schotter in it. Press `space`. Press it again.

That is the only Python command you will type this semester: **`uv run <file>`**.
It finds a Python if you have none, installs what the file needs, and runs it.
The file says what it needs in the first four lines:

```python
# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["pygame-ce"]
# ///
```

Read that as: *this program is not finished until it says what it needs.* Every
script you hand in from now on carries that block if it imports anything.

**Do not type `python`.** On a fresh Windows machine that word opens the Microsoft
Store. On a Mac it may be a Python from 2019. `uv run` sidesteps both.

If `setup.bat` set this machine up, VS Code also has the Python extension and a
`.venv` in this repo, so the **▷ Run** button at the top right of the editor runs
the open file too. Same result; the terminal is the one you can read errors in.

No `uv` on this machine? Download and double-click
<https://github.com/ait4x/v915-setup/releases/latest/download/setup.bat> (Windows),
or `brew install uv` (Mac), then come back.

---

## 0:10 — Your assignment repo: git, the check, the tick

Forty-five minutes. Everything in this block happens in **your assignment 1 repo**,
not in `pfad`. The brief is
[`assignments/01-why-are-we-here.md`](../assignments/01-why-are-we-here.md).

### 1. Get the repo onto this machine

Pick the line that is true for you:

- **No repo yet.** Make one now: <https://github.com/new>. Owner: your own account.
  Name: something short and lowercase, like `why-are-we-here`. **Public.** Tick
  *Add a README file*. Create it. That is week 1, step 5a — same moves.
- **The repo is on GitHub, but not on this computer.** Clone it:
  `git clone https://github.com/YOUR-USERNAME/YOUR-REPO`
- **It is already on this computer.** Good. Run `git pull` in it so it matches GitHub.

Then open **that folder** in VS Code (*File → Open Folder*) and open a terminal in
it (*Terminal → New Terminal*). Every command below runs there. If `git status`
says "not a git repository", you are in the wrong folder.

### 2. The four git words

Git is a folder that remembers. You change files; git does nothing until you tell it.
Four commands, always in this order:

```bash
git status                      # what changed since the last commit?
git add .                       # take everything that changed
git commit -m "Say what you did" # save a snapshot, with a note
git push                        # send the snapshots to GitHub
```

- `status` costs nothing. Run it before and after every other command until you
  can predict what it will say.
- A **commit** is a snapshot with a message. The message is for the you of next
  month: `"Cut the intro to one paragraph"` beats `"update"`.
- `push` is the only one that touches the internet. Until you push, GitHub has
  not seen your work, and neither have I.

Try it now with something small: add one sentence to `README.md`, save, then run
the four commands. Refresh the repo page on GitHub — the sentence is there.
`git log --oneline` shows the history you are building.

#### The same four words in VS Code

The **Source Control** panel (the branching icon in the left bar, `Ctrl+Shift+G`)
is the same four commands with buttons on them. Learn which button is which word:

| Terminal | VS Code Source Control panel |
|---|---|
| `git status` | The *Changes* list. A file there has changed since the last commit. |
| `git add` | The `+` next to a file, or the `+` on the *Changes* heading for all of them. The file moves to *Staged Changes*. |
| `git commit -m "…"` | Type the message in the box at the top, then **Commit**. |
| `git push` | **Sync Changes**. It pulls first, then pushes. |

Three things that catch people:

- **Commit and push are two steps.** After **Commit** the box empties, but nothing
  has left your computer. The button then changes to **Sync Changes**. Press it.
  Only then refresh GitHub.
- **"Pull" means take from GitHub; "push" means send to GitHub.** If you edited a
  file on the GitHub website, your computer is behind. **Sync Changes** pulls that
  edit down before pushing yours up, which is why it is one button and not two.
  In the terminal that is `git pull`, then `git push`.
- **A push that is "rejected"** means GitHub has a commit you do not have. Pull
  first (**Sync Changes** does this), then push again. If VS Code opens a file
  with `<<<<<<<` in it, both sides changed the same lines: delete the markers,
  keep the lines you want, save, commit.

Four minutes of video, from the VS Code team, walks through the panel:
<https://code.visualstudio.com/docs/introvideos/versioncontrol>. The written
version: <https://code.visualstudio.com/docs/sourcecontrol/overview>.

### 3. Run the check

The brief lists what the repo must contain. This script reads your repo and says
which of those things are there. Run it **inside your repo**:

```bash
uv run https://raw.githubusercontent.com/sd5913/pfad/2026/assignments/check.py
```

Read the list. Every `FAIL` line says what is wrong and, after the dash, what to do.

### 4. Fix the shape now

Some lines you can clear in the next twenty minutes, whatever state your essay is
in:

| The line says | Do this |
|---|---|
| `README.md is missing` / `is a placeholder` | The essay goes in `README.md`. Put in your title, your headings, and the first paragraph. A draft is fine today. |
| `no References heading` | Add `## References` at the bottom, with at least the lecture readings you will cite. |
| `PROCESS.md is missing` / `is empty` | Make `PROCESS.md`. Three honest lines: which tools you have used so far, one thing you kept, one thing you rejected. "None yet" is a valid first line. |
| `files that do not belong` | Delete them (`.DS_Store`, `.docx`, `.zip`, …) and commit the deletion. |
| `the repository is private` | GitHub → your repo → *Settings* → scroll to *Danger Zone* → *Change visibility* → Public. |

Two lines you **cannot** clear today, and that is expected:

- `README.md is N words; the essay is 500–1000` — that is the writing. Sunday.
- `commits, all on one day` — commit again tomorrow, from home, and it clears.

Commit after each fix, with a message that says what the fix was. Run the check
again. Watch the list get shorter.

### 5. Let GitHub run the check for you

Copy one file into your repo and GitHub runs the same check on every push, and
shows a **green tick** or a **red cross** next to your latest commit.

```bash
mkdir -p .github/workflows
curl -fsSL https://raw.githubusercontent.com/sd5913/pfad/2026/assignments/check.yml -o .github/workflows/check.yml
```

On Windows PowerShell write `curl.exe` instead of `curl`. Or skip the terminal:
open [`assignments/check.yml`](../assignments/check.yml) in your `pfad` clone,
copy all of it, and paste it into a new file at exactly
`.github/workflows/check.yml` in your assignment repo.

The folder name starts with a dot, so Finder and Explorer hide it. `git status`
does not — it should now list the new file. Then:

```bash
git add .github
git commit -m "Add the assignment check"
git push
```

Open your repo on GitHub and click the **Actions** tab. A run called *Assignment
check* appears within a minute. Click it, then *check*, then the *Check* step: the
same list you saw in the terminal. On the repo's front page the latest commit
now has a tick or a cross next to it. From now on every push gets one.

> **A small loop.** The check fails on any file that does not belong in the repo,
> and the workflow that runs the check is a file in the repo. So the checker has a
> line saying `.github/` is allowed, a rule it needs only because it exists. Could
> it check that the file really calls the real check? Not from inside: you could
> write a `check.yml` that prints `ok` and stops, and the tick would be just as
> green. That is why the tick is evidence, not proof, and why a tutor runs the
> same script from outside your repo. A system cannot vouch for itself (Gödel,
> 1931; Ken Thompson, *Reflections on Trusting Trust*, 1984). Keep that in mind
> every time a generated program says its own tests pass.

### 6. Submit

Post your repository URL on Canvas **now**, even if lines are still red:

```
https://github.com/YOUR-USERNAME/YOUR-REPO
```

Canvas records the address. What gets marked is what is in the repo at Sunday
23:59, and the check runs again then. Submitting today means you cannot forget
to on Sunday.

Then screenshot the Actions page — tick, cross, or the list — and upload it to
the ClassPoint question on the last slide. That is the attendance signal, and it
tells me who still needs help pushing.

---

## 0:55 — Read first, run second

Back in `pfad/week02`. Three programs, each one rule from the lecture. Open the
file **before** you run it.

| File | What it draws | Read this before running |
|---|---|---|
| `schotter.py` | Nees, *Schotter* — the week 1 sketch, live | `damage(row)`. Say in one sentence why the top stays calm. |
| `nake.py` | Nake, *Walk-through-Raster* — the rule from the slides, as lines | The `cap = ...` line. Say what combination it makes impossible. |
| `schotter3d.py` | Schotter, one dimension up — cubes instead of squares | `project()`, twenty lines at the bottom. Where does `distance` go? |

For each one: predict, say your prediction to the person next to you, then run
it. Then change **one** knob at the top and predict again. `S` saves a PNG if you
want to keep one.

`schotter3d.py` is the one to spend time on. There is no 3D library in it. A cube
is eight points; a point on screen is `x / depth` and `y / depth`; that is the
whole trick, and it has been the whole trick since 1435. Drag to orbit, and read
the function that makes the orbit happen.

---

## 1:15 — Tides: somebody else's data, your rule

```bash
cd tides
uv run tides.py
```

Twenty-four rings, one per quarter hour of a tidal forecast for Hong Kong waters,
each vertex on each ring shoved by the current at one point in the sea. This is a
Python translation of a two.js piece; it is the kind of thing assignment 2 asks for,
and week 3 is about getting data like this yourself.

- `tides.csv` is committed, so this runs without internet.
- `fetch_tides.py` is how the CSV was made: it asks the Hydrographic Office for a
  quarter-hour slot, caches the answer in `cache/`, and writes the CSV. Run it with
  `--now` if the room has wifi and you want today's water.
- The knobs are at the top of `tides.py`. `ORIENTATION`, `DISPLACEMENT` and `SPREAD`
  change the picture the most. Predict, then look.

One question: `ring()` reads the arrows with `i % len(arrows)`. What does the
picture do if you change that to `i * len(arrows) // RESOLUTION`? Say it before
you flip `SPREAD`.

---

## 1:30 — Find the fault

```bash
cd ../faults
```

Four programs. **Every one of them runs without an error message, and every one is
wrong.** The spec is in the docstring at the top of each file.

| File | Spec |
|---|---|
| `01_average.py` | The mean of six readings. |
| `02_grid.py` | A 3 × 5 grid of zeros with exactly one `1` in it. |
| `03_ramp.py` | Ten opacity steps, `0.0` to `0.9`. |
| `04_nake.py` | Nake's raster — but half the picture is a wall. |

For each: run it, say what is wrong with the output, find the line, fix it, run it
again. Three of the four are things that will surprise you from the lecture; the
fourth is one character. Compare lines with your neighbour before you move on.

---

## 1:45 — Does it meet the spec?

```bash
cd ../spec
uv run compare.py
```

`BRIEF.md` is four sentences about a picture. `candidate_a.py`, `candidate_b.py`
and `candidate_c.py` are three attempts at it, and `compare.py` puts them side by
side over a faint grid of where every square belongs. **Exactly one meets the
brief.** Press `space`. Look again.

You are the one signing it off. Say which candidate passes, and for each of the
other two: which rule you can *see* it break, and which line in the file breaks
it. `git diff --no-index candidate_a.py candidate_b.py` will find the differing
lines faster than your eyes will — there are only a handful.

---

## Before you leave

- [ ] Your assignment repo URL is on Canvas.
- [ ] `.github/workflows/check.yml` is in the repo, and the **Actions** tab shows a run.
- [ ] You know which red lines are left, and what clears each one.
- [ ] You have committed from this machine at least once and can do it again from home.

Sunday 13 September, 23:59. Push before then; the tick tells you when you are done.

---

## When it goes wrong

**`uv: command not found`** — the installer did not run, or the terminal predates
it. New terminal first; then the setup link above.

**`git push` asks who you are** — a browser window should open for you to sign in
to GitHub. If nothing opens, go back to week 1, *Tell git who you are*, and
*Step 3*; it takes two minutes.

**The Actions tab is empty** — the file is not where GitHub looks. The path must
be exactly `.github/workflows/check.yml`, and `git status` must have shown it
before you committed. `git ls-files .github` lists what git actually has.

**The check says the repository is private** — GitHub → *Settings* → *Danger
Zone* → *Change visibility*. A private repo cannot be marked.

**A window opens and closes at once** — read the terminal. The traceback names the
line. That is not a failure of the tutorial, that is the tutorial.

**`pygame` says it cannot open a display** — you are on a machine with no screen
(a remote server, or a lab image that boots headless). Every script here has
`--save out.png`, which draws one frame to a file without a window.

**The tides window is blank** — `tides.csv` is missing or empty. `git status` will
tell you if you deleted it; `git checkout tides.csv` brings it back.
