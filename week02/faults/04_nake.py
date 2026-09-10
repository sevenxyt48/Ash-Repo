# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["pygame-ce"]
# ///

"""
Spec: Nake's raster — a bar is likelier the nearer the cell is to the diagonal.

    uv run 04_nake.py

It runs. It writes 04_nake.png. Open it: one half of the picture is a solid wall of
bars. The rule is one character away from the one in ../nake.py. Find it, and say
why it fails on that side and not the other.
"""

import random
from pathlib import Path

import pygame

SIZE = 30
H_PROB = 0.20
SEED = 1966
CELL = 20
MARGIN = 40

INK = (17, 17, 17)
PAPER = (250, 248, 244)
STROKE_WIDTH = 2
EXTENT = SIZE * CELL + MARGIN * 2


def raster(seed, h_prob):
    rng = random.Random(seed)
    grid = []
    last_square_empty = False

    for w in range(SIZE):
        grid.append([])
        for h in range(SIZE):
            bar = rng.randint(0, SIZE - 2) >= w - h
            cap = (rng.randint(0, SIZE) > h_prob * SIZE) and last_square_empty

            grid[w].append((bar, cap))

            if bar or cap:
                last_square_empty = False
            else:
                last_square_empty = True

    return grid


def main():
    pygame.init()
    surface = pygame.Surface((EXTENT, EXTENT))
    surface.fill(PAPER)
    grid = raster(SEED, H_PROB)

    for w in range(SIZE):
        for h in range(SIZE):
            bar, cap = grid[w][h]
            x, y = MARGIN + w * CELL, MARGIN + h * CELL
            if bar:
                pygame.draw.line(surface, INK, (x, y), (x, y + CELL), STROKE_WIDTH)
            if cap:
                pygame.draw.line(surface, INK, (x, y), (x + CELL, y), STROKE_WIDTH)

    out = Path(__file__).parent / "04_nake.png"
    pygame.image.save(surface, str(out))

    bars = sum(cell[0] for column in grid for cell in column)
    print(f"wrote {out.name} — {bars} bars out of {SIZE * SIZE} cells")


if __name__ == "__main__":
    main()
