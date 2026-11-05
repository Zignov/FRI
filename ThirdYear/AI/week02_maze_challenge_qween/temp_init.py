# -*- coding: utf-8 -*-
"""
Maze Solo - Ghost Edition. A minimal, standalone, single-player terminal maze game.

A fresh random maze (recursive division) is generated every run.
Collect all 4 keys (red), then reach the door to escape before you run
out of moves; a ghost enemy hunts you — caught = instant loss! boost tiles (3x/1x) add extra moves.

Controls:
    arrows / WASD   move
    r               new maze
    q / ESC         quit

Run:
    python maze_solo_qween.py
    python maze_solo_qween.py --seed 42      # reproducible maze
    python maze_solo_qween.py --peek         # reveal whole maze

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
    """Clear the screen."""
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
    """Read one key on POSIX, tolerating slow terminal emulators."""
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
    """Read one keypress."""
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
    """Consume all pending keys (incl. partial escape sequences)."""
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

class Ghost:
    """The menacing ghost enemy that spawns mid-maze and hunts you."""

    def __init__(self, width, height, rng, player_pos, door_pos):
        self.width = width
        self.height = height
        self.rng = rng
        self.player_pos = player_pos
        self.position = self._spawn_position(player_pos, door_pos)
        self.move_turns = 0  # counts your moves since last ghost move

    def _spawn_position(self, player_pos, door_pos):
        """Spawn ghost mid-maze, as far from player/door as possible."""
        width, height = self.width, self.height
        p_x, p_y = player_pos[0], player_pos[1]
        d_x, d_y = door_pos[0], door_pos[1]
        
        best_pos = None
        max_dist = -1

        for y in range(self.height):
            for x in range(self.width):
                # Skip border cells (outside inner maze)
                if x < 2 or x >= width - 2 or y < 2 or y >= height - 2:
                    continue
                # Skip player position and door
                if (x, y) == player_pos or (x, y) == door_pos:
                    continue

                dist = max(abs(x - p_x), abs(y - p_y))
                if dist > max_dist:
                    max_dist = dist
                    best_pos = (x, y)

        return best_pos

    def move_toward(self):
        """Move one tile toward the player. Ghost can move through walls."""
        px, py = self.player_pos
        gx, gy = self.position

        # Calculate direction toward player
        dx, dy = 0, 0
        if abs(px - gx) > abs(py - gy):
            # horizontal movement dominates
            dx = 1 if gx < px else -1
        else:
            # vertical movement dominates
            dy = 1 if gy < py else -1

        self.position = (gx + dx, gy + dy)
        self.move_turns += 1

    def update(self):
        """Update ghost position every 3 of player's moves."""
        if self.move_turns < 3:
            return False  # haven't moved yet this cycle
        self.move_toward()
        self.move_turns = 0
        return True  # ghost has moved

    def get_pos(self):
        """Return current position of ghost."""
        return self.position


class Game:
    def __init__(self, width=25, height=15, moves=150, sight=3,
                 seed=None, peek=False, name="P"):
        self.rng = random.Random(seed)
        self.width, self.height = width, height
        self.name = name
        self.symbol = (name[:2] or "P").upper()
        if len(self.symbol) == 1:
            self.symbol += " "

        # Generate the maze
        self.maze = generate_maze(width, height, self.rng)

        # Place player at center-top starting position
        self.player = (1, 1)

        self.door = (width - 2, height - 2)
        self.code = hashlib.md5(
            repr(self.maze).encode("utf-8")).hexdigest()[:4]

        # Find valid room positions for keys and ghost spawn
        rooms = [(x, y) for y in range(1, height - 1)
                 for x in range(1, width - 1)
                 if self.maze[y][x] == OPEN and x % 2 and y % 2
    # --- world

    def is_open(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height \
            and self.maze[y][x] != WALL

    def mark_visited(self):
        px, py = self.player
        for x in range(max(0, px - self.sight),
                       min(self.width, px + self.sight + 1)):
            for y in range(max(0, py - self.sight),
                           min(self.height, py + self.sight + 1)):
                self.visited[y][x] = True

    def seen(self, x, y):
        return self.peek or self.visited[y][x]

    def near(self, x, y):
        px, py = self.player
        return max(abs(px - x), abs(py - y))

    def __init__(self, width=25, height=15, moves=150, sight=3,
                 seed=None, peek=False, name="P"):
        super().__init__()
        self.rng = random.Random(seed)
        self.width, self.height = width, height
        self.name = name
        self.symbol = (name[:2] or "P").upper() if len(name) >= 1 else "P"
        if len(self.symbol) == 1:
            self.symbol += " "

        # Generate the maze
        self.maze = generate_maze(width, height, self.rng)

        self.player = (1, 1)
        self.door = (width - 2, height - 2)
        self.code = hashlib.md5(repr(self.maze).encode("utf-8")).hexdigest()[:4]

        # Find valid room positions for keys and ghost spawn
        rooms = [(x, y) for y in range(1, height - 1)
                 for x in range(1, width - 1)
                 if self.maze[y][x] == OPEN and x % 2 and y % 2
                 and (x, y) not in {(1, 1), self.door}]
        
        random.shuffle(rooms)
        ghost_pos = self._find_room_farthest((1, 1), self.door, rooms)
        key_rooms_set = set(rooms) - {ghost_pos}

        # Place keys
        self.keys = set(list(key_rooms_set)[:NUM_KEYS])

        # Place boosts
        boost_list = list(key_rooms_set[NUM_KEYS:]) if len(key_rooms_set) > NUM_KEYS else []
        boost_rooms = boost_list[:2]
        self.boosts = {
            boost_rooms[0]: BOOST_BIG if len(boost_rooms) > 0 else None,
            boost_rooms[1]: BOOST_SMALL if len(boost_rooms) > 1 else None
        }

        # Place keys on maze
        for (x, y) in self.keys:
            self.maze[y][x] = KEY

        # Place boosts on maze
        for boom_pos, glyph in self.boosts.items():
            if glyph and boom_pos:
                self.maze[boom_pos[1]][boom_pos[0]] = glyph

        # Set ghost spawn room to open floor
        if ghost_pos:
            self.maze[ghost_pos[1]][ghost_pos[0]] = OPEN

        # Place door
        self.maze[self.door[1]][self.door[0]] = DOOR

    # --- ghost update

