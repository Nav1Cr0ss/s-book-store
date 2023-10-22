from dataclasses import dataclass, asdict
from datetime import date
from typing import Optional

from pydantic import RootModel, BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from internal.domain.book import Book, Genre

PydanticBook = sqlalchemy_to_pydantic(Book)


class BookSchema(PydanticBook):
    id: int

    class Config:
        from_attributes = True


class BookListSchema(RootModel):
    root: list[BookSchema]


@dataclass
class BookUpdate:
    genre: Optional[Genre] = None
    date_published: Optional[date] = None
    title: Optional[str] = None
    file_url: Optional[str] = None

    def as_update_data(self) -> dict:
        update_data = {key: value for key, value in asdict(self).items() if value is not None}
        return update_data

@dataclass
class BookBatchUpdate:
    titles_list: Optional[list[str]] = None
    authors_list: Optional[list[str]] = None

class BookFilter(BaseModel):
    genre: Optional[Genre] = None
    author_id: Optional[int] = None
    date_start: Optional[date] = None
    date_end: Optional[date] = None
