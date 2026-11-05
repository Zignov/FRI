# Pong Solo

A minimal, standalone, single-player terminal pong game.

- **One file** (`pong_solo.py`), **Python stdlib only** — no pip installs.
- Cross-platform: Windows / macOS / Linux (and scriptable via piped stdin).
- You against the machine; first to **11 points** wins.

## Game

- Move your paddle (red blocks) with the arrows / WASD and try to keep the
  ball away from it - the CPU paddle (blue blocks) chases the ball.
- The ball (yellow block) bounces off the top/bottom of the arena and off
  the paddles; when it sails past a paddle, the other side scores.
- First to **11 points** wins the match.

## Controls

| key | action |
|---|---|
| arrows / WASD | move |
| `r` | restart match |
| `q` / ESC | quit |

## Run

```bash
python pong_solo.py                # or: python3
python pong_solo.py --score-to-win 5   # first to 5 points
python pong_solo.py --keytest      # diagnostic: print every key the game receives
python pong_solo.py --no-color     # plain ASCII output
```

## Tests

Headless self-test (game rules + end-to-end scripted quit via piped stdin):

```bash
python test_pong_solo.py
```

## Notes

- Piped stdin (CI, scripts): the game is fully scriptable — each line of
  stdin is consumed one key at a time; EOF / `q` quits. That is how the
  e2e tests play real games.
- Screen clearing: `cls` on Windows, ANSI `\033[2J\033[H` on POSIX, plain
  newlines when piped. If you target *ancient* macOS Terminal.app (< 10.15),
  the ANSI clear is ignored — in that rare case swap the POSIX branch of
  `terminal_clear()` to `os.system("clear")`.
- The block glyphs need a UTF-8 capable terminal. Modern Windows
  console (10/11), Windows Terminal, iTerm2 and standard Linux emulators
  all handle them. In *real* terminals Python prints them as UTF-8
  regardless of the console code page; only *piped* output may be
  code-page-limited on legacy Windows.

---

*The original `maze_solo.py` / `test_maze_solo.py` files are kept unchanged
in this folder if you ever want to go back to the maze.*
