from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator


default_args = {
    "owner": "Tobi",
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
}


def get_mlflow():
    import mlflow
    print(f"MLflow version: {mlflow.__version__}")
    
def get_matplotlib():
    import matplotlib
    print(f"sklearn with version: {matplotlib.__version__} ")

# Define the DAG
with DAG(
    default_args=default_args,
    dag_id="mlflow_version_v6",
    start_date=datetime(2023, 10, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    get_mlflow_task = PythonOperator(
        task_id="get_mlflow",
        python_callable=get_mlflow,
    )

    task2 = PythonOperator(
        task_id="get_scikitlearn",
        python_callable=get_matplotlib,
    )


    get_mlflow_task >> task2