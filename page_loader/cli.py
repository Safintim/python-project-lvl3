import argparse
import os
from pathlib import Path


def create_argument_parser(args=None):
    parser = argparse.ArgumentParser(
        description="Page loader", usage="page-loader [options] <url>"
    )
    parser.add_argument("url", type=str)
    parser.add_argument(
        "-o",
        "--output",
        type=is_exists,
        metavar="dir",
        help="Output directory (default current working directory",
        default=os.getcwd(),
    )
    return parser.parse_args(args)


def is_exists(filepath):
    if Path(filepath).exists():
        return filepath
    raise argparse.ArgumentTypeError(f"Directory not found: {filepath}")
