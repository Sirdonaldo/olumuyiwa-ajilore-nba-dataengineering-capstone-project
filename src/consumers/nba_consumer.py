import json
from confluent_kafka import Consumer
import os

# Kafka configuration
conf = {
    'bootstrap.servers': "pkc-6192s.us-east1.gcp.confluent.cloud:9092",
    'security.protocol': "SASL_SSL",
    'sasl.mechanisms': "PLAIN",
    'sasl.username': "VJKWCDBIDE8G6IN",
    'sasl.password': "cfltBYT3Q+NAarLW4gWf6BFUy8ZedvkTfBJqsytEHNaetyu/z97D6LcJBUEdqhug",
    'group.id': 'nba-consumers',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(["nba_events"])  # topic name

# File to save events
os.makedirs("data", exist_ok=True)
output_file = "data/events.json"

print("Listening for NBA events...")

with open(output_file, "a") as f:  # append mode so it keeps growing
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        event = msg.value().decode("utf-8")
        print("Received:", event)  # still print for visibility

        try:
            parsed = json.loads(event)
            f.write(json.dumps(parsed) + "\n")  # newline-delimited JSON
        except Exception as e:
            print("Could not parse message:", e)


