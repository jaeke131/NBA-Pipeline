from pathlib import Path
from datetime import datetime, timezone
from nba_api.stats.endpoints import playercareerstats
import pandas as pd
from nba_api.stats.endpoints import playergamelogs
from requests import RequestException
RAW_DATA_DIR = ("etl/data/raw")
RAW_DATA_DIRECTORY = Path("data/raw")
def extract_player_games_log( 
     season: str = "2024-2025",
     season_type: str = "Regular-Season"
 ) ->pd.DataFrame:
    
    print(f"Pulling NBA player game logs for {season} - {season_type}...")

    logs = playergamelogs.PlayerGameLogs(
def extract_player_games_log(season):
    response = playergamelogs.PlayerGameLogs(
        season_nullable = season, 
        season_type_nullable = "Regular Season", 
        timeout = 60, 

    )
    return response
    
    print(f"Saved {len(df)} rows to {output_path}")
    
    return df 

if __name__ == "__main__":
    extract_player_game_logs()

                          
                            