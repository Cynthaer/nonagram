import pytest
import numpy as np
from typing import List
from nonogramboard import State, NonogramBoard
from utils import intersperse


def test_intersperse():
    assert intersperse([1, 2, 3], 0) == [1, 0, 2, 0, 3]


def test_read_json(tmpfile):
    pass


class TestNonogramBoard:
    @pytest.fixture
    def board(self):
        return NonogramBoard({
            "rows": [[1], [3]],
            "cols": [[2], [1], [1]]
        })

    def test_shape(self, board):
        assert board.shape == (2, 3)

    def test_get_and_set_line(self, board):
        board[0,:] = [State.YES, State.NO, State.NO]
        assert board[0,0] == State.YES
        assert board[0,1:].tolist() == [State.NO, State.NO]
