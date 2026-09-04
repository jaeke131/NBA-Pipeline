from pathlib import Path

import pandas as pd
from nba_api.stats.endpoints import playergamelogs

RAW_DATA_DIR = ("etl/data/raw")

def extract_player_games_log( 
     season: str = "2024-2025",
     season_type: str = "Regular-Season"
 ) ->pd.DataFrame:
    
    print(f"Pulling NBA player game logs for {season} - {season_type}...")

    logs = playergamelogs.PlayerGameLogs(
        season_nullable=season,
        season_type_nullable=season_type,
        timeout=60
    )      
    df = logs.get_data_frames()[0]
    
    output_path = RAW_DATA_DIR / f"player_game_logs_{season.replace('-', '_')}.csv" 
    df.to_csv(output_path, index = False) 
    
    print(f"Saved {len(df)} rows to {output_path}")
    
    return df 

if __name__ == "__main__":
    extract_player_game_logs()

                          
                            