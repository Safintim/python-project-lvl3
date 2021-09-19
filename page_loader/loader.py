import os
from pathlib import Path
from typing import Iterable, Tuple, Union
from urllib.parse import urlparse

import requests
from bs4.element import Tag

from page_loader import parser


CURRENT_DIR = os.getcwd()


def download_links(links: Iterable, output_dir: Union[Path, str]) -> None:
    for remote_link, local_link in links:
        response = requests.get(remote_link)
        path = output_dir / local_link
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(response.content)


def change_links(links_by_tag: dict[Tag: Tuple[str, str]]) -> None:
    for tag, (_, local_link) in links_by_tag.items():
        if tag.get("src"):
            tag["src"] = local_link
        elif tag.get("href"):
            tag["href"] = local_link


def download(url: str, output_dir: str = None) -> str:

    output_dir = Path(output_dir or CURRENT_DIR)
    if not output_dir.exists():
        raise FileNotFoundError(output_dir)

    response = requests.get(url)
    soup = parser.parse_html(response.text)
    parsed_url = urlparse(url)

    links_by_tag = parser.get_links_by_tag(soup, parsed_url)
    download_links(links_by_tag.values(), output_dir)
    change_links(links_by_tag)

    index_page_file_name = parser.get_index_page_file_name(parsed_url)
    index_page_path = output_dir / index_page_file_name
    index_page_path.write_text(soup.prettify())

    return str(index_page_path)
