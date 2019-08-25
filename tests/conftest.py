import pytest
import nonogramboard as nb


@pytest.fixture
def blank_board():
    return nb.NonogramBoard([[1], [3]], [[2], [1], [1]])


@pytest.fixture
def solved_board():
    return nb.NonogramBoard([[1], [3]], [[2], [1], [1]],
                            [[nb.State.YES, nb.State.NO, nb.State.BLANK],
                             [nb.State.YES, nb.State.YES, nb.State.YES]])


@pytest.fixture
def in_progress_board():
    return nb.NonogramBoard([[1], [3]], [[2], [1], [1]],
                            [[nb.State.YES, nb.State.NO, nb.State.BLANK],
                             [nb.State.YES, nb.State.BLANK, nb.State.YES]])
