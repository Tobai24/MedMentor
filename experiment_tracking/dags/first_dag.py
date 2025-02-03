from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "Tobs",
    "retries": 5,
    "retries_delay": timedelta(minutes=2)
}

with DAG(
    dag_id='our_first_v5',
    default_args=default_args,
    description="This is my first airflow dag",
    start_date=datetime(2025, 2, 3, 2),
    schedule_interval="@daily"
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command="echo hello world"
    )
    task2 = BashOperator(
        task_id="second_task",
        bash_command="echo i am the second task running after task1"
    )
    task3 = BashOperator(
        task_id="third_task",
        bash_command="echo i am the third task running after task1 or task 2"
    )
    
    # task1.set_downstream(task2)
    # task1.set_downstream(task3)
    # task1 >> task2
    # task1 >> task3
    task1 >> [task2, task3]