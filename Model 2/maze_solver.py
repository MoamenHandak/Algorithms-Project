import heapq
from collections import deque
import maze_generator  # Imports the generator file you just made

# ---------------------------------------------------------
# SETUP: Generate a Random Maze
# ---------------------------------------------------------
# We use odd numbers for dimensions because the generator works best that way
ROWS, COLS = 21, 21 
# Generate a fresh maze
MAZE = maze_generator.generate_maze(ROWS, COLS, density=0.05)

START = (0, 0)
GOAL = (ROWS - 1, COLS - 1)

# Helper to visualize the path in the terminal
def print_path(path, title):
    # Create a copy of the maze for printing
    display_maze = [[' ' if cell == 0 else '#' for cell in row] for row in MAZE]
    
    path_len = 0
    if path:
        path_len = len(path)
        for (r, c) in path:
            # Don't overwrite Start/Goal markers
            if (r, c) != START and (r, c) != GOAL:
                display_maze[r][c] = '.'
    
    display_maze[START[0]][START[1]] = 'S'
    display_maze[GOAL[0]][GOAL[1]] = 'E'
    
    print(f"\n--- {title} ---")
    if not path:
        print("No path found!")
        return

    print(f"Path Length: {path_len} steps")
    print("-" * (COLS * 2 + 2))
    for row in display_maze:
        print("|" + " ".join(row) + "|")
    print("-" * (COLS * 2 + 2))

# Helper to find valid neighbors
def get_neighbors(r, c):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and MAZE[nr][nc] == 0:
            yield (nr, nc)

# ---------------------------------------------------------
# 1. Depth-First Search (DFS)
# ---------------------------------------------------------
def solve_dfs():
    stack = [START]
    visited = set()
    parent = {}

    visited.add(START)

    while stack:
        current = stack.pop()
        
        if current == GOAL:
            break

        for neighbor in get_neighbors(*current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)
    
    return reconstruct_path(parent)

# ---------------------------------------------------------
# 2. Breadth-First Search (BFS)
# ---------------------------------------------------------
def solve_bfs():
    queue = deque([START])
    visited = set()
    parent = {}

    visited.add(START)

    while queue:
        current = queue.popleft()

        if current == GOAL:
            break

        for neighbor in get_neighbors(*current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    
    return reconstruct_path(parent)

# ---------------------------------------------------------
# 3. A* Search (A-Star)
# ---------------------------------------------------------
def heuristic(a, b):
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def solve_astar():
    pq = []
    heapq.heappush(pq, (0, START))
    
    parent = {}
    g_score = {START: 0}

    while pq:
        _, current = heapq.heappop(pq)

        if current == GOAL:
            break

        for neighbor in get_neighbors(*current):
            new_g_score = g_score[current] + 1
            
            if new_g_score < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = new_g_score
                f_score = new_g_score + heuristic(neighbor, GOAL)
                heapq.heappush(pq, (f_score, neighbor))
                parent[neighbor] = current

    return reconstruct_path(parent)

def reconstruct_path(parent):
    path = []
    current = GOAL
    if current not in parent:
        return None
    while current != START:
        path.append(current)
        current = parent[current]
    path.append(START)
    path.reverse()
    return path

# ---------------------------------------------------------
# Main Execution
# ---------------------------------------------------------
if __name__ == "__main__":
    print(f"Generated Random Maze Size: {ROWS}x{COLS}")
    
    # Show empty maze first
    print("\n--- The Maze ---")
    for row in MAZE:
        print(" ".join([' ' if c == 0 else '#' for c in row]))

    # Run algorithms
    dfs_path = solve_dfs()
    bfs_path = solve_bfs()
    astar_path = solve_astar()

    print_path(dfs_path, "DFS (Depth-First)")
    print_path(bfs_path, "BFS (Breadth-First)")
    print_path(astar_path, "A* (A-Star)")