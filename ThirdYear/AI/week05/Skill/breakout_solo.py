# -*- coding: utf-8 -*-
"""
Breakout Solo - the classic brick-breaker in one terminal, single player.

Standalone: one file, Python stdlib only, works on Windows / macOS / Linux.
Same framework as maze_solo.py / snake_solo.py / pong_solo.py (same terminal
IO, colors, and flags). One paddle at the bottom, a grid of coloured bricks
above: break the whole wall to win. The ball's angle changes depending on
where it hits a brick and on where you catch it with the paddle, and it gets
faster after every brick. Three lives; the ball auto-serves after a short
countdown.

Every 5th destroyed brick drops a pickup ('+'); catching one from the paddle
spawns an extra ball off the paddle.  A life is lost only when no balls remain.

Controls:
    a / d  or  left / right     move the paddle
    p                   pause / resume
    r                   new game
    q / ESC              quit

Run:
    python breakout_solo.py
    python breakout_solo.py --lives 3
    python breakout_solo.py --no-color

Uses only the standard library.
"""

import argparse
import os
import queue
import sys
import time
import io

# ------------------------------------------------------------- terminal IO

_TERMINAL_MODE = sys.stdin.isatty()

if os.name == "nt":
    import msvcrt


def _cbreak(fd):
    """Put stdin in cbreak mode: non-canonical, no echo, one-byte reads.

    cbreak, not raw: OPOST (output post-processing) stays on, so the tty
    keeps translating LF to carriage-return + LF for display while we wait
    for a key.  With raw mode every drawn row would start where the previous
    one ended (the screen splat on macOS). Works on old (tty.cbreak) and
    new (tty.setcbreak) Python versions.
    """
    import tty
    if hasattr(tty, "setcbreak"):
        tty.setcbreak(fd)
    else:
        tty.cbreak(fd)


def terminal_clear(out):
    if not _TERMINAL_MODE:
        out.write("\n")
    elif os.name == "nt":
        out.flush()
        os.system("cls")
    else:
        out.flush()
        try:
            os.system("clear")          # $TERM-aware; safe on Terminal.app / iTerm2
        except Exception:
            out.write("\033[2J\033[H")
        out.flush()


def _nt_key_char(k):
    return {80: "down", 72: "up", 75: "left", 77: "right"}.get(k, "")


_KEYQ = None


def _blocking_mac_key():
    """Blocking single-key read (cbreak mode, macOS/Linux).
    cbreak, not setraw: the tty keeps output post-processing (OPOST) on,
    so newlines still translate to carriage-return+LF while we wait for a
    key.  With setraw they would not, and every drawn row would start where
    the previous one ended (screen splat on macOS).
    """
    import termios
    import tty
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    _cbreak(fd)
    try:
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    if ch == "":
        return "eof"
    if ch != "\x1b":
        if ch in ("\r", "\n"):
            return "\r"
        if ch == 8:
            return ""
        return ch.lower()
    import select
    seq = ch
    for _ in range(5):
        if select.select([sys.stdin], [], [], 0.05)[0]:
            seq += sys.stdin.read(1)
        else:
            break
    if seq == "\x1b":
        return "esc"
    if len(seq) >= 3 and seq[1] in ("[", "O"):
        return _ARROW_SEQ.get(seq[2], "")
    return ""


def _ensure_key_reader():
    """One dedicated thread keeps cbreak mode and pushes parsed keys to a queue.
    poll_key() then never touches select() or termios -- robust on macOS."""
    global _KEYQ
    if _KEYQ is not None:
        return
    _KEYQ = queue.Queue()

    def run():
        try:
            while True:
                k = _blocking_mac_key()
                _KEYQ.put(k)
                if k == "eof":
                    break
        except Exception:
            try:
                _KEYQ.put("eof")
            except Exception:
                pass

    import threading
    threading.Thread(target=run, daemon=True).start()



