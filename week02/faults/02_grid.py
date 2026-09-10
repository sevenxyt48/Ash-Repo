"""
Spec: build a 3 x 5 grid of zeros, put a 1 in the top-left corner, exactly one 1.

    uv run 02_grid.py

It runs. It prints a grid. The grid is wrong. Find the line.
"""

ROWS, COLS = 3, 5

grid = [[0] * COLS] * ROWS
grid[0][0] = 1

for row in grid:
    print(row)

print("ones in the grid:", sum(sum(row) for row in grid))
