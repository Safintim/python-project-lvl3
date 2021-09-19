import logging
import sys

from page_loader import download, logger
from page_loader.cli import create_argument_parser


def main():
    logger.setup()
    arguments = create_argument_parser()
    try:
        path = download(arguments.url, arguments.output)
        sys.stdout.write(path)
    except Exception as error:
        logging.error(f"Error {error}")
        sys.stderr.write(f"Error {error}!")
        sys.exit(1)


if __name__ == "__main__":
    main()
