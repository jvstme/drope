from itertools import count
from pathlib import Path

import aiofiles
import aiofiles.os
from aiohttp import web


CHUNK_SIZE = 2 ** 16
static_path = Path(__file__).parent.joinpath("static").absolute()

routes = web.RouteTableDef()


async def unique_filename(original_path: str):
    if not await aiofiles.os.path.exists(original_path):
        return original_path
    
    split = original_path.rsplit(".", 1)
    base = split[0]
    ext = "." + split[1] if len(split) > 1 else ""

    for i in count(1):
        path = f"{base}({i}){ext}"

        if not await aiofiles.os.path.exists(path):
            return path


@routes.post("/")
async def post_index(request: web.Request):
    fields = await request.multipart()

    files_received = 0

    async for field in fields:
        if field.name != "file":
            continue

        filename = Path(field.filename or "").name

        if not filename:
            continue

        if not request.app["overwrite_duplicates"]:
            filename = await unique_filename(filename)

        async with aiofiles.open(filename, "wb") as f:
            chunk = await field.read_chunk(size=CHUNK_SIZE)

            while chunk:
                await f.write(chunk)
                chunk = await field.read_chunk(size=CHUNK_SIZE)
            
        files_received += 1
    
    if files_received:
        raise web.HTTPSeeOther(".")
    else:
        raise web.HTTPBadRequest(text="file field is required")


@routes.get("/")
async def get_index(_):
    return web.FileResponse(static_path / "index.html")


routes.static("/", static_path)


def make_app(*, overwrite_duplicates=False):
    app = web.Application()
    app.add_routes(routes)

    app["overwrite_duplicates"] = overwrite_duplicates

    return app
