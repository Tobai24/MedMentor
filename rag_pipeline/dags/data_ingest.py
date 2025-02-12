# import json
# import mlflow
# import logging
# import os
# import tempfile
# from io import BytesIO
# from datetime import datetime, timedelta
# from minio import Minio
# from langchain.chains import RetrievalQA
# from langchain.vectorstores import FAISS
# from langchain.text_splitter import CharacterTextSplitter
# from langchain_community.document_loaders.pdf import PyPDFLoader
# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from langchain.embeddings import OpenAIEmbeddings
# from transformers import AutoTokenizer, AutoModel



# logger = logging.getLogger('airflow')
# logger.setLevel(logging.DEBUG)


# minio_client = Minio(
#     "minio-new:9000",  
#     access_key="minioadmin",  
#     secret_key="minioadmin", 
#     secure=False
# )


# MLFLOW_TRACKING_URI =  "http://mlflow:5000"
# mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
# mlflow.set_experiment("Minio_Document_Processing")



# def read_split_doc_from_mino(bucket_name: str, chunk_size: int = 500, chunk_overlap: int = 120) -> list[str]:
#     """Function to read the PDFs from a Minio bucket and split them into chunks."""
#     try:
#         logger.info(f"Started reading and splitting documents from Minio bucket: {bucket_name}")
        
#         pdf_files = minio_client.list_objects(bucket_name)
#         document_chunk = []

#         for file in pdf_files:
#             logger.debug(f"Processing file: {file.object_name}")
#             pdf_data = minio_client.get_object(bucket_name, file.object_name)
#             pdf_content = pdf_data.read()
            
#             # Write the file to a temporary location
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
#                 tmp_file.write(pdf_content)
#                 tmp_file_path = tmp_file.name
            
#             # Load PDF using PyPDFLoader
#             pdf_loader = PyPDFLoader(tmp_file_path)
#             documents = pdf_loader.load()

#             # Delete the temporary file after loading
#             os.remove(tmp_file_path)

#             # Split the documents into smaller chunks
#             document_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
#             chunked_docs = document_splitter.split_documents(documents)
            
#             document_chunk.extend(chunked_docs)

#         logger.info(f"Total chunks processed: {len(document_chunk)}")
#         return document_chunk
    
#     except Exception as e:
#         logger.error(f"Error in reading and splitting document: {str(e)}")
#         raise

# def upload_chunked_docs_to_minio(bucket_name: str, chunked_docs: list[str], file_name: str):
#     """Function to upload chunked documents to Minio as a JSON file."""
#     try:
#         logger.info(f"Started uploading chunked documents to Minio bucket: {bucket_name}")

#         # Convert LangChain docs to dictionary format for serialization
#         chunked_data_json = json.dumps([{"text": doc.page_content, "metadata": doc.metadata} for doc in chunked_docs])

#         byte_data = BytesIO(chunked_data_json.encode('utf-8'))
        
#         minio_client.put_object(bucket_name, file_name, byte_data, len(byte_data.getvalue()))
        
#         logger.info(f"Uploaded {file_name} to bucket {bucket_name}")
#     except Exception as e:
#         logger.error(f"Error in uploading chunked documents to Minio: {str(e)}")
#         raise

# def process_and_upload_chunked_docs(bucket_name: str, file_name: str, chunk_size: int, chunk_overlap: int):
#     """Function to orchestrate reading, splitting, and uploading chunked docs with MLflow tracking."""
#     try:
#         logger.info("Starting the process to read, split, and upload chunked docs.")

#         with mlflow.start_run():
#             mlflow.log_param("bucket_name", bucket_name)
#             mlflow.log_param("file_name", file_name)
#             mlflow.log_param("chunk_size", chunk_size)
#             mlflow.log_param("chunk_overlap", chunk_overlap)

#             # Read and split documents from Minio
#             chunked_document = read_split_doc_from_mino(bucket_name, chunk_size, chunk_overlap)
#             logger.info(f"Total chunks: {len(chunked_document)}")

#             # Log number of chunks as a metric
#             mlflow.log_metric("total_chunks", len(chunked_document))

#             # Upload chunked documents back to Minio
#             upload_chunked_docs_to_minio(bucket_name, chunked_document, file_name)
    
#     except Exception as e:
#         logger.error(f"Error in process_and_upload_chunked_docs: {str(e)}")
#         raise

# default_args = {
#     'owner': 'Tobi',
#     'retries': 1,
#     'retry_delay': timedelta(minutes=5),
# }

# with DAG(
#     'minio_document_processing_tracking',
#     default_args=default_args,
#     description='A DAG to read, split, and upload PDF chunks to Minio',
#     schedule_interval=None,
#     start_date=datetime(2025, 2, 7),
#     catchup=False,
# ) as dag:
#     process_task = PythonOperator(
#         task_id='process_upload_chunked_docs',
#         python_callable=process_and_upload_chunked_docs,
#         op_args=["data", "chunked_data.json", 500, 120], 
#         dag=dag,
#     )

#     process_task



