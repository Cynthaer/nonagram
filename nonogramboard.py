import json
from builtins import hasattr
from enum import Enum
from itertools import groupby
from typing import List, Tuple, Union, Iterable, Any

import numpy as np


class State(Enum):
    BLANK = 0
    YES = 1
    NO = 2


class NonogramBoard:
    hints: List[List[List[int]]]
    tiles: np.ndarray

    def __init__(self,
                 row_hints: Iterable[Iterable[int]],
                 col_hints: Iterable[Iterable[int]],
                 tiles: Any = None) -> None:
        self.hints = [[list(rh) for rh in row_hints], [list(ch) for ch in col_hints]]

        if tiles:
            self.tiles = np.asarray(as_states(tiles))
        else:
            self.tiles = np.full(self.shape, State.BLANK)

        if not self._isvalid():
            raise Exception('Invalid hint configuration')

    def __repr__(self) -> str:
        return repr(self.tiles)

    def __str__(self) -> str:
        r_hints = _justify_hints(self.hints[0])
        # c_hints are horizontal for ease of display
        c_hints = _transpose(_justify_hints(self.hints[1]))

        hor_pad = ' ' * (len(r_hints[0]) * 2)

        output = ''
        for c_h in c_hints:
            output += f"{hor_pad}{' '.join(c_h)}\n"

        output += f"{hor_pad}{'-' * (self.shape[1] * 2 - 1)}\n"

        for i in range(len(r_hints)):
            output += f"{' '.join(r_hints[i])}|{' '.join([str(x.value) for x in self.tiles[i]])}\n"

        return output

    @property
    def shape(self) -> Tuple[int, int]:
        """:return: (height, width)"""
        if hasattr(self, 'tiles'):
            return self.tiles.shape
        return len(self.hints[0]), len(self.hints[1])

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
        hint = self.hints[axis][index]
        line = self.line(index, axis)

        if State.BLANK in line:
            return False

        line_state = [len(list(g)) for k, g in groupby(line) if k == State.YES]
        if len(line_state) == 0:
            line_state = [0]
        return line_state == hint

    def _isvalid(self) -> bool:
        if self.tiles.shape != (len(self.hints[0]), len(self.hints[1])):
            return False

        # row hints
        for hint in self.hints[0]:
            implied_width = sum(hint) + len(hint) - 1
            if implied_width > len(self.hints[1]) or implied_width > self.tiles.shape[1]:
                return False

        # col hints
        for hint in self.hints[1]:
            implied_width = sum(hint) + len(hint) - 1
            if implied_width > len(self.hints[0]) or implied_width > self.tiles.shape[0]:
                return False

        return True


def read_json(path: str) -> NonogramBoard:
    with open(path) as f:
        d = json.load(f)
        return NonogramBoard(**d)


def as_states(iterable: Iterable[Union[int, Iterable[int]]]) -> List[Union[State, List[State]]]:
    if isinstance(iterable[0], int):
        return [State(i) for i in iterable]

    return [[State(i) for i in row] for row in iterable]


def _justify_hints(hints: Iterable[List[int]]) -> List[List[str]]:
    max_len = max(map(len, hints))
    return [list(map(str, _left_padded(l, max_len, ' '))) for l in hints]


def _left_padded(l: List, length: int, value: object = None) -> List:
    x = l.copy()
    while len(x) < length:
        x.insert(0, value)
    return x


def _transpose(ls: Iterable[Iterable]) -> List[List]:
    return list(map(list, zip(*ls)))


if __name__ == '__main__':
    board = read_json('testboard.json')
    board.tiles[0,0] = State.YES
    board.tiles[0,1] = State.NO
    print(board)
