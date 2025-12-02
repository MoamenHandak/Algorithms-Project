import random

def generate_maze(rows, cols, density=0.05):
    """
    Generates a random maze using Recursive Backtracking.
    rows, cols: Dimensions of the maze (should be odd numbers for best results).
    density: Chance (0.0 to 1.0) to remove random walls after generation to create loops.
    Returns a 2D list: 0=open, 1=wall
    """
    # Ensure dimensions are odd
    if rows % 2 == 0:
        rows += 1
    if cols % 2 == 0:
        cols += 1

    # Initialize all cells as walls (1)
    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    def get_neighbors(r, c):
        # Look for neighbors 2 steps away (only in the carveable cells)
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
        random.shuffle(neighbors)
        return neighbors

    # Start carving from (1, 1) to ensure outer walls are intact
    start_r, start_c = 1, 1
    maze[start_r][start_c] = 0
    stack = [(start_r, start_c)]

    while stack:
        current_r, current_c = stack[-1]
        neighbors = get_neighbors(current_r, current_c)
        found_unvisited = False

        for nr, nc in neighbors:
            # Check if the potential neighbor is still a wall (unvisited)
            if maze[nr][nc] == 1:
                # Carve the cell
                maze[nr][nc] = 0
                # Calculate the wall position between current and neighbor
                wall_r = current_r + (nr - current_r) // 2
                wall_c = current_c + (nc - current_c) // 2
                # Carve the wall
                maze[wall_r][wall_c] = 0
                stack.append((nr, nc))
                found_unvisited = True
                break

        if not found_unvisited:
            stack.pop()

    # Add random loops (optional step)
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if maze[r][c] == 1 and random.random() < density:
                maze[r][c] = 0

    # Ensure start (0, 0) and goal (rows-1, cols-1) are open paths, by opening 
    # the path leading to them from the carved interior.
    # Start: (1, 0) or (0, 1) must be 0, we choose (0, 1) and (rows-1, cols-2)
    
    # Entrance (Top-left): Open the cell at (0, 1)
    maze[0][1] = 0
    # Exit (Bottom-right): Open the cell at (rows-1, cols-2)
    maze[rows - 1][cols - 2] = 0
    
    # Mark start and goal points (which are now (0, 0) and (rows-1, cols-1))
    # It is standard practice to let the solver handle the start/goal markers, 
    # but we ensure the cells themselves are open for the solver.
    # Since start/goal are (0,0) and (rows-1, cols-1) in the UI, we must open them:
    maze[0][0] = 0
    maze[rows - 1][cols - 1] = 0

    return maze