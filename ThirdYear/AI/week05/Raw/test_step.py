#!/usr/bin/env python3
"""Diagnostic test for step() function."""
import sys, io
sys.argv = ['test']

from breakout_solo import *
install_colors(False)

def run_test(name, balls_init, px=None):
    g = Game(lives=3)
    g.state = 'playing'
    g.balls = balls_init[:]
    if px is not None:
        g.px = px
    
    print(f"\n=== {name} ===")
    print(f"Start: balls={g.balls}, px={g.px}")
    
    breaks = []
    for i in range(30):
        n_balls_before = len(g.balls)
        
        # Capture positions before step for comparison (we need the NEW ones after)
        result = g.step()
        
        changed = ""
        new_breaks = [b for b in breaks if b not in breaks]
        
        status = ""
        if result == "life":
            status = " LIFE LOST"
        elif g.state != "playing":
            status = f" STATE={g.state}"
            
        balls_info = []
        for j, ball in enumerate(g.balls):
            bx, by, vx, vy = ball
            # Show velocity direction
            v_str = "+" if vx > 0 else ("-" if vx < 0 else "=")
            y_str = "D" if vy > 0 else "U"
            blk = g.block_at(bx, by)
            brick_info = ""
            if blk:
                r, c = blk
                brick_info = f"[{r},{c}:{'ALIVE' if g.alive[r][c] else 'dead'}]"
            balls_info.append(f"ball[{j}]=({bx},{by}) v=({vx:+d},{vy:+d}) {brick_info}")
        
        print(f"T{i+1}: {'; '.join(balls_info)}{status}{changed}")
        
        if g.state != "playing":
            break
            
    print(f"Final: bricks_left={g.bricks_left}, score={g.score}")


# Test 1: Ball aimed into brick zone, centered  
print("="*60)
run_test(
    "Ball aimed down-center",
    [(16, BRICK_Y0 - 1, 0, 1)], 
    px=GRID_W // 2 - PADDLE_W // 2  # center paddle
)

# Test 2: Ball off-center (should hit bricks and scatter)
print("\n" + "="*60)
run_test(
    "Ball aimed down-left",
    [(10, BRICK_Y0 - 1, -1, 1)], 
    px=GRID_W // 2 - PADDLE_W // 2  
)

# Test 3: Ball aimed up-right from brick row edge
print("\n" + "="*60)
run_test(
    "Ball in brick row going right-down",
    [(8, BRICK_Y0, 1, 1)],   # INSIDE a brick cell!
    px=GRID_W // 2 - PADDLE_W // 2  
)

# Test 4: Verify block_at mapping for key positions
print("\n" + "="*60)
g = Game(lives=3)
print("brick rows (BRICK_Y0={} to BRICK_Y0+{}-1):".format(BRICK_Y0, BRICK_ROWS))
for test_y in range(1, BRICK_Y0 + 4):
    for x_test in [5, 7, 8, 9, 15, 16, 23, 29]:
        blk = g.block_at(x_test, test_y)
        if blk:
            r, c = blk
            status = "ALIVE" if g.alive[r][c] else "dead"
            print(f"  block_at({x_test:2d}, {test_y}) -> ({r},{c}) brick[{status}]")
        else:
            # figure out why None
            rr = test_y - BRICK_Y0
            if rr < 0 or rr >= BRICK_ROWS:
                reason = f"yr={rr} out of row range"
            else:
                cc2 = (x_test - 1) // 2
                if cc2 < 0 or cc2 >= BRICK_COLS:
                    reason = f"xcell={x_test-1}, col_idx={(x_test-1)//2} out of bounds"
                else:
                    reason = "unknown"
            print(f"  block_at({x_test:2d}, {test_y}) -> None ({reason})")

# Test 5: Manual brick collision check - walk through step logic by hand
print("\n" + "="*60)
g = Game(lives=3)
balls_init = [(16, BRICK_Y0 - 1, 0, 1)]  # Start at center, just above bricks, going down

x_cur, y_cur = balls_init[0][0], balls_init[0][1]
vx_cur, vy_cur = balls_init[0][2], balls_init[0][3]

print("Hand-tracing step() for ball starting at (16, 1), vx=0, vy=1:")
for i in range(5):
    nx, ny = x_cur + vx_cur, y_cur + vy_cur
    
    # Side walls  
    wall_x = False
    if nx <= 1 or nx >= GRID_W - 2:
        print(f"  -> Wall hit at nx={nx}, clamping to {1 if nx <= 1 else GRID_W-2}")
        nx = 1 if nx <= 1 else GRID_W - 2
        vx_cur = -vx_cur
        wall_x = True
    
    # Ceiling  
    ceiling = False
    if ny <= 1:
        print(f"  -> Ceiling hit at ny={ny}, bouncing")
        ny = 2 - (ny - 1)
        vy_cur = -vy_cur
        ceiling = True
    
    # Brick check on clamped position
    blk = g.block_at(nx, ny)
    has_brick_collided = False
    if blk and g.alive[blk[0]][blk[1]]:
        was_alive = g.break_brick(*blk)
        if was_alive:
            vy_cur = -vy_cur
            vx_cur = 1 if nx % 2 == 1 else -1  
            has_brick_collided = True
            breaks_here = f"HIT brick {blk}, breaking! new_vel=({vx_cur:+d},{vy_cur:+d})"
        else:
            breaks_here = f"(brick was already dead)"
    else:
        breaks_here = ""
    
    # Paddle check
    paddle_hit = False  
    if vy_cur > 0 and ny == PADDLE_Y - 1:
        px_left, px_right = g.px, g.px + PADDLE_W - 1
        if px_left <= nx <= px_right:
            offset = nx - (g.px + PADDLE_W // 2)
            vy_cur = -1
            if offset <= -2: vx_cur = -1
            elif offset >= 2: vx_cur = 1
            paddle_hit = True
        
    # Fall check
    fell = ny >= GRID_H - 2
    
    print(f"  Step {i+1}: predicted=({nx},{ny}), wall={wall_x}, ceiling={ceiling}  brick={'HIT' if has_brick_collided else 'none'}  paddle={paddle_hit}  fell={fell}")
    print(f"           result pos=({nx},{ny}) vel=({vx_cur:+d},{vy_cur:+d}) {breaks_here or ''}")
    
    x_cur, y_cur = nx, ny
    
print(f"\nBricks remaining: {g.bricks_left}")

# Test 6: Multi-ball with paddle catch
print("\n" + "="*60)
run_test(
    "Multi-ball at paddle level catching pickup",
    [(14, PADDLE_Y - 2, 0, 1), (18, PADDLE_Y - 3, 0, 1)],  
    px=GRID_W // 2 - PADDLE_W // 2
)

print("\n=== All tests complete ===")
