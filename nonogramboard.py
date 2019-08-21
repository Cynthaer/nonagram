import json
import numpy as np
from enum import Enum
from typing import List, Dict, Tuple, Iterable
from itertools import groupby


class State(Enum):
    BLANK = 0
    YES = 1
    NO = 2


class NonogramTile:
    state: State

    def __init__(self, state: State = State.BLANK) -> None:
        self.state = state

    def __repr__(self) -> str:
        return 'NonagramTile(state={})'.format(self.state)

    def __str__(self) -> str:
        return str(self.state.name)

    def __eq__(self, other: object) -> bool:
        return self.state == other.state

    def show(self) -> str:
        if self.state == State.BLANK:
            return 'O'
        elif self.state == State.YES:
            return '■'
        elif self.state == State.NO:
            return '∙'

    def copy(self) -> "NonogramTile":
        return NonogramTile(self.state)


class NonogramLine(list):
    def update(self, values: Iterable[State]) -> None:
        it = iter(self)
        for v in values:
            # if type(v) != State:
            #     raise TypeError('Expected State, got {}'.format(type(v)))

            next(it).state = v

    def rle(self) -> List[Tuple[State, List[NonogramTile]]]:
        """Run-length encoding"""
        return [(k.state, list(g)) for k, g in groupby(self)]


class NonogramBoard:
    _row_hints: List[List[int]]
    _col_hints: List[List[int]]
    tiles: np.ndarray[State]

    def __init__(self, hints: Dict[str, List[List[int]]]) -> None:
        self._row_hints = hints['rows']
        self._col_hints = hints['cols']

        self.tiles = np.asarray([[State.BLANK for _ in range(self.shape[1])]
                                 for _ in range(self.shape[0])])

        if not self._isvalid():
            raise Exception('Invalid hint configuration')

    def __getitem__(self, key: int) -> List[NonogramTile]:
        return self.tiles[key]

    def __repr__(self) -> str:
        return repr(self.tiles)

    def __str__(self) -> str:
        r_hints = _justify_hints(self._row_hints)
        # c_hints are horizontal for ease of display
        c_hints = _transpose(_justify_hints(self._col_hints))

        hor_pad = len(r_hints[0]) * 2

        output = ''
        for i in range(len(c_hints)):
            output += '{pad}{hints}\n'.format(pad=' ' * hor_pad,
                                              hints=' '.join(c_hints[i]))

        output += '{pad}{line}\n'.format(pad=' ' * hor_pad,
                                         line='-' * (len(c_hints[0]) * 2 - 1))

        for i in range(len(r_hints)):
            output += '{hints}|{tiles}\n'.format(hints=' '.join(r_hints[i]),
                                                 tiles=' '.join([x.show() for x in self.tiles[i]]))

        return output

    @property
    def shape(self) -> Tuple[int, int]:
        """:return: (height, width)"""
        return len(self._row_hints), len(self._col_hints)

    def hints(self, axis: int) -> List[List[int]]:
        if axis == 0:
            return self._row_hints
        elif axis == 1:
            return self._col_hints

    def line(self, index: int, axis: int) -> NonogramLine:
        if axis == 0:
            return NonogramLine(self.tiles[index])
        elif axis == 1:
            return NonogramLine([r[index] for r in self.tiles])

    def solved(self, index: int = None, axis: int = None) -> bool:
        """
        Check if board or line is solved.

        If `index` is provided, only check the row/column according to the `axis`
        value. If `index` is `None` (default), check the entire board.

        :param index: row or column index (optional)
        :param axis: 0 = row, 1 = column (optional)
        :return: True if board or line is fully solved, else False
        """
        if index is not None:
            return self._line_solved(index, axis)

        for r in range(self.shape[0]):
            if not self._line_solved(r, 0):
                return False

        for c in range(self.shape[1]):
            if not self._line_solved(c, 1):
                return False

        return True

    def _line_solved(self, index: int, axis: int):
        hint = self.hints(axis)[index]
        line = self.line(index, axis)
        line_state = ([len(list(g))
                      for k, g in groupby(line, lambda x: x.state)
                      if k == State.YES])

        return line_state == hint

    def _isvalid(self) -> bool:
        # row hints
        for hint in self.hints(0):
            if sum(hint) + len(hint) - 1 > self.shape[1]:
                return False

        # col hints
        for hint in self.hints(1):
            if sum(hint) + len(hint) - 1 > self.shape[0]:
                return False

        return True


def read_json(path: str) -> NonogramBoard:
    with open(path) as f:
        d = json.load(f)
        return NonogramBoard(d)


def _pad_list(l: List, length: int, value: object = None) -> List:
    x = l.copy()
    while len(x) < length:
        x.insert(0, value)
    return x


def _justify_hints(hints: List[List[int]]) -> List[List[str]]:
    max_len = max(map(len, hints))
    return [list(map(str, _pad_list(l, max_len, ' '))) for l in hints]


def _transpose(ls: List[List]) -> List[List]:
    return list(map(list, zip(*ls)))


if __name__ == '__main__':
    board = read_json('testboard.json')
    board[0][0].state = State.YES
    board[0][1].state = State.NO
    print(board)

    nl = board.line(1, 0)
    print('line: {}'.format(nl))
    print(nl.rle())
