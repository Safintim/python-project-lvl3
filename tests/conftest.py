import pytest

from tests.plugins import RESOURCE_URLS


@pytest.fixture
def all_requests(requests_mock) -> None:
    for kwargs in RESOURCE_URLS:
        requests_mock.get(**kwargs)
