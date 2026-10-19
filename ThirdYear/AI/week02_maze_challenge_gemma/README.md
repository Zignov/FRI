# Maze Solo

A minimal, standalone, single-player terminal maze game.

- **One file** (`maze_solo.py`), **Python stdlib only** — no pip installs.
- Cross-platform: Windows / macOS / Linux (and scriptable via piped stdin).
- A fresh **random maze** (recursive division, perfect maze) every run.
- Visuals mirror the original multiplayer maze game: white block walls
  fading with distance (▓▓ style shading), ░░ border, ≡≡ keys, »« door,
  and the first two letters of your name as the player symbol.

## Game

- Collect all **4 keys (≡≡)**, then reach the **door (»«)** to escape.
- You have a limited move budget (default 150). Boosts `3x`/`1x` add 30/10 moves.
- Fog of war: you only explore a radius (`--sight`) around your position;
  explored walls stay visible (dimmed), unexplored areas are blank.
- Win/lose ends reveal the whole maze and print its 4-digit "maze code"
  (md5 prefix of the layout).

## Controls

| key | action |
|---|---|
| arrows / WASD | move |
| `r` | new maze |
| `q` / ESC | quit |

## Run

```bash
python maze_solo.py                # or: python3
python maze_solo.py --seed 42      # reproducible maze - share seeds!
python maze_solo.py --moves 200 --sight 5
python maze_solo.py --peek         # reveal the whole maze (easy mode)
```

Options: `--width`/`--height` (oddified automatically), `--moves 0` =
unlimited, `--no-color`.

## Tests

Headless self-test (maze invariants + end-to-end playthrough driven by a
BFS solver through piped stdin):

```bash
python test_maze_solo.py
```

## Notes

- Piped stdin (CI, scripts): the game is fully scriptable — each line of
  stdin is consumed one key at a time; EOF / `q` quits. That is how the
  e2e tests play real games.
- Screen clearing: `cls` on Windows, ANSI `\033[2J\033[H` on POSIX, plain
  newlines when piped. If you target *ancient* macOS Terminal.app (< 10.15),
  the ANSI clear is ignored — in that rare case swap the POSIX branch of
  `terminal_clear()` to `os.system("clear")`.
- The block/dingbat glyphs need a UTF-8 capable terminal. Modern Windows
  console (10/11), Windows Terminal, iTerm2 and standard Linux emulators
  all handle them. In *real* terminals Python prints them as UTF-8
  regardless of the console code page; only *piped* output may be
  code-page-limited on legacy Windows.
