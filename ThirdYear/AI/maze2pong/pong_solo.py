# -*- coding: utf-8 -*-
"""
Pong Solo - a minimal single-player terminal pong game.

Standalone: one file, Python stdlib only, works on Windows / macOS / Linux.
A fresh match against the machine is started every run; first to 11 points wins.

Controls:
    arrows / WASD   move
    q / ESC         quit

Run:
    python pong_solo.py

Uses only the standard library.
"""

import argparse
import os
import random
import sys
import time

# ------------------------------------------------------------- terminal IO

_TERMINAL_MODE = sys.stdin.isatty()

if os.name == "nt":
    import msvcrt


def terminal_clear(out):
    """Clear the screen in the most reliable way for this platform.

    Windows: 'cls' works on every console, regardless of Python version
    or VT-processing mode. POSIX: ANSI clear + cursor-home, supported by
    every modern terminal emulator (xterm-compatible).
    Piped input: no clearing, just separate frames with newlines.
    """
    if not _TERMINAL_MODE:
        out.write("\n")
    elif os.name == "nt":
        out.flush()
        os.system("cls")
    else:
        out.write("\033[2J\033[H")


_ARROW_SEQ = {"A": "up", "B": "down", "C": "right", "D": "left"}
_LAST_RAW = ""    # raw bytes of the last key - shown by --keytest


def _read_posix_key():
    """Read one key on POSIX, tolerating slow terminal emulators.

    Collects the full escape sequence before deciding, so a terminal that
    delivers ESC and [A with a small delay between bytes is not mistaken
    for a plain ESC (which would quit the game).
    """
    global _LAST_RAW
    import select
    import termios
    import tty
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch != "\x1b":
            _LAST_RAW = ch
            if ch in ("\r", "\n"):
                return "\r"
            if ch == "\b":
                return ""
            return ch.lower()
        seq = ch
        for _ in range(5):                          # at most ESC + 5 bytes
            if select.select([sys.stdin], [], [], 0.1)[0]:
                seq += sys.stdin.read(1)
            else:
                break
        _LAST_RAW = seq
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

    if seq == "\x1b":                    # plain ESC (nothing followed)
        return "esc"
    if len(seq) >= 3 and seq[1] in ("[", "O"):
        # ESC [ A  (xterm form)  or  ESC O A  (SS3 form)
        return _ARROW_SEQ.get(seq[2], "")     # unknown: ignore, don't quit
    return ""                              # some other sequence: ignore


def read_raw():
    """Read one keypress.

    Returns 'up'/'down'/'left'/'right'/'esc', or a single character
    (Enter as '\\r'). With piped stdin (not a TTY) each line is yielded
    one character at a time, which keeps the game scriptable/testable.
    """
    global _LAST_RAW
    if _TERMINAL_MODE:
        if os.name == "nt":
            k = ord(msvcrt.getch())
            if k in (0, 224):              # prefix for special keys
                k = ord(msvcrt.getch())
                _LAST_RAW = "ext 0x%02x" % k
                return {80: "down", 72: "up", 75: "left", 77: "right"}.get(
                    k, "")
            _LAST_RAW = chr(k)
            if k == 27:
                return "esc"
            if k in (13, 10):
                return "\r"
            if k == 8:
                return ""
            return chr(k).lower()
        return _read_posix_key()
    line = sys.stdin.readline()            # scripted mode
    if line == "":
        return ["eof"]
    return list(line.strip()) or [""]


_buffer = []


def next_key():
    """next_key() from read_raw(), buffering one line at a time."""
    if not _buffer:
        _buffer.extend(read_raw())
    return _buffer.pop(0)


def flush_stdin():
    """Consume all pending keys (incl. partial escape sequences).

    Terminal mode only - with piped stdin there is nothing to flush and
    (on Windows) msvcrt may not refer to the pipe at all.
    """
    if not _TERMINAL_MODE:
        return
    if os.name == "nt":
        try:
            while msvcrt.kbhit():
                msvcrt.getch()
        except Exception:
            pass
    else:
        import select
        while select.select([sys.stdin], [], [], 0)[0]:
            sys.stdin.read(1)


# ------------------------------------------------------------- colors

class C:
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"


def install_colors(enabled):
    if enabled:
        return
    for name in list(vars(C)):
        if not name.startswith("_") and name != "ENDC":
            setattr(C, name, "")


# ------------------------------------------------------------- game

