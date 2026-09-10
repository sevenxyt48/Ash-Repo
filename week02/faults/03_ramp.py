"""
Spec: print ten opacity steps — 0.0, 0.1, 0.2 ... up to 0.9 — one per line.

    uv run 03_ramp.py

It runs. It prints steps. Count them, and read the last one carefully.
"""

STEP = 0.1

value = 0.0
count = 0

while value < 1.0:
    print(f"step {count}: opacity {value}")
    value = value + STEP
    count += 1

print("steps printed:", count)
