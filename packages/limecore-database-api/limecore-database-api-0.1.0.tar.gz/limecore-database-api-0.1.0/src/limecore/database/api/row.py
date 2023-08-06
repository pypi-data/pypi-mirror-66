from typing import Any, Tuple


class Row:
    def __init__(self, columns: Tuple[str], values: Tuple[Any]):
        self._data = dict(zip(columns, values))