class Game:
    def __init__(self, width=25, height=13, score_to_win=11, name="CPU"):
        self.rng = random.Random()
        self.width, self.height = width, height
        self.score_to_win = score_to_win
        self.paddle_h = 2
        self.player_y = self.height // 2 - 1       # top row of player paddle
        self.ai_y = self.player_y
        self.ball = (self.width // 2, self.height // 2)
        self.dir = (self.rng.choice((-1, 1)), self.rng.choice((-1, 1)))
        self.score = 0                             # points we scored
        self.ai_score = 0                          # points the CPU scored
        self.state = "playing"
        self.started = time.time()
        self.last_tick = time.monotonic()
        self.tick_time = 0.07

    # --- world

    def _on_paddle(self, top, y):
        """Is row y covered by the paddle whose top row is `top`?"""
        return top <= y < top + self.paddle_h

    def _reset_ball(self):
        self.ball = (self.width // 2, self.height // 2)
        self.dir = (self.rng.choice((-1, 1)), self.rng.choice((-1, 1)))

    def _update_ai(self):
        """Chase the ball (or return to centre when it moves away)."""
        target = self.ball[1] if self.dir[0] > 0 else self.height // 2
        if self.ai_y < target:
            self.ai_y += 1
        elif self.ai_y > target:
            self.ai_y -= 1
        self.ai_y = max(1, min(self.ai_y, self.height - self.paddle_h - 1))

    # --- rules

    def try_move(self, dx, dy):
        """Apply one player move; returns the game state."""
        if self.state != "playing":
            return self.state
        ny = self.player_y + dy
        if 1 <= ny <= self.height - self.paddle_h - 1:
            self.player_y = ny
        return self.state

    def tick(self):
        """Advance the ball / the AI; returns the game state."""
        if self.state != "playing":
            return self.state
        bx, by = self.ball
        dx, dy = self.dir
        ny = by + dy
        if ny < 1 or ny > self.height - 2:
            dy = -dy
            ny = by + dy
        nx = bx + dx
        if dx < 0 and nx == 1 and self._on_paddle(self.player_y, ny):
            dx = -dx
            nx = bx + dx
        elif dx > 0 and nx == self.width - 2 and self._on_paddle(self.ai_y, ny):
            dx = -dx
            nx = bx + dx
        if nx <= 0 or nx >= self.width - 1:
            if nx <= 0:
                self.ai_score += 1            # player missed -> CPU scores
            else:
                self.score += 1               # CPU missed -> player scores
            self._reset_ball()
            if self.score >= self.score_to_win:
                self.state = "won"
            elif self.ai_score >= self.score_to_win:
                self.state = "lost"
            return self.state
        self.ball = (nx, ny)
        self.dir = (dx, dy)
        self._update_ai()
        return self.state

    # --- rendering

    def render(self, out, messages=()):
        terminal_clear(out)
        for y in range(self.height):
            for x in range(self.width):
                self._glyph(out, x, y)
            out.write("\n")
        out.write("\n")
        out.write("Score: You " + str(self.score) + " - CPU " + str(self.ai_score) +
                  " (first to " + str(self.score_to_win) + ")\n")
        for msg in messages:
            out.write(msg + "\n")
        if _TERMINAL_MODE:
            out.write(C.GRAY +
                      "\narrows/WASD: move | r: restart | q/ESC: quit\n")
        out.write(C.ENDC)

    def _glyph(self, out, x, y):
        # ball
        if (x, y) == self.ball:
            out.write(C.BOLD + C.YELLOW + "O" + C.ENDC + " ")
            return

        # outer border is always drawn
        if x in (0, self.width - 1) or y in (0, self.height - 1):
            out.write(C.WHITE + "░░" + C.ENDC)
            return

        # paddles: 2 tall, drawn as stacked solid blocks
        if x == 1 and self.player_y <= y < self.player_y + self.paddle_h:
            out.write(C.BOLD + C.RED + "██" + C.ENDC)
            return
        if x == self.width - 2 and self.ai_y <= y < self.ai_y + self.paddle_h:
            out.write(C.BOLD + C.BLUE + "██" + C.ENDC)
            return

        out.write("  ")                       # empty playfield


# ------------------------------------------------------------- driver

def get_player_name(args):
    if not _TERMINAL_MODE:
        return "Player"
    return input("Player 1 (press Enter for 'Player'): ").strip() or "Player"


def play(args):
    import io
    if args.keytest:
        out = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                               errors="replace", line_buffering=True)
        out.write("KEY TEST: press keys; each one the game receives is printed.")
        out.write("\nTry the arrows and w/a/s/d. Quit with q.")
        out.write("\n(Terminal mode: {}, platform: {})".format(
            _TERMINAL_MODE, os.name))
        out.write("\n")
        for _ in range(100):
            k = next_key()
            detail = "   (raw: {})".format(repr(_LAST_RAW)) if _TERMINAL_MODE else ""
            out.write("  got: {}{}\n".format(repr(k), detail))
            out.flush()
            if k in ("q", "esc", "eof"):
                break
        out.write("Done.\n")
        out.flush()
        return

    out = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                           errors="replace", line_buffering=True)
    name = get_player_name(args)
    game_factory = lambda: Game(score_to_win=args.score_to_win)
    move_vec = {
        "up": (0, -1), "w": (0, -1),
        "down": (0, 1), "s": (0, 1),
    }

    g = game_factory()
    messages = []
    flush_stdin()                          # drop stray Enter from prompt
    first = True

    while True:
        if g.state != "playing":
            if g.state == "won":
                g.render(out, [
                    C.GREEN + C.BOLD +
                    "You win, {}! First to {} points!".format(
                        name, g.score_to_win) + C.ENDC])
            else:
                g.render(out, [
                    C.RED + C.BOLD +
                    "You lose! The CPU scored {} points.".format(
                        g.ai_score) + C.ENDC])
            out.flush()
            try:
                input("\nPress Enter to play again (q quits)...")
            except EOFError:
                return
            if sys.stdin.readline().strip() == "q":
                out.write("Goodbye!\n")
                out.flush()
                return
            g = game_factory()
            messages = []
            first = True
            continue

        g.render(out, messages if first else [])
        first = False
        key = next_key()
        if key in ("q", "esc", "eof"):
            out.write("Goodbye!\n")
            out.flush()
            return
        if key == "r":
            g = game_factory()
            messages = ["New match!"]
            continue
        vec = move_vec.get(key)
        if vec:
            g.try_move(*vec)
            messages = []
        now = time.monotonic()
        if now - g.last_tick >= g.tick_time:
            g.tick()
            g.last_tick = now


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Pong Solo - single-player terminal pong game")
    p.add_argument("--score-to-win", type=int, default=11,
                   help="first to this many points wins")
    p.add_argument("--keytest", action="store_true",
                   help="diagnostic: print every key the game receives")
    p.add_argument("--no-color", action="store_true")
    args = p.parse_args(argv)

    install_colors(not args.no_color)

    try:
        play(args)
    except KeyboardInterrupt:
        print("\nGoodbye!")


if __name__ == "__main__":
    main()
