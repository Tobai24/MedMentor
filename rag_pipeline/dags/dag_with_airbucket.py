from minio import Minio
from airflow.operators.python import PythonOperator
from airflow import DAG
from datetime import datetime

def download_book_from_minio(book_name):
    client = Minio(
        "localhost:9000",
        access_key="minio",
        secret_key="minio123",
        secure=False
    )
    client.fget_object("books_bucket", book_name, f"/tmp/{book_name}")
    print(f"Book {book_name} downloaded successfully.")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 2, 3),
    'retries': 1,
}

with DAG(
    'book_pipeline',
    default_args=default_args,
    schedule_interval=None,
) as dag:

    download_book = PythonOperator(
        task_id='download_book',
        python_callable=download_book_from_minio,
        op_args=['Handbook of Clinical Diagnostics by Xue-Hong Wan, Rui Zeng (z-lib.org).pdf'],
    )
