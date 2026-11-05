# -*- coding: utf-8 -*-
# Throwaway self-test for maze_solo.py (run, then delete).
import collections
import itertools
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
import maze_solo as m

HERE = os.path.dirname(__file__)
PY = sys.executable

def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        raise SystemExit(1)

# --- structural checks
rng_ok = True
for seed in (1, 7, 42):
    g = m.Game(width=25, height=15, seed=seed, moves=99999)
    w, h = g.width, g.height
    border_ok = (
        all(g.maze[0][x] == m.WALL for x in range(w))
        and all(g.maze[h - 1][x] == m.WALL for x in range(w))
        and all(g.maze[y][0] == m.WALL for y in range(h))
        and all(g.maze[y][w - 1] == m.WALL for y in range(h))
    )
    check("border walls (seed %d)" % seed, border_ok)

    # connectivity: every open cell reachable from the start
    start = (1, 1)
    seen = {start}
    q = collections.deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and g.maze[ny][nx] != m.WALL \
                    and (nx, ny) not in seen:
                seen.add((nx, ny))
                q.append((nx, ny))
    opens = {(x, y) for y in range(h) for x in range(w)
             if g.maze[y][x] != m.WALL}
    check("fully connected (seed %d)" % seed, seen == opens)

check("4 keys placed", len(g.keys) == m.NUM_KEYS)
check("door reachable, distinct from keys",
      g.door in opens and not (g.keys & {g.door}) and (1, 1) not in g.keys)

a = m.Game(width=25, height=15, seed=42, moves=1)
b = m.Game(width=25, height=15, seed=42, moves=1)
check("same seed -> same maze", a.maze == b.maze and a.code == b.code)
c = m.Game(width=25, height=15, seed=43, moves=1)
check("different seed -> different maze", a.maze != c.maze)

def solve(g):
    """Greedy BFS tour: start -> each key -> door. Returns key string."""
    w, h = g.width, g.height
    pos = (1, 1)
    targets = list(g.keys) + [g.door]
    moves_out = []
    for t in targets:
        prev = {pos: None}
        q = collections.deque([pos])
        while q:
            cur = q.popleft()
            if cur == t:
                break
            x, y = cur
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, y + dy)
                if 0 <= n[0] < w and 0 <= n[1] < h and \
                        g.maze[n[1]][n[0]] != m.WALL and n not in prev:
                    prev[n] = cur
                    q.append(n)
        path = []
        cur = t
        while prev[cur] is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        for (px, py), (nx, ny) in zip([pos] + path, path):
            moves_out.append({(1, 0): "d", (-1, 0): "a",
                              (0, 1): "s", (0, -1): "w"}[(nx - px, ny - py)])
        pos = t
    return "".join(moves_out)

def first_n_moves(g, n):
    """First n valid moves of the full tour (guaranteed legal moves)."""
    return solve(g)[:n]

# --- end-to-end: scripted play of the actual game process
moves = solve(m.Game(width=25, height=15, seed=42, moves=99999))
stdin_win = moves + "\nx\nq\n"
r = subprocess.run([PY, os.path.join(HERE, "maze_solo.py"),
                    "--seed", "42", "--moves", "99999", "--no-color"],
                   input=stdin_win, capture_output=True, text=True,
                   timeout=60, cwd=HERE)
check("e2e win (seed 42)", "You win" in r.stdout)
check("e2e maze code shown", "Maze code:" in r.stdout)

r = subprocess.run([PY, os.path.join(HERE, "maze_solo.py"),
                    "--seed", "7", "--moves", "2", "--no-color"],
                   input=first_n_moves(m.Game(width=25, height=15, seed=7, moves=99999), 2)
                   + "\nx\nq\n", capture_output=True, text=True,
                   timeout=60, cwd=HERE)
check("e2e lose (2 moves)", "Out of moves" in r.stdout)

r = subprocess.run([PY, os.path.join(HERE, "maze_solo.py"),
                    "--seed", "7", "--peek", "--no-color"],
                   input="q\n", capture_output=True, text=True,
                   timeout=60, cwd=HERE)
check("q quits cleanly", "Goodbye" in r.stdout)

print("ALL TESTS PASSED")
