import pytest
import requests
from jsonschema import validate

endpoints = [("posts", 100), ("comments", 500), ("albums", 100), ("photos", 5000), ("todos", 200), ("users", 10)]


@pytest.fixture()
def _post_data():
    request_params = {
        'uri': 'https://jsonplaceholder.typicode.com/posts',
        'body': {"title": "foo", "body": "bar", "userId": 1},
        'headers': {"Content-type": "application/json; charset=UTF-8"}
    }
    return request_params


@pytest.mark.parametrize('endpoint', endpoints)
def test_get_endpoints_statuses(endpoint):
    response = requests.get(f'https://jsonplaceholder.typicode.com/{endpoint[0]}')
    assert response.status_code == 200


def test_post(_post_data):
    schema = {
        'type': 'object',
        'properties': {
            'title': {'type': 'string'},
            'body': {'type': 'string'},
            'userId': {'type': 'number'},
            'id': {'type': 'number'},
        },
        "required": ['title', 'body', 'userId', 'id']
    }
    response = requests.post(url=_post_data['uri'], headers=_post_data['headers'], json=_post_data['body'])
    validate(instance=response.json(), schema=schema)
    assert response.status_code == 201


def test_patch(_post_data):
    schema = {
        'type': 'object',
        'properties': {
            'title': {'type': 'string'},
            'body': {'type': 'string'},
            'userId': {'type': 'number'},
            'id': {'type': 'number'},
        },
        "required": ['title', 'body', 'userId', 'id']
    }
    response = requests.patch('https://jsonplaceholder.typicode.com/posts/1', json=_post_data['body'])
    validate(instance=response.json(), schema=schema)
    assert response.status_code == 200


@pytest.mark.parametrize('endpoint, expected_number', endpoints)
def test_amount_of_items_returned(endpoint, expected_number):
    response = requests.get(f'https://jsonplaceholder.typicode.com/{endpoint}')
    assert len(response.json()) == expected_number
    assert response.status_code == 200


def test_delete():
    response = requests.delete('https://jsonplaceholder.typicode.com/posts/1')
    assert response.status_code == 200





