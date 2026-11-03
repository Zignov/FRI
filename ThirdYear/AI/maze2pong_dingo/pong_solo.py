# -*- coding: utf-8 -*-
"""
Pong Solo - a minimal single-player terminal Pong game.

Standalone: one file, Python stdlib only, works on Windows / macOS / Linux.
Bounce the ball with your paddle (bottom area) to score points!
Miss = lose a life (3 total). How long can you survive?

Controls:
    arrows / WASD   move paddle
    space           serve / pause
    q / ESC         quit

Run:
    python pong_solo.py                          # normal play
    python pong_solo.py --seed 42                # reproducible ball physics

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


# ------------------------------------------------------------- game visuals
BALL         = C.BOLD + C.WHITE + "\u25cf\u25cf" + C.RED   + C.ENDC
PADDLE_BODY  = C.GREEN + C.BOLD + "\u2593\u2593" + C.ENDC
PADD_LEFT    = C.GREEN + C.BOLD + "\u259f\u2593" + C.ENDC
PADD_RIGHT   = C.GREEN + C.BOLD + "\u2593\u00b7" + C.ENDC
WALL_TOP     = C.DIM  + "\u25a1\u25a1" + C.ENDC
BLOCK_EMPTY  = C.GRAY + "\u25a1\u25a1" + C.ENDC


# ------------------------------------------------------------- game class

class Game:
    """A minimal single-player terminal Pong game."""
    W      = 28          # playable width (cells)
    PW     = 7           # paddle width (cells)
    WALL_Y = 0           # top wall row
    PAD_R  = 14          # paddle bottom row

    def __init__(self, seed=None):
        self.rng   = random.Random(seed)
        self.score = 0
        self.lives = 3
        self.state = "idle"
        self.t0    = time.time()
        self.bx    = self.W / 4.0
        self.by    = 3.0
        self.vx    = 0.0
        self.vy    = 0.0
        cx = max(1, min(self.W // 2 - self.PW // 2,
                        self.W - self.PW - 2))
        self.pad_x = cx

    def serve_ball(self):
        """Serve ball upward; returns status messages."""
        if self.lives <= 0:
            self.state = "gameover"
            return [C.RED + C.BOLD
                    + "Game over! Press Enter to restart." + C.ENDC]
        cx     = self.W // 2 - 1.0
        ang    = self.rng.uniform(0.3, 0.8)
        spd    = self.rng.uniform(3.0, 5.0)
        dr     = 1 if self.rng.random() < 0.5 else -1
        self.bx  = cx + self.rng.uniform(-1.5, 1.5)
        self.by  = 2.0
        self.vx  = spd * (dr * ang)
        self.vy  = -(spd * 0.7 + self.rng.uniform(0.5, 1.5))
        if self.bx < 1:
            self.bx = 1.0
        elif self.bx > self.W - 3:
            self.bx = float(self.W - 3)
        cx2 = max(1, min(self.W // 2 - self.PW // 2,
                         self.W - self.PW - 2))
        self.pad_x = cx2
        self.state = "playing"
        return []

    def move_paddle(self, direction):
        """direction: -1 (left) or +1 (right). Moves by 3 cells."""
        lo = 1
        hi = self.W - self.PW - 2
        if hi < lo:
            hi = lo
        self.pad_x = max(lo, min(self.pad_x + direction * 3, hi))

    def physics_tick(self):
        """One physics step. Returns messages for state changes."""
        if self.state != "playing":
            return []
        nx     = int(self.bx + self.vx)
        ny     = int(self.by + self.vy)
        bc     = self.bx + 0.5

        if nx <= 0:
            nx   = max(1, nx)
            self.vx = abs(self.vx)
        if nx >= self.W - 2:
            nx   = min(self.W - 3, nx)
            self.vx = -abs(self.vx)
        if ny <= Game.WALL_Y:
            ny   = max(1, ny)
            self.vy = abs(self.vy)

        pl     = self.pad_x
        pR     = pl + self.PW
        pr     = Game.PAD_R

        ok     = bc > pl and bc < pR
        if ok and int(self.by) >= pr - 3:
            hp   = (bc - pl) / float(self.PW)
            self.vx    = 8.0 * (hp - 0.5)
            self.vy    = -(abs(self.vy) + 0.2)
            ny         = pr - 2
            snap_x     = max(pl, min(pR - 1, int(bc)))
            self.bx    = float(snap_x)
            self.by    = float(pr - 2)
            self.score += 1
            return []

        if ny >= pr or int(self.by) >= pr:
            self.lives -= 1
            msg     = C.RED + ("Miss! " + str(self.lives)).ljust(16) + ("." + " lives left." ) + C.ENDC

            if self.lives <= 0:
                self.state   = "gameover"
                return [C.RED + C.BOLD + "Game over!" + C.ENDC, msg]
            cx2        = float(pl + self.PW // 2)
            snap_x     = max(pl, min(pR - 3, int(cx2)))
            self.bx    = float(snap_x)
            self.by    = float(pr)
            self.vx     = 0.0
            self.vy     = -3.5

        self.bx  = float(nx)
        self.by  = float(ny)
        return []

    def game_time(self):
        """Seconds elapsed since startup."""
        return max(0, int(time.time() - self.t0))


# ------------------------------------------------------------- rendering helpers

def _fg(g, x, y):
    """Return the double-width glyph for a grid cell."""
    if y == Game.WALL_Y:
        return WALL_TOP
    bx     = int(g.bx)
    by     = int(g.by)
    if abs(by - y) <= 1 and x >= bx and x < bx + 2:
        return BALL
    le     = float(x) / g.W
    re_    = float(g.W - 1 - x) / g.W
    edge   = max(le, re_)
    if edge > 0.85:
        a      = max(1, int((edge - 0.85) * 9))
        return C.DIM + ("\u25a1" * a)[:3] + C.ENDC
    elif edge > 0.7:
        return BLOCK_EMPTY
    return "  "


def _render(g, out, messages):
    """Render the complete game field to the output stream."""
    terminal_clear(out)
    w      = g.W
    grid_h = g.PAD_R + 4

    # title bar
    bn     = max(5, (70 - len(" PONG SOLO ")) // 2)
    out.write(C.GRAY + "\u250c" + "=" * bn + C.ENDC)
    out.write("\n")
    out.write("     " )
    out.write("\u26a1")
    out.write(" PONG SOLO ")
    out.write(C.GRAY + "=" * (bn + 1) + "\u2514" + C.ENDC)
    out.write("\n\n")

    # status line
    labels = {}
    idle_str   = "[Press SPACE to serve]"
    play_str   = "\u25cf Ball in play!"
    pause_str  = "\u23f8 PAUSED"
    labels["idle"]     = (C.CYAN,   " " + idle_str)
    labels["playing"]  = (C.GREEN,  " " + play_str)
    labels["paused"]   = (C.YELLOW + C.BOLD, " " + pause_str)
    col_, label_       = labels.get(g.state, ("", ""))
    pad_               = max(10, w * 6) - len(label_) - 3
    filler             = " " * max(0, pad_)
    out.write(C.GRAY + " \u2551" + C.ENDC)
    status = ("   " + col_ + label_ + C.ENDC)
    out.write(status + filler)
    out.write(C.GRAY + "\u2551\n")

    # grid rows
    for fy in range(grid_h):
        out.write(C.GRAY + " \u2551" + C.ENDC)
        for fx in range(w):
            out.write(_fg(g, fx, fy))
        out.write(" \u255a" + C.ENDC + "\n")

    # info: score / time / lives (hearts as 'c')
    sc_ = C.GREEN   + C.BOLD   + str(g.score).rjust(5)   + C.ENDC
    lt_ = C.DIM          + ("%04ds" % g.game_time())  + C.ENDC
    hrt = ""
    for i in range(3):
        if i < g.lives:
            hrt += C.GREEN       + "c"                 + C.ENDC
        else:
            hrt += C.GRAY        + "\u25cb"           + C.ENDC
    out.write("     Score:  " + sc_ + "    Time: " + lt_)
    out.write(hrt)
    out.write("\n")

    # extra messages
    for m_ in messages:
        out.write("       " + m_ + "\n")

    if _TERMINAL_MODE:
        cmd = "Arrows/WASD: move | space: serve/pause | q/Esc: quit"
    else:
        cmd = "[serve=space] [move=a/d] [quit=q/Esc]"
    out.write("      " + C.GRAY + cmd + C.ENDC + "\n")



# ------------------------------------------------------------- game driver

def play(args):
    """Main game loop - drives physics and rendering."""
    g          = Game(seed=args.seed)
    import io as _io
    out        = _io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                   errors="replace", line_buffering=True)
    messages   = []
    first      = True

    # welcome screen
    terminal_clear(out)
    bn         = max(4, (70 - len("  PONG SOLO  ")) // 2)
    out.write(C.GRAY + "\u250c" + "=" * bn + C.ENDC)
    out.write("\n")
    out.write("          Welcome\n")
    title = "  \u26a1 PONG SOLO  "
    out.write("     " + title)
    out.write("=" * (bn - len(title) // 2))
    out.write(C.GRAY + "=" + C.ENDC)
    out.write("\n\n")
    out.write(   "   arrows/WASD: move     SPACE: serve/pause     q/Esc: quit\n")
    out.write("                [Press SPACE to start]\n")
    flush_stdin()
    out.flush()

    last_tick    = time.time()
    tick_rate    = args.tick_rate
    rtime        = 1.0 / max(20, tick_rate * 2)
    last_render  = time.time()

    while True:
        flush_stdin()
        key     = next_key()
        msg     = messages[:]

        # quit check
        if key in ("q", "esc"):
            out.write("\n\nGoodbye! ")
            out.flush()
            return

        # paddle movement
        if key in ("a", "left"):
            g.move_paddle(-1)
        elif key in ("d", "right"):
            g.move_paddle(1)

        # serve / pause on space bar
        if key == " ":
            if g.state == "paused":
                msg    = [C.YELLOW + "  Resumed" + C.ENDC]
                g.state     = "playing"
            elif g.state in ("idle", "gameover"):
                msgs  = g.serve_ball()
                if g.state == "gameover":
                    _render(g, out, msgs)
                    out.flush()
                    time.sleep(0.5)
                    sys.stdout.write("  Play again? (Enter=yes, q=quit): ")
                    sys.stdout.flush()
                    reply   = sys.stdin.readline().strip().lower()
                    if len(reply) > 0 and reply[0] in ("q", "Q"):
                        out.write("\nGoodbye!\n")
                        out.flush()
                        return
                    g     = Game(seed=args.seed)
                    messages      = []
                    continue
                msg   = msgs
            elif g.state == "playing":
                g.state       = "paused"
                msg       = [C.YELLOW + C.BOLD + "  Paused" + C.ENDC]

        # physics tick (throttled)
        now       = time.time()
        elapsed   = now - last_tick
        if elapsed >= 1.0 / max(5, tick_rate):
            extra   = g.physics_tick()
            if extra:
                msg   = extra[:]
            last_tick     = time.time()

        # render (throttled to ~20fps or faster)
        dt      = now - last_render
        if dt >= rtime or first:
            _render(g, out, [] + msg)
            out.flush()
            last_render     = time.time()
            first     = False


def main(argv=None):
    p       = argparse.ArgumentParser(
        description="Pong Solo - single-player terminal Pong")
    p.add_argument("--seed", type=int, default=None,
                   help="fix ball physics (reproducible)")
    p.add_argument("-t", "--tick-rate", type=int, default=15,
                   help="physics steps per second (default: 15)")
    p.add_argument("--no-color", action="store_true")
    args      = p.parse_args(argv)
    install_colors(not args.no_color)
    try:
        play(args)
    except KeyboardInterrupt:
        print("\nGoodbye!")

if __name__ == "__main__":
    main()

