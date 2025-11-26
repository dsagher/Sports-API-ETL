from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow import DAG
from api.etl import etl


def run_etl_task(**context):
    """Wrapper function to call etl with required arguments"""
    
    league_id = context['league_id']
    season_year = context['season_year']
    etl(league_id, season_year)


default_args = {
    "depends_on_past": True,  # Each run waits for previous to complete
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "sports_api",
    default_args=default_args,
    description="Main default 482 Final Dag",
    schedule=timedelta(days=1),
    start_date=datetime(2024, 1, 1),  # Fixed start date (not datetime.now())
    stop_date=datetime(2025, 12, 15),
    catchup=True,  # Process all intervals sequentially
    max_active_runs=1,  # Only one DAG run at a time (ensures sequential execution)
    tags=["etl", "sports"]
) as dag:
    t1 = PythonOperator(
        task_id="run_etl",
        python_callable=run_etl_task,
    )
    