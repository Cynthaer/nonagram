import json
from builtins import hasattr

import numpy as np
from enum import Enum
from typing import List, Dict, Tuple, Union, MutableSequence, Iterable, Any
from itertools import groupby


Hint = Iterable[int]


class State(Enum):
    BLANK = 0
    YES = 1
    NO = 2


class NonogramBoard:
    _row_hints: List[List[int]]
    _col_hints: List[List[int]]
    tiles: np.ndarray

    def __init__(self, row_hints: Iterable[Hint], col_hints: Iterable[Hint]) -> None:
        self._row_hints = [list(rh) for rh in row_hints]
        self._col_hints = [list(ch) for ch in col_hints]
        self.tiles = np.asarray([[State.BLANK] * len(self._col_hints)] * self.shape[0])

        if not self._isvalid():
            raise Exception('Invalid hint configuration')

    def __getitem__(self, key: Any) -> Union[np.ndarray, State]:
        return self.tiles[key]

    def __setitem__(self, key: Any, value) -> None:
        self.tiles[key] = value

    def __repr__(self) -> str:
        return repr(self.tiles)

    def __str__(self) -> str:
        r_hints = _justify_hints(self._row_hints)
        # c_hints are horizontal for ease of display
        c_hints = _transpose(_justify_hints(self._col_hints))

        hor_pad = len(r_hints[0]) * 2

        output = ''
        for c_h in c_hints:
            output += f"{' ' * hor_pad}{' '.join(c_h)}\n"

        output += f"{' ' * hor_pad}{'-' * (self.shape[1] * 2 - 1)}\n"

        for i in range(len(r_hints)):
            output += '{hints}|{tiles}\n'.format(hints=' '.join(r_hints[i]),
                                                 tiles=' '.join([str(x.value) for x in self.tiles[i]]))

        return output

    @property
    def shape(self) -> Tuple[int, int]:
        """:return: (height, width)"""
        if hasattr(self, 'tiles'):
            return self.tiles.shape
        return len(self._row_hints), len(self._col_hints)

    def hints(self, axis: int) -> List[List[int]]:
        if axis == 0:
            return self._row_hints
        elif axis == 1:
            return self._col_hints

    def line(self, index: int, axis: int) -> np.ndarray:
        if axis == 0:
            return self.tiles[index]
        elif axis == 1:
            return self.tiles[:,index]

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
        line_state = [len(list(g)) for k, g in groupby(line) if k == State.YES]
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
        return NonogramBoard(**d)


def _justify_hints(hints: List[List[int]]) -> List[List[str]]:
    max_len = max(map(len, hints))
    return [list(map(str, _left_padded(l, max_len, ' '))) for l in hints]


def _left_padded(l: List, length: int, value: object = None) -> List:
    x = l.copy()
    while len(x) < length:
        x.insert(0, value)
    return x


def _transpose(ls: List[List]) -> List[List]:
    return list(map(list, zip(*ls)))


if __name__ == '__main__':
    board = read_json('testboard.json')
    board[0,0] = State.YES
    board[0,1] = State.NO
    print(board)
