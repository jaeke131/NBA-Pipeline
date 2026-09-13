from etl.app.extract.extract_player_game_logs import extract_player_game_logs
from etl.app.transform.transform_player_game_logs import transform_player_game_logs
from etl.app.load.create_tables import create_tables
from etl.app.load.load_player_game_logs import load_player_game_logs


def run_pipeline() -> None:
    extract_player_game_logs()
    transform_player_game_logs()
    create_tables()
    load_player_game_logs()


if __name__ == "__main__":
    run_pipeline()