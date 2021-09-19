import os
from argparse import ArgumentTypeError

import pytest

from page_loader.cli import create_argument_parser


BASE_URL = "https://ru.hex.com"


def test_cli() -> None:
    parsed = create_argument_parser([BASE_URL])
    assert parsed.url == BASE_URL
    assert parsed.output == os.getcwd()


def test_cli_not_url() -> None:
    with pytest.raises(SystemExit):
        create_argument_parser()


def test_cli_not_exists_dir() -> None:
    with pytest.raises(SystemExit):
        create_argument_parser([BASE_URL, "--output", "/shop-mop"])


