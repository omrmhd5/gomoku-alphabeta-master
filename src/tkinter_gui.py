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
FONT = ("Times New Roman", 12)
FONTCOLOR = "white"

class SetupWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gomoku Setup")
        self.root.geometry("400x210")
        self.root.configure(bg=BACKGROUND_COLOR)
        self.root.eval('tk::PlaceWindow . center')

        self.label = tk.Label(self.root, text="Select Board Size (9-19):", bg=BACKGROUND_COLOR, font=("Times New Roman", 15, "bold"), fg=FONTCOLOR)
        self.label.pack(pady=(30, 10))

        self.size_var = tk.IntVar(value=15)
        self.spinbox = ttk.Spinbox(self.root, from_=9, to=19, textvariable=self.size_var, width=5, font=FONT, justify='center')
        self.spinbox.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game,
                                      bg=BUTTON_BG, activebackground=BUTTON_ACTIVE_BG, fg=FONTCOLOR,
                                      relief=tk.FLAT, font=FONT)
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
        
        self.root.configure(bg=BACKGROUND_COLOR)
        

        self.board_size = board_size
        self.cell_size = 30
        self.margin = 20

        total_width = self.board_size * self.cell_size + 2 * self.margin
        total_height = self.board_size * self.cell_size + 2 * self.margin + 50
        self.root.geometry(f"{total_width+20}x{total_height}")

        # Canvas for board
        self.canvas = tk.Canvas(self.root, 
                                width=total_width,
                                height=self.board_size * self.cell_size + 2 * self.margin,
                                bg=CANVAS_BG,
                                highlightthickness=0)
        self.canvas.pack(pady=(10, 5))

        # Button under canvas
        self.restart_button = tk.Button(self.root, text="New Game", command=self.restart_game,
                                        bg=BUTTON_BG, activebackground=BUTTON_ACTIVE_BG , fg=FONTCOLOR,
                                        relief=tk.FLAT, font=FONT)
        self.restart_button.pack(pady=(0, 10))

        # Initialize game
        self.game = GameRunner(size=self.board_size)
        self.game.restart(player_index=1)
        self.draw_board()
        self.canvas.bind('<Button-1>', self.handle_click)

    def restart_game(self):
        self.root.destroy()
        setup = SetupWindow()
        board_size = setup.run()
        if board_size:
            gui = GomokuGUI(board_size)
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
    board_size = setup.run()

    if board_size:
        gui = GomokuGUI(board_size)
        gui.run()
