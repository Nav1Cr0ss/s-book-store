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
    # db conn instance
    db = Postgres()

    # gcp bucket
    storage_book = StorageBook()

    # book repository
    book_repo = BookRepo(db)

    # app layer
    book_app = BookApp(book_repo, storage_book)

    # http layer
    book_handler = BookHandler(book_app)

    # list of routes with adapter which helps with custom route level middlewares
    book_routes = get_routes(book_handler)

    # aioHttp
    app = web.Application()
    logging.basicConfig(level=logging.INFO)

    # compile all handlers
    # book_routes = RouterFactory.get_compiled_routes(book_routes)
    RouterFactory.register_routes(app, book_routes)

    # server config
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, config.Server.HOST, config.Server.PORT)
    await site.start()

    await asyncio.sleep(100 * 3600)


if __name__ == '__main__':
    asyncio.run(main())
