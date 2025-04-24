import tkinter as tk
from game import GameRunner

class GomokuGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gomoku")
        
        self.board_size = 19
        self.cell_size = 30
        self.margin = 20
        
        self.canvas = tk.Canvas(self.root, 
                               width=self.board_size * self.cell_size + 2 * self.margin,
                               height=self.board_size * self.cell_size + 2 * self.margin,
                               bg='white')
        self.canvas.pack()
        
        # Initialize game with player as black (1)
        self.game = GameRunner(size=self.board_size)
        self.game.restart(player_index=1)  # 1 for black
        self.draw_board()
        self.canvas.bind('<Button-1>', self.handle_click)
        
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
    gui = GomokuGUI()
    gui.run() 