import pytest
import requests
from jsonschema import validate
from http import HTTPStatus

expected_code = HTTPStatus.OK


def test_all_breeds():

    # Выполнить запрос на https://dog.ceo/api/breeds/list/all'
    r = requests.get('https://dog.ceo/api/breeds/list/all')

    # Проверка cтатус кода
    assert r.status_code == expected_code

    # Проверка схемы
    schema_dog = {
        'properties': {'message': {'type': 'object'}, 'status': {'const': 'success'}},
        "required": ["message", "status"]
    }
    validate(instance=r.json(), schema=schema_dog)


def test_random_image():

    # Выполнить запрос на https://dog.ceo/api/breeds/image/random
    r = requests.get('https://dog.ceo/api/breeds/image/random')

    # Проверка статус кода
    assert r.status_code == expected_code

    # Проверить что схема соответсвтует указанному формату:
    schema_dog = {
        'properties': {'message': {'type': 'string'}, 'status': {'const': 'success'}},
        "required": ["message", "status"]
    }
    validate(instance=r.json(), schema=schema_dog)


@pytest.mark.parametrize('number_of_images', [1, 2, 50])
def test_dog_multiple_images(number_of_images):

    # Выполнить запрос на https://dog.ceo/api/breeds/image/random/3
    uri = f'https://dog.ceo/api/breeds/image/random/{number_of_images}'
    r = requests.get(uri)

    # Проверить статус код
    assert r.status_code == expected_code

    # Проверить что схема соответсвтует указанному формату:
    schema_dog = {
        'properties': {'message': {'type': 'array'}, 'status': {'const': 'success'}},
        'required': ['message', 'status']
    }
    validate(instance=r.json, schema=schema_dog)

    # Проверить что в ответе пришло верное количество картинок
    parsed_response = r.json()
    assert len(parsed_response['message']) == number_of_images


@pytest.mark.parametrize('number_of_images', [51])
def test_dog_multiple_images_maxnumber(number_of_images):

    # Выполнить запрос на https://dog.ceo/api/breeds/image/random/3
    uri = f'https://dog.ceo/api/breeds/image/random/{number_of_images}'
    r = requests.get(uri)

    # Проверить статус код
    assert r.status_code == expected_code

    # Проверить что схема соответсвтует указанному формату:
    schema_dog = {
        'properties': {'message': {'type': 'array'}, 'status': {'const': 'success'}},
        'required': ['message', 'status']
    }
    validate(instance=r.json, schema=schema_dog)

    # Проверить что максимальное количество картинок в ответе = 50
    parsed_response = r.json()
    assert len(parsed_response['message']) == number_of_images-1


@pytest.mark.parametrize('breed', ['hound', 'akita', 'bulldog'])
def test_dog_multiple_images_by_breed(breed):

    # Выполнить запрос на https://dog.ceo/api/breed/hound/images
    uri = f'https://dog.ceo/api/breed/{breed}/images'
    r = requests.get(uri)

    # Проверить заголовки ответа
    assert r.status_code == expected_code

    # Проверить что схема соответсвтует указанному формату:
    schema_dog = {
        'properties': {'message': {'type': 'array'}, 'status': {'const': 'success'}},
        'required': ['message', 'status']
    }
    validate(instance=r.json, schema=schema_dog)

    # Проверить что в массив пришли только картинки указанной породы
    parsed_response = r.json()
    for i in parsed_response['message']:
        assert breed in i


