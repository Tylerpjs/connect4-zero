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


def test_new_board_is_empty_and_right_shape():
    b = new_board()
    assert b.shape == (ROWS, COLS)
    assert not b.any()


def test_apply_move_does_not_mutate_input():
    b = new_board()
    original = b.copy()
    apply_move(b, 3)
    assert np.array_equal(b, original)


def test_apply_move_raises_on_full_column():
    b = play([0] * ROWS)
    with pytest.raises(ValueError):
        apply_move(b, 0)


def test_has_run_basic_cases():
    assert _has_run(np.array([1, 1, 1, 1]), 1)
    assert _has_run(np.array([0, 1, 1, 1, 1, 0]), 1)
    assert not _has_run(np.array([1, 1, 1, 0, 1]), 1)
    assert not _has_run(np.array([1, 1, 1]), 1)


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


def test_game_result_detects_win_after_real_moves():
    # O plays 0,1,2,3 ; X plays 6 each time. After O's 4th move the board is
    # flipped, so the winner is -1 from the player-to-move's perspective.
    b = play([0, 6, 1, 6, 2, 6, 3])
    assert game_result(b) == -1