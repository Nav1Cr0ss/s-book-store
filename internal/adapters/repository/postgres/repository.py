from typing import Optional

from sqlalchemy import select, Insert, update, and_, or_
from sqlalchemy.engine import ScalarResult

from internal.adapters.repository.repository import BookRepoIface
from internal.app.book.dto.book import BookFilter, BookUpdate, BookBatchUpdate
from internal.domain.book import Book, Author, authors_books
from pkg.db.postgres.postgres import Postgres


class BookRepo(BookRepoIface):
    def __init__(self, db: Postgres):
        self.db = db

    async def get_author(self, author_id: int) -> Optional[Author]:
        stmt = select(Author).filter(Author.id == author_id)
        book = await self.db.select_one_or_none(stmt)

        return book

    async def attach_book_to_author(self, author_id: int, book_id: int) -> None:
        stmt = Insert(authors_books).values(
            author_id=author_id,
            book_id=book_id,
        )
        await self.db.insert(stmt)

    async def get_book(self, book_id: int) -> Optional[Book]:
        stmt = select(Book).filter(Book.id == book_id)
        book = await self.db.select_one_or_none(stmt)

        return book

    async def get_books(self, filters: BookFilter) -> ScalarResult[tuple[Book]]:
        stmt = select(Book)
        if filters.genre is not None:
            stmt = stmt.where(Book.genre == filters.genre)

        if filters.author_id is not None:
            stmt = stmt.join(Author, Book.authors)
            stmt = stmt.where(Author.id == filters.author_id)

        if filters.date_start is not None and filters.date_end is not None:
            stmt = stmt.where(Book.date_published.between(filters.date_start, filters.date_end))
        books = await self.db.select(stmt)
        return books

    async def create_book(self, book: dict) -> int:
        stmt = Insert(Book).values(**book)
        book_id = await self.db.insert(stmt)
        return book_id

    async def update_book(self, book_id: int, update_data: BookUpdate) -> None:
        data = update_data.as_update_data()
        stmt = update(Book).where(Book.id == book_id).values(**data)
        await self.db.update(stmt)

    async def restrict_books(self, update_data: BookBatchUpdate) -> None:
        stmt = (
            update(Book)
            .where(
                or_(
                    Book.authors.any(
                        and_(
                            Author.name.in_(update_data.authors_list),
                            Author.books.any(Book.id == Book.id)
                        )
                    ),
                    Book.title.in_(update_data.titles_list)
                )
            )
            .values(restricted=True)
        )
        await self.db.update(stmt)
