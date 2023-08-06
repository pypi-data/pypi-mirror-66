from types import TracebackType
from typing import Any, Optional, Type

from .result import Result


class Database:
    def commit(self):
        raise NotImplementedError()

    def execute(self, query: str, *params: Any) -> Result:
        raise NotImplementedError()

    def rollback(self):
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
