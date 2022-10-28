import argparse
import ftplib
import importlib
import sys
from io import TextIOWrapper
from urllib.parse import urlparse

from rich.console import Console

from _sget import determine_url_protocol, download

DEBUG = False


def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def main() -> None:
    console = Console()
    print = console.print

    argp = argparse.ArgumentParser()

    argp.add_argument(
        "-e", "--encoding", required=False, default="utf8", action="store"
    )
    argp.add_argument(
        "-o", "--output-file", required=False, default=None, action="store"
    )
    argp.add_argument(
        "-q", "--quiet", required=False, default=False, action="store_true"
    )
    argp.add_argument("-u", "--url", required=True, default=None, action="store")
    argp.add_argument("--debug", required=False, default=False, action="store_true")
    argp.add_argument(
        "-f", "--force", required=False, default=False, action="store_true"
    )

    ns = argp.parse_args()

    DEBUG = ns.debug
    dprint(locals())

    url = ns.url
    encoding = ns.encoding

    if ns.quiet:
        print = lambda *x, **kwargs: Ellipsis

    if ns.output_file == None:
        output = sys.stdout
    else:
        output = open(ns.output_file, "x")

    if determine_url_protocol(ns.url) == "http" and not ns.force:
        print(
            "Wait! http is not a safe protocol, press enter to continue, or Ctrl-C to cancel"
        )
        try:
            input()
        except KeyboardInterrupt:
            exit(1)

    download(url, encoding=encoding, output=output)

    if isinstance(output, TextIOWrapper):
        output.close()


if __name__ == "__main__":
    main()
