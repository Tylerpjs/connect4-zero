import numpy as np
### Connect 4 Game Package

ROWS = 6
COLS = 7
CONNECT = 4

#For convention of the game the top of the board is row 0 with the bottom being row index -1


#Creates a array filled with zeros that matches the size set from the ROWS and COLS variables
def new_board() -> np.ndarray:
    """Creates a new "board" (np matrix array) with the specificed rows and cols by the ROWS & COLS variables"""
    arr = np.zeros((ROWS,COLS),dtype=np.int8)
    return arr


#Returns a list of allowed columns to play
def legal_moves(board) -> list:
    """Returns a list of the legal moves allowed to be made by checking if the columns have available space"""
    legal_moves = []
    for i,var in enumerate(board[0]):
        if var == 0:
            legal_moves.append(i)
        None
    return legal_moves


#Applies a move to the board utilizing 'gravity' to fill the bottom most spot in the column
def apply_move(board,col) -> np.ndarray:
    """Applies a move to the board based on a target col, uses the bottom most spot available"""
    if board[0,col] != 0:
        raise ValueError("Move cannot be made in this column, column does not equal 0 in index 0")

    board = board.copy()
    
    for i in range(len(board) -1,-1,-1): 
        if board[i,col] == 0:
            board[i,col] = 1
            break
        else:
            None
    board = board * -1
    return board

def _has_run(line,player) -> bool:
    """Checks for a given line and player if there is a line of winning connects by the CONNECT variables length"""
    n = len(line)
    for start in range(n - CONNECT + 1):
        if np.all(line[start:start + CONNECT] == player):
            return True
    return False


def _all_lines(board):
    """Returns all available "lines" for a given board"""
    for r in range(ROWS):
        yield board[r, :]
    for c in range(COLS):
        yield board[:, c]
    for b in (board, np.fliplr(board)):            
        for k in range(-(ROWS - 1), COLS):         
            diag = np.diag(b, k)
            if len(diag) >= CONNECT:
                yield diag

def check_win(board, player) -> bool:
    """Checks for the win condition using the _all_lines function to pull the lines and the _has_run function to check for the win"""
    return any(_has_run(line, player) for line in _all_lines(board))

def game_result(board):
    if check_win(board,-1):
        return -1
    elif 0 not in board[0]:
        return 0
    return None

def mirror(board) -> np.ndarray:
    board = np.fliplr(board)
    return board


def render(board) -> str:
    """Return a human-readable drawing of the board, row 0 (top) first."""
    symbols = {1: "O", -1: "X", 0: "."}
    rows = []
    for r in range(ROWS):
        rows.append(" ".join(symbols[int(v)] for v in board[r]))
    return "\n".join(rows)


        
                