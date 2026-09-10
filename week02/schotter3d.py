# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["pygame-ce"]
# ///

"""
Schotter, one dimension up — cubes instead of squares.

Same rule as schotter.py: a grid that is a perfect lattice at the far edge and pure
rubble at the near one. Here the tiles are cubes, they are displaced and turned in
all three axes, and the whole thing is put on screen by twenty lines of arithmetic
at the bottom of this file. No OpenGL, no numpy — read `project()`, it is the
interesting part.

Run it:

    uv run schotter3d.py

Drag the mouse to orbit. Keys:
    arrows orbit · + - move the camera closer / further · SPACE new seed
    [ ] less / more chaos · W wireframe (see through the cubes) · R reset
    S save schotter3d.png · Q or Esc quit

Save a frame without opening a window:  uv run schotter3d.py --save out.png
"""

import math
import random
import sys

import pygame

# ---------------------------------------------------------------------------
# The knobs.
# ---------------------------------------------------------------------------

COLS = 9              # cubes across
ROWS = 16             # cubes deep — the chaos builds over this many rows
SEED = 5913           # any integer. Same seed = same pile.
CHAOS = 1.2           # 0 = perfect lattice, 3 = landslide
CUBE = 0.72           # cube edge, in grid units (1.0 would touch its neighbours)

# Where the camera starts. Yaw and pitch are in radians; DIST is how far back it sits.
YAW, PITCH, DIST = 0.60, 0.55, 25.0
FOCAL = 880           # bigger = longer lens = flatter perspective
HORIZON = 0.41        # where the middle of the world lands on screen (0.5 = centre)

INK = (17, 17, 17)
PAPER = (250, 248, 244)
STROKE_WIDTH = 2

WIDTH, HEIGHT = 900, 660
NEAR = 0.6            # never divide by a z smaller than this

# The eight corners of a cube of edge 1, centred on itself, and the six faces
# that join them. Each face is four corner numbers, in order around the square.
CORNERS = [(x, y, z) for x in (-0.5, 0.5) for y in (-0.5, 0.5) for z in (-0.5, 0.5)]
FACES = [(0, 1, 3, 2), (4, 5, 7, 6), (0, 1, 5, 4), (2, 3, 7, 6), (0, 2, 6, 4), (1, 3, 7, 5)]

# ---------------------------------------------------------------------------
# The rule, in three dimensions.
# ---------------------------------------------------------------------------


def spin(point, ax, ay, az):
    """Turn one point around the x, then y, then z axis. Angles in radians."""
    x, y, z = point
    y, z = y * math.cos(ax) - z * math.sin(ax), y * math.sin(ax) + z * math.cos(ax)
    x, z = x * math.cos(ay) + z * math.sin(ay), -x * math.sin(ay) + z * math.cos(ay)
    x, y = x * math.cos(az) - y * math.sin(az), x * math.sin(az) + y * math.cos(az)
    return x, y, z


def cubes(seed, chaos):
    """Every cube, as its eight corners in world coordinates."""
    rng = random.Random(seed)
    out = []

    for row in range(ROWS):
        # Exactly the 2D rule: disorder grows with the square of how far back you are.
        damage = chaos * (row / ROWS) ** 2

        for col in range(COLS):
            ax = rng.uniform(-1, 1) * damage * math.radians(45)
            ay = rng.uniform(-1, 1) * damage * math.radians(45)
            az = rng.uniform(-1, 1) * damage * math.radians(45)
            dx = rng.uniform(-1, 1) * damage * 0.5
            dy = rng.uniform(-1, 1) * damage * 0.5
            dz = rng.uniform(-1, 1) * damage * 0.5

            cx = col - (COLS - 1) / 2 + dx
            cy = dy
            cz = (ROWS - 1) / 2 - row + dz     # row 0 sits at the back

            out.append([
                (cx + px * CUBE, cy + py * CUBE, cz + pz * CUBE)
                for px, py, pz in (spin(c, ax, ay, az) for c in CORNERS)
            ])

    return out


# ---------------------------------------------------------------------------
# The projection. This is the whole of "3D": turn the world in front of the eye,
# then divide by how far away it is. Things far away divide by more, so they get
# smaller. That is it.
# ---------------------------------------------------------------------------


