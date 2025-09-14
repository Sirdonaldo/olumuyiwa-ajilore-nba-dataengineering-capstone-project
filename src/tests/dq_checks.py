import pandas as pd
import os
import json

# Paths
players_csv = "data/players.csv"
events_json = "data/events.json"

# --- Check players.csv ---
def check_players_data():
    print("\n--- Checking players.csv ---")
    df = pd.read_csv(players_csv)

    print(f"Row count: {len(df)}")
    print("Null values:\n", df.isnull().sum())
    print(f"Duplicate rows: {df.duplicated().sum()}")

    required_cols = {"id", "first_name", "last_name", "team_abbreviation"}
    missing = required_cols - set(df.columns)
    if missing:
        print("Missing columns:", missing)
    else:
        print("All required columns present")


# --- Check events.json ---
def check_events_data():
    print("\n--- Checking events.json ---")

    # Load raw JSON lines
    with open(events_json, "r") as f:
        raw = [json.loads(line) for line in f]

    # If "value" exists, flatten it into columns
    if "value" in raw[0]:
        events = pd.json_normalize([r["value"] for r in raw])
    else:
        events = pd.json_normalize(raw)

    print(f"Row count: {len(events)}")
    print("Null values:\n", events.isnull().sum())
    print(f"Duplicate rows: {events.duplicated().sum()}")

    required_cols = {"team", "player", "action", "timestamp"}
    missing = required_cols - set(events.columns)
    if missing:
        print("Missing columns:", missing)
    else:
        print("All required columns present")


if __name__ == "__main__":
    if os.path.exists(players_csv):
        check_players_data()
    else:
        print("players.csv not found")

    if os.path.exists(events_json):
        check_events_data()
    else:
        print("events.json not found")
