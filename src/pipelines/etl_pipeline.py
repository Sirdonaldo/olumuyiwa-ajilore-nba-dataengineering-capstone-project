import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# 1. Initialize Spark
spark = (
    SparkSession.builder
    .appName("NBA_ETL_Pipeline")
    .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog")
    .config("spark.sql.catalog.local.type", "hadoop")
    .config("spark.sql.catalog.local.warehouse", "warehouse")
    .getOrCreate()
)

# 2. Paths
players_csv = "data/players.csv"     # BallDontLie players
events_path = "data/events.json"     # Kafka-exported events
output_path = "warehouse/nba_iceberg"  # Iceberg/Parquet warehouse

# 3. Load static players data
players_df = spark.read.csv(players_csv, header=True, inferSchema=True)

print("Players schema:")
players_df.printSchema()

# Handle different possible column names
if "team_abbreviation" in players_df.columns:
    players_df = players_df.select(
        col("id").alias("player_id"),
        col("first_name"),
        col("last_name"),
        col("team_abbreviation").alias("team")
    )
elif "team" in players_df.columns:  # if CSV had team as flat string
    players_df = players_df.select(
        col("id").alias("player_id"),
        col("first_name"),
        col("last_name"),
        col("team")
    )
else:
    players_df = players_df.select(
        col("id").alias("player_id"),
        col("first_name"),
        col("last_name")
    )

# 4. Load events data
raw_df = spark.read.json(events_path)

events_df = (
    raw_df.selectExpr("CAST(value AS STRING) as json")
          .selectExpr(
              "from_json(json, 'team STRING, player STRING, action STRING, outcome STRING, timestamp STRING') as data"
          )
          .select("data.*")
)

# 5. Clean up schema
events_df = events_df.select(
    col("team"),
    col("player"),
    col("action"),
    col("outcome"),
    col("timestamp")
)

# 6. Join on player name
joined_df = events_df.join(
    players_df,
    (events_df.player.contains(players_df.first_name)) |
    (events_df.player.contains(players_df.last_name)),
    "left"
)

# 7. Write to Iceberg (persistent format)
(
    joined_df.write
    .format("iceberg")
    .mode("overwrite")
    .save("local.nba.enriched_events")
)

print("ETL completed. Data saved to Iceberg at:", output_path)
