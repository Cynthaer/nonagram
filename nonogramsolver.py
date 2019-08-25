from nonogramboard import State, NonogramBoard
from utils import *


class NonogramSolver:
    board: NonogramBoard

    def __init__(self, board: NonogramBoard):
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
            if rule == 0:
                self._rule0(i, axis)

    def _apply_rule(self, rule: str, index: int, axis: int):
        """Applies the indicated rule to the indicated line on the board.

        :param rule: the rule to apply
        :param index: the index of the line
        :param axis: 0 = rows, 1 = columns
        :return: True if the board has been updated, else False

        Rules
        =====
        *Rule 1:* If the hint covers the entire line, solve the line.
        """

        if self.board.solved(index, axis):
            return False

        hint = self.board.hints[axis][index]
        line = self.board.line(index, axis)

        if rule == 'full_hint':
            if sum(hint) + len(hint) - 1 != len(line):
                # doesn't apply
                return False

            pattern = [[State.YES] * h for h in hint]  # [[Y], [Y, Y]]
            line[:] = flatten(intersperse(pattern, [State.NO]))  # [Y, N, Y, Y]
            return True
        elif rule == 'extend edge':
            pass
        else:
            raise ValueError(f"'{rule}' is not a valid rule.")

        return False


if __name__ == '__main__':
    brd = nb.read_json('tests/testboard.json')

