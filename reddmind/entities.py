from pydantic import BaseModel
from typing import Any, List
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.sqlite import DATE
from pydantic import BaseModel, constr
from sqlalchemy.orm import registry
from sqlalchemy.orm.decl_api import DeclarativeMeta

mapper_registry = registry()


class Base(metaclass=DeclarativeMeta):
    __abstract__ = True
    registry = mapper_registry
    metadata = mapper_registry.metadata


class MovieORM(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, nullable=False)
    title: str = Column(String(50), index=False, nullable=False, unique=True)
    year = Column(Integer, nullable=False)
    director: str = Column(String(50), index=False, nullable=False, unique=True)


class Movie(BaseModel):
    title: str
    year: int
    director: str

    class Config:
        orm_mode = True
