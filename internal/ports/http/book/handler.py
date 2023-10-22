import json
from io import BytesIO
from typing import Optional

import openpyxl
from aiohttp.web_request import Request
from aiohttp.web_response import Response, StreamResponse
from pydantic import ValidationError

from internal.app.app import BookAppIface
from internal.app.book.dto.book import BookListSchema, BookSchema
from internal.ports.http.book.dto.book_create import BookCreateBody
from internal.ports.http.book.dto.book_filter_params import BookParamRequest
from internal.ports.http.handler import BookHandlerIface
from pkg.server.aiohttp.errors import ApiError


class BookHandler(BookHandlerIface):
    def __init__(self, app: BookAppIface):
        self.app = app

    async def get_book(self, request: Request) -> Response:
        book_id: int = int(request.match_info['id'])
        book: Optional[BookSchema] = await self.app.get_book(book_id)
        return Response(text=book.model_dump_json(), content_type='application/json', status=200)

    async def get_books(self, request: Request) -> Response:
        try:
            filter_params = BookParamRequest(**request.query)
        except ValidationError as ve:
            return Response(text=ve.json(), content_type='application/json', status=400)

        books: BookListSchema = await self.app.get_books(filter_params)
        return Response(text=books.model_dump_json(), content_type='application/json', status=200)

    async def create_book(self, request: Request) -> Response:
        try:
            book_body = BookCreateBody(**await request.json())
        except ValidationError as ve:
            return Response(text=ve.json(), content_type='application/json', status=400)

        try:
            book_id: int = await self.app.create_book(book_body)
        except ApiError as ae:
            return Response(text=str(ae), status=ae.code)

        return Response(text=json.dumps({"id": book_id}), content_type='application/json', status=200)

    async def upload_book_file(self, request: Request) -> Response:

        file = await request.content.read()
        book_id: int = int(request.match_info['id'])

        await self.app.upload_book_file(book_id, file)

        return Response(status=201)

    async def stream_book(self, request) -> StreamResponse:
        book_id: int = int(request.match_info['id'])
        try:
            file_b, file_name = await self.app.download_book_file(book_id)
        except ApiError as ae:
            return Response(text=str(ae), status=ae.code)

        response = StreamResponse()
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename="{file_name}'
        await response.prepare(request)

        chunk_size = 4096

        for offset in range(0, len(file_b), chunk_size):
            chunk = file_b[offset:offset + chunk_size]
            await response.write(chunk)

        await response.write_eof()
        return response

    async def download_book(self, request) -> Response:
        book_id: int = int(request.match_info['id'])

        try:
            file_b, file_name = await self.app.download_book_file(book_id, read_only=True)
        except ApiError as ae:
            return Response(text=str(ae), status=ae.code)

        if not file_b:
            return Response(text='File not found', status=404)

        response = Response(body=file_b)
        response.headers['Content-Disposition'] = f'attachment; filename="{file_name}"'  # Adjust the filename as needed
        return response

    async def upload_book_restrictions(self, request) -> Response:
        file_b = await request.content.read()

        await self.app.upload_book_restrictions(file_b)

        return Response(status=201)
