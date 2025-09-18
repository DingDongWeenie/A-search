import heapq
import random

# 3x3 puzzle (solved state)
solved_state = ((1, 2, 3), (4, 5, 6), (7, 8, 0))  # 0 represents the empty space

# Directions: up, down, left, right
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Heuristic: Manhattan distance
def manhattan(puzzle):
    distance = 0
    for r in range(3):
        for c in range(3):
            val = puzzle[r][c]
            if val == 0:
                continue
            target_r = (val - 1) // 3
            target_c = (val - 1) % 3
            distance += abs(r - target_r) + abs(c - target_c)
    return distance

# empty tile (0) finder
def find_zero(puzzle):
    for r in range(3):
        for c in range(3):
            if puzzle[r][c] == 0:
                return r, c

# Generate neighbors by sliding empty tile
def neighbors(puzzle):
    r, c = find_zero(puzzle)
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_puzzle = [list(row) for row in puzzle]
            # Swap zero with neighbor
            new_puzzle[r][c], new_puzzle[nr][nc] = new_puzzle[nr][nc], new_puzzle[r][c]
            yield tuple(tuple(row) for row in new_puzzle)

# A* search
def a_star(start):
    frontier = []
    heapq.heappush(frontier, (manhattan(start), 0, start, []))  # (priority, cost, state, path)
    explored = set()
    while frontier:
        priority, cost, state, path = heapq.heappop(frontier)
        if state == solved_state:
            return path + [state]
        if state in explored:
            continue
        explored.add(state)
        for next_state in neighbors(state):
            if next_state not in explored:
                heapq.heappush(frontier, (cost + 1 + manhattan(next_state), cost + 1, next_state, path + [state]))
    return None

# Puzzle Scrambler 
def scramble(puzzle, moves=20):
    current = puzzle
    for _ in range(moves):
        neighbors_list = list(neighbors(current))
        current = random.choice(neighbors_list)
    return current

def print_puzzle(puzzle):
    for row in puzzle:
        print(' '.join(str(x) if x != 0 else '_' for x in row))
    print()

# Generate scrambled puzzle
start_state = scramble(solved_state, 20)

print("Scrambled puzzle:")
print_puzzle(start_state)

solution_path = a_star(start_state)
if solution_path:
    print(f"Solution found in {len(solution_path)-1} moves:")
    for step in solution_path:
        print_puzzle(step)
else:
    print("No solution found.")