import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from drope.server import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_upload(tmpdir):
    os.chdir(tmpdir)
    original_file = NamedTemporaryFile()
    original_file.write(b"12345")
    original_file.seek(0)
    resp = client.post(
        "/",
        files=dict(file=original_file),
    )
    assert resp.status_code == 303
    with open(Path(original_file.name).name, "rb") as uploaded_file:
        assert uploaded_file.read() == b"12345"


def test_index():
    assert client.get("/").status_code == 200


def test_not_found():
    assert client.get("/nonexistent").status_code == 404
