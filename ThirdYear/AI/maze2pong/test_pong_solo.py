# -*- coding: utf-8 -*-
# Throwaway self-test for pong_solo.py (run, then delete).
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
import pong_solo as p

HERE = os.path.dirname(__file__)
PY = sys.executable

def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        raise SystemExit(1)

# --- structural checks
g = p.Game(width=25, height=13, score_to_win=11)
check("starts playing", g.state == "playing")
check("score 0-0", g.score == 0 and g.ai_score == 0)

g.try_move(0, -1)
check("player moves up", g.player_y == 4)
g.try_move(0, 99)
check("player clamped", g.player_y == 4)
g.try_move(0, 1)
check("player moves down", g.player_y == 5)

g.ball = (22, g.player_y + 1)
g.dir = (1, 0)
g.tick()
check("ai chases + ball bounced off ai", g.dir[0] == -1 and g.ball == (21, g.player_y + 1))

# --- scoring
g = p.Game(width=25, height=13, score_to_win=2)
g.ball = (23, g.height // 2)
g.dir = (1, 0)
g.tick()
check("player scored on cpu miss", g.score == 1 and g.state == "playing")

g = p.Game(width=25, height=13, score_to_win=2)
g.ball = (1, g.height // 2)
g.dir = (-1, 0)
g.tick()
check("cpu scored on player miss", g.ai_score == 1 and g.state == "playing")

g = p.Game(width=25, height=13, score_to_win=2)
g.ball = (23, g.height // 2)
g.dir = (1, 0)
g.tick()
g.ball = (23, g.height // 2)
g.dir = (1, 0)
g.tick()
check("player wins match", g.state == "won" and g.score == 2)

g = p.Game(width=25, height=13, score_to_win=2)
g.ball = (1, g.height // 2)
g.dir = (-1, 0)
g.tick()
g.ball = (1, g.height // 2)
g.dir = (-1, 0)
g.tick()
check("cpu wins match", g.state == "lost" and g.ai_score == 2)

# --- end-to-end: scripted quit of the actual game process
r = subprocess.run([PY, os.path.join(HERE, "pong_solo.py"),
                    "--score-to-win", "2", "--no-color"],
                   input="q\n", capture_output=True, text=True,
                   timeout=60, cwd=HERE)
check("e2e quit cleanly", "Goodbye" in r.stdout)

print("ALL TESTS PASSED")
