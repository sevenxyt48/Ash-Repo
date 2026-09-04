# Week 01 — Git, GitHub, and your first repository

By the end of this tutorial you will have:

1. a GitHub account, registered against your student ID,
2. git installed and working on the machine you will use all semester,
3. a local copy of this course repository,
4. **your own repository**, on GitHub, with a piece of generative art in it and at
   least two commits.

Budget two hours. Steps 1–3 are setup and are boring; step 4 is the part that
matters. If you get stuck, ask — being stuck on installation is not a character
flaw, it is Tuesday.

---

## Why any of this

You are going to write code for the next thirteen weeks. Code changes. It breaks.
You will want yesterday's version back at 2am. And at the end of the semester you
will hand in a group project that has to show *who wrote what*.

Git solves all three. It is a machine for remembering every version of a folder,
forever, with a note attached to each change. GitHub is where those folders live
on the internet so other people — your group, your instructors, a studio looking
at your portfolio — can see them.

That last part is not a throwaway. **Your commits are public by default and they
add up.** The assignments in this course are portfolio pieces. Treat them that way.

### The five words you need

| Word | What it actually is |
|---|---|
| **repository** (repo) | A folder that git is watching. Nothing more mystical than that. |
| **commit** | A saved snapshot of that folder, with a message saying what you changed. Permanent, and it has your name on it. |
| **remote** | A copy of the repo that lives somewhere else — usually on GitHub. Called `origin` by default. |
| **push** / **pull** | Send your commits to the remote / fetch everyone else's down. |
| **clone** | Download a whole repo, with its entire history, to your machine. |

Two more you will meet the moment you work with other people:

- **fork** — your own copy of *somebody else's* repo, under your account. You can
  do whatever you like to it without asking permission.
- **pull request** (PR) — "I made a change in my copy, please take it into yours."
  This is how essentially all open-source software gets written.

---

## Step 1 — GitHub account

If you already have one, skip to the education benefits.

1. Sign up at <https://github.com/signup>.
2. **Use your PolyU email** (`@connect.polyu.hk`), or add it later under
   *Settings → Emails*. It is what unlocks the student benefits below.
3. You will be asked to set up **two-factor authentication**. It is not optional
   and it needs your phone. Do it now, not in week 6 when you are locked out
   the night an assignment is due.
4. Pick a username you would be happy putting on a CV. It is in the URL of
   everything you will make this semester, and changing it later breaks links.

Then claim your student benefits — free private repos, Copilot, and a pile of
other things — at <https://github.com/education/students>. Verification can take
a day or two, so start it today.

## Step 2 — Register your account for this course

**New this year, and it takes one minute:**

### → <https://pfad.ait4x.org>

Sign in with GitHub, enter the last four digits and letter of your PolyU student
ID, done. This is how your commits get matched to you in the gradebook — if you
skip it, your assignments arrive from a username nobody can identify.

It reads your **public profile only**. No password, no access to your repos.

