# olumuyiwa-ajilore-nba-dataengineering-capstone-project

## 🏀 NBA Data Engineering Capstone Project

## Overview
This capstone project demonstrates how to design an end-to-end data engineering pipeline using modern tools. The goal is to show how raw NBA data can be ingested from multiple sources, transformed, validated, and surfaced as actionable insights through dashboards and conversational analytics.

This pipeline integrates two different sources and formats:
- BallDontLie API → static player data (exported to CSV).
- Confluent Kafka (Cloud) → real-time NBA event stream (JSON).

Together, these datasets exceed 1M+ rows, meeting the requirements for scale, variety, and complexity.

## Tech Stack
- Python / Pandas → data validation, schema checks
- BallDontLie API → static player data (CSV)
- Confluent Kafka (Cloud) → streaming NBA events (JSON)
- Apache Airflow (Astronomer) → ETL orchestration
- Apache Spark / Databricks → transformations, queries, persistence
- Databricks Dashboards → visualization of KPIs & insights
- Databricks Genie → conversational analytics over datasets

## Project Structure
├── data/

│   ├── players.csv       # Exported from BallDontLie API

│   └── events.json       # Exported from Confluent Kafka stream

├── dags/

│   └── nba_pipeline_dag.py   # Airflow DAG definition

├── src/

│   └── pipelines/

│       └── etl_pipeline.py   # ETL logic for events + players

├── warehouse/             # Iceberg/Parquet storage

└── README.md              # Documentation

## Architecture
<img width="1021" height="568" alt="Screenshot 2025-09-13 at 9 01 02 PM" src="https://github.com/user-attachments/assets/a50bd122-8e1c-4645-a46d-21c49a7fa1c8" />

## Data Sources
<img width="1912" height="1069" alt="image" src="https://github.com/user-attachments/assets/bc6f3357-4bf9-4369-a9bc-06a4aa9c871e" />
<img width="1908" height="1075" alt="image" src="https://github.com/user-attachments/assets/3b5b4d5b-1b73-494a-bfd3-46c8e2f8b47b" />
<img width="1912" height="1068" alt="image" src="https://github.com/user-attachments/assets/17d32e7a-4dd8-495a-8846-80a25f565d42" />

## Schema
<img width="1463" height="902" alt="image" src="https://github.com/user-attachments/assets/7af94ee0-fa2e-4637-af47-662c78bcd274" />

## Pipeline Workflow
## Deployed in Astronomer Cloud
<img width="1467" height="877" alt="Screenshot 2025-09-12 at 11 17 49 PM" src="https://github.com/user-attachments/assets/2c8ff51f-d249-4436-8631-617de047810e" />


1. Ingestion
   - Fetch NBA player data from BallDontLie API (CSV).
   - Stream NBA event data from Confluent Kafka Cloud (JSON).

2. Transformation
   - Clean and normalize schema.
   - Join player metadata with event actions.

3. Orchestration
   - Automate daily ETL runs using Airflow DAG (Astronomer).

4. Storage
   - Persist enriched data in Databricks Unity Catalog.

5. Analytics
   - Run SQL queries to calculate KPIs.
   - Build dashboards for visualization.

6. Conversational AI
   - Deploy Genie to allow natural language exploration.

## KPI's / SQL Queries Behind the Dashboard 

## Total Events Count:
SELECT COUNT(*) AS total_events
FROM tabular.dataexpert.events;

## Top 3-Point Attempts:
SELECT e.value.player, COUNT(*) AS shot_attempts
FROM tabular.dataexpert.events e
WHERE e.value.action = '3pt_shot'
GROUP BY e.value.player
ORDER BY shot_attempts DESC
LIMIT 10;

## 3-Point Shooting Efficiency:
SELECT 
  e.value.team,
  ROUND(100 * SUM(CASE WHEN e.value.outcome = 'made' THEN 1 ELSE 0 END) / COUNT(*), 2) AS success_pct
FROM tabular.dataexpert.events e
WHERE e.value.action = '3pt_shot'
GROUP BY e.value.team
ORDER BY success_pct DESC;

## Top Steals:
SELECT e.value.player, COUNT(*) AS steals
FROM tabular.dataexpert.events e
WHERE e.value.action = 'steal'
GROUP BY e.value.player
ORDER BY steals DESC
LIMIT 10;

## Top 10 Blocks:
SELECT e.value.player, COUNT(*) AS blocks
FROM tabular.dataexpert.events e
WHERE e.value.action = 'block'
GROUP BY e.value.player
ORDER BY blocks DESC
LIMIT 10;

## Players by Country:
SELECT country, COUNT(*) AS player_count
FROM tabular.dataexpert.players
GROUP BY country
ORDER BY player_count DESC;

## Visualizations

<img width="1470" height="956" alt="Screenshot 2025-09-13 at 7 53 58 PM" src="https://github.com/user-attachments/assets/55e9e4da-d35c-408a-9b02-26659ba106c5" />
<img width="1470" height="956" alt="Screenshot 2025-09-13 at 7 54 04 PM" src="https://github.com/user-attachments/assets/cd54290f-11ca-4a9f-ae2d-20ec6ec71a25" />
<img width="1470" height="956" alt="Screenshot 2025-09-13 at 7 54 11 PM" src="https://github.com/user-attachments/assets/fa8e1361-0124-45a9-b788-f847043bd608" />
<img width="1470" height="956" alt="Screenshot 2025-09-13 at 7 54 15 PM" src="https://github.com/user-attachments/assets/7d58e918-87de-4814-8b09-6040b6fb4332" />



- KPI cards (total events, total players)
- 3-point efficiency chart
- Steals leaderboard
- Blocks leaderboard
- Players by country
- Tabular player-event details

## Genie Demo Questions
- Who has the most 3-point attempts?
- Which team has the best shooting efficiency?
- Show me the top 5 players by steals
- How many NBA players are from Canada?
- Who leads in rebounds?

## Deliverables
- Automated Airflow DAG (Astronomer)
- ETL pipeline joining players + events
- Databricks SQL queries for KPIs
- Dashboards with interactive insights
- Genie for conversational analytics
- Documentation (README.md)

## Key Learnings
- Building a reproducible ETL workflow with Airflow
- Integrating API + streaming data sources
- Handling schema alignment between CSV and JSON
- Persisting and querying data with Databricks
- Enabling conversational BI with Genie


