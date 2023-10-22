from internal.ports.http.handler import BookHandlerIface
from pkg.server.aiohttp.data import Route
from pkg.server.aiohttp.methods import GET, POST
from pkg.server.aiohttp.middlewares.construct_request_body import construct_request_body
from pkg.server.aiohttp.middlewares.example import example


def get_routes(book_handler: BookHandlerIface):
    routes = [
        Route("/books/book_restrictions", POST, book_handler.upload_book_restrictions, no_auth=True, no_cors=True),
        Route("/books/{id}", GET, book_handler.get_book, middlewares=(example,)),
        Route("/books", GET, book_handler.get_books, no_auth=True, no_cors=True),
        Route("/books", POST, book_handler.create_book, no_auth=True, no_cors=True,
              middlewares=(construct_request_body,)),
        Route("/books/{id}/upload-file", POST, book_handler.upload_book_file, no_auth=True, no_cors=True),
        Route("/books/{id}/stream", GET, book_handler.stream_book, no_auth=True, no_cors=True),
        Route("/books/{id}/download", GET, book_handler.download_book, no_auth=True, no_cors=True),
    ]
    return routes
