import heapq
import random

# --- Puzzle and Moves Setup ---
GOAL_STATE = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right moves

# This is the solved puzzle or end/goal state.
# The empty space (0) can move in these four directions.

class Cell:
    def __init__(self, parent=None, g=float('inf'), h=0):
        # Remember where we came from
        self.parent = parent
        # Number of moves made so far
        self.g = g
        # Guess of moves left to solve
        self.h = h
    @property
    def f(self):
        # Total guess = moves done + guess moves left
        return self.g + self.h

# Cell keeps track of where we came from, how many moves done, and guess moves left.

def manhattan(puzzle):
    dist = 0
    for r in range(3):
        for c in range(3):
            val = puzzle[r][c]
            if val == 0:
                continue  # skip empty space
            tr, tc = divmod(val - 1, 3)
            dist += abs(r - tr) + abs(c - tc)
    return dist

# This counts how far every tile is from where it should be.
# Helps guess how close we are to solving.

def find_zero(puzzle):
    for r, row in enumerate(puzzle):
        for c, val in enumerate(row):
            if val == 0:
                return r, c

# Find the empty space location

def neighbors(puzzle):
    r, c = find_zero(puzzle)
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_puzzle = [list(row) for row in puzzle]
            # Swap empty space with neighbor tile
            new_puzzle[r][c], new_puzzle[nr][nc] = new_puzzle[nr][nc], new_puzzle[r][c]
            # Make it a tuple so we can use it as a key
            yield tuple(tuple(row) for row in new_puzzle)

# Give all puzzle states that come from moving empty space one step

def trace_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

# Follow back from goal to start to find the steps taken

def a_star(start):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    cost_so_far = {start: 0}
    cell_details = {start: Cell(parent=None, g=0, h=manhattan(start))}
    closed_set = set()

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == GOAL_STATE:
            return trace_path(came_from, current)

        if current in closed_set:
            continue
        closed_set.add(current)

        for nxt in neighbors(current):
            new_cost = cost_so_far[current] + 1  # Each move costs 1
            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                cost_so_far[nxt] = new_cost
                h = manhattan(nxt)
                cell_details[nxt] = Cell(parent=current, g=new_cost, h=h)
                came_from[nxt] = current
                f = new_cost + h
                heapq.heappush(open_list, (f, nxt))
    return None

# dito na yung A* search algo:
# chinecheck niya kung ano yung easiest move na pwedeng gawin.
# tapos trinatrack niya yung moves at guesses.
# then titigil na pag na solve na yung puzzle. (tinagalog ko nalang at inaantok nako sir)

def scramble(puzzle, moves=20):
    for _ in range(moves):
        puzzle = random.choice(list(neighbors(puzzle)))
    return puzzle

# randomizer

def print_puzzle(puzzle):
    for row in puzzle:
        print(' '.join(str(x) if x != 0 else '_' for x in row))
    print()

# Print the puzzle with empty space shown as _

if __name__ == "__main__":
    start = scramble(GOAL_STATE)
    print("Scrambled puzzle:")
    print_puzzle(start)

    solution_path = a_star(start)
    if solution_path:
        print(f"Solution found in {len(solution_path) - 1} moves:")
        for state in solution_path:
            print_puzzle(state)
    else:
        print("No solution found.")
