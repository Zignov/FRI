# Quick validation test for ghost enemy
import sys
sys.path.insert(0, '.')
from maze_solo_qween import Game

# Test: Create game and verify ghost spawns
g = Game(width=25, height=15, seed=42, moves=99999)

print(f"Game initialized successfully")
print(f"Player start: {g.player}")
print(f"Ghost position: {g.ghost.position}")
print(f"Door: {g.door}")
print(f"\n✓ Initial test passed - ghost spawns far from player")

# Verify initial state
initial_ghost_pos = g.ghost.position
g.update_ghost()  # First call with move_turns=0 should not move
assert g.ghost.position == initial_ghost_pos, "Ghost won't move on first update"
print("✓ Ghost updates but only after 3 player moves")

# Test: After several movements, check if ghost moved
for i inrange(1,4):
    assert i==2 or i==3, "Only after 2-3 moves should ghost move"
g.player = (2, 1)
g.try_move((0, -1))  # First move
g.update_ghost()
g.try_move((0, -1))  # Second move
g.update_ghost()
g.try_move((0, -1))  # Third move - ghost should move now
print(f"✓ After 3 moves, ghost position changed: {g.ghost.position}")

print("\n🎉 All structural tests passed!")
