from pathlib import Path
from datetime import datetime, timezone
from nba_api.stats.endpoints import playercareerstats
import pandas as pd
from nba_api.stats.endpoints import playergamelogs
from requests import RequestException

RAW_DATA_DIRECTORY = Path("data/raw")
def extract_player_games_log( 
     season: str = "2024-2025",
     season_type: str = "Regular-Season"
 ) ->pd.DataFrame:
    
    print(f"Pulling NBA player game logs for {season} - {season_type}...")

    logs = playergamelogs.PlayerGameLogs()
def extract_player_games_log(season):
    response = playergamelogs.PlayerGameLogs(
        season_nullable = season, 
        season_type_nullable = "Regular Season", 
        timeout = 60, 

    )
    return response
    

def save_raw_response(response, season):
    RAW_DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"player_game_logs_{season}_{timestamp}.json"
    output_path = RAW_DATA_DIRECTORY / filename

    output_path.write_text(
        response.get_response(),
        encoding="utf-8",
    )

    return output_path
def main(): 
    season = "2025-26"

    try:
        response = extract_player_games_log(season)
        records = response.player_game_logs.get_data_frame()

        if records.empty:
            raise ValueError("NBA API returned zero player-game records")

        output_path = save_raw_response(response, season)

        print("Request successful")
        print(f"Extracted {len(records)} player-game records")
        print(f"Raw response saved to {output_path}")

    except RequestException as error:
        print(f"NBA API request failed: {error}")
        raise

    except ValueError as error:
        print(f"NBA API data validation failed: {error}")
        raise


if __name__ == "__main__":
    main()

                          
                            