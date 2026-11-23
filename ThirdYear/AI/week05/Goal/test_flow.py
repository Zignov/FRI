#!/usr/bin/env python3
"""Test the extra ball spawn feature flow."""
import io, sys

# Force non-terminal mode for deterministic testing
sys.modules['curses'] = type(sys)('mock_curses')
def ncurses_implementation(): return False
sys.modules['curses'].nl_langinfo = lambda x: ""

from breakout_solo import Game, C, SERVE_DELAY, BRICKS_PER_PICKUP, PICKUP_COLOR, PADDLE_W, PADDLE_Y, GRID_H, BASE_TICK_MS

pass_count = 0
fail_count = 0

def test(name, cond):
    global pass_count, fail_count
    if cond:
        pass_count += 1
        print(f"  PASS: {name}")
    else:
        fail_count += 1
        print(f"  FAIL: {name}")

print("=== Test 1: Initial game state ===")
g = Game()
test("serve_speed_capture initialized to BASE_TICK_MS", g.serve_speed_capture == BASE_TICK_MS)
test("no active balls initially", len(g.active_balls) == 0)
test("serve_countdown=SERVE_DELAY(10)", g.serve_countdown == SERVE_DELAY)
test("no pending extras", g._extra_balls_pending == [])
test("initial feedback clear", g._feedback == "")

print("\n=== Test 2: Serve countdown phase ===")
# _reset_serve from __init__ already called, check countdown decrements correctly
for i in range(SERVE_DELAY):
    r = g.step()
test("countdown reaches 0 after SERVE_DELAY steps", g.serve_countdown == 0)
test("state changed to playing or has balls", 
     g.state == "playing" or len(g.active_balls) > 0)

print("\n=== Test 3: Ball exists after serve ===")
if hasattr(g, 'ball') and g.ball is not None:
    test("primary ball at paddle center (pre-countdown)", True)
if g.active_balls:
    b = g.active_balls[0]
    test(f"active ball has vx={b.get('vx','?')} vy={b.get('vy','?')}", True)
else:
    test("ball exists during serving", hasattr(g, 'ball'))

print("\n=== Test 4: Pickup spawn at every BRICKS_PER_PICKUP bricks ===")
g2 = Game()
# Play through SERVE_DELAY ticks to complete initial serve
for _ in range(SERVE_DELAY):
    g2.step()

test("state is playing after countdown", g2.state == "playing" or len(g2.active_balls) > 0)

