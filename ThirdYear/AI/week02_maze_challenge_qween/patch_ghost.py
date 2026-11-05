import re

with open('maze_solo_qween_clean.py', 'r') as f:
    lines_orig = f.readlines()

# Rebuild with Ghost support in __init__
ghost_init_code = '''        self.rng = random.Random(seed)
        self.width, self.height = width, height
        self.name = name or "Player"
        self.symbol = (self.name[:2] or "P").upper() if len(self.name) > 0 else "P"
        if len(self.symbol) == 1:
            self.symbol += " "
        
        # Generate the maze
        self.maze = generate_maze(width, height, self.rng)
        
        # Set door
        self.door = (width - 2, height - 2)
        
        # Find valid floor cell positions (for keys and ghost spawn)
        candidates = [(x, y) for y in range(1, height - 1)
                      for x in range(1, width - 1)
                      if self.maze[y][x] == OPEN and x % 2 and y % 2
                      and (x, y) not in {(1, 1), self.door}]
        
        # Pick spawn position: room farthest from player start and door
        random.shuffle(candidates)
        ghost_pos = None
        best_dist = -1
        px, py = self.player[0], self.player[1]
        dx, dy = self.door[0], self.door[1]
        for pos in candidates:
            d_player = max(abs(pos[0] - px), abs(pos[1] - py))
            d_door = max(abs(pos[0] - dx), abs(pos[1] - dy))
            if d_player + d_door > best_dist:
                best_dist, ghost_pos = d_player + d_door, pos
        
        # Separate rooms: one for ghost, rest for keys
        key_rooms_set = set(candidates) - {ghost_pos} if ghost_pos else candidates
        self.keys = set(list(key_rooms_set)[:4])  # 4 keys to collect
        
        # Boosts go in next available rooms after keys
        boost_candidates = list(key_rooms_set)[4:]
        self.boosts = {
            boost_candidates[0]: "3x" if boost_candidates else None,
            boost_candidates[1]: "1x" if len(boost_candidates) > 1 else None
        }
        
        # Place keys on maze
        for (kx, ky) in sorted(self.keys):
            self.maze[ky][kx] = KEY
        
        # Place boosts (skip positions that conflict with other elements)
        for bpos, glyph in self.boosts.items():
            if glyph and bpos != ghost_pos:
                bx, by = bpos
                self.maze[by][bx] = glyph
        
        # Set ghost spawn room to floor
        if ghost_pos:
            gx, gy = ghost_pos
            self.maze[gy][gx] = OPEN
        
        # Place door symbol (after all floor placements)
        self.maze[self.door[1]][self.door[0]] = DOOR

    '''

# Find the __init__ and replace it
for idx, l in enumerate(lines_orig):
    if 'def __init__(self, width=25, height=15' in l:
        # Get what comes before and after this def
        before = ''.join(lines_orig[:idx])  # everything up to the line we're replacing
        from_idx = idx + len(l)
        after_start = lines_orig[from_idx:from_idx+6]  # __init__ body
        
        print(f"Found __init__ at index {idx}, replacing first 8 lines")
        
        # Build new file content
        # Skip original init, add my version
        replacement = before + ghost_init_code.strip()
        
        # Find where the rest of methods begin (after try_move)
        for check_idx in range(from_idx, min(len(lines_orig), from_idx+100)):
            if 'def mark_visited(self):' in lines_orig[check_idx]:
                rest = '\n'.join(lines_orig[check_idx:])
                final = replacement + '\n' + rest
                break
        else:
            final = replacement
            
        with open('maze_solo_qwen.py', 'w') as out:
            out.write(final)
        print("Created maze_solo_qween.py successfully!")
        exit()

print("ERROR: Could not find __init__")
