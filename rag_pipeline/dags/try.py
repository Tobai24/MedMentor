from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def hello():
    print("Hello, Airflow!")
    return "Hello, Airflow!"

with DAG(
    "tell",
    start_date=datetime(2025, 2, 7),
    schedule_interval=None,
    catchup=False,
) as dag:
    task = PythonOperator(
        task_id="test_task",
    python_callable=hello
    )
