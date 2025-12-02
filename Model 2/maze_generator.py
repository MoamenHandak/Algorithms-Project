import random

def generate_maze(rows, cols, density=0.1):
    """
    Generates a random maze using Recursive Backtracking.
    rows, cols: Dimensions of the maze (should be odd numbers for best results).
    density: Chance (0.0 to 1.0) to remove random walls after generation 
    to create loops (multiple paths).
    """
    # 1. Initialize grid with all walls (1)
    # Ensure dimensions are odd to allow for walls between cells
    if rows % 2 == 0: rows += 1
    if cols % 2 == 0: cols += 1
    
    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    def get_neighbors(r, c):
        # Check nodes 2 steps away (jumping over walls)
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
        random.shuffle(neighbors)
        return neighbors

    # 2. Recursive Backtracking to carve paths
    # Start at (0, 0)
    maze[0][0] = 0
    stack = [(0, 0)]

    while stack:
        current_r, current_c = stack[-1]
        neighbors = get_neighbors(current_r, current_c)
        found_unvisited = False

        for nr, nc in neighbors:
            if maze[nr][nc] == 1: # If unvisited (still a wall)
                # Carve path to neighbor (set neighbor to 0)
                maze[nr][nc] = 0
                # Carve the wall strictly between them
                wall_r = current_r + (nr - current_r) // 2
                wall_c = current_c + (nc - current_c) // 2
                maze[wall_r][wall_c] = 0
                
                stack.append((nr, nc))
                found_unvisited = True
                break
        
        if not found_unvisited:
            stack.pop()

    # 3. Add random loops (optional but recommended for pathfinding comparisons)
    # Without this, there is only ONE path, so BFS and A* look identical.
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if maze[r][c] == 1: # If it's a wall
                # Randomly remove it to create a shortcut/loop
                if random.random() < density:
                    maze[r][c] = 0

    # Ensure start and end are open
    maze[0][0] = 0
    maze[rows-1][cols-1] = 0

    return maze

# Simple test if run directly
if __name__ == "__main__":
    m = generate_maze(15, 15)
    for row in m:
        print(" ".join(['#' if c == 1 else '.' for c in row]))