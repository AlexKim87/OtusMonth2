

def test_url(base_url, request_method, status_code):
    response = request_method(url=base_url)
    assert response.status_code == status_code

