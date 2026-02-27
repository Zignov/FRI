from functools import lru_cache

UNKNOWN = -1
EMPTY = 0
FILLED = 1


def generate_line_patterns(length, clues):
    """
    Generate all valid full line patterns for a given line length and clue list.
    Example: length=5, clues=(2,1) -> patterns like [1,1,0,1,0]
    """
    clues = tuple(clues)

    @lru_cache(None)
    def helper(pos, clue_idx):
        if clue_idx == len(clues):
            # no more blocks: rest must be empty
            return [tuple([EMPTY] * (length - pos))]

        block = clues[clue_idx]
        results = []

        # minimum space needed for remaining clues including separators
        remaining_blocks = clues[clue_idx:]
        min_needed = sum(remaining_blocks) + (len(remaining_blocks) - 1)

        max_start = length - min_needed
        for start in range(pos, max_start + 1):
            prefix = [EMPTY] * (start - pos) + [FILLED] * block

            next_pos = start + block
            if clue_idx < len(clues) - 1:
                # need at least one empty separator
                prefix.append(EMPTY)
                next_pos += 1

            for suffix in helper(next_pos, clue_idx + 1):
                results.append(tuple(prefix) + suffix)

        return results

    if not clues:
        return [tuple([EMPTY] * length)]

    return helper(0, 0)


def compatible(pattern, current_line):
    """Check if a full pattern fits a partially known line."""
    for p, c in zip(pattern, current_line):
        if c != UNKNOWN and p != c:
            return False
    return True


def intersect_patterns(patterns):
    """
    From a list of valid patterns, determine forced cells.
    If all patterns agree at a position, return that value; else UNKNOWN.
    """
    if not patterns:
        return None

    length = len(patterns[0])
    result = []
    for i in range(length):
        values = {p[i] for p in patterns}
        if len(values) == 1:
            result.append(values.pop())
        else:
            result.append(UNKNOWN)
    return result


def get_row(board, r):
    return board[r][:]


def set_row(board, r, values):
    changed = False
    for c in range(len(board[0])):
        if board[r][c] != values[c]:
            board[r][c] = values[c]
            changed = True
    return changed


def get_col(board, c):
    return [board[r][c] for r in range(len(board))]


def set_col(board, c, values):
    changed = False
    for r in range(len(board)):
        if board[r][c] != values[r]:
            board[r][c] = values[r]
            changed = True
    return changed


def propagate(board, row_clues, col_clues, row_patterns, col_patterns):
    """
    Repeatedly filter line possibilities and fill forced cells.
    Returns False if contradiction found, True otherwise.
    """
    changed = True
    rows = len(board)
    cols = len(board[0])

    while changed:
        changed = False

        # rows
        for r in range(rows):
            current = get_row(board, r)
            valid = [p for p in row_patterns[r] if compatible(p, current)]
            if not valid:
                return False
            row_patterns[r] = valid

            forced = intersect_patterns(valid)
            if forced is None:
                return False

            # contradiction check
            for i in range(cols):
                if board[r][i] != UNKNOWN and forced[i] != UNKNOWN and board[r][i] != forced[i]:
                    return False

            merged = [
                forced[i] if board[r][i] == UNKNOWN else board[r][i]
                for i in range(cols)
            ]
            if set_row(board, r, merged):
                changed = True

        # cols
        for c in range(cols):
            current = get_col(board, c)
            valid = [p for p in col_patterns[c] if compatible(p, current)]
            if not valid:
                return False
            col_patterns[c] = valid

            forced = intersect_patterns(valid)
            if forced is None:
                return False

            for i in range(rows):
                if board[i][c] != UNKNOWN and forced[i] != UNKNOWN and board[i][c] != forced[i]:
                    return False

            merged = [
                forced[i] if board[i][c] == UNKNOWN else board[i][c]
                for i in range(rows)
            ]
            if set_col(board, c, merged):
                changed = True

    return True


def is_solved(board):
    return all(cell != UNKNOWN for row in board for cell in row)


def clone_board(board):
    return [row[:] for row in board]


def clone_patterns(patterns):
    return [lst[:] for lst in patterns]


def solve_nonogram(row_clues, col_clues):
    rows = len(row_clues)
    cols = len(col_clues)

    board = [[UNKNOWN for _ in range(cols)] for _ in range(rows)]

    row_patterns = [list(generate_line_patterns(cols, tuple(clue))) for clue in row_clues]
    col_patterns = [list(generate_line_patterns(rows, tuple(clue))) for clue in col_clues]

    def backtrack(board, row_patterns, col_patterns):
        if not propagate(board, row_clues, col_clues, row_patterns, col_patterns):
            return None

        if is_solved(board):
            return board

        # choose the most constrained unsolved line
        best_is_row = True
        best_idx = -1
        best_count = float("inf")

        for r in range(len(row_patterns)):
            if UNKNOWN in board[r]:
                count = len(row_patterns[r])
                if 1 < count < best_count:
                    best_count = count
                    best_idx = r
                    best_is_row = True

        for c in range(len(col_patterns)):
            col = get_col(board, c)
            if UNKNOWN in col:
                count = len(col_patterns[c])
                if 1 < count < best_count:
                    best_count = count
                    best_idx = c
                    best_is_row = False

        # fallback: pick first unknown cell line if all counts are 1 (should usually already be solved)
        if best_idx == -1:
            return None

        if best_is_row:
            for pattern in row_patterns[best_idx]:
                if not compatible(pattern, get_row(board, best_idx)):
                    continue

                new_board = clone_board(board)
                new_row_patterns = clone_patterns(row_patterns)
                new_col_patterns = clone_patterns(col_patterns)

                set_row(new_board, best_idx, list(pattern))
                new_row_patterns[best_idx] = [pattern]

                result = backtrack(new_board, new_row_patterns, new_col_patterns)
                if result is not None:
                    return result
        else:
            for pattern in col_patterns[best_idx]:
                if not compatible(pattern, get_col(board, best_idx)):
                    continue

                new_board = clone_board(board)
                new_row_patterns = clone_patterns(row_patterns)
                new_col_patterns = clone_patterns(col_patterns)

                set_col(new_board, best_idx, list(pattern))
                new_col_patterns[best_idx] = [pattern]

                result = backtrack(new_board, new_row_patterns, new_col_patterns)
                if result is not None:
                    return result

        return None

    return backtrack(board, row_patterns, col_patterns)


def print_board(board):
    if board is None:
        print("No solution.")
        return

    for row in board:
        print(" ".join("#" if cell == FILLED else "." for cell in row))


# -------------------------
# EXAMPLE
# -------------------------

# 5x5 cross
row_clues = [
    [3],
    [2,1],
    [3,2],
    [2,2],
    [6],
    [1,5],
    [6],
    [1],
    [2]
]

col_clues = [
    [1,2],
    [3,1],
    [1,5],
    [7,1],
    [5],
    [3],
    [4],
    [3]
]

solution = solve_nonogram(row_clues, col_clues)
print_board(solution)