import os
import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
    )

def create_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dengue_weekly (
        geocode INT NOT NULL,
        epi_week INT NOT NULL,
        city_name VARCHAR(100),
        week_start_date DATE,
        cases INT,
        estimated_cases DOUBLE,
        incidence_100k DOUBLE,
        alert_level TINYINT,
        population INT,
        temp_avg DOUBLE,
        humidity_avg DOUBLE,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (geocode, epi_week)
    )
    """)

UPSERT_SQL = """
INSERT INTO dengue_weekly (
    geocode, epi_week, city_name, week_start_date, cases, estimated_cases,
    incidence_100k, alert_level, population, temp_avg, humidity_avg
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) AS incoming
ON DUPLICATE KEY UPDATE
    city_name = incoming.city_name,
    week_start_date = incoming.week_start_date,
    cases = incoming.cases,
    estimated_cases = incoming.estimated_cases,
    incidence_100k = incoming.incidence_100k,
    alert_level = incoming.alert_level,
    population = incoming.population,
    temp_avg = incoming.temp_avg,
    humidity_avg = incoming.humidity_avg
"""

def upsert_data(cursor, rows):
    for row in rows:
        cursor.execute(UPSERT_SQL, (
            row["geocode"],
            row["epi_week"],
            row["city_name"],
            row["week_start_date"],
            row["cases"],
            row["estimated_cases"],
            row["incidence_100k"],
            row["alert_level"],
            row["population"],
            row["temp_avg"],
            row["humidity_avg"],
        ))