def project(point, yaw, pitch, dist):
    """One world point -> (screen x, screen y, depth). Depth is used to sort faces."""
    x, y, z = point

    # Spin the world around the vertical axis (yaw)...
    x, z = x * math.cos(yaw) + z * math.sin(yaw), -x * math.sin(yaw) + z * math.cos(yaw)
    # ...then tip it, so you look down on the grid and the far edge rises up the frame.
    y, z = y * math.cos(pitch) + z * math.sin(pitch), -y * math.sin(pitch) + z * math.cos(pitch)
    # ...then push the whole scene out in front of the camera.
    z = max(z + dist, NEAR)

    scale = FOCAL / z
    return WIDTH / 2 + x * scale, HEIGHT * HORIZON - y * scale, z


# ---------------------------------------------------------------------------
# The drawing. Faces are sorted back to front and painted opaque, so a near cube
# hides a far one. That is a painter's algorithm, and it is older than computers.
# ---------------------------------------------------------------------------


def render(surface, font, state):
    surface.fill(PAPER)
    yaw, pitch, dist = state["yaw"], state["pitch"], state["dist"]

    quads = []
    for cube in state["cubes"]:
        screen = [project(p, yaw, pitch, dist) for p in cube]
        for face in FACES:
            points = [(screen[i][0], screen[i][1]) for i in face]
            depth = sum(screen[i][2] for i in face) / 4
            quads.append((depth, points))

    quads.sort(key=lambda q: q[0], reverse=True)      # furthest first

    for _, points in quads:
        if not state["wireframe"]:
            pygame.draw.polygon(surface, PAPER, points)
        pygame.draw.lines(surface, INK, True, points, STROKE_WIDTH)

    readout = (f"seed {state['seed']}   chaos {state['chaos']:.2f}   "
               f"drag to orbit   [ ] chaos   + - zoom   W wireframe   S save")
    surface.blit(font.render(readout, True, (120, 116, 110)), (30, HEIGHT - 26))


def main():
    pygame.init()
    font = pygame.font.Font(None, 20)
    state = {"seed": SEED, "chaos": CHAOS, "yaw": YAW, "pitch": PITCH,
             "dist": DIST, "wireframe": False, "cubes": cubes(SEED, CHAOS)}

    if "--save" in sys.argv:
        name = sys.argv[sys.argv.index("--save") + 1]
        frame = pygame.Surface((WIDTH, HEIGHT))
        render(frame, font, state)
        pygame.image.save(frame, name)
        print(f"wrote {name}")
        return

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Schotter in three dimensions")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
                state["yaw"] += event.rel[0] * 0.006
                state["pitch"] = max(-1.4, min(1.4, state["pitch"] + event.rel[1] * 0.006))
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_SPACE:
                    state["seed"] = random.randint(0, 999999)
                elif event.key == pygame.K_LEFTBRACKET:
                    state["chaos"] = max(0.0, state["chaos"] - 0.1)
                elif event.key == pygame.K_RIGHTBRACKET:
                    state["chaos"] = min(4.0, state["chaos"] + 0.1)
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                    state["dist"] = max(6.0, state["dist"] - 1.0)
                elif event.key == pygame.K_MINUS:
                    state["dist"] = min(60.0, state["dist"] + 1.0)
                elif event.key == pygame.K_w:
                    state["wireframe"] = not state["wireframe"]
                elif event.key == pygame.K_r:
                    state.update(seed=SEED, chaos=CHAOS, yaw=YAW, pitch=PITCH, dist=DIST)
                elif event.key == pygame.K_s:
                    pygame.image.save(screen, "schotter3d.png")
                    print("wrote schotter3d.png")

                if event.key in (pygame.K_SPACE, pygame.K_LEFTBRACKET,
                                 pygame.K_RIGHTBRACKET, pygame.K_r):
                    state["cubes"] = cubes(state["seed"], state["chaos"])

        keys = pygame.key.get_pressed()
        state["yaw"] += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 0.02
        state["pitch"] = max(-1.4, min(1.4, state["pitch"]
                                       + (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 0.02))

        render(screen, font, state)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
