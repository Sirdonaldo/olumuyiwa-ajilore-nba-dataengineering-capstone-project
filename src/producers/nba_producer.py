from confluent_kafka import Producer
import json, random, time
from datetime import datetime
from fetch_players import get_nba_players, organize_by_team

def read_config():
    """Read Kafka Client configuration from client.properties"""
    config = {}
    with open("client.properties") as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.split("=", 1)
                config[parameter] = value.strip()
    return config


def produce(topic, config):
    """Produce random NBA events using real player data"""
    producer = Producer(config)

    # Fetch players from API and organize by team
    print("Fetching NBA players from API...")
    players = get_nba_players()
    teams = organize_by_team(players)
    print(f"Fetched {len(players)} players across {len(teams)} teams")

    # Define possible actions
    actions = ["2pt_shot", "3pt_shot", "assist", "rebound", "steal", "block", "turnover"]

    while True:
        # Pick a random team and player
        team = random.choice(list(teams.keys()))
        player = random.choice(teams[team])

        # Create random action (with outcome for shots)
        action = random.choice(actions)
        event = {
            "team": team,
            "player": player,
            "action": action,
            "outcome": random.choice(["made", "missed"]) if "shot" in action else None,
            "timestamp": datetime.utcnow().isoformat(),
        }

        # Convert to JSON
        value = json.dumps(event)

        # Send to Kafka
        producer.produce(topic, key=team, value=value)
        print(f"Produced: {value}")

        # Ensure delivery
        producer.flush()
        time.sleep(0.01)


def main():
    config = read_config()
    topic = "nba_events"   # keep this the same as your Kafka topic
    produce(topic, config)


if __name__ == "__main__":
    main()
