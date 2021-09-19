from pathlib import Path
from typing import Union
from urllib.parse import urljoin


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
RESOURCE_SCRIPT = read(
    BASE_FIXTURE_DIR / BASE_RESOURCE_DIR / RESOURCE_SCRIPT_PATH
)
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
