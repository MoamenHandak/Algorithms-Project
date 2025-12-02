import time

def dfs_solve(maze, start, goal):
    """
    DFS that records steps for visualization using an explicit stack.
    Returns (steps, path, real_time)
    steps actions: ("visit", (r,c)), ("backtrack", (r,c))
    """
    rows = len(maze)
    cols = len(maze[0])

    t0 = time.time()

    parent = {}
    visited = set([start])
    steps = []
    
    # Stack stores the current cell being explored
    stack = [start]
    steps.append(("visit", start))

    found = False

    def get_neighbors(r, c):
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0:
                yield (nr, nc)

    while stack:
        current = stack[-1] 
        
        if current == goal:
            found = True
            break
        
        r, c = current
        
        # Try to find the first unvisited neighbor
        next_cell = None
        for neighbor in get_neighbors(r, c):
            if neighbor not in visited:
                next_cell = neighbor
                break
        
        if next_cell:
            # Move forward (Deepen)
            parent[next_cell] = current
            visited.add(next_cell)
            steps.append(("visit", next_cell))
            stack.append(next_cell)
        else:
            # Backtrack
            steps.append(("backtrack", current))
            stack.pop() 

    t1 = time.time()
    real_time = t1 - t0

    # Reconstruct path
    if not found:
        return steps, None, real_time

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