import functools

from aiohttp.web_routedef import RouteDef

from pkg.server.aiohttp.data import Route
from pkg.server.aiohttp.middlewares.auth import auth
from pkg.server.aiohttp.middlewares.cors import cors


class HandlerFactory:
    @staticmethod
    def chain_middlewares(inner, outer_handlers):
        chained_handler = inner
        for outer_handler in outer_handlers:
            chained_handler = functools.partial(outer_handler, handler=chained_handler)
        return chained_handler

    @classmethod
    def build_handler(cls, route: Route) -> RouteDef:
        middlewares = []
        if not route.no_auth:
            middlewares.append(auth)
        if not route.no_cors:
            middlewares.append(cors)
        if route.middlewares:
            middlewares.extend(route.middlewares)

        chained_handler = cls.chain_middlewares(route.handler, middlewares)
        handler = route.method(route.url, handler=chained_handler)

        return handler
