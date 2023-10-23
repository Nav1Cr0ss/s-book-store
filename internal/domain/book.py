import enum
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, Enum, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pkg.orm.models.base import Base

authors_books = Table(
    "authors_books",
    Base.metadata,
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
    Column("book_id", ForeignKey("books.id"), primary_key=True),
)


class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))

    books: Mapped[list["Book"]] = relationship(
        secondary=authors_books, back_populates="authors"
    )

    def __repr__(self) -> str:
        return self.name


class Genre(enum.StrEnum):
    fiction = "Fiction"
    non_fiction = "Non-Fiction"


class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    genre: Mapped[enum.Enum] = mapped_column(Enum(Genre))
    authors: Mapped[list[Author]] = relationship(
        secondary=authors_books, back_populates="books"
    )
    date_published: Mapped[datetime] = mapped_column(DateTime())
    file_name: Mapped[str] = mapped_column(String(150), default="")
    restricted: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return self.title
