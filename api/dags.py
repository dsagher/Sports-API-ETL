from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.models.param import Param
from airflow import DAG
from api.etl import etl


default_args = {
    "depends_on_past": True, 
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "sports_api",
    default_args=default_args,
    description="Main default 482 Final Dag",
    schedule=timedelta(days=1),
    start_date=datetime(2024, 1, 1),  
    catchup=True, 
    max_active_runs=1, 
    tags=["etl", "sports"]
) as dag:
    t1 = PythonOperator(
        task_id="run_etl",
        python_callable=etl,
        op_args= [39,2022]
    )
    