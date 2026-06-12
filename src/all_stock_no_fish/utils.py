def flatten_raw_chesscom_game(game: dict, archive_url) -> dict:
    return {
        "uuid":             game.get("uuid"),
        "url":              game.get("url"),
        "pgn":              game.get("pgn"),
        "time_control":     game.get("time_control"),
        "time_class":       game.get("time_class"),
        "start_time":       game.get("start_time"),
        "end_time":         game.get("end_time"),
        "rated":            game.get("rated"),
        "rules":            game.get("rules"),
        "eco":              game.get("eco"),

        "white_username":   game.get("white", {}).get("username"),
        "white_uuid":       game.get("white", {}).get("uuid"),
        "white_rating":     game.get("white", {}).get("rating"),
        "white_result":     game.get("white", {}).get("result"),

        "black_username":   game.get("black", {}).get("username"),
        "black_uuid":       game.get("black", {}).get("uuid"),
        "black_rating":     game.get("black", {}).get("rating"),
        "black_result":     game.get("black", {}).get("result"),

        "fen":              game.get("fen"),
        "archive_url":      archive_url,
    }
