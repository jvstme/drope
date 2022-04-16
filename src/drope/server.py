import logging
from itertools import count
from pathlib import Path

import aiofiles
import aiofiles.os
from aiohttp import web
from aiohttp.multipart import BodyPartReader


CHUNK_SIZE = 2 ** 16
static_path = Path(__file__).parent.joinpath("static").absolute()

logger = logging.getLogger(__name__)
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


async def write_file(field: BodyPartReader, filename: str):
    async with aiofiles.open(filename, "wb") as f:
        chunk = await field.read_chunk(size=CHUNK_SIZE)

        while chunk:
            await f.write(chunk)
            chunk = await field.read_chunk(size=CHUNK_SIZE)


@routes.post("/")
async def post_index(request: web.Request):
    try:
        fields = await request.multipart()
    except (ValueError, AssertionError):
        raise web.HTTPBadRequest(
            text="multipart/form-data expected in request body",
        )

    files_received = 0

    async for field in fields:
        if field.name != "file":
            continue

        filename = Path(field.filename or "").name

        if not filename:
            continue

        logger.info("Receiving %s", filename)

        part_filename = filename + ".part"

        if not request.app["overwrite_duplicates"]:
            part_filename = await unique_filename(part_filename)
        
        await write_file(field, part_filename)

        if not request.app["overwrite_duplicates"]:
            filename = await unique_filename(filename)
        elif await aiofiles.os.path.exists(filename):
            await aiofiles.os.remove(filename)
        
        await aiofiles.os.rename(part_filename, filename)

        logger.info("Completed %s", filename)
            
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
