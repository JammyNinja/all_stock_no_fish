import requests
import os
from google.cloud import bigquery
from datetime import datetime, timezone


from bq_schemas import GAMES_RAW_SCHEMA, FETCHED_ARCHIVES_SCHEMA
from utils import flatten_raw_chesscom_game

BASE_URL = "https://api.chess.com/pub"
HEADERS  = {"User-Agent": "all-stock-no-fish/0.1"}
GCP_PROJECT = os.environ.get("GCP_PROJECT_ID")

def get_profile(username):
    r = requests.get(f"{BASE_URL}/player/{username}", headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()

def get_stats(username):
    r = requests.get(f"{BASE_URL}/player/{username}/stats", headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()

def fetch_and_store_all_raw_games(username):
    #call api to see all available archives (months where user has played a game)
    #result is a list of links like: https://api.chess.com/pub/player/jammyninja/games/2011/03

    #checks for pre-fetched ones, excluding current month
    archives_to_fetch = get_archives_to_fetch(username)
    #loop through archive, collect all games
    print(f"found {len(archives_to_fetch)} archives to fetch")
    BATCH_SIZE = 1000

    batch = []
    fetched_archive_urls = []
    for i, url in enumerate(archives_to_fetch):
        games = fetch_archive(url)
        batch.extend([flatten_raw_chesscom_game(g,url) for g in games])
        fetched_archive_urls.append(url)

        if len(batch) >= BATCH_SIZE:
            store_raw_games_in_bq(batch)
            mark_archives_as_fetched(username, fetched_archive_urls)
            batch = []
            fetched_archive_urls = []

    if batch:
        store_raw_games_in_bq(batch)
        mark_archives_as_fetched(username, fetched_archive_urls)

def get_all_archives_from_chess_com(username):
    r = requests.get(
        f"{BASE_URL}/player/{username}/games/archives",
        headers=HEADERS,
        timeout=10
    )
    r.raise_for_status()
    all_archive_urls = r.json().get("archives", [])
    return all_archive_urls

def get_archives_to_fetch(username: str) -> list[str]:
    #get all possible months
    all_archive_urls = get_all_archives_from_chess_com(username)

    #get pre fetched months
    try:
        client = bigquery.Client(project=GCP_PROJECT)
        query = f"""
            SELECT archive_url FROM `{GCP_PROJECT}.chess_com_games.fetched_archives`
            WHERE username = '{username}'
        """
        already_fetched_urls = {row.archive_url for row in client.query(query).result()}
    except:
        already_fetched_urls = set()

    current_month = datetime.now(timezone.utc).strftime("%Y/%m")

    return [
        url for url in all_archive_urls
        if url not in already_fetched_urls or current_month in url
    ]

def fetch_archive(url):
    print(f"Fetching archive {url}")
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    games = r.json().get("games", [])
    return games

def mark_archives_as_fetched(username: str, archive_urls: list[str]) -> None:
    PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
    DATASET_ID = "chess_com_games"
    TABLE_ID   = "fetched_archives"
    client = bigquery.Client(project=PROJECT_ID)
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    rows = [
        {
            "username": username,
            "archive_url": url,
            "fetched_at": datetime.now(timezone.utc).isoformat()
        }
        for url in archive_urls
    ]

    job_config = bigquery.LoadJobConfig(
        schema=FETCHED_ARCHIVES_SCHEMA,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )

    job = client.load_table_from_json(
        rows,
        table_ref,
        job_config=job_config
    )
    result = job.result()
    print(f"Loaded {result.output_rows} rows into {result.destination}")


def store_raw_games_in_bq(games):
    #games is a list of dict - should be flattened by flatten func in utils
    PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
    DATASET_ID = "chess_com_games"
    TABLE_ID   = "raw_games"

    client = bigquery.Client(project=PROJECT_ID)
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    job_config = bigquery.LoadJobConfig(
        schema=GAMES_RAW_SCHEMA,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )

    job = client.load_table_from_json(
        games,
        table_ref,
        job_config=job_config
    )
    result = job.result()
    print(f"Loaded {result.output_rows} rows into {result.destination}")


def test_bq():
    creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", None)
    print(creds)

    client = bigquery.Client(project=GCP_PROJECT)
    datasets = client.list_datasets()
    print("datasets available:")
    return [ds.dataset_id for ds in datasets]

if __name__ == "__main__":
    # from dev import recreate_tables
    # recreate_tables()

    username='JammyNinja'
    # test_bq()
    # results = get_profile(username)
    # print(results)
    fetch_and_store_all_raw_games(username)
