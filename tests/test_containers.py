"""Tests module."""

from typing import Iterator
from unittest import mock

import pytest

from reddmind.containers import Container


@pytest.fixture
def container() -> Iterator[Container]:
    container = Container()
    container.config.from_dict(
        {
            "finder": {
                "type": "csv",
                "csv": {
                    "path": "/fake-movies.csv",
                    "delimiter": ",",
                },
                "sqlite": {
                    "path": "/fake-movies.db",
                },
            },
        }
    )
    yield container


def test_movies_directed_by(container: Container) -> None:
    finder_mock = mock.Mock()
    finder_mock.find_all.return_value = [
        container.movie(title="The 33", year=2015, director="Patricia Riggen"),
        # container.movie("The Jungle Book", 2016, "Jon Favreau"),
    ]

    with container.finder.override(finder_mock):
        lister = container.lister()
        movies = lister.movies_directed_by("Jon Favreau")

    assert len(movies) == 0
    with pytest.raises(IndexError):
        assert movies[0].title == "The Jungle Book"


def test_movies_released_in(container: Container) -> None:
    finder_mock = mock.Mock()
    finder_mock.find_all.return_value = [
        container.movie(title="The 33", year=2015, director="Patricia Riggen"),
        # container.movie("The Jungle Book", 2016, "Jon Favreau"),
    ]

    with container.finder.override(finder_mock):
        lister = container.lister()
        movies = lister.movies_released_in(2015)

    assert len(movies) == 1
    assert movies[0].title == "The 33"