def read_raw():
    """Read one keypress (blocking). Piped stdin: line yielded char by char.
    In piped mode every key advances one tick, so the game stays scriptable."""
    if _TERMINAL_MODE:
        if os.name == "nt":
            k = ord(msvcrt.getch())
            if k in (0, 224):
                k = ord(msvcrt.getch())
                return _nt_key_char(k)
            if k == 27:
                return "esc"
            if k in (13, 10):
                return "\r"
            if k == 8:
                return ""
            return chr(k).lower()
        import select
        import termios
        import tty
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            _cbreak(fd)
            ch = sys.stdin.read(1)
            if ch != "\x1b":
                if ch in ("\r", "\n"):
                    return "\r"
                if ch == "\b":
                    return ""
                return ch.lower()
            seq = ch
            for _ in range(5):
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    seq += sys.stdin.read(1)
                else:
                    break
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        if seq == "\x1b":
            return "esc"
        if len(seq) >= 3 and seq[1] in ("[", "O"):
            return {"A": "up", "B": "down", "C": "right", "D": "left"}.get(
                seq[2], "")
        return ""
    line = sys.stdin.readline()
    if line == "":
        return ["eof"]
    return list(line.strip()) or [""]


def poll_key():
    if not _TERMINAL_MODE:
        return None
    if os.name == "nt":
        if not msvcrt.kbhit():
            return None
        k = ord(msvcrt.getch())
        if k in (0, 224):
            if msvcrt.kbhit():
                k = ord(msvcrt.getch())
            return _nt_key_char(k)
        if k == 27:
            return "esc"
        if k in (13, 10):
            return "\r"
        if k == 8:
            return None
        return chr(k).lower()
    _ensure_key_reader()
    try:
        return _KEYQ.get_nowait()
    except queue.Empty:
        return None



_BUFFER = []


def next_key():
    if not _BUFFER:
        _BUFFER.extend(read_raw())
    return _BUFFER.pop(0)


def flush_stdin():
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
    RED = "\033[91m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"


def install_colors(enabled):
    if enabled:
        return
    for name in list(vars(C)):
        if not name.startswith("_"):
            setattr(C, name, "")


ROW_COLORS = ["RED", "YELLOW", "GREEN", "CYAN", "BLUE", "MAGENTA",
              "RED", "YELLOW"]

# ------------------------------------------------------------- game

BRICK_COLS = 15
BRICK_ROWS = 8
GRID_W = 32            # unit columns (0 and GRID_W-1 are the walls)
GRID_H = 20            # unit rows (0 and GRID_H-1 are the floor/ceiling)
BRICK_Y0 = 2           # first brick row
PADDLE_W = 5
PADDLE_Y = GRID_H - 3
BASE_TICK_MS = 140      # ball flight speed at the start (Nokia-ish: you can track it)
MIN_TICK_MS = 60
TICK_STEP_MS = 3       # faster after every broken brick
SERVE_DELAY = 10       # ticks between a life being lost and the serve
POINTS_PER_BRICK = 10
LIVES_DEFAULT = 3
PICKUP_CHAR = "+"      # char drawn for a falling powerup
BREAKS_PER_PICKUP = 5  # destroy N bricks to earn one


