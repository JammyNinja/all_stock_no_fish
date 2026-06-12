import requests
import os
from google.cloud import bigquery


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

def test_bq():
    creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", None)
    print(creds)

    client = bigquery.Client(project=GCP_PROJECT)
    datasets = client.list_datasets()
    print("datasets available:")
    return [ds.dataset_id for ds in datasets]


if __name__ == "__main__":
    test_bq()
    # results = get_profile("JammyNinja")
    # print(results)
