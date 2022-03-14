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

    import uvicorn
    from .server import app
    uvicorn.run(app, host=args.host, port=args.port)
