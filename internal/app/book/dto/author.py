from typing import Optional

from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from internal.app.book.dto.book import BookListSchema
from internal.domain.book import Author

PydanticAuthor = sqlalchemy_to_pydantic(Author)


class AuthorSchema(PydanticAuthor):
    id: int
    name: str
    books: Optional[BookListSchema]

    class Config:
        from_attributes = True

