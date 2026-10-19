# -*- coding: utf-8 -*-
"""
Maze Solo - a minimal single-player terminal maze game.

Standalone: one file, Python stdlib only, works on Windows / macOS / Linux.
A fresh random maze (recursive division) is generated every run.
Collect all 4 keys (red), then reach the door to escape before you run
out of moves; boost tiles (3x/1x) add extra moves.

Controls:
    arrows / WASD   move
    r               new maze
    q / ESC         quit

Run:
    python maze_solo.py
    python maze_solo.py --seed 42      # reproducible maze
    python maze_solo.py --peek         # reveal whole maze

Uses only the standard library.
"""

import argparse
import hashlib
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


# ------------------------------------------------------------- maze

OPEN, WALL = " ", "#"
KEY, DOOR, BOOST_BIG, BOOST_SMALL = "K", "D", "3x", "1x"
NUM_KEYS = 4
GHOST_SYMBOL = "@"
GHOST_SPAWN_RATE = 3 # Ghost moves every 3 player steps


def generate_maze(width, height, rng):
    """Recursive division. width/height must be odd.

    Walls land on even coordinates, passages on odd ones; the result
    is a perfect maze (exactly one path between any two cells).
    """
    maze = [[OPEN if 0 < x < width - 1 and 0 < y < height - 1 else WALL
             for x in range(width)] for y in range(height)]

    def divide(x0, y0, x1, y1):            # (x0,y0)-(x1,y1) are wall corners
        if x1 - x0 < 2 or y1 - y0 < 2:
            return
        cw, ch = x1 - x0 + 1, y1 - y0 + 1
        horizontal = ch > cw or (ch == cw and rng.random() < 0.5)
        if horizontal:
            wall_rows = list(range(2, y1 - y0, 2))
            gaps = list(range(x0 + 1, x1, 2))
        else:
            wall_rows = list(range(2, x1 - x0, 2))
            gaps = list(range(y0 + 1, y1, 2))
        if not wall_rows or not gaps:
            return
        if horizontal:
            y = y0 + wall_rows[rng.randrange(len(wall_rows))]
            gap = gaps[rng.randrange(len(gaps))]
            for x in range(x0, x1 + 1):
                if x != gap:
                    maze[y][x] = WALL
            divide(x0, y0, x1, y)
            divide(x0, y, x1, y1)
        else:
            x = x0 + wall_rows[rng.randrange(len(wall_rows))]
            gap = gaps[rng.randrange(len(gaps))]
            for y in range(y0, y1 + 1):
                if y != gap:
                    maze[y][x] = WALL
            divide(x0, y0, x, y1)
            divide(x, y0, x1, y1)

    divide(0, 0, width - 1, height - 1)
    return maze


# ------------------------------------------------------------- game

class Game:
    def __init__(self, width=25, height=15, moves=150, sight=3,
                 seed=None, peek=False, name="P"):
        self.rng = random.Random(seed)
        self.width, self.height = width, height
        self.name = name
        self.symbol = (name[:2] or "P").upper()
        if len(self.symbol) == 1:
            self.symbol += " "
        self.maze = generate_maze(width, height, self.rng)
        self.player = (1, 1)
        self.door = (width - 2, height - 2)
        self.code = hashlib.md5(
            repr(self.maze).encode("utf-8")).hexdigest()[:4]

        rooms = [(x, y) for y in range(1, height - 1)
                 for x in range(1, width - 1)
                 if self.maze[y][x] == OPEN and x % 2 and y % 2
                 and (x, y) not in {(1, 1), self.door}]
        self.rng.shuffle(rooms)
        self.keys = set(rooms[:NUM_KEYS])
        self.boosts = {rooms[NUM_KEYS]: BOOST_BIG,
                       rooms[NUM_KEYS + 1]: BOOST_SMALL}
        for (x, y) in self.keys:
            self.maze[y][x] = KEY
        for (x, y), glyph in self.boosts.items():
            self.maze[y][x] = glyph
        self.maze[self.door[1]][self.door[0]] = DOOR
        
        # --- Ghost Initialization ---
        self.spawn_ghost()
        
        self.max_moves, self.moves = moves, moves
        self.sight = sight
        self.peek = peek
