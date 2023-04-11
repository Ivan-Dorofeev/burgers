import requests
from geopy.distance import lonlat, distance
from geo_places.models import Address


def fetch_coordinations(address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": 'c2fb9276-ddef-49b6-84ee-79c40be0a81a',
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_distance_to_rest(rest_address, client_address):
    all_address = Address.objects.all()

    client_coordinations = [(addr.lat, addr.lon) for addr in all_address if addr.name == client_address]
    if not client_coordinations:
        client_coordinations = fetch_coordinations(client_address)
        Address.objects.create(
            name=client_address,
            lon=client_coordinations[0],
            lat=client_coordinations[1],
        )
    else:
        client_coordinations = client_coordinations[0]

    rest_coordinations = [(addr.lat, addr.lon) for addr in all_address if addr.name == rest_address]
    if not rest_coordinations:
        rest_coordinations = fetch_coordinations(rest_address)
        Address.objects.create(
            name=rest_address,
            lon=rest_coordinations[0],
            lat=rest_coordinations[1],
        )
    else:
        rest_coordinations = rest_coordinations[0]

    """Подсчитываем расстояние"""
    distance_to_rest = round(distance(lonlat(*client_coordinations), lonlat(*rest_coordinations)).km, 2)
    return distance_to_rest
