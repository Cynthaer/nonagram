import pytest
import numpy as np
import nonogramboard as nb
import nonogramsolver as ns
from utils import intersperse


def test_intersperse():
    assert intersperse([1, 2, 3], 0) == [1, 0, 2, 0, 3]


class TestNonogramBoard:
    @pytest.fixture
    def blank_board(self):
        return nb.NonogramBoard([[1], [3]], [[2], [1], [1]])

    @pytest.fixture
    def solved_board(self):
        return nb.NonogramBoard([[1], [3]], [[2], [1], [1]],
                                [[nb.State.YES, nb.State.NO, nb.State.BLANK],
                                 [nb.State.YES, nb.State.YES, nb.State.YES]])

    @pytest.fixture
    def in_progress_board(self):
        return nb.NonogramBoard([[1], [3]], [[2], [1], [1]],
                                [[nb.State.YES, nb.State.NO, nb.State.BLANK],
                                 [nb.State.YES, nb.State.BLANK, nb.State.YES]])

    def test_shape(self, blank_board):
        assert blank_board.shape == (2, 3)

    def test_get_and_set_line(self, blank_board):
        blank_board.line(0, 0)[:] = [nb.State.YES, nb.State.NO, nb.State.NO]
        assert blank_board.tiles[0,0] == nb.State.YES
        assert blank_board.tiles[0,1:].tolist() == [nb.State.NO, nb.State.NO]

    def test_invalid_hints_fail(self):
        with pytest.raises(Exception):
            nb.NonogramBoard([[1]], [[2]])

    def test_invalid_tile_shape_fails(self):
        with pytest.raises(Exception):
            nb.NonogramBoard([[1]], [[1]], [[nb.State.BLANK, nb.State.BLANK]])

    def test_identify_solved_lines(self, in_progress_board):
        board = in_progress_board
        assert board.solved(0, 0)
        assert not board.solved(1, 0)
        assert board.solved(0, 1)
        assert not board.solved(1, 1)
        assert board.solved(2, 1)

    def test_identify_solved_board(self, blank_board, in_progress_board, solved_board):
        assert not blank_board.solved()
        assert not in_progress_board.solved()
        assert solved_board.solved()


class TestNonogramSolver:
    pass
