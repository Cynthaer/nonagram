import itertools
from typing import List, Iterable, Tuple, TypeVar, Dict, Union

T = TypeVar('T')


def intersperse(iterable: Iterable, delimiter: object) -> List:
    output = []
    it = iter(iterable)
    output.append(next(it))
    for x in it:
        output.extend([delimiter, x])

    return output


def flatten(iterables: Iterable[Iterable]) -> List:
    return list(itertools.chain(*iterables))


def grouped(iterable: Iterable[T]) -> List[Tuple[T, int]]:
    return [(k, len(list(g))) for k, g in itertools.groupby(iterable)]


def run_length_encode(iterable: Iterable[T]) -> List[Dict[str, Union[T, int]]]:
    return [{'state': k, 'length': len(list(g))} for k, g in itertools.groupby(iterable)]