Shortly after, you will get an email inviting you to the
[`sd5913`](https://github.com/sd5913) organisation. Accept it. That is where the
course material and your project repos live.

## Step 3 — Install the tools

You need **git** and **VS Code**. In the V915 lab both may already be there; on
your own laptop, probably not.

<details>
<summary><strong>Windows</strong></summary>

Open PowerShell and run:

```powershell
winget install --id Git.Git -e
winget install --id Microsoft.VisualStudioCode -e
```

**Close PowerShell and open a new one afterwards.** Installers change your `PATH`
and a window that was already open never notices. This is the single most common
reason "git is not recognized" appears after a successful install.

If you would rather have a package manager that makes the rest of the semester
easier, install [scoop](https://scoop.sh/) first and use `scoop install git`.
</details>

<details>
<summary><strong>macOS</strong></summary>

Install [Homebrew](https://brew.sh/) if you do not have it, then:

```bash
brew install git
brew install --cask visual-studio-code
```

macOS ships an ancient git and will offer you the Xcode command line tools the
first time you type `git`. That works too, but brew's is newer.
</details>

Check it worked. Open a **new** terminal (in VS Code: `` Ctrl+` `` / `` Cmd+` ``):

```bash
git --version
```

A version number means you are fine. `command not found` means either the install
failed or you are in a terminal that predates it.

### Tell git who you are

Git stamps your name and email onto every commit. Do this once, ever:

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

> **Use the same email as your GitHub account.** If it does not match, your commits
> still work but GitHub will not connect them to your profile — they show up as a
> grey anonymous avatar and they do not count toward your contribution graph. This
> is the number-one reason people finish a semester with an empty-looking profile.
> Don't want your real address public? GitHub gives you a private relay address at
> *Settings → Emails → Keep my email addresses private*; use that one here.

## Step 4 — Clone the course repository

This is the repo you are reading right now.

```bash
cd Documents          # or wherever you keep your work — not Desktop, be kind to yourself
git clone https://github.com/sd5913/pfad
cd pfad
code .                # opens the folder in VS Code
```

Each week, before class, get the new material with:

```bash
git pull
```

### While you are in here: branches

This repo has two branches. You landed on `2026`, this year's course. The other
one, `2025`, holds last year's complete thirteen weeks.

A branch is a parallel version of the same repository. Same remote, same history
up to a point, different contents. Try it:

```bash
git branch -a        # every branch this clone knows about
git switch 2025      # last year's course
ls                   # week01 ... week13, completely different files
git switch 2026      # back to this year
```

Notice that the files on disk *changed* when you switched, and changed back. You
did not download anything the second time — your clone already had both, because
`git clone` brings the whole repository, not just the version you see.

Last year's material is worth a look, and it is where the week 1 web-scraping
code lives (`week01/main.py` on the `2025` branch) if you want to get ahead on
assignment 2. It is on its own branch so that this year's folder stays about this
year.

You will use branches properly in the group project, when three of you need to
change the same code without standing on each other. For now: they exist,
switching is free, and nothing is lost.

### Try to push to it. Seriously.

Change something in this file, commit it, and try to send it back:

```bash
git commit -am "my important contribution"
git push
```

It will be **rejected**. You are a member of the organisation, but you have
*read* access to this repo, not *write*. This is not a bug and not personal —
it is how every shared codebase on earth works.

So how do people contribute to repos they cannot write to? Two ways, and you
should know both exist:

- **Issues** — you found a bug, or something in the material is wrong or unclear.
  Open an issue: <https://github.com/sd5913/pfad/issues>. Describe what you did,
  what you expected, and what happened. This is a real and welcome contribution.
- **Fork + pull request** — you *fixed* the thing. Fork this repo to your own
  account, commit the fix there, and open a pull request back here. If it is
  good, it gets merged and your name is in the history of the course.

Undo your experiment before moving on:

```bash
git reset --hard origin/main
```

## Step 5 — Your first repository

Now the part that is yours. You will publish a piece of generative art and then
change it.

### 5a. Make the repo on GitHub

Go to <https://github.com/new>.

- **Owner**: your own account.
- **Name**: `schotter` (or anything you like — lowercase, hyphens not spaces).
- **Public**.
- Tick **Add a README file**.
- Create it.

### 5b. Clone it and add the sketch

```bash
cd ..                                          # out of pfad
git clone https://github.com/YOUR-USERNAME/schotter
cd schotter
```

Copy `week01/first-repo/sketch.py` from this course repo into your new folder.
Drag it in Finder/Explorer, or:

```bash
cp ../pfad/week01/first-repo/sketch.py .       # macOS
copy ..\pfad\week01\first-repo\sketch.py .     # Windows PowerShell
```

Run it:

```bash
python sketch.py
```

(On Windows that may be `py sketch.py`.) It writes `sketch.svg`. Open that file —
double-click it, or right-click → *Open with* → your browser.

What you are looking at is a homage to **Georg Nees' *Schotter*, 1968** — one of
the first artworks made by a computer, and a contemporary of the Frieder Nake
prints from the lecture. A grid of squares, perfectly ordered at the top,
progressively falling apart as it descends. Nees plotted it on a Zuse Graphomat.
You just made one on a laptop in a second, with no libraries at all.

([This](first-repo/sketch.svg) is what the default settings produce — but yours should not stay the default for long.)

### 5c. Commit and push

```bash
git add sketch.py sketch.svg
git commit -m "Add Schotter sketch"
git push
```

Refresh your repo page on GitHub. Your art is on the internet.

> Doing this in VS Code instead: the **Source Control** panel in the left sidebar
> (the branching icon, `Ctrl+Shift+G`). Changed files appear under *Changes*; the
> `+` next to a file is `git add`; type a message and hit the tick to commit;
> the sync arrows push. It is the same three commands with buttons on them —
> which is exactly why you typed them once first.

### 5d. Change it and commit again

This is the step that teaches you what git is *for*.

Open `sketch.py` and change one of the constants near the top — `SEED` to any
other number is the most dramatic, or push `CHAOS` up to `1.8`, or make `COLS`
and `ROWS` a wide letterbox instead of a portrait.

Run it again. Then:

```bash
git add .
git commit -m "Turn up the chaos"
git push
```

Now on GitHub, click the **commits** link on your repo, then your new commit.
GitHub shows you the *diff* — every line that changed. For `sketch.svg` it will
offer you a **side-by-side image comparison** and a swipe slider. There is your
old piece and your new piece, both kept forever, with a note saying what you did.

That is the whole idea. You cannot lose work, and you can always explain it.

### 5e. Write the README

Every repo you hand in this course needs one. Open `README.md` in your repo and
say: what this is, how to run it, and what the knobs do. It is the first thing
anyone sees. Commit it.

---

## Homework

1. **[Assignment 1 — "Why are we here?"](../assignments/01-why-are-we-here.md)**
   (5%, due **Sunday 13 September, 23:59**). A 500–1000 word reflection on why a
   designer should learn to program *now*, when machines write code on request.

   It is another repository — the essay is the README, exactly like the one you
   just made. You submit the URL on Canvas, nothing else. Read the brief; it asks
   for a `PROCESS.md` about your AI use, and it expects a commit history that
   shows you drafted rather than pasted.

   Watch [Dylan Beattie's *The Art of Code*](https://www.youtube.com/watch?v=6avJHaC3C2U)
   first — about an hour, and the best argument I know for why this class exists.

2. **Precrastinate on Assignment 2** (10%, the data visualisation project). Last
   year's starter scrapes tide data from the Hong Kong Observatory; it is on the
   other branch:

   ```bash
   git switch 2025
   cd week01
   ```

   Run it. Break it. Point it at a different page. Then `git switch 2026` and come
   to week 2 with a natural phenomenon you actually want to look at.

---

## When it goes wrong

**`git: command not found` / `'git' is not recognized`**
You are in a terminal that opened before git installed. Close it, open a new one.
If it still fails, the install did not finish.

**`Support for password authentication was removed`**
Git is asking for your GitHub password on the command line; that has not worked
since 2021. Install the [GitHub CLI](https://cli.github.com/) and run `gh auth login`,
or let VS Code sign you in (it will prompt in a browser the first time you push).

**`fatal: not a git repository`**
You are in the wrong folder. `cd` into your project. `pwd` (macOS) or `cd`
(Windows) tells you where you are.

**`Updates were rejected because the remote contains work that you do not have`**
Someone (or a past you, via the GitHub web editor) committed to the remote and
your local copy has not seen it. `git pull` first, then push.

**"Nothing to commit, working tree clean"**
Git sees no changes. Either you did not save the file (`Ctrl+S`), or you edited a
file in a different folder from the one you are in.

**Your commits show a grey avatar and are not on your contribution graph**
Your `git config user.email` does not match an email on your GitHub account. Fix
the config; past commits stay grey unless you go out of your way to rewrite them,
which is why we set it before your first commit.

**Copilot cannot do this for you**
It can install git, it can explain an error message, it can write the sketch. It
cannot create your GitHub account, accept your org invitation, or register your
student ID. Those are yours.
