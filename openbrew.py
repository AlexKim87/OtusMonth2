import pytest
import requests
from jsonschema import validate

expected_statuscode = 200


def test_single_brewery():
    # Делаем запрос
    request = requests.get('https://api.openbrewerydb.org/breweries/madtree-brewing-cincinnati')
    # Проверяем статус-код
    assert request.status_code == expected_statuscode
    # Задаем схему для валидации
    schema = {
        'type': 'object',
        'properties': {
            'id': {'type': 'string'},
            'name': {'type': 'string'},
            'brewery_type': {'type': 'string'},
            'street': {'type': 'string'},
            'address_2': {'type': ['string', 'null']},
            'address_3': {'type': ['string', 'null']},
            'city': {'type': 'string'},
            'state': {'type': 'string'},
            'county_province': {'type': ['string', 'null']},
            'postal_code': {'type': 'string'},
            'country': {'type': 'string'},
            'longitude': {'type': 'string'},
            'latitude': {'type': 'string'},
            'phone': {'type': 'string'},
            'website_url': {'type': 'string'},
            'updated_at': {'type': 'string'},
            'created_at': {'type': 'string'},
        },
        'required': ['id', 'name', 'brewery_type', 'street', 'state', 'city']}
    # Валидируем схему
    validate(instance=request.json(), schema=schema)


@pytest.mark.parametrize('number_of_breweries', [1, 2, 3, 10, 50])
def test_brewery_list(number_of_breweries):
    # Делаем запрос
    request = requests.get(f'https://api.openbrewerydb.org/breweries?per_page={number_of_breweries}')
    # Проверяем статус-код
    assert request.status_code == expected_statuscode
    # Проверяем что количество пивнушек в ответе соответствует значению параметра per_page в урле
    assert (len(request.json())) == number_of_breweries


@pytest.mark.xfail(strict=True)
@pytest.mark.parametrize('number_of_breweries', [-1, 51])
def test_brewery_list_negative(number_of_breweries):
    # Делаем запрос
    request = requests.get(f'https://api.openbrewerydb.org/breweries?per_page={number_of_breweries}')
    # Проверяем статус-код
    assert request.status_code == expected_statuscode
    # Проверяем что количество пивнушек в ответе соответствует значению параметра per_page в урле
    assert (len(request.json())) == number_of_breweries


@pytest.mark.parametrize('city, number_of_breweries',
                         [
                             ("san_diego", 1),
                             ("san_diego", 2),
                             pytest.param("naglazievsk", 3, marks=pytest.mark.skip(reason="Just for fun"))
                         ])
def test_brewery_by_city(city, number_of_breweries):
    # Делаем запрос
    request = requests.get(f'https://api.openbrewerydb.org/breweries?by_city={city}&per_page={number_of_breweries}')
    # Проверяем статус-код
    assert request.status_code == expected_statuscode
    # Задаем схему для валидации
    schema = {
        'type': 'array',
        'items': {
            'properties': {
                'anal': {'type': 'string'},
                'id': {'type': 'string'},
                'name': {'type': 'string'},
                'brewery_type': {'type': 'string'},
                'street': {'type': 'string'},
                'address_2': {'type': ['string', 'null']},
                'address_3': {'type': ['string', 'null']},
                'city': {'type': 'string'},
                'state': {'type': 'string'},
                'county_province': {'type': ['string', 'null']},
                'postal_code': {'type': 'string'},
                'country': {'type': 'string'},
                'longitude': {'type': 'string'},
                'latitude': {'type': 'string'},
                'phone': {'type': ['string', 'null']},
                'website_url': {'type': ['string', 'null']},
                'updated_at': {'type': 'string'},
                'created_at': {'type': 'string'}},
            "required": ["id", "name", "brewery_type", "street", "state", "city"]
        }}
    # Валидируем схему
    validate(instance=request.json(), schema=schema)
    assert (len(request.json())) == number_of_breweries


@pytest.mark.parametrize('para', ['dog', 'pasta'])
def test_brewery_search_autocomplete(para):
    # Делаем запрос
    request = requests.get(f'https://api.openbrewerydb.org/breweries/autocomplete?query={para}')
    # Проверяем статус-код
    assert request.status_code == expected_statuscode
    # Задаем схему
    schema = {
        'type': 'array',
        'items': {
            'properties': {
                'id': {'type': 'string'},
                'name': {'type': 'string'}},
            "required": ["id", "name"]
            }}
    # Валидируем схему
    validate(instance=request.json(), schema=schema)


