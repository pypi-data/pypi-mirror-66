from types import TracebackType
from typing import Any, Iterable, Optional, Tuple, Type

from .row import Row


class Result:
    @property
    def last_id(self) -> Any:
        raise NotImplementedError()

    @property
    def row_count(self) -> int:
        raise NotImplementedError()

    def fetch(self) -> Optional[Row]:
        row = self._fetch()

        return Row(self._get_column_names(), row) if row is not None else None

    def fetch_all(self):
        columns = self._get_column_names()

        return [Row(columns, r) for r in self._fetch_all()]

    def _fetch(self) -> Tuple[Any]:
        raise NotImplementedError()

    def _fetch_all(self) -> Iterable[Tuple[Any]]:
        raise NotImplementedError()

    def _get_column_names(self) -> Tuple[str]:
        raise NotImplementedError()

    def __enter__(self):
        raise NotImplementedError()

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        raise NotImplementedError()
