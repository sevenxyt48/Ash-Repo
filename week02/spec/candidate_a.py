"""
Candidate A for the brief in BRIEF.md.

    uv run compare.py          # all three candidates side by side, in a window
    uv run candidate_a.py    # this one alone, to candidate_a.svg

Nothing to install — on its own this uses only what ships with Python.
"""

import random

COLS, ROWS = 12, 22
SEED = 5913
CHAOS = 1.0
SQUARE = 30
MARGIN = 45
STROKE = "#111111"
BACKGROUND = "#faf8f4"


def damage(row):
    """How disordered row `row` is: 0 at the top, CHAOS at the bottom."""
    return CHAOS * row / (ROWS - 1)


def place(rng, row):
    """One square: how far it turns, and how far it slides, in x and in y."""
    hurt = damage(row)
    angle = rng.uniform(-1, 1) * hurt * 45
    dx = rng.uniform(-1, 1) * hurt * SQUARE * 0.5
    dy = rng.uniform(-1, 1) * hurt * SQUARE * 0.5
    return angle, dx, dy


def layout():
    """Every square: (x, y, angle, dx, dy). This is what compare.py draws."""
    rng = random.Random(SEED)
    squares = []
    for row in range(ROWS):
        for col in range(COLS):
            angle, dx, dy = place(rng, row)
            squares.append((MARGIN + col * SQUARE, MARGIN + row * SQUARE, angle, dx, dy))
    return squares


def main():
    width = COLS * SQUARE + MARGIN * 2
    height = ROWS * SQUARE + MARGIN * 2
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
             f'viewBox="0 0 {width} {height}">',
             f'  <rect width="100%" height="100%" fill="{BACKGROUND}" />',
             f'  <g fill="none" stroke="{STROKE}" stroke-width="1.4">']
    for x, y, angle, dx, dy in layout():
        cx, cy = x + SQUARE / 2, y + SQUARE / 2
        parts.append(f'  <rect x="{x:.2f}" y="{y:.2f}" width="{SQUARE}" height="{SQUARE}" '
                     f'transform="translate({dx:.2f} {dy:.2f}) rotate({angle:.2f} {cx:.2f} {cy:.2f})" />')
    parts += ["  </g>", "</svg>"]
    with open("candidate_a.svg", "w", encoding="utf-8") as handle:
        handle.write("\n".join(parts))
    print("wrote candidate_a.svg — open it in a browser")


if __name__ == "__main__":
    main()
