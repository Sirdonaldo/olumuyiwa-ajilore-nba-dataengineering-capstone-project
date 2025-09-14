from pyspark.sql import SparkSession
from pyspark.sql.functions import col, monotonically_increasing_id

# Initialize Spark with Iceberg support
spark = (
    SparkSession.builder
    .appName("NBA Capstone - Save Fact Table")
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
    .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog")
    .config("spark.sql.catalog.local.type", "hadoop")
    .config("spark.sql.catalog.local.warehouse", "warehouse/iceberg")
    .getOrCreate()
)

# Path to raw parquet produced by nba_consumer
input_path = "data/raw/nba_events.parquet"

# Read raw events
df = spark.read.parquet(input_path)

print("Sample of raw events:")
df.show(5, truncate=False)

# Add event_id (unique key)
df_fact = (
    df.withColumn("event_id", monotonically_increasing_id())
      .select(
          col("event_id"),
          col("timestamp").alias("event_time"),
          col("team").alias("team_id"),       # placeholder until we build teams_dim
          col("player").alias("player_id"),   # placeholder until we build players_dim
          col("action"),
          col("outcome")
      )
)

# Save to Iceberg fact table
fact_table = "local.db.nba_events_fact"
df_fact.writeTo(fact_table).createOrReplace()

print(f"Fact table created at {fact_table}")

# Example query
spark.sql(f"""
    SELECT action, COUNT(*) as cnt
    FROM {fact_table}
    GROUP BY action
    ORDER BY cnt DESC
    LIMIT 10
""").show()
