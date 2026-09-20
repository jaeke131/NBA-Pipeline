import argparse
from pathlib import Path

from etl.app.extract.extract_player_game_logs import extract_player_games_log
from etl.app.transform.transform_player_game_logs import transform_player_game_logs
from etl.app.load.create_tables import create_tables
from etl.app.load.load_player_game_logs import load_player_game_logs

def main():
    parser = argparse.ArgumentParser(description="Run NBA ETL pipeline")
    parser.add_argument("--season", default="2025-26")
    parser.add_argument(
        "--output-file",
        default="etl/app/data/processed/player_game_logs_cleaned.csv",
    )
    parser.add_argument("--table-name", default="fact_player_game_logs")
    args = parser.parse_args()

    response = extract_player_games_log(args.season)
    raw_df = response.player_game_logs.get_data_frame()

    if raw_df.empty:
        raise ValueError("NBA API returned zero player-game records")

    transformed_df = transform_player_game_logs(raw_df)

    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    transformed_df.to_csv(output_path, index=False)

    create_tables()
    load_player_game_logs(
        file_name=output_path.name,
        table_name=args.table_name,
    )

if __name__ == "__main__":
    main()