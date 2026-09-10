# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["pygame-ce"]
# ///

"""
Tidal streams — concentric rings pushed out of shape by the currents in tides.csv.

One ring per time slot in the data. Each ring starts as a circle; every vertex on it
is shoved by one current arrow — hard where the water runs fast, in the direction the
water runs. Ring n is drawn at (n + 1) / RINGS of full size, so the inner rings are
earlier and smaller and the outer ones are later and bigger.

Run it:

    uv run tides.py              # writes tides.svg and opens a window
    uv run tides.py --save a.png # one frame to a PNG, no window

Keys:  SPACE new orientation · ← → less / more displacement
       [ ] fewer / more rings · R reset · S save tides.png · Q or Esc quit

This is a Python translation of a two.js piece; the original is at
github.com/venetanji/tides. tides.csv comes from fetch_tides.py.
"""

import csv
import math
import random
import sys
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# The knobs. Every one of these changes the picture. Try them.
# ---------------------------------------------------------------------------

RINGS = 24            # how many rings — one per time slot, so at most what the csv has
RESOLUTION = 200      # vertices per ring, and how many current arrows each ring reads
DISPLACEMENT = 25.0   # how hard a knot of current pushes a vertex, in pixels
LINE_WIDTH = 1.5      # multiplied by the ring's mean speed, so fast water draws thicker
ORIENTATION = 0.70    # 1 = circles. Below 1 it squashes them and eases off the push.
CENTRE_VOID = 0.0     # 0 = rings all the way in. Raise it to hollow out the middle.
SPREAD = False        # False = the first RESOLUTION arrows, as the original did.
                      # True = spread them over the whole territory. Try both.

PAPER = "#d5cfbf"     # the paper
STROKE = "#d6591d"    # the ink

WIDTH, HEIGHT = 900, 900
RADIUS = HEIGHT / 2.3

HERE = Path(__file__).parent
DATA = HERE / "tides.csv"
SVG_OUT = HERE / "tides.svg"

# ---------------------------------------------------------------------------
# The data. One list of arrows per time slot, oldest first.
# ---------------------------------------------------------------------------


def load_slots(path):
    """tides.csv -> [[(knot, deg), ...], ...], one inner list per time slot."""
    by_time = defaultdict(list)
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            by_time[row["time"]].append((int(row["point_id"]),
                                         float(row["knot"]), float(row["deg"])))

    slots = []
    for when in sorted(by_time):
        arrows = sorted(by_time[when])                 # always the same order
        slots.append([(knot, deg) for _, knot, deg in arrows])
    return slots


# ---------------------------------------------------------------------------
# The rule. A circle, and one arrow pushing each of its vertices.
# ---------------------------------------------------------------------------


def ring(arrows, scale, displacement, orientation):
    """One closed ring: its points, and the line width the mean speed asks for."""
    points = []
    total_speed = 0.0

    for i in range(RESOLUTION):
        index = i * len(arrows) // RESOLUTION if SPREAD else i % len(arrows)
        knot, deg = arrows[index]
        total_speed += knot

        # Where we would be on a plain circle...
        angle = i / RESOLUTION * 2 * math.pi
        x = math.sin(angle) * RADIUS
        y = math.cos(angle) * RADIUS * orientation

        # ...and where this arrow's current pushes us. deg is a compass bearing,
        # so it turns clockwise from north: sin for x, cos for y.
        phi = math.radians(deg)
        x += orientation * knot * math.sin(phi) * displacement
        y += knot * math.cos(phi) * displacement

        points.append((WIDTH / 2 + x * scale, HEIGHT / 2 + y * scale))

    return points, LINE_WIDTH * total_speed / RESOLUTION


def rings(slots, count, displacement, orientation):
    """Every ring, innermost first."""
    out = []
    for n in range(count):
        scale = CENTRE_VOID + (1 - CENTRE_VOID) * (n + 1) / count
        out.append(ring(slots[n % len(slots)], scale, displacement, orientation))
    return out


# ---------------------------------------------------------------------------
# Output 1 — an SVG file, written by hand, exactly like week01/first-repo/sketch.py.
# ---------------------------------------------------------------------------


def write_svg(path, drawn):
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
             f'viewBox="0 0 {WIDTH} {HEIGHT}">',
             f'  <rect width="100%" height="100%" fill="{PAPER}" />']

    for points, width in drawn:
        coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
        parts.append(f'  <polygon points="{coords}" fill="none" stroke="{STROKE}" '
                     f'stroke-width="{width:.2f}" />')

    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")
    print(f"wrote {path.name} — open it in a browser")


# ---------------------------------------------------------------------------
# Output 2 — a window you can push around.
# ---------------------------------------------------------------------------


def colour(hex_string):
    """'#d6591d' -> (214, 89, 29)"""
    return tuple(int(hex_string[i:i + 2], 16) for i in (1, 3, 5))


def show(slots):
    import pygame

    pygame.init()
    font = pygame.font.Font(None, 20)
    state = {"count": min(RINGS, len(slots)), "disp": DISPLACEMENT, "orient": ORIENTATION}
    drawn = rings(slots, state["count"], state["disp"], state["orient"])

    def paint(surface):
        surface.fill(colour(PAPER))
        for points, width in drawn:
            pygame.draw.lines(surface, colour(STROKE), True, points, max(1, round(width)))
        readout = (f"{state['count']} rings   displacement {state['disp']:.0f}   "
                   f"orientation {state['orient']:.2f}   SPACE  arrows  [ ]  S save")
        surface.blit(font.render(readout, True, (90, 84, 72)), (24, HEIGHT - 26))

    if "--save" in sys.argv:
        frame = pygame.Surface((WIDTH, HEIGHT))
        paint(frame)
        name = sys.argv[sys.argv.index("--save") + 1]
        pygame.image.save(frame, name)
        print(f"wrote {name}")
        return

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tidal streams — Hong Kong")
    clock = pygame.time.Clock()

    running = True
    while running:
        changed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                changed = True
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_SPACE:
                    state["orient"] = random.random()
                elif event.key == pygame.K_RIGHT:
                    state["disp"] = min(60.0, state["disp"] + 1)
                elif event.key == pygame.K_LEFT:
                    state["disp"] = max(0.0, state["disp"] - 1)
                elif event.key == pygame.K_RIGHTBRACKET:
                    state["count"] = min(96, state["count"] + 1)
                elif event.key == pygame.K_LEFTBRACKET:
                    state["count"] = max(1, state["count"] - 1)
                elif event.key == pygame.K_r:
                    state.update(count=min(RINGS, len(slots)), disp=DISPLACEMENT,
                                 orient=ORIENTATION)
                elif event.key == pygame.K_s:
                    pygame.image.save(screen, "tides.png")
                    print("wrote tides.png")

        if changed:
            drawn = rings(slots, state["count"], state["disp"], state["orient"])

        paint(screen)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


def main():
    if not DATA.exists():
        print(f"{DATA.name} is missing — run:  uv run fetch_tides.py")
        return

    slots = load_slots(DATA)
    print(f"{DATA.name}: {len(slots)} time slots, {len(slots[0])} arrows each")

    write_svg(SVG_OUT, rings(slots, min(RINGS, len(slots)), DISPLACEMENT, ORIENTATION))

    try:
        show(slots)
    except Exception as problem:                       # no display, no pygame, no matter
        print(f"no window ({problem}) — the svg is there either way")


if __name__ == "__main__":
    main()
