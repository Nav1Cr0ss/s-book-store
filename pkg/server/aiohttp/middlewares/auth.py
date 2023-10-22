from aiohttp.web import middleware
from aiohttp.web_request import Request
from aiohttp.web_response import Response


@middleware
async def auth(request: Request, handler: callable) -> Response:
    print("Authenticated")
    resp = await handler(request)
    return resp
