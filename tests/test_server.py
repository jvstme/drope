import os
from io import BytesIO

import aiohttp
import pytest
from drope.server import make_app


@pytest.fixture
async def client(aiohttp_client):
    app = make_app()
    client = await aiohttp_client(app)
    return client


async def test_upload(client, tmpdir):
    os.chdir(tmpdir)

    form = aiohttp.FormData()
    form.add_field("file", BytesIO(b"12345"), filename="12345.txt")
    resp = await client.post("/", data=form)

    assert resp.status == 200

    with open("12345.txt", "rb") as uploaded_file:
        assert uploaded_file.read() == b"12345"


async def test_index(client):
    resp = await client.get("/")
    assert resp.status == 200


async def test_not_found(client):
    resp = await client.get("/nonexistent")
    assert resp.status == 404
