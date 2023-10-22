from abc import ABC, abstractmethod

from aiohttp.web_request import Request
from aiohttp.web_response import Response, StreamResponse


class BookHandlerIface(ABC):
    @abstractmethod
    async def get_books(self, request: Request) -> Response: ...

    @abstractmethod
    async def get_book(self, request: Request) -> Response: ...

    @abstractmethod
    async def create_book(self, request: Request) -> Response: ...

    @abstractmethod
    async def upload_book_file(self, request: Request) -> Response: ...

    @abstractmethod
    async def stream_book(self, request) -> StreamResponse: ...

    @abstractmethod
    async def download_book(self, request) -> Response: ...

    @abstractmethod
    async def upload_book_restrictions(self, request) -> Response: ...


