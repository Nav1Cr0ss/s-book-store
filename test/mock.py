from datetime import datetime
from typing import Optional

from sqlalchemy import ScalarResult

from internal.adapters.repository.repository import BookRepoIface
from internal.app.book.dto.book import BookFilter, BookUpdate, BookBatchUpdate
from internal.domain.book import Author, Book, Genre


# TODO: create possibility to setup return values
class BookRepoMock(BookRepoIface):

    async def get_author(self, author_id: int) -> Optional[Author]:
        ...

    async def attach_book_to_author(self, author_id: int, book_id: int) -> None:
        ...

    async def get_book(self, book_id: int) -> Optional[Book]:
        new_book = Book(
            id=1,
            title="Sample Book",
            genre=Genre.fiction,
            date_published=datetime.now(),
            file_name="sample_book.pdf",
            restricted=False
        )
        return new_book

    async def get_books(self, filters: BookFilter) -> ScalarResult[tuple[Book]]:
        ...

    async def create_book(self, book: dict) -> int:
        ...

    async def update_book(self, book_id: int, update_data: BookUpdate) -> None:
        ...

    async def restrict_books(self, update_data: BookBatchUpdate) -> None:
        ...
