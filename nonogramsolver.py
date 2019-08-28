from nonogramboard import State, NonogramBoard, read_json
from utils import *


class NonogramSolver:
    board: NonogramBoard
    verbosity: int

    def __init__(self, board: NonogramBoard, verbosity: int = 0):
        self.board = board
        self.verbosity = verbosity

    def solve(self) -> None:
        while not self.board.solved():
            if not self._full_pass():
                if self.verbosity > 0:
                    print('Cannot solve board.')
                break

    def _full_pass(self, rule: int = None) -> bool:
        rules = [self._zero_hint, self._full_hint, self._extend_edge]

        if rule is None:
            for i in range(len(rules)):
                if self._full_pass(i):
                    return True
            return False

        for axis in range(2):
            for l in range(self.board.shape[axis]):
                if rules[rule](l, axis):
                    return True

        return False

    def _zero_hint(self, index: int, axis: int) -> bool:
        """ If hint is 0, entire line must be blank.

        :param index: the index of the line
        :param axis: 0 = rows, 1 = columns
        :return: True if the board has been updated, else False
        """
        if self.board.solved(index, axis):
            return False

        hint = self.board.hints[axis][index]
        line = self.board.line(index, axis)

        if hint[0] != 0:
            return False

        line[:] = State.NO
        if self.verbosity > 0:
            print(self.board)
        return True

    def _full_hint(self, index: int, axis: int) -> bool:
        """
        :param index: the index of the line
        :param axis: 0 = rows, 1 = columns
        :return: True if the board has been updated, else False
        """
        if self.board.solved(index, axis):
            return False

        hint = self.board.hints[axis][index]
        line = self.board.line(index, axis)

        if sum(hint) + len(hint) - 1 != len(line):
            # doesn't apply
            return False

        pattern = [[State.YES] * h for h in hint]  # [[Y], [Y, Y]]
        line[:] = flatten(intersperse(pattern, [State.NO]))  # [Y, N, Y, Y]
        if self.verbosity > 0:
            print(self.board)
        return True

    def _extend_edge(self, index: int, axis: int) -> bool:
        """
        If filled box is flush with an edge (including NOs), complete that block.

        :param index: the index of the line
        :param axis: 0 = rows, 1 = columns
        :return: True if the board has been updated, else False
        """
        if self.board.solved(index, axis):
            return False

        hint = self.board.hints[axis][index]
        line = self.board.line(index, axis)

        # avoid strange behavior for 0 hints
        if hint[0] == 0:
            return False

        def update_line(ln: np.ndarray, hnt: List[int]):
            rle = run_length_encode(ln)

            # clip the leading NOs
            if ln[0] == State.NO:
                ln = ln[rle[0]['length']:]
                rle = run_length_encode(ln)

            if (rle[0]['state'] == State.YES
                    and rle[0]['length'] <= hnt[0]
                    and rle[1]['state'] == State.BLANK):

                fill_sequence = ([State.YES] * hnt[0])

                # cap off with a NO if sequence doesn't hit the edge
                if len(fill_sequence) < len(ln):
                    fill_sequence += [State.NO]

                ln[:len(fill_sequence)] = fill_sequence
                if self.verbosity > 0:
                    print(self.board)
                return True
            return False

        # forward or backward, but only one
        return update_line(line, hint) or update_line(line[::-1], hint[::-1])


def _changed(old: np.ndarray, new: np.ndarray):
    return np.any(old != new)


if __name__ == '__main__':
    brd = read_json('testboard.json')
    solver = NonogramSolver(brd, 1)
    print(brd)
    solver.solve()
