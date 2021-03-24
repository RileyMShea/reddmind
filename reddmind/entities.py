from pydantic import BaseModel


class Movie(BaseModel):
    title: str
    year: int
    director: str

    def __repr__(self) -> str:
        return "BANANNA"
