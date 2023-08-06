from injector import inject
from limecore.database.api import Database as Base
from limecore.logging import LoggerFactory
from psycopg2 import connect
from types import TracebackType
from typing import Optional, Type

from .configuration import Configuration
from .result import Result


class Database(Base):
    @inject
    def __init__(self, configuration: Configuration, logger_factory: LoggerFactory):
        self._auto_commit = False
        self._configuration = configuration
        self._logger = logger_factory(__name__)

    def commit(self):
        self._connection.commit()

    def execute(self, query: str, *params) -> Result:
        try:
            self._cursor.execute(
                query, self._configuration.type_adapter.to_db_types(params)
            )

            return Result(self._cursor)
        except Exception:
            self.rollback()

            raise

    def rollback(self):
        self._connection.rollback()

    def __enter__(self):
        self._logger.info("Opening Database Connection to %s" % self._configuration)

        self._connection = connect(**self._configuration.__dict__)
        self._connection.autocommit = self._auto_commit

        self._cursor = self._connection.cursor()

        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        self._cursor.close()
        self._connection.close()

        self._logger.info("Closed Database Connection to %s" % self._configuration)
