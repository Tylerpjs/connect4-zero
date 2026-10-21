import numpy as np
import pytest

from connect4zero.game import (
    ROWS, COLS, new_board, legal_moves, apply_move,
    check_win, game_result, mirror, render, _has_run)


def play(cols):
    """Apply a sequence of column moves to a fresh board, alternating players."""
    board = new_board()
    for c in cols:
        board = apply_move(board, c)
    return board


def board_from_rows(rows):
    """Build a board from a list of 6 strings like '.......' using O=+1, X=-1."""
    symbols = {"O": 1, "X": -1, ".": 0}
    return np.array([[symbols[ch] for ch in row] for row in rows], dtype=np.int8)


# --- board basics -----------------------------------------------------------

def test_new_board_is_empty_and_right_shape():
    b = new_board()
    assert b.shape == (ROWS, COLS)
    assert not b.any()


def test_legal_moves_on_empty_board_is_every_column():
    assert legal_moves(new_board()) == list(range(COLS))


def test_legal_moves_excludes_full_column():
    b = play([0] * ROWS)
    assert 0 not in legal_moves(b)
    assert len(legal_moves(b)) == COLS - 1


# --- apply_move -------------------------------------------------------------

def test_apply_move_does_not_mutate_input():
    b = new_board()
    original = b.copy()
    apply_move(b, 3)
    assert np.array_equal(b, original)


def test_apply_move_raises_on_full_column():
    b = play([0] * ROWS)
    with pytest.raises(ValueError):
        apply_move(b, 0)


def test_apply_move_uses_gravity_and_flips_perspective():
    b = play([3])
    # The piece lands on the bottom row and, after the flip, belongs to -1.
    assert b[ROWS - 1, 3] == -1
    assert b.sum() == -1
    b = play([3, 3])
    # Second piece stacks on top; after two flips the first piece is +1 again.
    assert b[ROWS - 1, 3] == 1
    assert b[ROWS - 2, 3] == -1


# --- _has_run ---------------------------------------------------------------

def test_has_run_basic_cases():
    assert _has_run(np.array([1, 1, 1, 1]), 1)
    assert _has_run(np.array([0, 1, 1, 1, 1, 0]), 1)
    assert not _has_run(np.array([1, 1, 1, 0, 1]), 1)
    assert not _has_run(np.array([1, 1, 1]), 1)
    assert not _has_run(np.array([]), 1)


# --- check_win --------------------------------------------------------------

def test_horizontal_win_bottom_row():
    b = board_from_rows([
        ".......",
        ".......",
        ".......",
        ".......",
        ".......",
        "XXXX...",
    ])
    assert check_win(b, -1)
    assert not check_win(b, 1)


def test_vertical_win():
    b = board_from_rows([
        ".......",
        ".......",
        "...X...",
        "...X...",
        "...X...",
        "...X...",
    ])
    assert check_win(b, -1)
    assert not check_win(b, 1)


def test_diagonal_win_rising():
    b = board_from_rows([
        ".......",
        ".......",
        "...X...",
        "..X....",
        ".X.....",
        "X......",
    ])
    assert check_win(b, -1)


def test_diagonal_win_falling():
    b = board_from_rows([
        ".......",
        ".......",
        "O......",
        ".O.....",
        "..O....",
        "...O...",
    ])
    assert check_win(b, 1)
    assert not check_win(b, -1)


def test_win_in_top_right_corner():
    b = board_from_rows([
        "...OOOO",
        ".......",
        ".......",
        ".......",
        ".......",
        ".......",
    ])
    assert check_win(b, 1)


def test_three_in_a_row_is_not_a_win():
    b = board_from_rows([
        ".......",
        ".......",
        ".......",
        ".......",
        ".......",
        "XXX....",
    ])
    assert not check_win(b, -1)


def test_four_with_a_gap_is_not_a_win():
    b = board_from_rows([
        ".......",
        ".......",
        ".......",
        ".......",
        ".......",
        "XXX.X..",
    ])
    assert not check_win(b, -1)


def test_alternating_line_is_not_a_win():
    b = board_from_rows([
        ".......",
        ".......",
        ".......",
        ".......",
        ".......",
        "XOXOXOX",
    ])
    assert not check_win(b, -1)
    assert not check_win(b, 1)


# --- game_result ------------------------------------------------------------

def test_game_result_none_mid_game():
    assert game_result(play([3, 3, 4])) is None


def test_game_result_detects_win_after_real_moves():
    # O plays 0,1,2,3 ; X plays 6 each time. After O's 4th move the board is
    # flipped, so the winner is -1 from the player-to-move's perspective.
    b = play([0, 6, 1, 6, 2, 6, 3])
    assert game_result(b) == -1


def test_game_result_draw_on_full_board():
    b = board_from_rows([
        "OOXXOOX",
        "XXOOXXO",
        "OOXXOOX",
        "XXOOXXO",
        "OOXXOOX",
        "XXOOXXO",
    ])
    assert not check_win(b, 1)
    assert not check_win(b, -1)
    assert legal_moves(b) == []
    assert game_result(b) == 0


# --- mirror / render --------------------------------------------------------

def test_mirror_flips_columns():
    b = play([0])
    m = mirror(b)
    assert m[ROWS - 1, COLS - 1] == -1
    assert m[ROWS - 1, 0] == 0
    assert np.array_equal(mirror(m), b)


def test_render_one_move():
    expected = "\n".join([". . . . . . ."] * (ROWS - 1) + [". . . X . . ."])
    assert render(play([3])) == expected