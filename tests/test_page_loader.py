from pathlib import Path
from typing import Union
from urllib.parse import urljoin, urlparse

import pytest
import page_loader
from page_loader import download
from page_loader.parser import get_links_by_tag, parse_html


def read(path: Union[Path, str], mode: str = "r") -> str:
    with open(path, mode=mode) as f:
        result = f.read()
    return result


BASE_RESOURCE_DIR = Path("ru-hexlet-io-courses_files")
RESOURCE_CSS_PATH = Path("ru-hexlet-io-assets-application.css")
RESOURCE_IMAGE_PATH = Path("ru-hexlet-io-assets-professions-nodejs.png")
RESOURCE_SCRIPT_PATH = Path("ru-hexlet-io-packs-js-runtime.js")
RESOURCE_CANONICAL_HTML_PATH = Path("ru-hexlet-io-coursess.html")
RESOURCE_INDEX_HTML_PATH = Path("ru-hexlet-io-courses.html")

BASE_FIXTURE_DIR = Path("tests/fixtures")
RESOURCE_CSS = read(BASE_FIXTURE_DIR / BASE_RESOURCE_DIR / RESOURCE_CSS_PATH)
RESOURCE_IMAGE = read(
    BASE_FIXTURE_DIR / BASE_RESOURCE_DIR / RESOURCE_IMAGE_PATH, mode="rb"
)
RESOURCE_SCRIPT = read(BASE_FIXTURE_DIR / BASE_RESOURCE_DIR / RESOURCE_SCRIPT_PATH)
RESOURCE_CANONICAL_HTML = read(
    BASE_FIXTURE_DIR / BASE_RESOURCE_DIR / RESOURCE_CANONICAL_HTML_PATH
)
RESOURCE_INDEX_HTML = read(BASE_FIXTURE_DIR / RESOURCE_INDEX_HTML_PATH)
SOURCE_HTML = read(BASE_FIXTURE_DIR / "hexlet-courses.html")

BASE_URL = "https://ru.hexlet.io/"
PROJECT_DIR = Path(__file__).parent.parent.absolute()


RESOURCE_URLS = (
    {"url": urljoin(BASE_URL, "courses"), "text": SOURCE_HTML},
    {"url": urljoin(BASE_URL, "coursess"), "text": RESOURCE_CANONICAL_HTML},
    {"url": urljoin(BASE_URL, "assets/application.css"), "text": RESOURCE_CSS},
    {
        "url": urljoin(BASE_URL, "assets/professions/nodejs.png"),
        "content": RESOURCE_IMAGE,
    },
    {"url": urljoin(BASE_URL, "packs/js/runtime.js"), "text": RESOURCE_SCRIPT},
)

RESOURCE_PATHS = (
    (BASE_RESOURCE_DIR / RESOURCE_CSS_PATH, RESOURCE_CSS),
    (BASE_RESOURCE_DIR / RESOURCE_CANONICAL_HTML_PATH, RESOURCE_CANONICAL_HTML),
    (BASE_RESOURCE_DIR / RESOURCE_SCRIPT_PATH, RESOURCE_SCRIPT),
)

RESOURCE_IMAGE_PATH = (BASE_RESOURCE_DIR / RESOURCE_IMAGE_PATH, RESOURCE_IMAGE)


@pytest.fixture
def all_requests(requests_mock) -> None:
    for kwargs in RESOURCE_URLS:
        requests_mock.get(**kwargs)


def test_page_loader(tmp_path, all_requests) -> None:

    result = download(BASE_URL + "courses", str(tmp_path))
    assert result == str(tmp_path / RESOURCE_INDEX_HTML_PATH)
    assert Path(result).exists()
    assert read(result) == RESOURCE_INDEX_HTML

    for path, content in RESOURCE_PATHS:
        assert read(tmp_path / path) == content

    img_path, img_content = RESOURCE_IMAGE_PATH
    assert read(tmp_path / img_path, mode="rb") == img_content


def test_page_loader_default_dir(tmp_path, all_requests, mocker) -> None:
    mocker.patch.object(page_loader.loader, "CURRENT_DIR", str(tmp_path))
    result = download(BASE_URL + "courses")
    assert result == str(tmp_path / RESOURCE_INDEX_HTML_PATH)
    assert read(result) == RESOURCE_INDEX_HTML
    assert (tmp_path / BASE_RESOURCE_DIR).exists()


def test_page_loader_not_exists_dir(tmp_path, all_requests) -> None:
    path = tmp_path / "shop"

    assert not Path(path).exists()

    with pytest.raises(FileNotFoundError):
        download(BASE_URL, str(path))


def test_get_resource_links_by_tag(tmp_path) -> None:
    soup = parse_html(SOURCE_HTML)
    url = urljoin(BASE_URL, "courses")
    parsed_url = urlparse(url)
    assert get_links_by_tag(soup, parsed_url) == {
        soup.select_one('[href="/assets/application.css"]'): (
            "https://ru.hexlet.io/assets/application.css",
            str(RESOURCE_PATHS[0][0]),
        ),
        soup.select_one('[href="/coursess"]'): (
            "https://ru.hexlet.io/coursess",
            str(RESOURCE_PATHS[1][0]),
        ),
        soup.select_one('[src="/assets/professions/nodejs.png"]'): (
            "https://ru.hexlet.io/assets/professions/nodejs.png",
            str(RESOURCE_IMAGE_PATH[0]),
        ),
        soup.select_one('[src="https://ru.hexlet.io/packs/js/runtime.js"]'): (
            "https://ru.hexlet.io/packs/js/runtime.js",
            str(RESOURCE_PATHS[2][0]),
        ),
    }
