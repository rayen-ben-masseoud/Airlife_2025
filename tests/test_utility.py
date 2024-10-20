from src.utils import get_request_with_retries


def test_get_request_with_retries():
    url = "https://httpstat.us/200"
    response = get_request_with_retries(url)
    assert response.status_code == 200
