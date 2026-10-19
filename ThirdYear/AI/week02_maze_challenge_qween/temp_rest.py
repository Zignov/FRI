        self.maze[self.door[1]][self.door[0]] = DOOR

        # Init ghost - spawns at chosen position
        self.ghost = Ghost(self.width, self.height, self.rng,
                          g_pos, self.door)
        
        # Initialize player at fixed start position
        self.player = (1, 1)

        self.max_moves, self.moves = moves, moves
        self.sight = sight
        self.peek = peek
        self.visited = [[False] * width for _ in range(height)]
        self.mark_visited()
        self.keys_found = 0
        self.steps = 0
        self.state = "playing"
        self.started = time.time()

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

    @staticmethod
    def _find_room_farthest(start, end, rooms):
        """Pick a valid maze room farthest from start/end positions."""
        best = None
        mx = -1
        p_x, p_y = start
        e_x, e_y = end
        for r in rooms:
            d1 = max(abs(r[0] - p_x), abs(r[1] - p_y))
            d2 = max(abs(r[0] - e_x), abs(r[1] - e_y))
            if d1 + d2 > mx:
                mx, best = d1 + d2, r
        return best

    # --- ghost update

    def _check_ghost_catch(self):
        """Check if player is caught by ghost."""
        gx, gy = self.ghost.position
        if (gx, gy) == self.player:
            self.state = "lost"
            return True
        return False

    def update_ghost(self):
        """Update ghost position every 3 of player's moves. Must be called after try_move."""
        if self.ghost.update():
            # Check for catch immediately after ghost spawns or moves
            self._check_ghost_catch()
        elif hasattr(self, "px"):  # After move attempt, check catch on movement into ghost's cell
            gx, gy = self.ghost.position
            if (self.player[0] == gx and self.player[1] == gy):
                self.state = "lost"

    def try_move(self, dx, dy):
        """Apply one move; returns the game state."""
        if self.state != "playing":
            return self.state

        # First check if trying to move INTO the ghost's tile = instant death
        nx, ny = self.player[0] + dx, self.player[1] + dy
        gx, gy = self.ghost.position
        if (nx == gx and ny == gy):  # Running toward the ghost!
            self.state = "lost"
            return self.state

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

        # Update ghost - it moves every 3 of your moves
        self.update_ghost()

        # Check if caught after move
        gx, gy = self.ghost.position
        if (nx == gx and ny == gy):
            self.state = "lost"

        if self.moves <= 0 and self.state == "playing":
            self.state = "lost"
        return self.state

    # --- rendering

    def render(self, out, messages=()):
        terminal_clear(out)
        
        # Render maze
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
        
        # Keys remaining indicator
        keys = "".join((C.BOLD + C.WHITE + "■ " if i < NUM_KEYS - self.keys_found
                       else C.GRAY + "_ ") for i in range(NUM_KEYS))
        out.write("Keys:  " + keys + "     Steps: " + str(self.steps) + "\n")

        # Ghost indicator
        if self.state == "playing":
            gx, gy = self.ghost.position
            ghost_near = max(abs(gx - self.player[0]), abs(gy - self.player[1])) <= 4
            ghost_warn = C.RED + "⚠ Ghost is near!" if ghost_near else ""
        elif self.state == "lost":
            gx, gy = self.ghost.position
            px, py = self.player
            dist = max(abs(gx - px), abs(gy - py))
            ghost_warn = C.RED + "CAUGHT: You got caught by the ghost!" + C.ENDC if dist == 0 else ""
        
        out.write(ghost_warn)

        if self.keys_found < NUM_KEYS:
            out.write(C.CYAN +
