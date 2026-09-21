from pathlib import Path
import json

import pandas as pd


RAW_DATA_DIRECTORY = Path("etl/app/data/raw")
PROCESSED_DATA_DIRECTORY = Path("etl/app/data/processed")


COLUMN_RENAMES = {
    "SEASON_YEAR": "season_year",
    "PLAYER_ID": "player_id",
    "PLAYER_NAME": "player_name",
    "TEAM_ID": "team_id",
    "TEAM_ABBREVIATION": "team_abbreviation",
    "GAME_ID": "game_id",
    "GAME_DATE": "game_date",
    "MATCHUP": "matchup",
    "WL": "wl",
    "MIN": "minutes",
    "PTS": "points",
    "REB": "rebounds",
    "AST": "assists",
    "STL": "steals",
    "BLK": "blocks",
    "TOV": "turnovers",
    "FGM": "field_goals_made",
    "FGA": "field_goals_attempted",
    "FG_PCT": "field_goal_pct",
    "FG3M": "three_pointers_made",
    "FG3A": "three_pointers_attempted",
    "FG3_PCT": "three_point_pct",
    "FTM": "free_throws_made",
    "FTA": "free_throws_attempted",
    "FT_PCT": "free_throw_pct",
    "PLUS_MINUS": "plus_minus",
}


def get_latest_raw_file() -> Path:
    raw_files = list(RAW_DATA_DIRECTORY.glob("player_game_logs_*.json"))

    if not raw_files:
        raise FileNotFoundError(
            f"No raw player game log JSON files found in {RAW_DATA_DIRECTORY}"
        )

    return max(raw_files, key=lambda file: file.stat().st_mtime)


def build_dataframe_from_raw_json(raw_data) -> pd.DataFrame:
    if isinstance(raw_data, list):
        return pd.DataFrame(raw_data)

    if not isinstance(raw_data, dict):
        raise ValueError("Raw JSON format is not supported.")

    if "headers" in raw_data and "rowSet" in raw_data:
        return pd.DataFrame(raw_data["rowSet"], columns=raw_data["headers"])

    if "data" in raw_data and isinstance(raw_data["data"], list):
        return pd.DataFrame(raw_data["data"])

    if "resultSets" in raw_data:
        result_sets = raw_data["resultSets"]

        if isinstance(result_sets, list) and len(result_sets) > 0:
            first_result_set = result_sets[0]

            if "headers" in first_result_set and "rowSet" in first_result_set:
                return pd.DataFrame(
                    first_result_set["rowSet"],
                    columns=first_result_set["headers"],
                )

    raise ValueError(
        f"Could not find headers/rowSet data in raw JSON. Top-level keys: {list(raw_data.keys())}"
    )


def transform_player_game_logs() -> pd.DataFrame:
    raw_file = get_latest_raw_file()

    print(f"Transforming raw file: {raw_file}")

    with open(raw_file, "r", encoding="utf-8") as file:
        raw_data = json.load(file)

    df = build_dataframe_from_raw_json(raw_data)

    print(f"Raw rows: {len(df)}")
    print(f"Raw columns: {list(df.columns)}")

    df = df.rename(columns=COLUMN_RENAMES)

    columns_to_keep = [
        column for column in COLUMN_RENAMES.values()
        if column in df.columns
    ]
    #iterate through the primary keys and transform the data type of the id columns to string 
    for column in identifier_columns:
        transformed[column] = transformed[column].astype("string")
    #Converts the game date column to datetime values. Prevents invalid dates from raising an excption instead of invaliding or missing data. 
    transformed["game_date"] = pd.to_datetime(
        transformed["game_date"],
        errors="coerce",
    )
    #Take the statistical columns and convert the data types of them to clean numerica pandas data type 

    df = df[columns_to_keep].copy()

    if "game_date" in df.columns:
        df["game_date"] = pd.to_datetime(df["game_date"], errors="coerce").dt.date

    numeric_columns = [
        "minutes",
        "points",
        "rebounds",
        "assists",
        "steals",
        "blocks",
        "turnovers",
        "field_goals_made",
        "field_goals_attempted",
        "field_goal_pct",
        "three_pointers_made",
        "three_pointers_attempted",
        "three_point_pct",
        "free_throws_made",
        "free_throws_attempted",
        "free_throw_pct",
        "plus_minus",
    ]
    #Iterate through the numeric columns to convert to pandas data type numeric. Any invalid data that comes throws an error coerce 
    
    for column in numeric_columns: 
        transformed[column] = pd.to_numeric( 
            transformed[column],
            errors = "coerce"
        )
    #
    required_columns = [ 
        "player_id", 
        "game_id", 
        "game_date", 
    
    ]
    null_counts = transformed[required_columns].isna.sum() 
    
    if null_counts.any(): 
        raise ValueError("Required columns contain null values\n{null_counts}"
        
        )
    
    duplicate_count = transformed.duplicated(
        subset = ["game_id", "player_id"]).sum()
    
    

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.drop_duplicates()

    PROCESSED_DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)

    output_path = PROCESSED_DATA_DIRECTORY / "player_game_logs_cleaned.csv"
    df.to_csv(output_path, index=False)

    print(f"Transformed {len(df)} player-game records")
    print(f"Cleaned CSV saved to {output_path}")
    print(f"Cleaned columns: {list(df.columns)}")

    return df


if __name__ == "__main__":
    transform_player_game_logs()