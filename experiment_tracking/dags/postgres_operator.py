from datetime import timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    'owner': 'tobi',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='dag_with_postgres_operator_v5',
    default_args=default_args,
    start_date=days_ago(1),  
    schedule='0 0 * * *',  
    catchup=False  
) as dag:
    
    task1 = PostgresOperator(
        task_id='create_postgres_table',
        postgres_conn_id='postgres_localhost',
        sql="""
            CREATE TABLE IF NOT EXISTS dag_runs (
                dt DATE,
                dag_id VARCHAR,
                PRIMARY KEY (dt, dag_id)
            )
        """
    )

    task2 = PostgresOperator(
        task_id='insert_into_table',
        postgres_conn_id='postgres_localhost',
        sql="""
            INSERT INTO dag_runs (dt, dag_id) VALUES ('{{ ds }}', '{{ dag.dag_id }}')
        """,
        autocommit=True
    )

    task3 = PostgresOperator(
        task_id='delete_data_from_table',
        postgres_conn_id='postgres_localhost',
        sql="""
            DELETE FROM dag_runs WHERE dt = '{{ ds }}' AND dag_id = '{{ dag.dag_id }}';
        """,
        autocommit=True
    )

    task1 >> task3 >> task2
