import pytest

import nonogramboard as nb


@pytest.fixture
def blank_board():
    return nb.NonogramBoard([[3, 1], [1, 3], [2], [3], [1]],
                            [[2], [1], [2, 1], [3], [5]])


@pytest.fixture
def in_progress_board():
    return nb.NonogramBoard([[3, 1], [1, 3], [2], [3], [1]],
                            [[2], [1], [2, 1], [3], [5]],
                            [[1, 1, 1, 2, 1],
                             [0, 2, 1, 1, 1],
                             [0, 0, 0, 0, 1],
                             [0, 2, 0, 0, 1],
                             [0, 0, 0, 0, 1]])


@pytest.fixture
def solved_board():
    return nb.NonogramBoard([[3, 1], [1, 3], [2], [3], [1]],
                            [[2], [1], [2, 1], [3], [5]],
                            [[1, 1, 1, 2, 1],
                             [1, 2, 1, 1, 1],
                             [2, 2, 2, 1, 1],
                             [2, 2, 1, 1, 1],
                             [2, 2, 2, 2, 1]])


@pytest.fixture
def blank_board_with_zero():
    return nb.NonogramBoard([[3], [2], [0]],
                            [[2], [2], [1]])


@pytest.fixture
def in_progress_board_with_edges():
    return nb.NonogramBoard([[2], [2], [3], [1, 2], [4], [4]],
                            [[1, 4], [1, 1, 2], [5], [1, 3]],
                            [[1, 0, 0, 0],
                             [2, 2, 1, 0],
                             [0, 0, 1, 2],
                             [0, 0, 0, 1],
                             [1, 0, 0, 0],
                             [0, 0, 0, 1]])
