
import pytest
import requests
from jsonschema import validate

endpoints = [("posts", 100), ("comments", 500), ("albums", 100), ("photos", 5000), ("todos", 200), ("users", 10)]


@pytest.fixture()
def _post_data():
    request_params = {
        'url': 'https://jsonplaceholder.typicode.com/posts',
        'json': {"title": "foo", "body": "bar", "userId": 1},
        'headers': {"Content-type": "application/json; charset=UTF-8"}
    }
    return request_params


@pytest.mark.parametrize('endpoint', endpoints)
def test_get_endpoints_statuses(endpoint):
    r = requests.get(f'https://jsonplaceholder.typicode.com/{endpoint[0]}')
    assert r.status_code == 200


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
    r = requests.post(**_post_data)
    validate(instance=r.json(), schema=schema)
    assert r.status_code == 201


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
    r = requests.patch('https://jsonplaceholder.typicode.com/posts/1', json=_post_data['json'])
    validate(instance=r.json(), schema=schema)
    assert r.status_code == 200


@pytest.mark.parametrize('endpoint, expected_number', endpoints)
def test_amount_of_items_returned(endpoint, expected_number):
    r = requests.get(f'https://jsonplaceholder.typicode.com/{endpoint}')
    assert len(r.json()) == expected_number
    assert r.status_code == 200


def test_delete():
    r = requests.delete('https://jsonplaceholder.typicode.com/posts/1')
    assert r.status_code == 200





