import nonogramboard as nb
from itertools import chain
from utils import *


def solve(board: nb.NonogramBoard) -> None:
    pass


def _full_pass(board: nb.NonogramBoard) -> None:
    rules = [0]
    for rule in rules:
        _pass(board, rule, 0)
        _pass(board, rule, 1)


def _pass(board: nb.NonogramBoard, rule: int, axis: int) -> None:
    for i in range(board.shape[axis]):
        if board.solved(i, axis):
            continue

        if rule == 0:
            _rule0(board, i, axis)


def _rule0(board: nb.NonogramBoard, index: int, axis: int) -> bool:
    """If a single hint `h` is the full length of line `l`, then
    the entire line must be filled.

    :return: True if the board has been updated, else False
    """
    # already handled
    if board.solved(index, axis):
        return False

    hint = board.hints(axis)[index]
    line = board.line(index, axis)

    # does rule apply?
    if sum(hint) + len(hint) - 1 != len(line):
        return False

    pattern = [[nb.State.YES] * h for h in hint]  # [[Y], [Y, Y]]
    pattern = list(chain(*intersperse(pattern, [nb.State.NO])))  # [Y, N, Y, Y]
    line.update(pattern)

    return True


def _rule1(board: nb.NonogramBoard, index: int, axis: int) -> bool:
    """

    :return: True if the board has been updated, else False
    """
    hint = board.hints(axis)[index]
    line = board.line(index, axis)

    # already handled
    if board.solved(index, axis):
        return False


if __name__ == '__main__':
    brd = nb.read_json('testboard.json')
    print(brd)
    _full_pass(brd)
    print(brd)
