from google.cloud import bigquery

FETCHED_ARCHIVES_SCHEMA = [
    bigquery.SchemaField("username",    "STRING"),
    bigquery.SchemaField("archive_url", "STRING"),
    bigquery.SchemaField("fetched_at",  "TIMESTAMP"),
]

GAMES_RAW_SCHEMA = [
    bigquery.SchemaField("uuid",            "STRING"),
    bigquery.SchemaField("white_username",  "STRING"),
    bigquery.SchemaField("black_username",  "STRING"),
    bigquery.SchemaField("time_class",      "STRING"),
    bigquery.SchemaField("time_control",    "STRING"),
    bigquery.SchemaField("rated",           "BOOLEAN"),
    bigquery.SchemaField("white_rating",    "INTEGER"),
    bigquery.SchemaField("black_rating",    "INTEGER"),
    bigquery.SchemaField("white_result",    "STRING"),
    bigquery.SchemaField("black_result",    "STRING"),
    bigquery.SchemaField("eco",             "STRING"),
    bigquery.SchemaField("pgn",             "STRING"),
    bigquery.SchemaField("url",             "STRING"),
    bigquery.SchemaField("archive_url",     "STRING"),
    bigquery.SchemaField("start_time",      "INTEGER"),
    bigquery.SchemaField("end_time",        "INTEGER"),
    bigquery.SchemaField("fen",             "STRING"),
    bigquery.SchemaField("white_uuid",      "STRING"),
    bigquery.SchemaField("black_uuid",      "STRING"),
    bigquery.SchemaField("rules",           "STRING"),
]
