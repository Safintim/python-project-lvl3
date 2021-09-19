from urllib.parse import urljoin, urlparse

from page_loader.parser import get_links_by_tag, parse_html
from tests.plugins import (
    BASE_URL,
    RESOURCE_IMAGE_PATH,
    RESOURCE_PATHS,
    SOURCE_HTML,
)


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