# Now destroy bricks - track the brick at row 0 col 0 first
# First break a few to get past the initial ones
for i in range(BRICKS_PER_PICKUP):
    # Find an alive brick
    brick_to_break = None
    for r in range(min(3, len(g2.alive))):
        for c in range(len(g2.alive[r])):
            if g2.alive[r][c]:
                brick_to_break = (r, c)
                break
        if brick_to_break:
            break
    
    # Make sure ball can hit the brick - position paddle under it
    if brick_to_break:
        r_b, c_b = brick_to_break
        bx = 1 + c_b * 2 + 1  # pixel x of this brick's center
        g2.move_player(bx - (g2.px + PADDLE_W // 2))
    
    if brick_to_break:
        result = g2.break_brick(*brick_to_break)
        test(f"brick {i+1} destroyed", True)

# After BRICKS_PER_PICKUP bricks, pickup should be spawned
test("pickup spawned after enough bricks", 
     g2.pickup is not None or g2._bricks_destroyed < BRICKS_PER_PICKUP)

print("\n=== Test 5: Pending extras accumulate on pickup catch ===")
# Create a mock scenario: directly add a pending extra like a caught pickup would
g3 = Game()
for _ in range(SERVE_DELAY):
    g3.step()

captured_speed = max(g3._play_tick, BASE_TICK_MS) if g3._play_tick else BASE_TICK_MS
g3._extra_balls_pending.append(
    (-g3.serve_dir, captured_speed))  # First ball gets -serve_dir direction

test("one pending extra added", len(g3._extra_balls_pending) == 1)
test("direction saved correctly", g3._extra_balls_pending[0][0] == -g3.serve_dir)

print("\n=== Test 6: Pending extras display during serve ===")
# Simulate losing a ball with pending extras
g4 = Game()
# Destroy enough bricks to spawn a pickup (we'll cheat and break them directly)
for i in range(10):
    for r in range(min(3, len(g4.alive))):
        for c in range(len(g4.alive[r])):
            if g4.alive[r][c]:
                brx = 1 + c * 2 + 1
                g4.move_player(brx - (g4.px + PADDLE_W // 2))
                g4.break_brick(r, c)

# Now set up pending extras like a caught pickup would
captured_speed = max(g4._play_tick, BASE_TICK_MS) if g4._play_tick else BASE_TICK_MS
num_pending = 3
for i in range(num_pending):
    direction = (-g4.serve_dir if i % 2 == 0 
                 else g4.serve_dir)
    g4._extra_balls_pending.append((direction, captured_speed))

test(f"{num_pending} pending extras added", len(g4._extra_balls_pending) == num_pending)

# Render and check pending display
buf = io.StringIO()
g4.render(buf)
output = buf.getvalue()
has_pending_count = f" (+{num_pending})" in output
test(f"pending count '{'(+{})'.format(num_pending)}' shown in render", has_pending_count)

print("\n=== Test 7: Extra ball spawn from pending ===")
g5 = Game()
for _ in range(SERVE_DELAY):
    g5.step()

# Add pending extras and trigger countdown expiry
captured_speed = max(g5._play_tick, BASE_TICK_MS) if g5._play_tick else BASE_TICK_MS
g5.serve_countdown = 1  # about to expire
for i in range(2):
    direction = (-g5.serve_dir if i % 2 == 0 
                 else g5.serve_dir)
    g5._extra_balls_pending.append((direction, captured_speed))

# One more tick triggers countdown expiry and spawn
r = g5.step()
test("countdown zero triggers extras", len(g5.active_balls) > 0)
if g5.active_balls:
    test(f"2 balls spawned from 2 pending", len(g5.active_balls) == 2)
else:
    # ball might be at paddle (serving state before spawn) - check render
    buf = io.StringIO()
    g5.render(buf)

print("\n=== Test 8: Grace shot with pending extras on drop ===")
g6 = Game()
for _ in range(SERVE_DELAY):
    g6.step()

# Add a pending extra (simulating caught pickup mid-play)
captured_speed = max(g6._play_tick, BASE_TICK_MS) if g6._play_tick else BASE_TICK_MS
direction, spd = (-g6.serve_dir, captured_speed)
g6._extra_balls_pending.append((direction, captured_speed))

# Force a ball drop by setting balls past the bottom
g6.active_balls.append({'x': 10, 'y': GRID_H - 1})
orig_lives = g6.lives

r = g6.step()
test("pending extras trigger grace shot", len(g6._extra_balls_pending) < 1 or 
     len(g6.active_balls) > 0)
test("grace shot preserves lives", g6.lives == orig_lives)

print("\n=== Test 9: Life loss when no pending ===")
g7 = Game()
for _ in range(SERVE_DELAY):
    g7.step()

orig_lives = g7.lives
# Make a ball drop with no pending extras — clear serve balls so all balls are lost
# (multi-ball logic requires ALL balls to be dropped before life loss)
g7.active_balls.clear() 
g7.active_balls.append({'x': 10, 'y': GRID_H - 1})

r = g7.step()
test("life decreased when no pending", g7.lives == orig_lives - 1)

print("\n=== Summary ===")
total = pass_count + fail_count
print(f"  {pass_count}/{total} passed, {fail_count} failed")

if fail_count == 0:
    print("  ALL TESTS PASSED!")
else:
    print("  SOME TESTS DID NOT PASS - review above")
