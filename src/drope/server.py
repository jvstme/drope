from pathlib import Path

import aiofiles
from aiohttp import web


CHUNK_SIZE = 2 ** 16
static_path = Path(__file__).parent.joinpath("static").absolute()

routes = web.RouteTableDef()


@routes.post("/")
async def post_index(request: web.Request):
    fields = await request.multipart()

    async for field in fields:
        if field.name != "file" or not field.filename:
            continue

        async with aiofiles.open(field.filename, "wb") as f:
            chunk = await field.read_chunk(size=CHUNK_SIZE)

            while chunk:
                await f.write(chunk)
                chunk = await field.read_chunk(size=CHUNK_SIZE)
    
        raise web.HTTPSeeOther(".")
    
    raise web.HTTPBadRequest(text="file field is required")


@routes.get("/")
async def get_index(_):
    return web.FileResponse(static_path / "index.html")


routes.static("/", static_path)


def make_app():
    app = web.Application()
    app.add_routes(routes)
    return app
