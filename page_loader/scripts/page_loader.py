import argparse
from pathlib import Path

from page_loader import download


def is_exists(filepath):
    if Path(filepath).exists():
        return filepath
    raise argparse.ArgumentTypeError


def main():
    parser = argparse.ArgumentParser(description="Page loader")
    parser.add_argument("url")
    parser.add_argument("-o", "--output", type=is_exists, help="Output directory")
    namespace = parser.parse_args()
    print(download(namespace.url, namespace.output))


if __name__ == "__main__":
    main()
