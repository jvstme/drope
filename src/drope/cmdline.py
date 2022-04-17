import logging
import sys
from argparse import ArgumentParser
from pathlib import Path

from . import server


parser = ArgumentParser(
    description="Run a service to receive file uploads",
)
parser.add_argument(
    "-H",
    "--host",
    default="127.0.0.1",
    help="bind socket to this host (default: %(default)s)",
)
parser.add_argument(
    "-P",
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


def setup_logging():
    formatter = logging.Formatter('%(asctime)s %(message)s', '%H:%M:%S')
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    server.logger.setLevel(logging.INFO)
    server.logger.addHandler(handler)


def main():
    import os
    from aiohttp.web import run_app

    setup_logging()

    args = parser.parse_args()
    os.chdir(args.dir)
    app = server.make_app(overwrite_duplicates=args.overwrite_duplicates)

    run_app(app, host=args.host, port=args.port)
