import tkinter as tk
from tkinter import ttk
from game import GameRunner
import time

# Styling configuration for a modern, neutral palette
BACKGROUND_COLOR = "#547792"
CANVAS_BG = "#e8e8e8"
GRID_COLOR = "#a0a0a0"
BLACK_PIECE = "#333333"
WHITE_PIECE = "#ffffff"
BUTTON_BG = "#2E3D49"
BUTTON_ACTIVE_BG = "#547792"
BUTTON_HOVER_BG = "#3c4c60"  # New hover background for button
SPINBOX_BG = "#405466"  # Lighter shade for spinbox background
SPINBOX_FG = "white"
SPINBOX_BORDER = "#a0a0a0"
FONT = ("Times New Roman", 12)
FONTCOLOR = "white"

class SetupWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gomoku Setup")
        self.root.geometry("400x300")  # Increased height for difficulty selection
        self.root.configure(bg=BACKGROUND_COLOR)
        self.root.eval('tk::PlaceWindow . center')

        self.label = tk.Label(self.root, text="Select Board Size (9-19):", bg=BACKGROUND_COLOR, font=("Times New Roman", 15, "bold"), fg=FONTCOLOR)
        self.label.pack(pady=(30, 10))

        self.size_var = tk.IntVar(value=15)
        self.spinbox = tk.Spinbox(self.root, 
                                 from_=9, 
                                 to=19, 
                                 textvariable=self.size_var, 
                                 width=10, 
                                 font=FONT,
                                 justify='center',
                                 bg=SPINBOX_BG,
                                 fg=SPINBOX_FG,
                                 relief=tk.FLAT,
                                 bd=6,
                                 highlightthickness=1,
                                 highlightbackground=SPINBOX_BORDER,
                                 highlightcolor=SPINBOX_BORDER,
                                 buttonbackground='gray',
                                 buttonuprelief=tk.FLAT,
                                 buttondownrelief=tk.FLAT)
        self.spinbox.pack(pady=10)

        # Add difficulty selection
        self.difficulty_label = tk.Label(self.root, text="Select Difficulty Level:", bg=BACKGROUND_COLOR, font=("Times New Roman", 15, "bold"), fg=FONTCOLOR)
        self.difficulty_label.pack(pady=(20, 10))

        self.difficulty_var = tk.StringVar(value="Medium")
        difficulties = ["Easy", "Medium", "Hard"]
        self.difficulty_menu = ttk.Combobox(self.root, 
                                          textvariable=self.difficulty_var,
                                          values=difficulties,
                                          state="readonly",
                                          font=FONT,
                                          width=10)
        self.difficulty_menu.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game,
                                      bg=BUTTON_BG, activebackground=BUTTON_HOVER_BG, fg=FONTCOLOR,
                                      relief=tk.FLAT, font=FONT)
        self.start_button.pack(pady=10)
        
        # Add hover effects for Start Game button
        self.start_button.bind("<Enter>", lambda e: self.start_button.configure(bg=BUTTON_HOVER_BG))
        self.start_button.bind("<Leave>", lambda e: self.start_button.configure(bg=BUTTON_BG))

        self.selected_size = None
        self.selected_difficulty = None

    def start_game(self):
        self.selected_size = self.size_var.get()
        self.selected_difficulty = self.difficulty_var.get()
        self.root.destroy()

    def run(self):
        self.root.mainloop()
        return self.selected_size, self.selected_difficulty

class GomokuGUI:
    def __init__(self, board_size, difficulty="Medium"):
        self.root = tk.Tk()
        self.root.title("Gomoku")
        
        self.root.configure(bg=BACKGROUND_COLOR)
        
        self.board_size = board_size
        self.difficulty = difficulty
        self.cell_size = 35
        self.margin = 40

        # Calculate window dimensions
        board_width = self.board_size  * self.cell_size
        board_height = self.board_size * self.cell_size 
        total_width = board_width + 6 * self.margin
        total_height = board_height + 3 * self.margin + 60
        
        # Set window size and position it on the left side
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x_position = 50
        y_position = (screen_height - total_height) // 2
        
        self.root.geometry(f"{total_width}x{total_height}+{x_position}+{y_position}")

        # Canvas for board
        self.canvas = tk.Canvas(self.root, 
                                width=board_width + 2 * self.margin,
                                height=board_height + 2 * self.margin,
                                bg=CANVAS_BG,
                                highlightthickness=0)
        self.canvas.pack(pady=(30, 20))

        # Button under canvas
        self.restart_button = tk.Button(self.root, text="New Game", command=self.restart_game,
                                        bg=BUTTON_BG, activebackground=BUTTON_HOVER_BG, fg=FONTCOLOR,
                                        relief=tk.FLAT, font=FONT)
        self.restart_button.pack(pady=(0, 10))
        
        # Add hover effects for New Game button
        self.restart_button.bind("<Enter>", lambda e: self.restart_button.configure(bg=BUTTON_HOVER_BG))
        self.restart_button.bind("<Leave>", lambda e: self.restart_button.configure(bg=BUTTON_BG))

        # Initialize game with difficulty
        self.game = GameRunner(size=self.board_size, difficulty=self.difficulty)
        self.game.restart(player_index=1)
        self.draw_board()
        self.canvas.bind('<Button-1>', self.handle_click)

    def restart_game(self):
        self.root.destroy()
        setup = SetupWindow()
        board_size, difficulty = setup.run()
        if board_size:
            gui = GomokuGUI(board_size, difficulty)
            gui.run()

    def draw_board(self):
        self.canvas.delete('all')
        for i in range(self.board_size):
            self.canvas.create_line(
                self.margin, self.margin + i * self.cell_size,
                self.board_size * self.cell_size + self.margin,
                self.margin + i * self.cell_size,
                fill=GRID_COLOR)

            self.canvas.create_line(
                self.margin + i * self.cell_size, self.margin,
                self.margin + i * self.cell_size,
                self.board_size * self.cell_size + self.margin,
                fill=GRID_COLOR)

        for i in range(self.board_size):
            for j in range(self.board_size):
                piece = self.game.state.values[i, j]
                if piece != 0:
                    x = self.margin + j * self.cell_size
                    y = self.margin + i * self.cell_size
                    color = BLACK_PIECE if piece == 1 else WHITE_PIECE
                    self.canvas.create_oval(x - 12, y - 12, x + 12, y + 12,
                                            fill=color, outline=GRID_COLOR)

    def handle_click(self, event):
        if self.game.finished:
            self.game.restart(player_index=1)
            self.draw_board()
            return

        board_x = round((event.x - self.margin) / self.cell_size)
        board_y = round((event.y - self.margin) / self.cell_size)

        if 0 <= board_x < self.board_size and 0 <= board_y < self.board_size:
            if self.game.play(board_y, board_x):
                self.draw_board()
                self.root.update()
                time.sleep(0.5)
                self.game.aiplay()
                self.draw_board()

                if self.game.finished:
                    winner = "Black" if self.game.state.winner == 1 else "White"
                    self.canvas.create_text(
                        self.board_size * self.cell_size // 2 + self.margin,
                        self.board_size * self.cell_size // 2 + self.margin,
                        text=f"{winner} wins! Click to restart",
                        fill="red",
                        font=("Helvetica", 16, "bold"))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    setup = SetupWindow()
    board_size, difficulty = setup.run()

    if board_size:
        gui = GomokuGUI(board_size, difficulty)
        gui.run()
