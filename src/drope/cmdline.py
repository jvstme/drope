from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from pathlib import Path

parser = ArgumentParser(
    description="Run a service to receive file uploads",
    formatter_class=ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "--host", default="127.0.0.1", help="bind socket to this host"
)
parser.add_argument(
    "--port", type=int, default=8000, help="bind socket to this port"
)
parser.add_argument(
    "-d", "--dir", type=Path, default=Path("."), help="save uploads here"
)


def main():
    args = parser.parse_args()

    import os
    os.chdir(args.dir)

    from .server import make_app
    app = make_app()

    from aiohttp.web import run_app
    run_app(app, host=args.host, port=args.port)
