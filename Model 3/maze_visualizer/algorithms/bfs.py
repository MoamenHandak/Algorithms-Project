import time
from collections import deque

def bfs_solve(maze, start, goal):
    """
    BFS that records steps for visualization.
    Returns (steps, path, real_time)
    steps actions: ("visit", (r,c))
    """
    rows = len(maze)
    cols = len(maze[0])

    t0 = time.time()

    visited = set([start])
    parent = {}
    steps = []

    q = deque([start])

    found = False

    while q:
        current = q.popleft()
        steps.append(("visit", current)) # Record visit upon popping (consistent with A*)
        
        if current == goal:
            found = True
            break

        r, c = current
        for nr, nc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
            neighbor = (nr, nc)
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                q.append(neighbor)

    t1 = time.time()
    real_time = t1 - t0

    if not found:
        return steps, None, real_time

    # Reconstruct path
    path = []
    cur = goal
    while cur != start and cur in parent:
        path.append(cur)
        cur = parent[cur]
    
    if cur == start:
        path.append(start)
        path.reverse()
        return steps, path, real_time
    else:
        return steps, None, real_time