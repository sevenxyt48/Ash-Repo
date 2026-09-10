# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["pygame-ce"]
# ///

"""
Schotter, live — after Georg Nees, 1968.

Same rule as week01/first-repo/sketch.py, but drawn in a window you can argue with:
change the seed, change the chaos, watch the grid fall apart.

Run it:

    uv run schotter.py

Keys:  SPACE new seed · ← → seed -1 / +1 · ↑ ↓ more / less chaos
       R reset the knobs · S save schotter.png · Q or Esc quit

Nothing to install. The `# /// script` block at the top tells uv what this file
needs, and uv fetches it the first time you run. To save a frame without opening
a window (useful on a locked-down lab machine):  uv run schotter.py --save out.png
"""

import math
import random
import sys

import pygame

# ---------------------------------------------------------------------------
# The knobs. These are yours. Change one, run again, look.
# ---------------------------------------------------------------------------

COLS = 12             # squares across
ROWS = 22             # squares down — the chaos builds over this many rows
SEED = 5913           # any integer. Same seed = same picture, every time, forever.
CHAOS = 1.0           # how fast order collapses. 0 = perfect grid. 2 = rubble.
SQUARE = 30           # size of one square, in pixels
MARGIN = 45           # breathing room around the grid

INK = (17, 17, 17)          # line colour
PAPER = (250, 248, 244)     # background
STROKE_WIDTH = 2            # line thickness in pixels

WIDTH = COLS * SQUARE + MARGIN * 2
HEIGHT = ROWS * SQUARE + MARGIN * 2 + 28   # + 28 for the readout at the bottom

# ---------------------------------------------------------------------------
# The rule. One square: rotated about its own centre, nudged off its slot.
# ---------------------------------------------------------------------------


def corners(cx, cy, size, angle):
    """The four corners of a square centred on (cx, cy), turned by `angle` radians."""
    half = size / 2
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    return [
        (cx + x * cos_a - y * sin_a, cy + x * sin_a + y * cos_a)
        for x, y in ((-half, -half), (half, -half), (half, half), (-half, half))
    ]


def squares(seed, chaos):
    """Every square in the grid, as a list of four-corner lists."""
    rng = random.Random(seed)
    out = []

    for row in range(ROWS):
        # Disorder grows with depth. Squaring it keeps the top calm and lets the
        # bottom really come apart — the whole point of the piece.
        damage = chaos * (row / ROWS) ** 2

        for col in range(COLS):
            angle = rng.uniform(-1, 1) * damage * math.radians(45)
            dx = rng.uniform(-1, 1) * damage * SQUARE * 0.5
            dy = rng.uniform(-1, 1) * damage * SQUARE * 0.5

            cx = MARGIN + col * SQUARE + SQUARE / 2 + dx
            cy = MARGIN + row * SQUARE + SQUARE / 2 + dy
            out.append(corners(cx, cy, SQUARE, angle))

    return out


# ---------------------------------------------------------------------------
# The drawing.
# ---------------------------------------------------------------------------


def render(surface, font, seed, chaos):
    surface.fill(PAPER)
    for points in squares(seed, chaos):
        pygame.draw.lines(surface, INK, True, points, STROKE_WIDTH)

    readout = f"seed {seed}   chaos {chaos:.2f}   SPACE reseed  arrows tune  S save"
    label = font.render(readout, True, (120, 116, 110))
    surface.blit(label, (MARGIN, HEIGHT - 22))


def main():
    pygame.init()
    font = pygame.font.Font(None, 20)
    seed, chaos = SEED, CHAOS

    # --save writes one frame to a file and stops. No window, so it works over ssh
    # and on a machine that will not open one.
    if "--save" in sys.argv:
        name = sys.argv[sys.argv.index("--save") + 1]
        frame = pygame.Surface((WIDTH, HEIGHT))
        render(frame, font, seed, chaos)
        pygame.image.save(frame, name)
        print(f"wrote {name}")
        return

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Schotter — after Georg Nees, 1968")
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
                    seed += 1
                elif event.key == pygame.K_LEFT:
                    seed -= 1
                elif event.key == pygame.K_UP:
                    chaos = min(chaos + 0.1, 4.0)
                elif event.key == pygame.K_DOWN:
                    chaos = max(chaos - 0.1, 0.0)
                elif event.key == pygame.K_r:
                    seed, chaos = SEED, CHAOS
                elif event.key == pygame.K_s:
                    pygame.image.save(screen, "schotter.png")
                    print(f"wrote schotter.png — seed {seed}, chaos {chaos:.2f}")

        render(screen, font, seed, chaos)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
