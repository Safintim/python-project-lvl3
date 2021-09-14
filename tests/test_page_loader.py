from pathlib import Path
from contextlib import contextmanager

import pytest
import requests_mock

from page_loader import download
from page_loader.page_loader import get_file_name


def read(path):
    with open(path) as f:
        result = f.read()
    return result


HEXLET_COURSES_HTML = read("tests/fixtures/hexlet-courses.html")
HEXLET_COURSES_URL = "https://ru.hexlet.io/courses"
PROJECT_DIR = Path(__file__).parent.parent.absolute()


@pytest.fixture(autouse=True)
def create_project_dir(fs):
    fs.create_dir(PROJECT_DIR)


@pytest.fixture
def hexlet_courses_html():
    file_ = open("tests/fixtures/hexlet-courses.html")
    yield file_.read()
    file_.close()


@pytest.fixture
def hexlet_courses_html_fs(hexlet_courses_html, fs):
    path = "/tmp/hexlet-courses.html"
    fs.create_file(path)
    with open(path, "w") as f:
        f.write(hexlet_courses_html)


@contextmanager
def mock_request_get(url, **kwargs):
    with requests_mock.Mocker() as mock:
        mock.register_uri("GET", url, **kwargs)
        yield mock


@mock_request_get(HEXLET_COURSES_URL, text=HEXLET_COURSES_HTML)
def test_page_loader(fs):
    result = download(HEXLET_COURSES_URL, "/tmp")
    assert result == "/tmp/ru-hexlet-io-courses.html"
    assert Path(result).exists()
    assert open(result).read() == HEXLET_COURSES_HTML


@mock_request_get(HEXLET_COURSES_URL, text=HEXLET_COURSES_HTML)
def test_page_loader_default_dir(fs):
    result = download(HEXLET_COURSES_URL)
    assert result == str(PROJECT_DIR / "ru-hexlet-io-courses.html")
    assert Path(result).exists()
    assert open(result).read() == HEXLET_COURSES_HTML


@mock_request_get(HEXLET_COURSES_URL, text=HEXLET_COURSES_HTML)
def test_page_loader_not_exists_dir(fs):
    path = "/tmp/shop"

    assert not Path(path).exists()

    with pytest.raises(FileNotFoundError):
        download(HEXLET_COURSES_URL, path)


def test_get_file_name(fs):
    url1 = "https://ru.hexlet.io/projects/51/members/17085"
    expected1 = "ru-hexlet-io-projects-51-members-17085.html"
    assert get_file_name(url1) == expected1

    url2 = "https://ru.hexlet.io/my/ratings/week?q%5Bcity_id_eq%5D=60"
    expected2 = "ru-hexlet-io-my-ratings-week.html"
    assert get_file_name(url2) == expected2
