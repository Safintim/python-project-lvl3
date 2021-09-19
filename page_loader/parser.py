import os
from collections import ChainMap
from typing import Tuple
from urllib.parse import ParseResult, urlparse, urlunparse

from bs4 import BeautifulSoup
from bs4.element import Tag


ATTR_BY_TAG = {
    "img": "src",
    "link": "href",
    "script": "src",
}


def parse_html(html: str, default: str = "html.parser") -> BeautifulSoup:
    return BeautifulSoup(html, default)


def get_links_by_tag(
        soup: BeautifulSoup,
        parsed_url: ParseResult,
) -> dict[Tag: Tuple[str, str]]:
    parsed_links = parse_links_from_soup(soup)
    link_paths = get_path_links_same_host(parsed_url.hostname, parsed_links)
    return create_downloads_links(parsed_url, link_paths)


def parse_links_from_soup(
        soup: BeautifulSoup,
        tags: dict[str:str] = None
) -> dict[Tag:ParseResult]:
    attr_by_tag = tags or ATTR_BY_TAG
    links_for_all_tag = [
        find_links_by_tag(soup, tag, attr) for tag, attr in attr_by_tag.items()
    ]
    links_by_tag = ChainMap(*links_for_all_tag)
    return {tag: urlparse(link) for tag, link in links_by_tag.items()}


def get_path_links_same_host(
        hostname: str,
        parsed_links: dict[Tag:ParseResult],
) -> dict[Tag: ParseResult]:
    return {
        tag: link.path
        for tag, link in parsed_links.items()
        if is_same_host(link.hostname, hostname)
    }


def find_links_by_tag(
        soup: BeautifulSoup,
        tag: str,
        attr: str,
) -> dict[Tag:str]:
    return {
        element: element.get(attr)
        for element in soup.find_all(tag)
        if element.get(attr)
    }


def create_downloads_links(
    parsed_url: ParseResult,
    link_paths: dict[Tag: ParseResult],
    local_dir_suffix: str = "_files",
) -> dict[Tag: Tuple[str, str]]:

    local_hostname = get_local_hostname(parsed_url.hostname)
    local_dir = get_full_path(parsed_url) + local_dir_suffix

    return {
        tag: (
            create_remote_url(parsed_url, path),
            create_local_url(local_dir, local_hostname, path),
        )
        for tag, path in link_paths.items()
    }


def is_same_host(source: str, target: str) -> bool:
    return source == target or not source


def create_remote_url(parsed_url: ParseResult, path: str) -> str:
    return urlunparse((parsed_url.scheme, parsed_url.netloc, path, None, None, None))


def create_local_url(
        local_dir: str,
        local_hostname: str,
        path: str,
        ext: str = ".html",
) -> str:
    path, extension = os.path.splitext(path)
    extension = extension if extension else ext
    local_path = get_local_path(path) + extension
    local_resource_path = "{}-{}".format(local_hostname, local_path)
    return "{}/{}".format(local_dir, local_resource_path)


def get_local_hostname(hostname: str) -> str:
    split_hostname = hostname.split(".")
    return "-".join(split_hostname)


def get_local_path(path: str) -> str:
    start_not_empty = 1
    split_path = path.split("/")[start_not_empty:]
    return "-".join(split_path)


def get_full_path(parsed_url: ParseResult) -> str:
    local_path = get_local_path(parsed_url.path)
    local_hostname = get_local_hostname(parsed_url.hostname)
    not_empty = filter(None, [local_hostname, local_path])
    return "-".join(not_empty)


def get_index_page_file_name(parsed_url: ParseResult, extension: str = ".html") -> str:
    return get_full_path(parsed_url) + extension
