# Week 2 Lab: Maze Agent Challenge

Ungraded practice · ~2 h. Pick **one feature** from the menu and implement it
with **three different local models** — same prompt, fresh file for each.
You write the prompt; the agent writes and runs the code; you verify by
playing the game.

## 1. Setup

1. Install Pi: `npm install -g --ignore-scripts @earendil-works/pi-coding-agent`
2. Pull **three small models** from the "Agentic Models That Run at Home"
   slide (the top rows, e.g. `gemma4:e4b`, `lfm2.5:8b`, `qwen3.5:9b`) —
   they must all run comfortably on a laptop. CPU-only: prefer the MoE rows.
   The 20B+ rows are next week's dingo task, not this lab.
3. Copy `models_local.json` to Pi's config dir (macOS/Linux:
   `~/.pi/agent/`, Windows: `C:\Users\<you>\.pi\agent\`) as `models.json`;
   set the `id` fields to the three tags you pulled.
4. Open `pi` in this folder; `/model` must list all three.
5. Play a few minutes of the game (`python maze_solo.py`) so you know what a
   working feature has to do.

## 2. Task

1. Choose **one** feature from the menu below.
2. Write the prompt **once**, yourself: describe the feature's rules exactly
   and end with "show me how to start it and how it ends." Keep a copy —
   the prompt is identical for all three models.
3. For each model (smallest first):
   - save a fresh copy: `maze_a.py`, `maze_b.py`, `maze_c.py` (each starts
     from the untouched `maze_solo.py`);
   - give the prompt to Pi with that model selected;
   - run the copy yourself and play-test the feature;
   - note every follow-up prompt you had to send.
4. If a model fails repeatedly, that is a valid result — record it, move to
   the next model.

### Feature menu (all medium)

- **Ghost enemy** — spawns mid-maze, moves 1 tile toward you every 3 of
  your moves; caught = lose.
- **Moving pickup** — a sparkle respawns at a random floor tile every
  50 moves; stepping on it grants +20 moves.
- **Three levels** — clearing the door loads a new, bigger maze; your move
  budget carries over; win after level 3.
- **Save & load** — `s` writes position/state to `save.dat`, entering a
  maze code from a previous run resumes it; show the format.
- **Secret key** — one golden key behind a locked room; opening the door
  first time costs 7 moves, second time it's free.

**Rules** — one file, stdlib only; don't break the existing game (keys,
door, budgets, fog); no internet for the feature design; identical prompt for all three models.

## 3. Report (we will discuss it next week during lectures, no report needed, just make sure you have your answers & comments ready, you could also have a demo with you if you have a laptop)

Four short answers:

1. Your prompt (as typed) and, per model: follow-up prompts needed.
2. Did the feature actually work in-game per model? What broke?
3. What did each model do differently — plan, self-correction, code quality?
4. Which model for this kind of change, and when would you use the others?
