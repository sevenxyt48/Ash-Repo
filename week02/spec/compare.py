# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["pygame-ce"]
# ///

"""
The three candidates for BRIEF.md, side by side. Look; do not count.

    uv run compare.py

Keys:  SPACE run all three again · S save compare.png · Q or Esc quit

The faint grid under each one is where the squares were supposed to be. The
brief is four sentences; each is something you can see in these pictures, and
one of them you can only see by pressing SPACE.

Save a frame without opening a window:  uv run compare.py --save out.png
"""

import importlib
import math
import sys
from pathlib import Path

import pygame

sys.path.insert(0, str(Path(__file__).parent))
CANDIDATES = ["candidate_a", "candidate_b", "candidate_c"]

INK = (17, 17, 17)
PAPER = (250, 248, 244)
SLOT = (215, 210, 200)      # the faint grid of where each square belongs
LABEL = (90, 90, 90)
GAP = 30


def rotated_square(x, y, size, angle_deg, dx, dy):
    """The four corners of one square, turned about its centre and nudged."""
    cx, cy = x + size / 2 + dx, y + size / 2 + dy
    a = math.radians(angle_deg)
    half = size / 2
    corners = []
    for px, py in ((-half, -half), (half, -half), (half, half), (-half, half)):
        corners.append((cx + px * math.cos(a) - py * math.sin(a),
                        cy + px * math.sin(a) + py * math.cos(a)))
    return corners


def draw_candidate(surface, module, ox, oy, font):
    """One panel: the slot grid, then the squares the candidate laid out."""
    size = module.SQUARE
    for row in range(module.ROWS):
        for col in range(module.COLS):
            x = ox + module.MARGIN + col * size
            y = oy + module.MARGIN + row * size
            pygame.draw.rect(surface, SLOT, (x, y, size, size), 1)
    for x, y, angle, dx, dy in module.layout():
        pygame.draw.polygon(surface, INK, rotated_square(ox + x, oy + y, size, angle, dx, dy), 2)
    name = module.__name__.replace("candidate_", "").upper()
    surface.blit(font.render(name, True, LABEL), (ox + module.MARGIN, oy + 12))


def render(surface, modules, font):
    surface.fill(PAPER)
    ox = GAP
    for module in modules:
        draw_candidate(surface, module, ox, 0, font)
        ox += module.COLS * module.SQUARE + module.MARGIN * 2 + GAP
    hint = "SPACE run again   S save   Q quit        the faint grid is where each square belongs"
    surface.blit(font.render(hint, True, LABEL), (GAP, surface.get_height() - 28))


def main():
    modules = [importlib.import_module(name) for name in CANDIDATES]
    panel_w = modules[0].COLS * modules[0].SQUARE + modules[0].MARGIN * 2
    panel_h = modules[0].ROWS * modules[0].SQUARE + modules[0].MARGIN * 2
    size = (GAP + (panel_w + GAP) * len(modules), panel_h + 20)

    pygame.init()
    font = pygame.font.SysFont("dejavusansmono,consolas,menlo,monospace", 15)

    if "--save" in sys.argv:
        out = sys.argv[sys.argv.index("--save") + 1]
        surface = pygame.Surface(size)
        render(surface, modules, font)
        pygame.image.save(surface, out)
        print(f"wrote {out}")
        return

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("BRIEF.md — three candidates")
    render(screen, modules, font)
    pygame.display.flip()

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_q, pygame.K_ESCAPE):
                break
            if event.key == pygame.K_SPACE:
                render(screen, modules, font)      # layout() runs again for each
                pygame.display.flip()
            if event.key == pygame.K_s:
                pygame.image.save(screen, "compare.png")
                print("wrote compare.png")
    pygame.quit()


if __name__ == "__main__":
    main()
