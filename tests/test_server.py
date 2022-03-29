import os
from io import BytesIO

import aiohttp
import pytest
from drope import server


@pytest.fixture
async def client(aiohttp_client):
    app = server.make_app()
    client = await aiohttp_client(app)
    return client


async def test_unique_filename(tmpdir):
    os.chdir(tmpdir)

    assert await server.unique_filename("nonduplicate") == "nonduplicate"

    with open("duplicate", "w"):
        pass
    assert await server.unique_filename("duplicate") == "duplicate(1)"

    with open("duplicate(1)", "w"):
        pass
    assert await server.unique_filename("duplicate") == "duplicate(2)"
    assert await server.unique_filename("duplicate(1)") == "duplicate(1)(1)"


async def test_upload_with_duplicates(client, tmpdir):
    os.chdir(tmpdir)

    form1 = aiohttp.FormData()
    form1.add_field("file", BytesIO(b"12345"), filename="12345.txt")
    
    resp1 = await client.post("/", data=form1)
    assert resp1.status == 200

    form2 = aiohttp.FormData()
    form2.add_field("file", BytesIO(b"12345"), filename="12345.txt")

    resp2 = await client.post("/", data=form2)
    assert resp2.status == 200

    with open("12345.txt", "rb") as uploaded_file:
        assert uploaded_file.read() == b"12345"

    with open("12345(1).txt", "rb") as uploaded_file:
        assert uploaded_file.read() == b"12345"


async def test_upload_overwrite_duplicates(aiohttp_client, tmpdir):
    app = server.make_app(overwrite_duplicates=True)
    client = await aiohttp_client(app)

    os.chdir(tmpdir)

    form1 = aiohttp.FormData()
    form1.add_field("file", BytesIO(b"123"), filename="123.txt")
    
    resp1 = await client.post("/", data=form1)
    assert resp1.status == 200

    with open("123.txt", "rb") as uploaded_file:
        assert uploaded_file.read() == b"123"

    form2 = aiohttp.FormData()
    form2.add_field("file", BytesIO(b"other content"), filename="123.txt")

    resp2 = await client.post("/", data=form2)
    assert resp2.status == 200

    with open("123.txt", "rb") as uploaded_file:
        assert uploaded_file.read() == b"other content"


async def test_upload_multiple_files(client, tmpdir):
    os.chdir(tmpdir)

    with open("first", "w") as f:
        f.write("first")

    form = aiohttp.FormData()
    form.add_field("file", BytesIO(b"new_first"), filename="first")
    form.add_field("file", BytesIO(b"second"), filename="second")

    resp = await client.post("/", data=form)
    assert resp.status == 200

    with open("first") as first:
        assert first.read() == "first"
    with open("first(1)") as new_first:
        assert new_first.read() == "new_first"
    with open("second") as second:
        assert second.read() == "second"


async def test_index(client):
    resp = await client.get("/")
    assert resp.status == 200


async def test_not_found(client):
    resp = await client.get("/nonexistent")
    assert resp.status == 404
