from typing import Sequence, List


def intersperse(iterable: Sequence, delimiter: object) -> List:
    output = []
    it = iter(iterable)
    output.append(next(it))
    for x in it:
        output.extend([delimiter, x])

    return output
