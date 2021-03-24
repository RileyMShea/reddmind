"""Containers module."""

from dependency_injector import containers, providers
from . import finders, entities, listers


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    movie: providers.Factory[entities.Movie] = providers.Factory(entities.Movie)

    csv_finder = providers.Singleton(
        finders.CsvMovieFinder,
        movie_factory=movie.provider,
        path=config.finder.csv.path,
        delimiter=config.finder.csv.delimiter,
    )

    sqlite_finder = providers.Singleton(
        finders.SqliteMovieFinder,
        movie_factory=movie.provider,
        path=config.finder.sqlite.path,
    )

    lister = providers.Factory(listers.MovieLister, movie_finder=sqlite_finder)
