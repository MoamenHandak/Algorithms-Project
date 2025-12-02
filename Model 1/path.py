import heapq
from collections import deque

# ---------------------------------------------------------
#                   Maze Definition
# ---------------------------------------------------------

# 0 = Open path, 1 = Wall
# the Maze
MAZE = [
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

START = (0, 0)
GOAL = (8, 9)
ROWS = len(MAZE)
COLS = len(MAZE[0])

# converter form numbers to visual
def print_path(path, title):
    # Create a copy of the maze
    display_maze = [[' ' if cell == 0 else '#' for cell in row] for row in MAZE]
    
    # Mark the path
    if path:
        for (r, c) in path:
            display_maze[r][c] = '.'
        display_maze[START[0]][START[1]] = 'S'
        display_maze[GOAL[0]][GOAL[1]] = 'E'
    
    print(f"\n--- {title} ---")
    if not path:
        print("No path found!")
        return

    print(f"Path Length: {len(path)} steps")
    print("-" * (COLS * 2 + 2))
    for row in display_maze:
        print("|" + " ".join(row) + "|")
    print("-" * (COLS * 2 + 2))

# Helper to find valid neighbors
def get_neighbors(r, c):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and MAZE[nr][nc] == 0:
            yield (nr, nc)

# ---------------------------------------------------------
#               1. Depth-First Search (DFS)
#           Uses a Stack (LIFO - Last In, First Out)
# ---------------------------------------------------------
def solve_dfs():
    stack = [START]
    visited = set()
    parent = {} # To reconstruct path

    visited.add(START)

    while stack:
        current = stack.pop() # LIFO behavior
        
        if current == GOAL:
            break

        for neighbor in get_neighbors(*current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)
    
    return reconstruct_path(parent)

# ---------------------------------------------------------
#               2. Breadth-First Search (BFS)
#           Uses a Queue (FIFO - First In, First Out)
# ---------------------------------------------------------
def solve_bfs():
    queue = deque([START])
    visited = set()
    parent = {}

    visited.add(START)

    while queue:
        current = queue.popleft() # FIFO behavior

        if current == GOAL:
            break

        for neighbor in get_neighbors(*current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    
    return reconstruct_path(parent)

# ---------------------------------------------------------
#               3. A* Search (A-Star)
#       Uses a Priority Queue (Min-Heap) + Heuristic
# ---------------------------------------------------------
def heuristic(a, b):
    # Manhattan distance: |x1 - x2| + |y1 - y2|
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def solve_astar():
    # Priority Queue stores tuples: (f_score, current_node)
    pq = []
    heapq.heappush(pq, (0, START))
    
    parent = {}
    g_score = {START: 0} # Cost from start to current node

    while pq:
        _, current = heapq.heappop(pq) # Get node with lowest f_score

        if current == GOAL:
            break

        for neighbor in get_neighbors(*current):
            new_g_score = g_score[current] + 1
            
            # If we found a better path to this neighbor
            if new_g_score < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = new_g_score
                f_score = new_g_score + heuristic(neighbor, GOAL)
                heapq.heappush(pq, (f_score, neighbor))
                parent[neighbor] = current

    return reconstruct_path(parent)

# ---------------------------------------------------------
# Helper to backtrack from Goal to Start using parent dictionary
# ---------------------------------------------------------
def reconstruct_path(parent):
    path = []
    current = GOAL
    if current not in parent:
        return None # Goal never reached
    
    while current != START:
        path.append(current)
        current = parent[current]
    path.append(START)
    path.reverse()
    return path

# ---------------------------------------------------------
#                       Main Execution
# ---------------------------------------------------------
if __name__ == "__main__":
    print(f"Maze Size: {ROWS}x{COLS}")
    print("S = Start\n E = End\n . = Path\n # = Wall")

    # Run DFS
    dfs_path = solve_dfs()
    print_path(dfs_path, "DFS (Depth-First Search)")
    print("Notice: DFS often zig-zags and is rarely the shortest path.")

    # Run BFS
    bfs_path = solve_bfs()
    print_path(bfs_path, "BFS (Breadth-First Search)")
    print("Notice: BFS is guaranteed to be the shortest path.")

    # Run A*
    astar_path = solve_astar()
    print_path(astar_path, "A* (A-Star Search)")
    print("Notice: A* is also the shortest path, but usually visits fewer nodes than BFS.")