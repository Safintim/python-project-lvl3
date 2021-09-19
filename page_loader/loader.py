import logging
import os
from pathlib import Path
from typing import Iterable, Tuple, Union
from urllib.parse import urlparse

import requests
from bs4.element import Tag
from page_loader import parser

CURRENT_DIR = os.getcwd()


def download_links(links: Iterable, output_dir: Union[Path, str]) -> None:

    logging.info("The downloading of resources has started..")

    for remote_link, local_link in links:
        response = requests.get(remote_link)

        if response.ok:
            logging.info(f"Resource {remote_link} has been uploaded")
            path = output_dir / local_link
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(response.content)
            logging.info(f"Resource has been saved by path: {path}")
        else:
            logging.warning(
                f"Resource {remote_link} has not been loaded. HTTP-code: {response.status_code}"
            )
            response.raise_for_status()

    logging.info("All resources downloaded")


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

    if response.ok:
        logging.info(f"Request for {url} fulfilled")
    else:
        logging.error(f"Failed request for - {url}")
        response.raise_for_status()

    soup = parser.parse_html(response.text)
    parsed_url = urlparse(url)

    links_by_tag = parser.get_links_by_tag(soup, parsed_url)
    logging.info(f"Number of {len(links_by_tag)} references found")

    download_links(links_by_tag.values(), output_dir)
    change_links(links_by_tag)

    index_page_file_name = parser.get_index_page_file_name(parsed_url)
    index_page_path = output_dir / index_page_file_name
    index_page_path.write_text(soup.prettify())
    logging.info(f"Index page saved to path: {index_page_path}")

    return str(index_page_path)
