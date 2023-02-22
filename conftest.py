import pytest
import requests


def pytest_addoption(parser):

    parser.addoption(
        "--url",
        default="https://ya.ru/",
        help="URL"
    )

    parser.addoption(
        "--method",
        default="get",
        choices=["get", "post", "put", "patch", "delete"],
        help='Method',
    )

    parser.addoption(
        "--status_code",
        default="200",
        help="Status"
    )


@pytest.fixture
def base_url(request):
    return request.config.getoption("--url")


@pytest.fixture
def request_method(request):
    return getattr(requests, request.config.getoption("--method"))


@pytest.fixture
def status_code(request):
    return int(request.config.getoption("--status_code"))



