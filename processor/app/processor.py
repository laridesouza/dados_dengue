import logging
from datetime import date

from db import connect_to_db, create_table, upsert_data
from loader import list_json_files, load_data
from transformer import transform_weeks

DATA_DIR = "/data"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    # 1. achar os arquivos brutos da extração de hoje
    today = date.today().strftime("%Y-%m-%d")
    files = list_json_files(f"{DATA_DIR}/{today}")

    if not files:
        raise FileNotFoundError(f"Nenhum JSON encontrado em {DATA_DIR}/{today}")

    # 2. ler cada arquivo e transformar em linhas de tabela
    rows = []
    for file_path in files:
        geocode = int(file_path.stem)  
        raw_data = load_data(file_path)
        rows.extend(transform_weeks(raw_data, geocode))

    logger.info("%s arquivos lidos, %s linhas prontas para carga", len(files), len(rows))

    # 3. carregar no MySQL
    db = connect_to_db()
    cursor = db.cursor()

    try:
        create_table(cursor)
        upsert_data(cursor, rows)
        db.commit()
        logger.info("Carga concluída")
    except Exception:
        db.rollback()  
        raise
    finally:
        cursor.close()
        db.close()


if __name__ == "__main__":
    main()