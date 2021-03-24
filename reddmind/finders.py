"""Movie finders module."""

import csv
import sqlite3
from abc import ABC, abstractmethod
from typing import Any, List, Protocol

from .entities import Movie


class IMovie(Protocol):
    def __call__(self, *args: Any, **kwargs: Any) -> Movie:
        ...


class MovieFinder(ABC):
    def __init__(self, movie_factory: IMovie) -> None:
        self._movie_factory = movie_factory

    @abstractmethod
    def find_all(self) -> List[Movie]:
        ...


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
            csv_reader = csv.reader(csv_file, delimiter=self._delimiter)
            return [
                self._movie_factory(title=row[0], year=row[1], director=row[2])
                for row in csv_reader
            ]


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
            rows = db.execute("SELECT title, year, director FROM movies")

            return [
                self._movie_factory(title=row[0], year=row[1], director=row[2])
                for row in rows
            ]
