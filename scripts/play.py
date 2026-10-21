"""Play Connect Four in the terminal: two humans, O moves first.

    python scripts/play.py
"""

from connect4zero.game import COLS, new_board, legal_moves, apply_move, game_result, render

SYMBOLS = {1: "O", -1: "X"}
COLUMN_LABELS = " ".join(str(c) for c in range(COLS))

def display(board, to_move):
    """Print the board with O always drawn as O, regardless of whose turn it is.

    `board` is from the player-to-move's perspective (+1 = to_move). Multiplying
    by `to_move` maps it back to absolute colors: +1 = O, -1 = X.
    """
    print()
    print(render(board * to_move))
    print(COLUMN_LABELS)
    print()


def ask_for_column(board, to_move):
    """Prompt until the player enters a legal column; return it as an int."""
    legal = legal_moves(board)
    while True:
        raw = input(f"Player {SYMBOLS[to_move]}, choose a column {legal}: ").strip()
        if raw.lower() in ("q", "quit"):
            raise SystemExit("Game abandoned.")
        if not raw.isdigit():
            print("Please enter a number.")
            continue
        col = int(raw)
        if col not in legal:
            print(f"Column {col} is not available.")
            continue
        return col

def main():
    board = new_board()
    to_move = 1  # absolute color of the player about to move: +1 = O, -1 = X

    while True:
        display(board, to_move)
        col = ask_for_column(board, to_move)
        board = apply_move(board, col)

        result = game_result(board)
        if result == -1:
            display(board, -to_move)
            print(f"Player {SYMBOLS[to_move]} wins!")
            return
        if result == 0:
            display(board, -to_move)
            print("Draw.")
            return

        to_move = -to_move


if __name__ == "__main__":
    main()