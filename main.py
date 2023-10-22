import asyncio
import logging

from aiohttp import web

from internal.adapters.repository.postgres.repository import BookRepo
from internal.adapters.storage.gbacket.book_storage import StorageBook
from internal.app.book.book import BookApp
from internal.ports.http.book.handler import BookHandler
from internal.ports.http.book.router import get_routes
from pkg.db.postgres.postgres import Postgres
from pkg.server.aiohttp.router import RouterFactory
from settings import config


async def main():
    db = Postgres()

    book_repo = BookRepo(db)
    storage_book = StorageBook()
    book_app = BookApp(book_repo, storage_book)

    book_handler = BookHandler(book_app)

    book_routes = get_routes(book_handler)
    book_routes = RouterFactory.get_routes(book_routes)

    app = web.Application()
    logging.basicConfig(level=logging.INFO)

    app.add_routes(book_routes)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, config.Server.HOST, config.Server.PORT)
    await site.start()

    await asyncio.sleep(100 * 3600)


if __name__ == '__main__':
    asyncio.run(main())
