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
    for a key. With raw mode every drawn row would start where the previous
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
    key. With setraw they would not, and every drawn row would start where
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

# Multi-ball extras
BRICKS_PER_PICKUP = 5          # break this many bricks before a pickup drops
PICKUP_CHAR = "*"              # character for the bonus pickup item
PICKUP_COLOR = C.YELLOW        # yellow highlight (same class as in terminal setup)


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
        # --- pickup / multi-ball feature (new)
        self._bricks_destroyed = 0           # resets every BRICKS_PER_PICKUP
        self.pickup = None                    # (x, y) or None
        self._extra_balls_pending = []        # [(alt_vx, capture_speed)]
        self.serve_speed_capture = BASE_TICK_MS
        self.active_balls = []               # multi-ball state [{x,y,vx,vy}]
        self._play_tick = BASE_TICK_MS       # current game speed during play
        self._feedback = ""
        # --- original serve bookkeeping (kept for compatibility)
        self.countdown = SERVE_DELAY
        self.serve_countdown = SERVE_DELAY   # countdown before first serve and extras
        self.ball = (self.px + PADDLE_W // 2, PADDLE_Y - 1)
        self.vx = 0
        self.vy = 0

    def _reset_serve(self):
        """Schedule a new serve. Sets countdown if not already counting down."""
        self.state = "serving"
        self.countdown = SERVE_DELAY
        self.ball = (self.px + PADDLE_W // 2, PADDLE_Y - 1)
        self.vx = 0
        self.vy = 0
        # Clear any leftover balls for a fresh serve
        self.active_balls.clear()
        # Also update serve_countdown for the step() path
        if not hasattr(self, 'serve_countdown') or self.serve_countdown == 0:
            self.serve_countdown = SERVE_DELAY

    # --- geometry helpers

    def block_at(self, x, y):
        """Brick (r, c) covering unit cell (x, y), or None if none there."""
        r = y - BRICK_Y0
        if r < 0 or r >= BRICK_ROWS:
            return None
        c = (x - 1) // 2
        if c < 0 or c >= BRICK_COLS:
            return None
        return (r, c)

    # --- rules

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
        # --- pickup feature: spawn every BRICKS_PER_PICKUP bricks
        self._bricks_destroyed += 1
        if self._bricks_destroyed >= BRICKS_PER_PICKUP:
            _bx, _by = 1 + c * 2 + 1, BRICK_Y0 + r
            self.pickup = (_bx, _by)
            self._bricks_destroyed = 0
        if self.bricks_left == 0 and self.state != "lost":
            self.state = "won"
        return True

    def _spawn_pending_extras(self):
        """Consume pending extra balls and add them to active_balls.
        Returns count of balls spawned (0 if none left)."""
        n = len(self._extra_balls_pending)
        # When spawning from pending, clear any old balls from prior play
        if n > 0:
            self.active_balls.clear()
        for alt_vx, spd in self._extra_balls_pending:
            self.active_balls.append({
                'x': self.px + PADDLE_W // 2,
                'y': PADDLE_Y - 1,
                'vx': alt_vx,
                'vy': -1,
            })
        if n > 0:
            self.serve_speed_capture = max(spd, BASE_TICK_MS)
        self._extra_balls_pending.clear()
        return n

    def step(self):
        """Advance one tick. Returns 'brick', 'life', 'pickup' or None."""
        self._feedback = ""  # transient feedback clears every tick
        if self.state in ("won", "lost"):
            return None
        # Track game speed during active play
        if self.state == "playing":
            self._play_tick = self.tick

        # --- countdown / spawn phase ---
        if hasattr(self, 'serve_countdown') and self.serve_countdown > 0:
            self.serve_countdown -= 1
            if self.serve_countdown == 0:
                spawned = self._spawn_pending_extras()
                if not spawned:
                    # No pending extras → normal serve: create active ball + play
                    self.serve_speed_capture = max(self._play_tick, BASE_TICK_MS)
                    bx_c = self.px + PADDLE_W // 2
                    self.active_balls.append({
                        'x': bx_c, 'y': PADDLE_Y - 1,
                        'vx': self.serve_dir, 'vy': -1,
                    })
                if not self.active_balls:
                    self.countdown = SERVE_DELAY
                self.state = "playing" if self.active_balls else "serving"
            return None  # still in countdown phase

        # --- countdown for ball drop from paddle ---
        self.countdown -= 1
        if self.countdown <= 0 and not self.active_balls:
            bx_c = self.px + PADDLE_W // 2
            self.active_balls.append({
                'x': bx_c, 'y': PADDLE_Y - 1,
                'vx': self.serve_dir, 'vy': -1,
            })
            self.serve_dir = -self.serve_dir
            return None  # give a frame before physics kicks in

        if not self.active_balls:
            return None  # waiting for serve drop

        # --- dropped (fell below paddle)? ---
        dropped = [i for i, b in enumerate(self.active_balls)
                   if b['y'] >= GRID_H - 2]
        if dropped:
            # Always pop dropped balls
            for idx in reversed(sorted(dropped)):
                self.active_balls.pop(idx)
            # Grace shot: any drop event with pending extras prevents life loss
            if self._extra_balls_pending:
                remaining = len(self._extra_balls_pending)
                self.active_balls.clear()   # start fresh serve
                self.serve_countdown = SERVE_DELAY
                self.state = "serving"
                self._spawn_pending_extras()
                if remaining:
                    self._feedback = (C.YELLOW +
                        f"Grace shot! {remaining} extras spawning." + C.ENDC)
                return "life"
            elif not self.active_balls:
                # All balls gone, no pending → lose a life.
                self.lives -= 1
                if self.lives >= 1:
                    self._reset_serve()
                if self.state != "lost":
                    self.countdown = SERVE_DELAY
                return "life"
            # else: partial drop with no pending — remaining balls survive

        # --- move all active balls ---
        for ball_info in list(self.active_balls):
            bx2 = ball_info['x']
            by2 = ball_info['y']
            vx = ball_info['vx']
            vy = ball_info['vy']
            nx, ny = bx2 + vx, by2 + vy
            # Side walls
            if nx <= 1 or nx >= GRID_W - 2:
                nx = 1 if nx <= 1 else GRID_W - 2
                ball_info['vx'] = -vx
            # Ceiling
            if ny <= 1:
                ny = 2 - (ny - 1)
                ball_info['vy'] = -vy
            ball_info['x'] = nx
            ball_info['y'] = ny
            # Brick collision
            blk = self.block_at(nx, ny)
            if blk and self.alive[blk[0]][blk[1]]:
                self.break_brick(*blk)
                ball_info['vy'] = -vy
                ball_info['vx'] = 1 if nx % 2 == 1 else -1
                return "brick"
            # Paddle collision
            if (ball_info['vy'] > 0 and ny >= PADDLE_Y - 1
                    and self.px <= nx <= self.px + PADDLE_W - 1):
                ball_info['vy'] = -1
                offset = nx - (self.px + PADDLE_W // 2)
                if offset <= -2:
                    ball_info['vx'] = -1
                elif offset >= 2:
                    ball_info['vx'] = 1
            # Ball fell past paddle → already handled as dropped above

        # --- pickup gravity / catch ---
        if self.pickup is not None and self.state == "playing":
            ux, uy = self.pickup
            if uy >= GRID_H - 2:
                self.pickup = None
            elif (self.active_balls
                  and self.px <= ux <= self.px + PADDLE_W - 1):
                captured_spd = max(self.serve_speed_capture, BASE_TICK_MS)
                idx2 = len(self._extra_balls_pending)
                alt_vx = (-self.serve_dir if idx2 % 2 == 0 else self.serve_dir)
                self._extra_balls_pending.append((alt_vx, captured_spd))
                self.pickup = None
                self._feedback = (C.GREEN + "Pickup caught!" + C.ENDC)
                return "pickup"
            else:
                ux2, uy2 = self.pickup
                self.pickup = (ux2, uy2 + 1)

    # --- rendering

    def render(self, out, messages=()):
        terminal_clear(out)
        grid = [[(" ", "")] * GRID_W for _ in range(GRID_H)]
        for r in range(BRICK_ROWS):
            for c in range(BRICK_COLS):
                if self.alive[r][c]:
                    col = getattr(C, ROW_COLORS[r % len(ROW_COLORS)])
                    y = BRICK_Y0 + r
                    grid[y][2 * c + 1] = ("[", col)
                    grid[y][2 * c + 2] = ("]", col)
        # --- draw paddle ---
        for i in range(PADDLE_W):
            grid[PADDLE_Y][self.px + i] = ("\u2588", C.BOLD + C.CYAN)
        # --- draw active balls or legacy ball ---
        if self.active_balls:
            for bi in self.active_balls:
                bxx, byy = bi['x'], bi['y']
                grid[byy][bxx] = ("\u25cf", C.BOLD + C.WHITE)
        elif self.state in ("serving", "playing") and hasattr(self, 'ball') and self.ball is not None:
            bxx, byy = self.ball
            grid[byy][bxx] = ("\u25cf", C.BOLD + C.WHITE)
        # --- render pending extras indicator ---
        pending_text = ""
        if self._extra_balls_pending:
            pending_text = C.YELLOW + f" (+{len(self._extra_balls_pending)})" + C.ENDC
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
        if pending_text:
            out.write(pending_text + "\n")
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
