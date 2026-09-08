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

    transformed = records[selected_columns].copy()
    transformed.columns = transformed.columns.str.lower()

    identifier_columns = [
        "player_id",
        "team_id",
        "game_id",
    ]

    for column in identifier_columns:
        transformed[column] = transformed[column].astype("string")

    transformed["game_date"] = pd.to_datetime(
        transformed["game_date"],
        errors="coerce",
    )

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

    for column in numeric_columns:
        transformed[column] = pd.to_numeric(
            transformed[column],
            errors="coerce",
        )

    required_columns = [
        "player_id",
        "game_id",
        "game_date",
    ]

    null_counts = transformed[required_columns].isna().sum()

    if null_counts.any():
        raise ValueError(
            f"Required columns contain null values:\n{null_counts}"
        )

    duplicate_count = transformed.duplicated(
        subset=["game_id", "player_id"]
    ).sum()

    if duplicate_count > 0:
        raise ValueError(
            f"Found {duplicate_count} duplicate player-game records"
        )

    transformed = transformed.sort_values(
        by=["game_date", "game_id", "player_id"]
    ).reset_index(drop=True)

    return transformed