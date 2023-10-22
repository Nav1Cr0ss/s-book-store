from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.engine import ScalarResult

from internal.app.book.dto.book import BookFilter, BookUpdate, BookBatchUpdate
from internal.domain.book import Book, Author


class BookRepoIface(ABC):

    @abstractmethod
    async def get_author(self, author_id: int) -> Optional[Author]: ...

    @abstractmethod
    async def attach_book_to_author(self, author_id: int, book_id: int) -> None: ...

    @abstractmethod
    async def get_book(self, book_id: int) -> Optional[Book]: ...

    @abstractmethod
    async def get_books(self, filters: BookFilter) -> ScalarResult[tuple[Book]]: ...

    @abstractmethod
    async def create_book(self, book: dict) -> int: ...

    @abstractmethod
    async def update_book(self, book_id: int, update_data: BookUpdate) -> None: ...

    @abstractmethod
    async def restrict_books(self, update_data: BookBatchUpdate) -> None: ...
