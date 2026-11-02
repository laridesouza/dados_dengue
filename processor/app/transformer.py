from datetime import datetime, timezone

def ms_to_date(milliseconds):
    return datetime.fromtimestamp(milliseconds / 1000, tz=timezone.utc).date()

def to_int(value):
    return int(float(value)) if value is not None else None

def to_float(value):
    return float(value) if value is not None else None

def transform_week(record, geocode):
    return {
        "geocode": geocode,
        "city_name": record.get("municipio_nome"),
        "epi_week": record["SE"],                       
        "week_start_date": ms_to_date(record["data_iniSE"]),
        "cases": record.get("casos"),
        "estimated_cases": record.get("casos_est"),
        "incidence_100k": record.get("p_inc100k"),
        "alert_level": record.get("nivel"),
        "population": to_int(record.get("pop")),
        "temp_avg": to_float(record.get("tempmed")),
        "humidity_avg": to_float(record.get("umidmed")),
    }


def transform_weeks(raw_data, geocode):
    return [transform_week(record, geocode) for record in raw_data]