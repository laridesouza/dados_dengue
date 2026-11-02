import logging

import requests

from config import (
    API_URL,
    CITIES,
    DISEASE,
    EW_END,
    EW_START,
    EY_END,
    EY_START,
    FORMAT,
    TIMEOUT_SECONDS,
)

logger = logging.getLogger(__name__)


def fetch_city_data(geocode):

    params = {
        "geocode": geocode,
        "disease": DISEASE,
        "format": FORMAT,
        "ew_start": EW_START,
        "ew_end": EW_END,
        "ey_start": EY_START,
        "ey_end": EY_END,
    }

    response = requests.get(API_URL, params=params, timeout=TIMEOUT_SECONDS)

    response.raise_for_status()

    data = response.json()

    if not isinstance(data, list):
        raise ValueError(f"Resposta inesperada da API para o geocode {geocode}: {data}")

    if len(data) == 0:
        logger.warning("A API não devolveu nenhuma semana para o geocode %s", geocode)

    return data


def fetch_data_for_cities():

    data_by_geocode = {}

    for city_name, geocode in CITIES.items():
        logger.info("Buscando %s (geocode %s)...", city_name, geocode)
        data_by_geocode[geocode] = fetch_city_data(geocode)
        logger.info("%s: %s semanas recebidas", city_name, len(data_by_geocode[geocode]))

    return data_by_geocode