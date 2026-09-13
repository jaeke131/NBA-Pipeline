from pathlib import Path

import pandas as pd

from etl.app.db.connection import engine


PROCESSED_DATA_DIRECTORY = Path("etl/app/data/processed")


def load_player_game_logs(
    file_name: str = "player_game_logs_cleaned.csv",
    table_name: str = "fact_player_game_logs",
) -> None:
    file_path = PROCESSED_DATA_DIRECTORY / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"Could not find processed file: {file_path}")

    df = pd.read_csv(file_path)

    print(f"Loading {len(df)} rows into {table_name}...")

    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False,
    )

    print(f"Loaded {len(df)} rows into {table_name} successfully.")


if __name__ == "__main__":
    load_player_game_logs()