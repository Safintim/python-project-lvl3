from http import HTTPStatus
from pathlib import Path

import page_loader
import pytest
import requests
from page_loader import download
from tests.plugins import (
    BASE_RESOURCE_DIR,
    BASE_URL,
    RESOURCE_IMAGE_PATH,
    RESOURCE_INDEX_HTML,
    RESOURCE_INDEX_HTML_PATH,
    RESOURCE_PATHS,
    RESOURCE_URLS,
    read,
)


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


def test_page_loader_index_not_available(requests_mock) -> None:
    url = RESOURCE_URLS[0]["url"]
    requests_mock.get(url=url, status_code=HTTPStatus.NOT_FOUND)

    with pytest.raises(requests.HTTPError):
        download(url)


def test_page_loader_resource_not_available(
        requests_mock, all_requests
) -> None:
    url = RESOURCE_URLS[1]["url"]
    requests_mock.get(url=url, status_code=HTTPStatus.FORBIDDEN)

    with pytest.raises(requests.HTTPError):
        download(url)


def test_page_loader_not_permission_for_write(mocker, all_requests) -> None:
    url = RESOURCE_URLS[0]["url"]
    mocker.patch.object(Path, "write_text", side_effect=PermissionError)

    with pytest.raises(PermissionError):
        download(url)
