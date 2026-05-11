import requests

BASE_URL = "https://api.chess.com/pub"
HEADERS  = {"User-Agent": "all-stock-no-fish/0.1"}


def get_profile(username):
    r = requests.get(f"{BASE_URL}/player/{username}", headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()


def get_stats(username):
    r = requests.get(f"{BASE_URL}/player/{username}/stats", headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":

    results = get_profile("JammyNinja")
    print(results)
