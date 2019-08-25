import itertools
import numpy as np
from typing import List, Iterable


def intersperse(iterable: Iterable, delimiter: object) -> List:
    output = []
    it = iter(iterable)
    output.append(next(it))
    for x in it:
        output.extend([delimiter, x])

    return output


def flatten(iterables: Iterable[Iterable]) -> List:
    return list(itertools.chain(iterables))
