from abc import ABC, abstractmethod
from typing import Optional

from internal.app.book.dto.book import BookListSchema, BookSchema, BookFilter
from internal.ports.http.book.dto.book_create import BookCreateBody


class BookAppIface(ABC):

    @abstractmethod
    async def get_book(self, book_id: int) -> Optional[BookSchema]: ...

    @abstractmethod
    async def get_books(self, filters: BookFilter) -> BookListSchema: ...

    @abstractmethod
    async def create_book(self, book: BookCreateBody) -> int: ...

    @abstractmethod
    async def upload_book_file(self, book_id: int, file_bytes: bytes) -> None: ...

    @abstractmethod
    async def download_book_file(self, book_id: int, read_only: Optional[bool] = False) -> (bytes, str): ...

    @abstractmethod
    async def upload_book_restrictions(self, restrictions_file: bytes) -> None: ...