class Game:
    def __init__(self, lives=LIVES_DEFAULT):
        self.lives = lives
        self.alive = [[True] * BRICK_COLS for _ in range(BRICK_ROWS)]
        self.bricks_left = BRICK_COLS * BRICK_ROWS
        self.score = 0
        self.state = "serving"
        self.tick = BASE_TICK_MS
        self.px = GRID_W // 2 - PADDLE_W // 2
        self.serve_dir = 1
        self.breaks_since_pickup = 0
        self.balls: list[tuple] = []       # all active (x, y) tuples
        self.pickups: list[tuple[int, int]] = []   # falling (x, y) pickups
        self._reset_serve()

    def _reset_serve(self):
        """Reset the serve state & spawn one ball."""
        self.state = "serving"
        self.countdown = SERVE_DELAY
        self.serve_dir = -self.serve_dir  # alternate start direction
        self.balls.clear()
        self.pickups.clear()
        self.balls.append((self.px + PADDLE_W // 2, PADDLE_Y - 1))
        # serve velocity (shared by all balls for the countdown trickle)
        self.vx_serv = self.serve_dir
        self.vy_serv = 0

    # --- geometry helpers ── unchanged

    def block_at(self, x, y):
        """Brick (r, c) covering unit cell (x, y), or None if none there."""
        r = y - BRICK_Y0
        if r < 0 or r >= BRICK_ROWS:
            return None
        c = (x - 1) // 2
        if c < 0 or c >= BRICK_COLS:
            return None
        return (r, c)

    # --- rules ── unchanged except for power-up counter

    def move_player(self, dx):
        if self.state not in ("playing", "serving"):
            return
        self.px = max(1, min(GRID_W - 1 - (PADDLE_W - 1), self.px + dx))

    def break_brick(self, r, c):
        """Break one brick; returns True if it was alive."""
        if not self.alive[r][c]:
            return False
        self.alive[r][c] = False
        self.bricks_left -= 1
        self.score += POINTS_PER_BRICK
        self.tick = max(MIN_TICK_MS, self.tick - TICK_STEP_MS)
        # every 5th broken brick → spawn a falling power-up
        self.breaks_since_pickup += 1
        if self.bricks_left == 0 and self.state != "lost":
            self.state = "won"
        return True

    def step(self):
        """Advance one tick. Returns 'brick', 'life', or None."""
        if self.state in ("won", "lost"):
            return None

        # --- serving countdown ── balls trickle toward the paddle
        if self.state == "serving":
            self.countdown -= 1
            if self.countdown <= 0:
                # convert all current balls to (x,y,vx,vy) with initial velocities
                self.vx_serv = self.serve_dir
                self.vy_serv = -1
                for idx in range(len(self.balls)):
                    b = self.balls[idx]
                    if len(b) < 4:
                        self.balls[idx] = (b[0], b[1],
                                           self.vx_serv, self.vy_serv)
                self.serve_dir = -self.serve_dir
                self.state = "playing"        # game starts here
            else:
                for idx in range(len(self.balls) - 1, -1, -1):
                    bx, by = self.balls[idx]
                    ny = max(by + 2, BRICK_Y0 + BRICK_ROWS)   # down 2/tick
                    ny = min(ny, PADDLE_Y - 2)                  # stop above paddle
                    self.balls[idx] = (bx, ny)
            return None

        # --- per-ball simulation ── one life lost only when ALL balls vanish
        for idx in range(len(self.balls) - 1, -1, -1):
            b = self.balls[idx]
            if len(b) == 4:          # bounce-affected velocity data persists
                bx, by, vx_local, vy_local = b
            else:                    # legacy 2-tuple (shouldn't happen during play)
                bx, by = b
                vx_local = self.vx_serv
                vy_local = self.vy_serv
            nx, ny = bx + vx_local, by + vy_local

            if nx <= 1 or nx >= GRID_W - 2:          # side walls
                nx = 1 if nx <= 1 else GRID_W - 2
                vx_local = -vx_local
            if ny <= 1:                              # ceiling
                ny = 2 - (ny - 1)
                vy_local = -vy_local
            # persist bounce-affected velocity along with new position  
            self.balls[idx] = (nx, ny, vx_local, vy_local)

            blk = self.block_at(nx, ny)
            if blk and self.alive[blk[0]][blk[1]]:   # living brick?
                self.break_brick(*blk)
                vy_local = -vy_local
                vx_local = 1 if nx % 2 == 1 else -1
                continue                              # already flipped, skip paddle

            if (vy_local > 0 and ny == PADDLE_Y - 1
                    and self.px <= nx < self.px + PADDLE_W):
                vy_local = -1
                offset = nx - (self.px + PADDLE_W // 2)
                if offset <= -2:
                    vx_local = -1
                elif offset >= 2:
                    vx_local = 1

            # fell past the paddle → mark for removal
            if ny >= GRID_H - 2:
                del self.balls[idx]
                if not any(self.balls):          # last ball? lose a life
                    self.lives -= 1
                break                              # only one ball can drop per tick

        # spawn power-ups after this batch of simulations
        self._maybe_spawn_pickups()

        # process falling pickups: advance & catch against paddle
        self._process_pickups()
        return None

    def _maybe_spawn_pickups(self):
        """Check if enough bricks were broken to earn a pickup; spawn it."""
        while self.breaks_since_pickup >= BREAKS_PER_PICKUP and any(self.balls):
            self.breaks_since_pickup -= BREAKS_PER_PICKUP
            # place it below the brick wall (row 10 = BRICK_Y0+BRICK_ROWS)
            bx = self.balls[0][0]                  # borrow ball's x for spawn pos
            self.pickups.append((bx, BRICK_Y0 + BRICK_ROWS))

    def _process_pickups(self):
        """Fall pickups down and catch any that reach the paddle."""
        any_balls = any(self.balls)   # remember before we might add balls
        for up in range(len(self.pickups) - 1, -1, -1):
            px_x, py_y = self.pickups[up]
            ny = py_y + 1             # fall one tick
            if ny >= GRID_H - 2:      # fell off bottom without catching
                del self.pickups[up]
                continue
            self.pickups[up] = (px_x, ny)
            # caught by paddle?
            if (ny == PADDLE_Y - 1 and self.px <= px_x < self.px + PADDLE_W):
                any_balls = True     # force "balls exist" test below
                sx = px_x
                # spawn new ball just above the paddle at the catch x
                self.balls.append((sx, ny - 1))
                del self.pickups[up]

    # --- rendering ── updated for pickups

    def render(self, out, messages=()):
        terminal_clear(out)
        grid = [[(" ", "")] * GRID_W for _ in range(GRID_H)]
# bricks first (power-ups can overwrite once they drop below brick area)
        for r in range(BRICK_ROWS):
            for c in range(BRICK_COLS):
                if self.alive[r][c]:
                    col = getattr(C, ROW_COLORS[r % len(ROW_COLORS)])
                    y = BRICK_Y0 + r
                    grid[y][2 * c + 1] = ("[", col)
                    grid[y][2 * c + 2] = ("]", col)
# falling power-ups
        for px_x, py_y in self.pickups:
            if 0 <= px_x < GRID_W and 1 <= py_y < GRID_H - 1:
                cell_color = getattr(C, "YELLOW", "")
                grid[py_y][px_x] = (PICKUP_CHAR, C.BOLD + cell_color)
# paddle ── unchanged rendering
        for i in range(PADDLE_W):
            grid[PADDLE_Y][self.px + i] = ("\u2588", C.BOLD + C.CYAN)
# balls — drawn last so they sit on top
        if self.state in ("playing", "serving"):
            for bx, by in self.balls:
                if 0 <= by < GRID_H and 0 <= bx < GRID_W:
                    grid[by][bx] = ("\u25cf", C.BOLD + C.WHITE)
# HUD ── unchanged from original formatting
        out.write(C.WHITE + "\u2591" * GRID_W + C.ENDC + "\n")
        for y in range(1, GRID_H - 1):
            out.write(C.WHITE + "\u2591" + C.ENDC)
            for x in range(1, GRID_W - 1):
                ch, col = grid[y][x]
                cell = (col + ch + C.ENDC) if col else ch
                out.write(cell if ch.strip() else " ")
            out.write(C.WHITE + "\u2591" + C.ENDC + "\n")
        out.write(C.WHITE + "\u2591" * GRID_W + C.ENDC + "\n")
        lives = "O" * self.lives + "-" * max(0, LIVES_DEFAULT - self.lives)
        if self.state == "serving":
            status = C.YELLOW + "  serve in {}".format(self.countdown) + C.ENDC
        elif self.state == "won":
            status = C.GREEN + "  WALL CLEARED!" + C.ENDC
        elif self.state == "lost":
            status = C.RED + "  GAME OVER" + C.ENDC
        else:
            status = ""
        out.write("\n")
        out.write("Score: " + C.BOLD + "{:d}".format(self.score) + C.ENDC +
                  "    Bricks left: " + str(self.bricks_left) + "    "
                  "Speed: " + C.YELLOW + "{:.1f}".format(
                      BASE_TICK_MS / self.tick) + "x" + C.ENDC +
                  "    Lives: " + C.CYAN + lives + C.ENDC + status + "\n")
        for msg in messages:
            out.write(msg + "\n")
        if _TERMINAL_MODE:
            out.write(C.GRAY +
                      "\na/d or arrows: paddle | p: pause | r: new game | q/ESC: quit\n")
        out.write(C.ENDC)


# ------------------------------------------------------------- driver

def _end_screen(out, g):
    if g.state == "won":
        out.write(C.GREEN + C.BOLD +
                  "You cleared the wall - score {}.".format(g.score) + C.ENDC)
    else:
        out.write(C.RED + C.BOLD + "Game over - score {}.".format(g.score)
                  + C.ENDC)
    out.flush()


def play(args):
    if args.keytest:
        out = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                               errors="replace", line_buffering=True)
        out.write("KEY TEST: press keys; each one the game receives is printed.\n")
        out.write("Try a/d and the arrows. Quit with q.\n")
        for _ in range(100):
            k = next_key()
            out.write("  got: {}\n".format(repr(k)))
            out.flush()
            if k in ("q", "esc", "eof"):
                break
        out.write("Done.\n")
        out.flush()
        return

    out = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                           errors="replace", line_buffering=True)
    g = Game(lives=args.lives)
    paused = False
    messages = []
    flush_stdin()

    while True:
        if g.state in ("won", "lost"):
            g.render(out, [])
            _end_screen(out, g)
            try:
                input("\nPress Enter to play again (q quits)...")
            except EOFError:
                return
            if sys.stdin.readline().strip() == "q":
                out.write("Goodbye!\n")
                out.flush()
                return
            g = Game(lives=args.lives)
            paused = False
            messages = []
            continue

        g.render(out, messages if messages else
                 ([C.MAGENTA + "PAUSED - press p to resume" + C.ENDC]
                 if paused else []))

        if not _TERMINAL_MODE:
            key = next_key()
            if key in ("q", "esc", "eof"):
                out.write("Goodbye!\n")
                out.flush()
                return
            if key == "r":
                g = Game(lives=args.lives)
                paused = False
                messages = ["New game!"]
                continue
            if key == "p":
                paused = not paused
                messages = []
                continue
            if not paused:
                if key == "a":
                    g.move_player(-1)
                elif key == "d":
                    g.move_player(1)
                g.step()
            continue

        deadline = time.time() + g.tick / 1000.0
        while True:
            remaining = deadline - time.time()
            if remaining <= 0:
                break
            key = poll_key()
            if key:
                if key in ("q", "esc"):
                    out.write("Goodbye!\n")
                    out.flush()
                    return
                if key == "r":
                    g = Game(lives=args.lives)
                    paused = False
                    messages = ["New game!"]
                    break
                elif key == "p":
                    paused = not paused
                    messages = []
                elif not paused:
                    if key in ("a", "left"):
                        g.move_player(-1)
                    elif key in ("d", "right"):
                        g.move_player(1)
            if remaining > 0 and not paused:
                time.sleep(min(0.005, remaining))
        if not paused:
            g.step()


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Breakout Solo - single-player terminal brick-breaker")
    p.add_argument("--lives", type=int, default=LIVES_DEFAULT)
    p.add_argument("--no-color", action="store_true")
    p.add_argument("--keytest", action="store_true",
                   help="diagnostic: print every key the game receives")
    args = p.parse_args(argv)

    args.lives = max(1, args.lives)
    install_colors(not args.no_color)

    try:
        play(args)
    except KeyboardInterrupt:
        print("\nGoodbye!")


if __name__ == "__main__":
    main()