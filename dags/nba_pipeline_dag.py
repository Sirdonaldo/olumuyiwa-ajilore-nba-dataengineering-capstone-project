from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "donaldson",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "nba_pipeline",
    default_args=default_args,
    description="NBA Events + Players ETL",
    schedule_interval="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:

    fetch_players = BashOperator(
        task_id="fetch_players",
        bash_command="python3 /usr/local/airflow/src/producers/fetch_players.py",
    )

    fetch_events = BashOperator(
        task_id="fetch_events",
        bash_command="python3 /usr/local/airflow/src/producers/nba_producer.py",
    )

    run_etl = BashOperator(
        task_id="run_etl",
        bash_command="python3 /usr/local/airflow/src/pipelines/etl_pipeline.py",
    )

    [fetch_players, fetch_events] >> run_etl
