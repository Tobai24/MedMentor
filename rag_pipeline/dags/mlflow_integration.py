from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import mlflow

# MLflow tracking URI
MLFLOW_TRACKING_URI = "http://host.docker.internal:5000"

# Default arguments for the DAG
default_args = {
    "owner": "Tobi",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

# Function to log an experiment with MLflow
def log_mlflow_experiment():
    # Set the tracking URI
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    # Start an MLflow run
    with mlflow.start_run():
        # Log parameters
        mlflow.log_param("param1", 5)
        mlflow.log_param("param2", "hello")

        # Log metrics
        mlflow.log_metric("accuracy", 0.95)
        mlflow.log_metric("loss", 0.05)

        # Log artifacts (e.g., a text file)
        with open("output.txt", "w") as f:
            f.write("This is a test artifact.")
        mlflow.log_artifact("output.txt")

        print("Experiment logged successfully!")

# Define the DAG
with DAG(
    dag_id="mlflow_integration_tired_v3",
    default_args=default_args,
    start_date=datetime(2023, 10, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    # Task to log an MLflow experiment
    log_experiment_task = PythonOperator(
        task_id="log_mlflow_experiment_v2",
        python_callable=log_mlflow_experiment,
    )
    
    log_experiment_task2 = PythonOperator(
        task_id="log_mlflow_experiment_v3",
        python_callable=log_mlflow_experiment,
    )
    
    log_experiment_task >> log_experiment_task2