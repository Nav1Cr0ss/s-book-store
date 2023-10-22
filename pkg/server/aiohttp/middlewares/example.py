from aiohttp.web import middleware
from aiohttp.web_request import Request
from aiohttp.web_response import Response


@middleware
async def example(request: Request, handler: callable) -> Response:
    print("Something helpful done")
    resp = await handler(request)
    return resp
