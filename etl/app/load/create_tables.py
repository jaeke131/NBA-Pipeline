from pathlib import Path

from etl.app.db.connection import engine


SCHEMA_PATH = Path(__file__).resolve().parents[1] / "db" / "schema.sql"


def create_tables() -> None:
    """
    Create the Postgres tables needed for the ETL pipeline.
    """

    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        schema_sql = file.read()

    with engine.begin() as connection:
        connection.exec_driver_sql(schema_sql)

    print("Postgres tables created successfully.")


if __name__ == "__main__":
    create_tables()