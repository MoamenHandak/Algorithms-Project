import tkinter as tk
from tkinter import ttk
import time

# Import all necessary modules
from generator.maze_generator import generate_maze
from algorithms.dfs import dfs_solve
from algorithms.bfs import bfs_solve
from algorithms.astar import astar_solve


class MazeApp:
    def __init__(self, rows=31, cols=31, cell_size=20):
        self.root = tk.Tk()
        self.root.title("Maze Solver Visualizer")

        # --- Configuration ---
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.maze = []
        self.rect_ids = []
        
        self.colors = {
            'wall': '#2C3E50',
            'open': '#ECF0F1',
            'start': '#2ECC71',
            'goal': '#E74C3C',
            'visit': '#3498DB',     # Exploring
            'backtrack': '#F39C12', # DFS Backtrack
            'path': '#9B59B6'       # Final Solution Path
        }

        # --- UI Setup ---
        
        # 1. Main Canvas
        self.canvas = tk.Canvas(self.root, width=cols * cell_size, height=rows * cell_size, bg=self.colors['wall'])
        self.canvas.pack(padx=10, pady=10)

        # 2. Controls Frame
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)

        # 3. Algorithm Selector
        self.algo_var = tk.StringVar(value='A*')
        algo_options = ['A*', 'BFS', 'DFS']
        algo_label = ttk.Label(control_frame, text="Algorithm:")
        algo_label.pack(side=tk.LEFT, padx=5)
        algo_menu = ttk.OptionMenu(control_frame, self.algo_var, 'A*', *algo_options)
        algo_menu.pack(side=tk.LEFT, padx=5)
        
        # 4. Speed Slider
        self.speed_slider = ttk.Scale(control_frame, from_=1, to=100, orient=tk.HORIZONTAL)
        self.speed_slider.set(20) # Default speed (20ms delay)
        speed_label = ttk.Label(control_frame, text="Delay (ms):")
        speed_label.pack(side=tk.LEFT, padx=10)
        self.speed_slider.pack(side=tk.LEFT, padx=5)

        # 5. Buttons
        ttk.Button(control_frame, text="Generate New Maze", command=self.generate_new_maze).pack(side=tk.LEFT, padx=10)
        ttk.Button(control_frame, text="Solve Maze", command=lambda: self.solve_maze(self.algo_var.get())).pack(side=tk.LEFT, padx=10)
        
        # 6. Status Label
        self.time_label = ttk.Label(self.root, text="Actual Solve Time: N/A")
        self.time_label.pack(pady=5)

        # --- Initial Setup ---
        self.generate_new_maze()
        
        # Start main loop
        self.root.mainloop()

    def generate_new_maze(self):
        """Generates a new maze and resets the UI state."""
        self.rows = int(self.rows / 2) * 2 + 1 # Ensure odd
        self.cols = int(self.cols / 2) * 2 + 1
        self.maze = generate_maze(self.rows, self.cols)
        self.rect_ids = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.draw_grid()
        self.time_label.config(text="Actual Solve Time: N/A")

    # --- Methods provided by the user (with class context added) ---
    def solve_maze(self, algo):
        """
        Solves the maze using the selected algorithm and starts the animation.
        This block uses the user's provided logic for algorithm execution.
        """
        # Reset state and visualization
        self.draw_grid()
        self.time_label.config(text="Actual Solve Time: Computing...")
        
        start = (0, 0)
        goal = (self.rows - 1, self.cols - 1)

        # Choose algorithm
        if algo == 'DFS':
            steps, path, real_time = dfs_solve(self.maze, start, goal)
        elif algo == 'BFS':
            steps, path, real_time = bfs_solve(self.maze, start, goal)
        else: # Default or A*
            steps, path, real_time = astar_solve(self.maze, start, goal)

        self.steps = steps
        self.path = path
        self.solve_time = real_time

        # Start animating the recorded steps
        self.anim_index = 0
        self.visited_set = set()
        # Tkinter's root.after is the correct way to schedule the animation loop
        self.root.after(0, self.animate_step)


    def draw_grid(self):
        """
        Draws the initial maze grid on the canvas.
        This block uses the user's provided logic for drawing the grid.
        """
        self.canvas.delete('all')
        cell = self.cell_size
        self.canvas.config(width=self.cols * cell, height=self.rows * cell)
        
        # Ensure rect_ids is correctly sized after maze generation
        self.rect_ids = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * cell
                y1 = r * cell
                x2 = x1 + cell
                y2 = y1 + cell
                color = self.colors['wall'] if self.maze[r][c] == 1 else self.colors['open']
                rid = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')
                self.rect_ids[r][c] = rid

        # mark start and goal (0,0) and (rows-1, cols-1)
        self.canvas.itemconfig(self.rect_ids[0][0], fill=self.colors['start'])
        self.canvas.itemconfig(self.rect_ids[self.rows - 1][self.cols - 1], fill=self.colors['goal'])


    def animate_step(self):
        """
        Animates the search process step-by-step.
        This block uses the user's provided logic for animation.
        """
        delay = self.speed_slider.get()
        if self.anim_index < len(self.steps):
            action, cell = self.steps[self.anim_index]
            r, c = cell
            
            # Check if cell is not start or goal before coloring
            is_special = (r, c) == (0, 0) or (r, c) == (self.rows - 1, self.cols - 1)
            
            if action == 'visit':
                if not is_special:
                    self.canvas.itemconfig(self.rect_ids[r][c], fill=self.colors['visit'])
            elif action == 'backtrack':
                # DFS specific action
                if not is_special:
                    self.canvas.itemconfig(self.rect_ids[r][c], fill=self.colors['backtrack'])
            
            self.anim_index += 1
            self.root.after(int(delay), self.animate_step)
        else:
            # finished exploring; draw final path if exists
            if self.path:
                # Color the path cells
                for (r, c) in self.path:
                    is_special = (r, c) == (0, 0) or (r, c) == (self.rows - 1, self.cols - 1)
                    if not is_special:
                        self.canvas.itemconfig(self.rect_ids[r][c], fill=self.colors['path'])

                # Re-ensure start and goal colors are dominant
                self.canvas.itemconfig(self.rect_ids[0][0], fill=self.colors['start'])
                self.canvas.itemconfig(self.rect_ids[self.rows - 1][self.cols - 1], fill=self.colors['goal'])
                
            # show real solve time
            self.time_label.config(text=f"Actual Solve Time: {self.solve_time:.6f} seconds")