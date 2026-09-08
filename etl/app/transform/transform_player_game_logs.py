def transform_player_game_logs(records):
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

    missing_columns = set(selected_columns) - set(records.columns)

    if missing_columns:
        raise ValueError(
            f"Source data is missing columns: {sorted(missing_columns)}"
        )