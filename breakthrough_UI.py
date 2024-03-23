import tkinter as tk

BOARD_SIZE = 8
# Initialize the game board
def init_board():
    board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    for i in range(2):
        for j in range(BOARD_SIZE):
            board[i][j] = 2  # Black pieces
            board[BOARD_SIZE - 1 - i][j] = 1  # White pieces
    return board

class BreakthroughGUI:
    def __init__(self, master):
        self.master = master
        self.board = init_board()
        self.players = [None, "Human", "Human"]  # Default to human vs. human
        self.current_player = 1  # White starts
        self.selected_piece = None  # No piece is selected initially
        self.move_history = []  # Track history of moves and captures
        self.create_widgets()
    
    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.handle_click)
        # Bind 'z' to undo_move on the master window
        self.master.bind("z", self.undo_move)


    def draw_board(self):
        self.canvas.delete("all")
        tile_size = 400 // BOARD_SIZE
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                color = "white" if (i + j) % 2 == 0 else "gray"
                self.canvas.create_rectangle(j*tile_size, i*tile_size, j*tile_size+tile_size, i*tile_size+tile_size, fill=color)
                if self.board[i][j] == 1:
                    self.canvas.create_oval(j*tile_size+10, i*tile_size+10, j*tile_size+40, i*tile_size+40, fill="white")
                elif self.board[i][j] == 2:
                    self.canvas.create_oval(j*tile_size+10, i*tile_size+10, j*tile_size+40, i*tile_size+40, fill="black")

    def handle_click(self, event):
        print("Clicked at", event.x, event.y)
        col = event.x // (400 // BOARD_SIZE)
        row = event.y // (400 // BOARD_SIZE)
        if self.selected_piece:
            print("Moving from", self.selected_piece, "to", (row, col))
            self.try_move(self.selected_piece, (row, col))
            self.selected_piece = None
        else:
            print("Selecting", (row, col))
            if self.board[row][col] == self.current_player:
                self.selected_piece = (row, col)
    
    def try_move(self, from_pos, to_pos):
        if self.validate_move(from_pos, to_pos):
            self.execute_move(from_pos, to_pos)
            if self.check_game_over():
                tk.messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_game()
            else:
                self.switch_player()
            self.draw_board()

    def undo_move(self, event=None):  # `event=None` allows it to be called as a callback without arguments
        if self.move_history:
            from_pos, to_pos, moving_piece, captured_piece = self.move_history.pop()
            self.board[from_pos[0]][from_pos[1]] = moving_piece
            self.board[to_pos[0]][to_pos[1]] = captured_piece  # Restore the captured piece, if any
            self.switch_player()
            self.draw_board()


    def validate_move(self, from_pos, to_pos):
        row_from, col_from = from_pos
        row_to, col_to = to_pos
        if row_to < 0 or row_to >= BOARD_SIZE or col_to < 0 or col_to >= BOARD_SIZE:
            print("Move is out of bounds")
            return False  # Move is out of bounds
        if abs(col_from - col_to) > 1 or abs(row_from - row_to) > 1:
            print("Move is too far")
            return False  # Move is too far
        if self.board[row_to][col_to] == self.current_player:
            print("Cannot capture own piece")
            return False  # Cannot capture own piece
        if self.current_player == 1 and row_to >= row_from:
            print("White must move upwards")
            return False  # Corrected: White must move upwards
        if self.current_player == 2 and row_to <= row_from:
            print("Black must move downwards")
            return False  # Corrected: Black must move downwards
        print("Valid move")
        return True


    def execute_move(self, from_pos, to_pos):
        row_from, col_from = from_pos
        row_to, col_to = to_pos
        captured_piece = self.board[row_to][col_to]  # Save the captured piece, if any
        moving_piece = self.board[row_from][col_from]
        # Record the move with details
        self.move_history.append((from_pos, to_pos, moving_piece, captured_piece))
        # Execute the move
        self.board[row_to][col_to] = moving_piece
        self.board[row_from][col_from] = 0


    def check_game_over(self):
        # Check if any white piece has reached the top row, indicating a win for white.
        for col in range(BOARD_SIZE):
            if self.board[0][col] == 1:  # White reaches the top
                print("Game over: White reaches the top row.")
                return True
                
        # Check if any black piece has reached the bottom row, indicating a win for black.
        for col in range(BOARD_SIZE):
            if self.board[BOARD_SIZE-1][col] == 2:  # Black reaches the bottom
                print("Game over: Black reaches the bottom row.")
                return True

        return False



    def switch_player(self):
        self.current_player = 3 - self.current_player
    
    def reset_game(self):
        self.board = init_board()
        self.current_player = 1 # White starts
        self.selected_piece = None
        self.draw_board()
# Make sure the BreakthroughGUI class is defined here or imported if it's defined in another file

def main():
    root = tk.Tk()
    root.title("Breakthrough Game")
    
    # Create an instance of your game's GUI class. This should set up the game board and UI.
    bg = BreakthroughGUI(root)
    
    # Start the Tkinter event loop. This will keep your application running and responsive to user interactions.
    root.mainloop()

if __name__ == "__main__":
    main()


