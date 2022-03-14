from pathlib import Path

import aiofiles
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

CHUNK_SIZE = 8192

static_path = Path(__file__).parent.joinpath("static").absolute()

app = FastAPI()


@app.post("/")
async def post_index(file: UploadFile = File(...)):
    async with aiofiles.open(file.filename, "wb") as f:
        while chunk := await file.read(CHUNK_SIZE):
            await f.write(chunk)
    return RedirectResponse(".", 303)


app.mount("/", StaticFiles(directory=static_path, html=True))
