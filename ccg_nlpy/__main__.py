from __future__ import print_function

import argparse

from .download import main as download_main

parser = argparse.ArgumentParser(prog='ccg_nlpy')
subparsers = parser.add_subparsers(help='commands')

# Create the parser for download command
parser_download = subparsers.add_parser('download', help='download help')
parser_download.add_argument(
    "--version", help="CogComp model version", required=False)
parser_download.set_defaults(func=download_main)

if __name__ == "__main__":
    import logging

    # Set the logging level for this mode.
    logging.basicConfig(level=logging.DEBUG)

    args = parser.parse_args()

    try:
        args.func(args)
    except AttributeError:
        parser.print_help()
