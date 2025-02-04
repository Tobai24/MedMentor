from airflow.providers.amazon.aws.hooks.s3 import S3Hook

MINIO_BUCKET = "books"
MINIO_CONN_ID = "minio_conn"

def download_and_process_book(book_key):
    hook = S3Hook(aws_conn_id=MINIO_CONN_ID)
    book_content = hook.read_key(key=book_key, bucket_name=MINIO_BUCKET)
    print(f"Processing book: {book_key}")
    # Add your processing logic here