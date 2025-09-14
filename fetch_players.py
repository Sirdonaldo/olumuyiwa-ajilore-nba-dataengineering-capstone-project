import requests
import pandas as pd
from collections import defaultdict


API_KEY = "ef5b1a42-1ebf-4722-9338-196f5ba9a527"
BASE_URL = "https://api.balldontlie.io/v1/players"

def get_nba_players():
    """Fetch all NBA players from BallDontLie API (handles pagination)."""
    players = []
    page = 1
    per_page = 100  # max allowed
    headers = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}

    while True:
        url = f"{BASE_URL}?page={page}&per_page={per_page}"
        res = requests.get(url, headers=headers)

        if res.status_code != 200:
            raise Exception(f"API request failed with status {res.status_code}: {res.text[:200]}")

        data = res.json()
        players.extend(data["data"])

        # Stop if no more pages
        if not data["meta"].get("next_page"):
            break

        page += 1

    return players

def organize_by_team(players):
    """Organize players into teams using their abbreviations."""
    teams = defaultdict(list)
    for p in players:
        team = p["team"]["abbreviation"]
        name = f"{p['first_name']} {p['last_name']}"
        teams[team].append(name)
    return dict(teams)

if __name__ == "__main__":
    print("Fetching NBA players from BallDontLie API...")
    players = get_nba_players()
    teams = organize_by_team(players)

    # Save full player dataset to CSV
    df = pd.DataFrame(players)
    df.to_csv("data/players.csv", index=False)

    print(f"Saved {len(players)} players to data/players.csv")
    print(f"Found {len(teams)} teams")
    print("Sample LAL players:", teams.get("LAL", [])[:5])
