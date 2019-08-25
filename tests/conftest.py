import pytest
import nonogramboard as nb


@pytest.fixture
def blank_board():
    return nb.NonogramBoard([[3, 1], [1, 3], [2], [3], [1]],
                            [[2], [1], [2, 1], [3], [5]])


@pytest.fixture
def solved_board():
    return nb.NonogramBoard([[3, 1], [1, 3], [2], [3], [1]],
                            [[2], [1], [2, 1], [3], [5]],
                            nb.as_states(
                                [[1, 1, 1, 2, 1],
                                 [1, 2, 1, 1, 1],
                                 [0, 0, 0, 1, 1],
                                 [0, 2, 1, 1, 1],
                                 [0, 0, 0, 0, 1]]
                            ))


@pytest.fixture
def in_progress_board():
    return nb.NonogramBoard([[3, 1], [1, 3], [2], [3], [1]],
                            [[2], [1], [2, 1], [3], [5]],
                            nb.as_states(
                                [[1, 1, 1, 2, 1],
                                 [1, 2, 1, 1, 1],
                                 [0, 0, 0, 0, 1],
                                 [0, 2, 0, 0, 1],
                                 [0, 0, 0, 0, 1]]
                            ))
