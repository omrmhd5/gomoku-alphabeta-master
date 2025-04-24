import tkinter as tk
from tkinter import ttk
from game import GameRunner
import time

class SetupWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gomoku Setup")
        self.root.geometry("300x150")
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        
        # Create and pack widgets
        self.label = ttk.Label(self.root, text="Select Board Size (9-19):", font=('Arial', 12))
        self.label.pack(pady=20)
        
        self.size_var = tk.IntVar(value=15)  # Default value
        self.spinbox = ttk.Spinbox(self.root, from_=9, to=19, textvariable=self.size_var, width=5, font=('Arial', 12))
        self.spinbox.pack(pady=10)
        
        self.start_button = ttk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=10)
        
        self.selected_size = None
        
    def start_game(self):
        self.selected_size = self.size_var.get()
        self.root.destroy()
        
    def run(self):
        self.root.mainloop()
        return self.selected_size

class GomokuGUI:
    def __init__(self, board_size):
        self.root = tk.Tk()
        self.root.title("Gomoku")
        
        self.board_size = board_size
        self.cell_size = 30
        self.margin = 20
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas
        self.canvas = tk.Canvas(self.main_frame, 
                               width=self.board_size * self.cell_size + 2 * self.margin,
                               height=self.board_size * self.cell_size + 2 * self.margin,
                               bg='white')
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Create button frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Add restart button
        self.restart_button = ttk.Button(self.button_frame, text="New Game", command=self.restart_game)
        self.restart_button.pack(pady=10)
        
        # Initialize game with player as black (1)
        self.game = GameRunner(size=self.board_size)
        self.game.restart(player_index=1)  # 1 for black
        self.draw_board()
        self.canvas.bind('<Button-1>', self.handle_click)
        
    def restart_game(self):
        self.root.destroy()
        # Show setup window again
        setup = SetupWindow()
        board_size = setup.run()
        if board_size:  # If user selected a size
            # Start new game with selected size
            gui = GomokuGUI(board_size)
            gui.run()
        
    def draw_board(self):
        self.canvas.delete('all')
        
        # Draw grid
        for i in range(self.board_size):
            # Horizontal lines
            self.canvas.create_line(self.margin, 
                                  self.margin + i * self.cell_size,
                                  self.board_size * self.cell_size + self.margin,
                                  self.margin + i * self.cell_size)
            # Vertical lines
            self.canvas.create_line(self.margin + i * self.cell_size,
                                  self.margin,
                                  self.margin + i * self.cell_size,
                                  self.board_size * self.cell_size + self.margin)
        
        # Draw pieces
        for i in range(self.board_size):
            for j in range(self.board_size):
                piece = self.game.state.values[i, j]
                if piece != 0:
                    x = self.margin + j * self.cell_size
                    y = self.margin + i * self.cell_size
                    color = 'black' if piece == 1 else 'white'
                    self.canvas.create_oval(x - 12, y - 12, x + 12, y + 12,
                                          fill=color, outline='black')
    
    def handle_click(self, event):
        if self.game.finished:
            self.game.restart(player_index=1)  # Restart as black
            self.draw_board()
            return
            
        # Convert screen coordinates to board coordinates
        board_x = round((event.x - self.margin) / self.cell_size)
        board_y = round((event.y - self.margin) / self.cell_size)
        
        if 0 <= board_x < self.board_size and 0 <= board_y < self.board_size:
            if self.game.play(board_y, board_x):
                self.draw_board()
                self.root.update()  # Force update the display
                time.sleep(0.5)  # 500ms delay after player's move is shown
                self.game.aiplay()
                self.draw_board()
                
                if self.game.finished:
                    winner = "Black" if self.game.state.winner == 1 else "White"
                    self.canvas.create_text(self.board_size * self.cell_size // 2 + self.margin,
                                          self.board_size * self.cell_size // 2 + self.margin,
                                          text=f"{winner} wins! Click to restart",
                                          fill='red',
                                          font=('Arial', 20))
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Show setup window first
    setup = SetupWindow()
    board_size = setup.run()
    
    if board_size:  # If user selected a size
        # Start main game with selected size
        gui = GomokuGUI(board_size)
        gui.run() 