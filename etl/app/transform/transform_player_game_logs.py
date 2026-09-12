import pandas as pd

#Transformed function
def transform_player_game_logs(records):
    # Commit 1: Define and validate the source schema.
    #\Defines the columns required from the source from player info to game info. 
    # These are the fields that the transformation expects
    
    
    selected_columns = [
        "SEASON_YEAR",
        "PLAYER_ID",
        "PLAYER_NAME",
        "TEAM_ID",
        "TEAM_ABBREVIATION",
        "TEAM_NAME",
        "GAME_ID",
        "GAME_DATE",
        "MATCHUP",
        "WL",
        "MIN",
        "PTS",
        "REB",
        "AST",
        "STL",
        "BLK",
        "TOV",
        "FGM",
        "FGA",
        "FG_PCT",
        "FG3M",
        "FG3A",
        "FG3_PCT",
        "FTM",
        "FTA",
        "FT_PCT",
        "PLUS_MINUS",
    ]
    #Missing columns compares the required columns with record.columns and converting both into a set to find the required columsn that are missing 
    missing_columns = set(selected_columns) - set(records.columns)
    #if columns are missing raise a ValueError and return error message 
    if missing_columns:
        raise ValueError(
            f"Source data is missing columns: {sorted(missing_columns)}"
        )

    #Create a new DataFrame called transformed this holds the columns listed in Selected Columns
    #The columns are copied adn then copied to ensure that we're working with an independent copy of data. 
    transformed = records[selected_columns].copy()
    #Column names are then converted to lowercase so the rest of the pipeline can use consistent naming 
    transformed.columns = transformed.columns.str.lower()
    #Primary key columns : player id, team id, and game id 
    
    identifier_columns = [
        "player_id",
        "team_id",
        "game_id",
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

    numeric_columns = [
        "min",
        "pts",
        "reb", 
        "ast",
        "stl",
        "blk", 
        "tov", 
        "fgm",
        "fga",
        "fg_pct", 
        "fg3m", 
        "fg3a", 
        "fg3_pct",
        "ftm",
        "fta",
        "ft_pct",
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
    
    

