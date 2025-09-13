# olumuyiwa-ajilore-nba-dataengineering-capstone-project

🏀 NBA Data Engineering Capstone Project
📌 Overview

This project builds an end-to-end data pipeline for NBA player and event data. The pipeline ingests, transforms, and analyzes data using Astronomer (Airflow), Databricks, and Genie, producing actionable insights through automated ETL and dashboards.

⚙️ Tech Stack

Python / Pandas → Initial validation & schema checks

Apache Airflow (Astronomer Runtime) → ETL orchestration

Databricks SQL / Spark → Storage, transformations, and queries

Databricks Dashboards → Visualizations (3pt shooting, steals, rebounds, blocks, etc.)

Databricks Genie → Conversational analytics on datasets

📂 Project Structure
├── data/
│   ├── players.csv       # Static player data (BallDontLie API export)
│   └── events.json       # Kafka-exported NBA event data
├── dags/
│   └── nba_pipeline_dag.py   # Airflow DAG definition
├── src/
│   └── pipelines/
│       └── etl_pipeline.py   # ETL logic for events + players
├── warehouse/             # Iceberg/Parquet storage
└── README.md              # Project documentation

🔄 Pipeline Workflow

Ingest → Load players.csv (static) and events.json (streaming export).

Transform → Clean + join events with player metadata.

Orchestrate → Airflow DAG runs ETL daily.

Store → Save enriched events in Databricks (Unity Catalog).

Analyze → SQL queries power dashboards & Genie insights.

🚀 How to Run
1️⃣ Setup

Clone repo:

git clone <your_repo>
cd nba-dataengineering-capstone


Install dependencies:

pip install -r requirements.txt

2️⃣ Run Airflow DAG (Astronomer)
astro dev start


Access Airflow UI → http://localhost:8081

Enable and trigger nba_pipeline_dag

3️⃣ Databricks Integration

Upload players.csv + events.json to Databricks catalog.

Run SQL queries (see /notebooks).

4️⃣ Dashboards & Genie

Open Databricks → Dashboards → NBA Insights Dashboard

Use Genie → Query datasets in natural language.

📊 Visualizations (Examples)

3-Point Shooting Efficiency by team

Top Steals by player

Top 10 Rebounders (donut chart)

Blocks Leaders

Player counts by country

Total event volume (KPI card)

(Insert screenshots here)

🤖 Genie Insights

Examples of natural language queries powered by Genie:

“Who has the most steals?”

“Show me 3-point efficiency by player.”

“How many players are from Canada?”

✅ Deliverables

Automated Airflow DAG for ETL

Databricks SQL Dashboard with NBA insights

Genie conversational analytics

Documentation (this README)

🎯 Key Learnings

Building reproducible pipelines with Airflow

Combining static + streaming datasets

Running analytics in Databricks SQL & Dashboards

Enhancing exploration with Genie
