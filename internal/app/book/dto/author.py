from typing import Optional


from internal.app.book.dto.book import BookListSchema
from internal.domain.book import Author
from pkg.pydantic_sqlalchemy.connector import sqlalchemy_to_pydantic

PydanticAuthor = sqlalchemy_to_pydantic(Author)


class AuthorSchema(PydanticAuthor):
    id: int
    name: str
    books: Optional[BookListSchema]

    class Config:
        from_attributes = True

