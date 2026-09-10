"""
Spec: print the mean surface speed, in knots, of the six readings below.

    uv run 01_average.py

It runs. It prints a number. The number is wrong. Find the line.
"""

READINGS = """time,knot
14:00,1.20
14:15,1.05
14:30,0.80
14:45,0.55
15:00,0.30
15:15,0.10
"""

rows = READINGS.strip().splitlines()
speeds = [float(row.split(",")[1]) for row in rows[1:]]

print(f"{len(speeds)} readings")
print(f"mean speed: {sum(speeds) / len(rows):.4f} knots")
