"""Movie finders module."""

import csv
import sqlite3
from abc import ABC, abstractmethod
from typing import Any, List, Protocol, Iterator
from sqlalchemy import create_engine

from .entities import Movie, MovieORM
from sqlalchemy.orm import Session
import logging
from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


logging.basicConfig(handlers=[InterceptHandler()], level=0)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


class DataIterator(Protocol):
    def __iter__(self) -> Iterator[List[str]]:
        ...


class IMovie(Protocol):
    """Anything that returns a `Movie` when Called."""

    def __call__(self, *args: Any, **kwargs: Any) -> Movie:
        ...


class MovieFinder(ABC):
    def __init__(self, movie_factory: IMovie) -> None:
        self._movie_factory = movie_factory

    @abstractmethod
    def find_all(self) -> List[Movie]:
        ...

    def as_list(self, reader: DataIterator) -> List[Movie]:
        return [
            self._movie_factory(title=row[0], year=row[1], director=row[2])
            for row in reader
        ]


class CsvMovieFinder(MovieFinder):
    def __init__(
        self,
        movie_factory: IMovie,
        path: str,
        delimiter: str,
    ) -> None:
        self._csv_file_path = path
        self._delimiter = delimiter
        super().__init__(movie_factory)

    def find_all(self) -> List[Movie]:
        with open(self._csv_file_path) as csv_file:
            reader = csv.reader(csv_file, delimiter=self._delimiter)

            return self.as_list(reader)


class SqliteMovieFinder(MovieFinder):
    def __init__(
        self,
        movie_factory: IMovie,
        path: str,
    ) -> None:
        self._database = sqlite3.connect(path)
        super().__init__(movie_factory)

    def find_all(self) -> List[Movie]:
        with self._database as db:
            reader = db.execute("SELECT title, year, director FROM movies")

            return self.as_list(reader)


class ORMSqliteFinder(MovieFinder):
    def __init__(
        self,
        movie_factory: IMovie,
        path: str,
    ) -> None:
        self._engine = create_engine(f"sqlite:///{path}", echo=False)
        super().__init__(movie_factory)

    def find_all(self) -> List[Movie]:
        # with self._database as db:
        #     reader = db.execute("SELECT title, year, director FROM movies")
        with Session(self._engine) as session:

            session.add(MovieORM(director="Riley Shea", year=2342, title="My own life"))

            print(session.new)
            session.commit()

        return [Movie(director="Francis Lawrence", year=2342, title="dsafsdfaf")]
