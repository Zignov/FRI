import re

with open('maze_solo.py', 'r') as f:
    base = f.read()

lines = base.split('\n')

# Find the line just before _check_ghost_catch (end of original Game class)
target_line = None
for i, ln in enumerate(lines):
    if '_check_ghost_catch(self)' in l:
        target_line = i - 6
        break

init_code = '''    def __init__(self, width=25, height=15, moves=150, sight=3,
                 seed=None, peek=False, name="P"):
        self.rng = random.Random(seed)
        self.width, self.height = width, height
        self.name = name
        self.symbol = (name[:2] or "P").upper() if len(name) > 0 else "P"
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

        # Randomly shuffle rooms, pick one for ghost spawn (farthest from player/door)
        random.shuffle(rooms)
        ghost_pos = self._find_room_far((1, 1), self.door, list(rooms))
        key_rooms_set = set(rooms) - {ghost_pos}

        # Place keys in available rooms  
        self.keys = set(list(key_rooms_set)[:NUM_KEYS])

        # Place boosts (next two available rooms after keys)
        if len(key_rooms_set) > NUM_KEYS:
            boost_list = list(key_rooms_set[NUM_KEYS:])[:2]
        else:
            boost_list = []
        self.boosts = {
            boost_list[0]: BOOST_BIG if boost_list else None,
            boost_list[1]: BOOST_SMALL if len(boost_list) > 1 and boost_list[1] else None
        }

        # Place keys and boosts on the maze
        for (x, y) in self.keys:
            self.maze[y][x] = KEY
        
        for bpos, glyph in self.boosts.items():
            if glyph and bpos:
                self.maze[bpos[1]][bpos[0]] = glyph

        # Set ghost spawn room to open floor  
        if ghost_pos:
            self.maze[ghost_pos[1]][ghost_pos[0]] = OPEN

        # Place door
        self.maze[self.door[1]][self.door[0]] = DOOR

    def _find_room_far(self, start, end, rooms):
        """Find room position farthest from both start and end."""
        sx, sy = start
        ex, ey = end
        mx = -1
        best = None
        for r in rooms:
            d1 = max(abs(r[0] - sx), abs(r[1] - sy))
            d2 = max(abs(r[0] - ex), abs(r[1] - ey))
            if d1 + d2 > mx:
                mx, best = d1 + d2, r
        return best

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

'''

write_file('maze_solo_qween.py', init_code)
with open('maze_solo_qween.py', 'a') as f:
    l = lines[target_line+6:]
    f.write('\n'.join(l))
print("File created and appended successfully!")
