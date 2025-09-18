import heapq
import random

# Goal state of the 8-puzzle
GOAL_STATE = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Moves: up, down, left, right

class Cell:
    def __init__(self, parent=None, g=float('inf'), h=0):
        self.parent = parent  # Parent state
        self.g = g  # Cost from start to this state
        self.h = h  # Heuristic cost to goal

    @property
    def f(self):
        return self.g + self.h

def manhattan(puzzle):
    dist = 0
    for r in range(3):
        for c in range(3):
            val = puzzle[r][c]
            if val == 0:
                continue
            tr, tc = divmod(val - 1, 3)
            dist += abs(r - tr) + abs(c - tc)
    return dist

def find_zero(puzzle):
    for r, row in enumerate(puzzle):
        for c, val in enumerate(row):
            if val == 0:
                return r, c

def neighbors(puzzle):
    r, c = find_zero(puzzle)
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_puzzle = [list(row) for row in puzzle]
            new_puzzle[r][c], new_puzzle[nr][nc] = new_puzzle[nr][nc], new_puzzle[r][c]
            yield tuple(tuple(row) for row in new_puzzle)

def trace_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

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
            new_cost = cost_so_far[current] + 1  # uniform cost per move
            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                cost_so_far[nxt] = new_cost
                h = manhattan(nxt)
                cell_details[nxt] = Cell(parent=current, g=new_cost, h=h)
                came_from[nxt] = current
                f = new_cost + h
                heapq.heappush(open_list, (f, nxt))
    return None

def scramble(puzzle, moves=20):
    for _ in range(moves):
        puzzle = random.choice(list(neighbors(puzzle)))
    return puzzle

def print_puzzle(puzzle):
    for row in puzzle:
        print(' '.join(str(x) if x != 0 else '_' for x in row))
    print()

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