from limecore.database.api import Result as Base
from psycopg2.extensions import cursor as Cursor
from types import TracebackType
from typing import Any, Iterable, Optional, Tuple, Type


class Result(Base):
    def __init__(self, cursor: Cursor):
        self._cursor = cursor

    @property
    def last_id(self) -> Any:
        return self._cursor.fetchone()[0]

    @property
    def row_count(self) -> int:
        return self._cursor.rowcount

    def _fetch(self) -> Tuple[Any]:
        return self._cursor.fetchone()

    def _fetch_all(self) -> Iterable[Tuple[Any]]:
        return self._cursor.fetchall()

    def _get_column_names(self) -> Tuple[str]:
        return tuple(*[c.name for c in self._cursor.description])

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        self._cursor.close()
