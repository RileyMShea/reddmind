# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

from hypothesis import given
from hypothesis import strategies as st

import reddmind.entities


@given(title=st.text(), year=st.integers(), director=st.text())
def test_fuzz_Movie(title: str, year: int, director: str) -> None:
    reddmind.entities.Movie(title=title, year=year, director=director)
