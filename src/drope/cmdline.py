from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser(
    description="Run a service to receive file uploads",
)
parser.add_argument(
    "--host",
    default="127.0.0.1",
    help="bind socket to this host (default: %(default)s)",
)
parser.add_argument(
    "--port",
    type=int,
    default=8000,
    help="bind socket to this port (default: %(default)s)",
)
parser.add_argument(
    "-d",
    "--dir",
    type=Path,
    default=Path("."),
    help="save uploads here (default: %(default)s)",
)
parser.add_argument(
    "--overwrite-duplicates",
    action="store_true",
    help="If a file with the same name exists, replace it with the upload. " \
        "When this option is not present, duplicate files are saved with an " \
        "(i) suffix.",
)


def main():
    args = parser.parse_args()

    import os
    os.chdir(args.dir)

    from .server import make_app
    app = make_app(overwrite_duplicates=args.overwrite_duplicates)

    from aiohttp.web import run_app
    run_app(app, host=args.host, port=args.port)
