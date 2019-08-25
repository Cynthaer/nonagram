import nonogramboard as nb
from itertools import chain
from utils import *


class NonogramSolver:
    board: nb.NonogramBoard

    def __init__(self, board: nb.NonogramBoard):
        self.board = board

    def solve(self) -> None:
        pass

    def _full_pass(self) -> None:
        rules = [0]
        for rule in rules:
            self._pass(rule, 0)
            self._pass(rule, 1)

    def _pass(self, rule: int, axis: int) -> None:
        for i in range(self.board.shape[axis]):
            if self.board.solved(i, axis):
                continue

            if rule == 0:
                self._rule0(i, axis)

    def _rule0(self, index: int, axis: int) -> bool:
        """If a single hint `h` is the full length of line `l`, then
        the entire line must be filled.

        :return: True if the board has been updated, else False
        """
        # already handled
        if self.board.solved(index, axis):
            return False

        hint = self.board.hints[axis][index]
        line = self.board.line(index, axis)

        # does rule apply?
        if sum(hint) + len(hint) - 1 != len(line):
            return False

        pattern = [[nb.State.YES] * h for h in hint]  # [[Y], [Y, Y]]
        line[:] = flatten(*intersperse(pattern, [nb.State.NO]))  # [Y, N, Y, Y]
        return True

    def _rule1(self, index: int, axis: int) -> bool:
        """

        :return: True if the board has been updated, else False
        """
        hint = self.board.hints[axis][index]
        line = self.board.line(index, axis)

        # already handled
        if self.board.solved(index, axis):
            return False


if __name__ == '__main__':
    brd = nb.read_json('tests/testboard.json')

