# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["pygame-ce"]
# ///

"""
Walk-through-Raster — after Frieder Nake, 1966.

The rule you read in the lecture, drawn as lines instead of characters. Two marks
per cell: a vertical *bar* down its left edge, a horizontal *cap* along its top.

Run it:

    uv run nake.py

Keys:  SPACE new roll of the dice · ← → cap chance down / up
       R reset the knobs · S save nake.png · Q or Esc quit

The rule is the one in the slides, line for line. The spec it has to keep is one
sentence: *a cap never sits under a cell that has anything in it.* Look for a
counter-example in the picture; if you find one, the code is wrong.

Save a frame without opening a window:  uv run nake.py --save out.png
"""

import random
import sys

import pygame

# ---------------------------------------------------------------------------
# The knobs.
# ---------------------------------------------------------------------------

SIZE = 30             # cells across and down
H_PROB = 0.20         # smaller = caps are more likely (read the line, it is backwards)
SEED = 1966           # any integer. Same seed = same picture.
CELL = 20             # size of one cell, in pixels
MARGIN = 40           # breathing room around the raster

INK = (17, 17, 17)
PAPER = (250, 248, 244)
STROKE_WIDTH = 2

WIDTH = SIZE * CELL + MARGIN * 2
HEIGHT = SIZE * CELL + MARGIN * 2 + 28    # + 28 for the readout at the bottom

# ---------------------------------------------------------------------------
# The rule. Column by column, top to bottom, carrying one boolean between cells.
# ---------------------------------------------------------------------------


def raster(seed, h_prob):
    """A list of columns; each cell is a pair (bar, cap) of booleans."""
    rng = random.Random(seed)
    grid = []
    last_square_empty = False

    for w in range(SIZE):
        grid.append([])
        for h in range(SIZE):
            # A bar is likely near the diagonal, where abs(w - h) is small, and
            # rare far from it. That is the whole composition.
            bar = rng.randint(0, SIZE - 2) >= abs(w - h)

            # A cap is only ever allowed under an empty cell. `last_square_empty`
            # is the cell ABOVE, because h is the inner loop.
            cap = (rng.randint(0, SIZE) > h_prob * SIZE) and last_square_empty

            grid[w].append((bar, cap))

            # ...and it is updated AFTER the cell is decided, from both marks.
            # Move this above the cap, or drop the `or cap`, and the spec breaks
            # while the picture still looks about right. That is the drill.
            if bar or cap:
                last_square_empty = False
            else:
                last_square_empty = True

    return grid


# ---------------------------------------------------------------------------
# The drawing.
# ---------------------------------------------------------------------------


def render(surface, font, seed, h_prob):
    surface.fill(PAPER)
    grid = raster(seed, h_prob)

    for w in range(SIZE):
        for h in range(SIZE):
            bar, cap = grid[w][h]
            x = MARGIN + w * CELL
            y = MARGIN + h * CELL
            if bar:
                pygame.draw.line(surface, INK, (x, y), (x, y + CELL), STROKE_WIDTH)
            if cap:
                pygame.draw.line(surface, INK, (x, y), (x + CELL, y), STROKE_WIDTH)

    readout = f"seed {seed}   cap threshold {h_prob:.2f}   SPACE reroll  arrows caps  S save"
    label = font.render(readout, True, (120, 116, 110))
    surface.blit(label, (MARGIN, HEIGHT - 22))


def main():
    pygame.init()
    font = pygame.font.Font(None, 20)
    seed, h_prob = SEED, H_PROB

    if "--save" in sys.argv:
        name = sys.argv[sys.argv.index("--save") + 1]
        frame = pygame.Surface((WIDTH, HEIGHT))
        render(frame, font, seed, h_prob)
        pygame.image.save(frame, name)
        print(f"wrote {name}")
        return

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Walk-through-Raster — after Frieder Nake, 1966")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_SPACE:
                    seed = random.randint(0, 999999)
                elif event.key == pygame.K_RIGHT:
                    h_prob = min(h_prob + 0.05, 1.0)
                elif event.key == pygame.K_LEFT:
                    h_prob = max(h_prob - 0.05, 0.0)
                elif event.key == pygame.K_r:
                    seed, h_prob = SEED, H_PROB
                elif event.key == pygame.K_s:
                    pygame.image.save(screen, "nake.png")
                    print(f"wrote nake.png — seed {seed}, cap threshold {h_prob:.2f}")

        render(screen, font, seed, h_prob)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
