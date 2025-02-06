import mlflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

def train_model():
    with mlflow.start_run():
        mlflow.log_param("param1", 5)
        mlflow.log_metric("metric1", 0.85)
        mlflow.log_artifact("output.txt")

default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 10, 1),
}

dag = DAG("mlflow_example", default_args=default_args, schedule_interval="@once")

train_task = PythonOperator(
    task_id="train_model",
    python_callable=train_model,
    dag=dag,
)
train_task2 = PythonOperator(
    task_id="train_model2",
    python_callable=train_model,
    dag=dag,
)

train_task >> train_task2