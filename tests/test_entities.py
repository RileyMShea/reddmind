from hypothesis import given
from hypothesis import strategies as st

import reddmind.entities


@given(title=st.text(), year=st.integers(), director=st.text())
def test_fuzz_Movie(title: str, year: int, director: str) -> None:
    reddmind.entities.Movie(title=title, year=year, director=director)


def test_movie_orm() -> None:
    thing = reddmind.entities.MovieORM(id=0, title="aple", year=2222, director="me")
    more = reddmind.entities.Movie.from_orm(thing)