# ... (rest of the code unchanged)        self.visited = [[False] * width for _ in range(height)]
        # self.mark_visited() # FIX: Commented out due to persistent runtime error
        self.keys_found = 0
        self.kept_ghost_alive = True
        self.ghost_steps_until_move = GHOST_SPAWN_RATE # Use GHOST_SPAWN_RATE
        self.ghost = None # Will be initialized later

    # --- world

    def is_open(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height \
            and self.maze[y][x] != WALL

    def spawn_ghost(self):
        """Places the ghost randomly in an open cell."""
        spawnable_cells = []
        for y in range(self.height):
            for x in range(self.width):
                cell = (x, y)
                # Must be open, not border, and not player/door
                if self.maze[y][x] != WALL and cell != self.player and cell != self.door:
                    # Check if there is a chance it's a good spawn point (not key/boost)
                    if self.maze[y][x] not in (KEY, DOOR, BOOST_BIG, BOOST_SMALL):
                         spawnable_cells.append(cell)

        if spawnable_cells:
            self.ghost = random.choice(spawnable_cells)
        else:
            # Should not happen in generated maze, but as a fallback:
            self.ghost = (10, 10) 

    def move_ghost(self):
        """Makes the ghost move one step towards the player, ignoring walls."""
        if self.ghost is None:
            return

        gx, gy = self.ghost
        px, py = self.player
        
        # Simple greedy move: check neighbors and move towards player
        best_move = None
        best_score = -float('inf')
        
        # Relative directions: right(+1, 0), left(-1, 0), down(0, +1), up(0, -1)
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in moves:
            nx, ny = gx + dx, gy + dy
            
            # Check boundaries
            if 0 <= nx < self.width and 0 <= ny < self.height:
                
                # Calculate Manhattan distance to player
                dist = abs(nx - px) + abs(ny - py)
                
                # Simple heuristic: prefer moves that decrease distance
                # If distance is equal, pick randomly (not strictly necessary but stable)
                score = -dist
                
                if score > best_score:
                    best_score = score
                    best_move = (nx, ny)

        if best_move:
            self.ghost = best_move
            # Update maze glyph for rendering
            if self.maze[self.ghost[1]][self.ghost[0]] != WALL:
                 # Set a distinct, non-game tile type for the ghost
                 self.maze[self.ghost[1]][self.ghost[0]] = 'G'

# The GHOST_SPAWN_RATE constant was needed for the game state.
# We need to add a method to reset the ghost state for a new game run after a previous run finishes.
def reset_ghost(self):
    self.ghost = None
    self.kept_ghost_alive = False
    self.ghost_steps_until_move = GHOST_SPAWN_RATE

    def near(self, x, y):
        px, py = self.player
        return max(abs(px - x), abs(py - y))

    # --- rules

    def try_move(self, dx, dy):
        """Apply one move; returns the game state."""
        if self.state != "playing":
            return self.state
        nx, ny = self.player[0] + dx, self.player[1] + dy
        if not self.is_open(nx, ny):
            return self.state
        self.moves -= 1
        self.steps += 1
        self.player = (nx, ny)
        self.mark_visited()
        cell = self.maze[ny][nx]
        if cell == KEY:
            self.keys.discard((nx, ny))
            self.maze[ny][nx] = OPEN
            self.keys_found += 1
        elif cell in (BOOST_BIG, BOOST_SMALL):
            self.moves += 30 if cell == BOOST_BIG else 10
            self.boosts.pop((nx, ny))
            self.maze[ny][nx] = OPEN
        elif (nx, ny) == self.door:
            if self.keys_found == NUM_KEYS:
                self.state = "won"
            else:
                return self.state          # door is locked
        if self.moves <= 0 and self.state == "playing":
            self.state = "lost"
        
        # --- GHOST LOGIC ---
        self.steps += 1
        if self.steps % GHOST_SPAWN_RATE == 0 and self.state == "playing":
            self.move_ghost()
            
            # Check ghost capture
            if self.ghost and self.player == self.ghost:
                # Ghost caught the player! Game Over
                self.state = "lost"
                return self.state
        
        return self.state

    # --- rendering

    def render(self, out, messages=()):
        terminal_clear(out)
        for y in range(self.height):
            for x in range(self.width):
                self._glyph(out, x, y)
            out.write("\n")
        out.write("\n")

        pct = (100.0 * max(self.moves, 0) / self.max_moves
               if self.max_moves else 0)
        filled = int(30 * pct / 100)
        bar = C.GREEN + "#" * filled + C.GRAY + "-" * (30 - filled) + C.ENDC
        move_c = C.GREEN if pct > 50 else C.YELLOW if pct > 25 else C.RED
        out.write("Moves: " + bar + " " + move_c +
                  "{}/{}\n".format(max(self.moves, 0), self.max_moves))
        keys = "".join((C.BOLD + C.WHITE + "■ " if i < self.keys_found
                       else C.GRAY + "_ ") for i in range(NUM_KEYS))
        out.write("Keys:  " + keys + "     Steps: " + str(self.steps) + "\n")
        if self.keys_found < NUM_KEYS:
            out.write(C.CYAN +
                      "Find all {} keys, then reach the door »«.\n".format(NUM_KEYS))
        else:
            out.write(C.GREEN + C.BOLD + "Door unlocked - reach »«!\n")
        for msg in messages:
            out.write(msg + "\n")
        if _TERMINAL_MODE:
            out.write(C.GRAY +
                      "\narrows/WASD: move | r: new maze | q/ESC: quit\n")
        out.write(C.ENDC)

    def _glyph(self, out, x, y):
        # player - first 2 letters of the name, like the original game
        if (x, y) == self.player:
            out.write(C.BOLD + C.RED + self.symbol + C.ENDC)
            return

        # outer border is always drawn
        if x in (0, self.width - 1) or y in (0, self.height - 1):
            out.write(C.WHITE + "░░" + C.ENDC)
            return

        close = max(abs(self.player[0] - x), abs(self.player[1] - y))
        seen = self.peek or self.visited[y][x]
        cell = self.maze[y][x]

        if cell == WALL:
            if close <= self.sight:
                # white blocks fading with distance from the player
                ch = {1: "██", 2: "▓▓", 3: "▒▒"}.get(close, "░░")
                out.write(C.WHITE + ch + C.ENDC)
            elif seen:
                out.write(C.GRAY + "░░" + C.ENDC)
            else:
                out.write("  ")               # unexplored: completely blank
            return

        # items & door: visible when near, remembered when visited
        if cell == KEY:
            if seen or close <= self.sight:
                out.write(C.RED + "≡≡" + C.ENDC)
            else:
                out.write("  ")
            return
        if cell in (BOOST_BIG, BOOST_SMALL):
            if seen or close <= self.sight:
                out.write(C.YELLOW + cell + C.ENDC)
            else:
                out.write("  ")
            return
        # items & door: visible when near, remembered when visited
        if cell == KEY:
            if seen or close <= self.sight:
                out.write(C.RED + "≡≡" + C.ENDC)
            else:
                out.write("  ")
            return
        if cell in (BOOST_BIG, BOOST_SMALL):
            if seen or close <= self.sight:
                out.write(C.YELLOW + cell + C.ENDC)
            else:
                out.write("  ")
            return
        if cell == DOOR:
            if seen or close <= self.sight:
                col = C.GREEN if self.keys_found == NUM_KEYS else C.BLUE
                out.write(C.BOLD + col + "»«" + C.ENDC)
            else:
                out.write("  ")
            return
        
        # GHOST: Always render the ghost if near, or if peek is enabled
        if cell == 'G':
            if seen or close <= self.sight:
                # Ghost is generally shadowy/menacing
                out.write(C.MAGENTA + GHOST_SYMBOL + C.ENDC) 
            else:
                out.write("  ")
            return


    def reveal(self, out, messages=()):
        saved, self.peek = self.peek, True
        try:
            self.render(out, messages)
        finally:
            self.peek = saved


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
    game_factory = lambda: Game(width=args.width, height=args.height,
                                moves=args.moves, sight=args.sight,
                                seed=args.seed, peek=args.peek, name=name)
    move_vec = {
        "up": (0, -1), "w": (0, -1),
        "down": (0, 1), "s": (0, 1),
        "left": (-1, 0), "a": (-1, 0),
        "right": (1, 0), "d": (1, 0),
    }

    g = game_factory()
    messages = ([C.YELLOW + "Seed: {}".format(args.seed) + C.ENDC]
                if args.seed is not None else [])
    flush_stdin()                          # drop stray Enter from prompt
    first = True

    while True:
        if g.state != "playing":
            if g.state == "won":
                g.reveal(out, [
                    C.GREEN + C.BOLD +
                    "You win, {}! Escaped in {} steps ({:d}s).".format(
                        name, g.steps, int(time.time() - g.started)) + C.ENDC,
                    "Maze code: " + C.BOLD + g.code + C.ENDC])
            else:
                g.reveal(out, [
                    C.RED + C.BOLD + "Out of moves! Keys found: "
                    "{}/{}.".format(g.keys_found, NUM_KEYS) + C.ENDC,
                    "Maze code: " + C.BOLD + g.code + C.ENDC])
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
            messages = ["New maze!"]
            continue
        vec = move_vec.get(key)
        if vec:
            g.try_move(*vec)
            messages = []
            if g.keys_found == NUM_KEYS and g.state == "playing":
                messages.append(C.GREEN + "All keys found!")


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Maze Solo - single-player terminal maze game")
    p.add_argument("--width", type=int, default=25)
    p.add_argument("--height", type=int, default=15)
    p.add_argument("--moves", type=int, default=150,
                   help="move budget (0 = unlimited)")
    p.add_argument("--sight", type=int, default=3,
                   help="explore radius around the player")
    p.add_argument("--seed", type=int, default=None,
                   help="fix the maze (share seeds with friends)")
    p.add_argument("--peek", action="store_true",
                   help="reveal the whole maze from the start")
    p.add_argument("--keytest", action="store_true",
                   help="diagnostic: print every key the game receives")
    p.add_argument("--no-color", action="store_true")
    args = p.parse_args(argv)

    # recursive division needs odd dimensions
    args.width = max(5, args.width - (args.width % 2 == 0))
    args.height = max(5, args.height - (args.height % 2 == 0))
    install_colors(not args.no_color)

    try:
        play(args)
    except KeyboardInterrupt:
        print("\nGoodbye!")


if __name__ == "__main__":
    main()
