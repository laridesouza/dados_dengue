import logging

from data_extractor import fetch_data_for_cities
from file_writer import save_data_to_file

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    
    data_by_geocode = fetch_data_for_cities()

    for geocode, data in data_by_geocode.items():
        save_data_to_file(geocode, data)

    logger.info("Extração finalizada: %s cidades salvas", len(data_by_geocode))


if __name__ == "__main__":
    main()