# Brief — the fall of a grid

You are the person who has to sign this off, not the person who wrote it.

## What was asked for

A **Schotter**: a grid of squares, in order at the top, coming apart towards the
bottom. Georg Nees, 1968; the picture from week 1.

## The rules it has to meet

1. **The top row is untouched.** Twelve squares, perfectly in their slots.
2. **The top stays calm.** The first third of the grid is barely disturbed; the
   damage comes on late and fast, all of it in the bottom half.
3. **Same picture every time.** Run it twice, get the same squares. Forever.
4. **Nothing leaves home.** Even at the bottom, every square stays within half a
   square of its own slot. Rubble, not scatter.

## Your job

Three people handed in `candidate_a.py`, `candidate_b.py`, `candidate_c.py`.
All three run. Look at them side by side:

```bash
uv run compare.py
```

The faint grid under each picture is where the squares belong. Press **SPACE** to
run all three again.

**Exactly one meets the brief.** Say which. For each of the other two, say which
numbered rule you can *see* it break, then open the file and find the line that
breaks it — the three files differ by a handful of characters:

```bash
git diff --no-index candidate_a.py candidate_b.py
git diff --no-index candidate_b.py candidate_c.py
```

That is the same view GitHub shows you on a commit, pointed at two files instead
of two versions.
