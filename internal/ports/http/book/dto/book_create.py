from datetime import date

from pydantic import BaseModel

from internal.domain.book import Genre


class BookCreateBody(BaseModel):
    title: str
    genre: Genre
    date_published: date
    author_id: int
