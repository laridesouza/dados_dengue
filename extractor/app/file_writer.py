import json
import logging
import os
from datetime import date

from config import OUTPUT_DIR

logger = logging.getLogger(__name__)


def save_data_to_file(geocode, data):

    today = date.today().strftime("%Y-%m-%d")
    folder = os.path.join(OUTPUT_DIR, today)
    os.makedirs(folder, exist_ok=True)

    file_path = os.path.join(folder, f"{geocode}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    logger.info("Arquivo salvo: %s", file_path)
    return file_path