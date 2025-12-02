import time
import heapq

def heuristic(a, b):
    """Calculates Manhattan distance between two points a and b."""
    # a and b are (r, c) tuples
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_solve(maze, start, goal):
    """
    A* that records steps when nodes are expanded (popped from open set).
    Returns (steps, path, real_time)
    steps: ("visit", (r,c))
    """
    rows = len(maze)
    cols = len(maze[0])

    t0 = time.time()

    # open_heap stores (f_score, g_score, coordinates)
    # The lowest f_score is popped first
    open_heap = []
    heapq.heappush(open_heap, (0 + heuristic(start, goal), 0, start))
    parent = {}
    gscore = {start: 0}
    closed = set()
    steps = []

    found = False

    while open_heap:
        f, g, current = heapq.heappop(open_heap)
        
        # If the node was already processed via a better path (in closed set)
        if current in closed:
            continue

        closed.add(current)
        steps.append(("visit", current))

        if current == goal:
            found = True
            break

        r, c = current
        # Check 4 neighbors (Up, Down, Left, Right)
        for nr, nc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
            neighbor = (nr, nc)
            # Check bounds and if the cell is not a wall (0 is open path)
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0:
                tentative_g = g + 1
                
                if tentative_g < gscore.get(neighbor, float('inf')):
                    # Found a better path
                    parent[neighbor] = current
                    gscore[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_heap, (f_score, tentative_g, neighbor))

    t1 = time.time()
    real_time = t1 - t0

    if not found:
        return steps, None, real_time

    # Reconstruct path
    path = []
    cur = goal
    # Safety check for path reconstruction
    while cur != start and cur in parent:
        path.append(cur)
        cur = parent[cur]
    
    if cur == start:
        path.append(start)
        path.reverse()
        return steps, path, real_time
    else:
        # Should not happen if found is True, but good practice
        return steps, None, real_time