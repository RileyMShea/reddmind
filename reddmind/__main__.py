import sys
from enum import Enum

import typer
from dependency_injector.wiring import Provide, inject


from .containers import Container
from .listers import MovieLister



class FinderType(str, Enum):
    csv = "csv"
    sqlite = "sqlite"
    orm_sqlite = "orm_sqlite"


@inject
def main(
    lister: MovieLister = Provide[Container.lister],
) -> None:
    print("Francis Lawrence movies:")
    for movie in lister.movies_directed_by("Francis Lawrence"):
        print("\t-", movie)

    print("2016 movies:")
    for movie in lister.movies_released_in(2016):
        print("\t-", movie)


app = typer.Typer()
container = Container()
container.config.from_yaml("config.yml")
container.wire(modules=[sys.modules[__name__]])


@app.callback()
def callback() -> None:
    """
    Riley's CLI app
    """


@app.command()
def movies(finder_type: FinderType, stuff: bool = True) -> None:
    """
    Show movies in database
    """
    container.config.finder.type.override(finder_type)
    main()


if __name__ == "__main__":
    movies(FinderType.orm_sqlite)
