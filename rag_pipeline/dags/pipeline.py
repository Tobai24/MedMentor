import json
import mlflow
import logging
import os
import tempfile
from io import BytesIO
from datetime import datetime, timedelta
from minio import Minio
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders.pdf import PyPDFLoader
from airflow import DAG
from airflow.operators.python import PythonOperator
from langchain.embeddings import OpenAIEmbeddings
from transformers import AutoTokenizer, AutoModel
import numpy as np

logger = logging.getLogger('airflow')
logger.setLevel(logging.DEBUG)

minio_client = Minio(
    "minio-new:9000",  
    access_key="minioadmin",  
    secret_key="minioadmin", 
    secure=False
)

MLFLOW_TRACKING_URI = "http://mlflow:5000"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("Preprocessing")


def read_split_doc_from_mino(bucket_name: str, chunk_size: int = 500, chunk_overlap: int = 120) -> list[str]:
    """Function to read the PDFs from a Minio bucket and split them into chunks."""
    try:
        logger.info(f"Started reading and splitting documents from Minio bucket: {bucket_name}")
        
        pdf_files = minio_client.list_objects(bucket_name)
        document_chunk = []

        for file in pdf_files:
            logger.debug(f"Processing file: {file.object_name}")
            pdf_data = minio_client.get_object(bucket_name, file.object_name)
            pdf_content = pdf_data.read()
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(pdf_content)
                tmp_file_path = tmp_file.name
            
            pdf_loader = PyPDFLoader(tmp_file_path)
            documents = pdf_loader.load()

            os.remove(tmp_file_path)

            document_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            chunked_docs = document_splitter.split_documents(documents)
            
            document_chunk.extend(chunked_docs)

        logger.info(f"Total chunks processed: {len(document_chunk)}")
        return document_chunk
    
    except Exception as e:
        logger.error(f"Error in reading and splitting document: {str(e)}")
        raise

def upload_chunked_docs_to_minio(bucket_name: str, chunked_docs: list[str], file_name: str):
    """Function to upload chunked documents to Minio as a JSON file."""
    try:
        logger.info(f"Started uploading chunked documents to Minio bucket: {bucket_name}")

        chunked_data_json = json.dumps([{"text": doc.page_content, "metadata": doc.metadata} for doc in chunked_docs])

        byte_data = BytesIO(chunked_data_json.encode('utf-8'))
        
        minio_client.put_object(bucket_name, file_name, byte_data, len(byte_data.getvalue()))
        
        logger.info(f"Uploaded {file_name} to bucket {bucket_name}")
    except Exception as e:
        logger.error(f"Error in uploading chunked documents to Minio: {str(e)}")
        raise

def data_ingestion_pipeline(bucket_name: str, file_name: str, chunk_size: int, chunk_overlap: int):
    """Function to orchestrate reading, splitting, and uploading chunked docs."""
    try:
        logger.info("Starting the data ingestion pipeline.")

        with mlflow.start_run(run_name="data_ingestion"):
            mlflow.log_param("bucket_name", bucket_name)
            mlflow.log_param("file_name", file_name)
            mlflow.log_param("chunk_size", chunk_size)
            mlflow.log_param("chunk_overlap", chunk_overlap)

            chunked_document = read_split_doc_from_mino(bucket_name, chunk_size, chunk_overlap)
            logger.info(f"Total chunks: {len(chunked_document)}")

            mlflow.log_metric("total_chunks", len(chunked_document))

            upload_chunked_docs_to_minio(bucket_name, chunked_document, file_name)
    
    except Exception as e:
        logger.error(f"Error in data ingestion pipeline: {str(e)}")
        raise

def load_chunked_docs_from_minio(bucket_name: str, file_name: str):
    """Function to load chunked documents from MinIO."""
    try:
        logger.info(f"Loading chunked documents from MinIO bucket: {bucket_name}")

        response = minio_client.get_object(bucket_name, file_name)
        chunked_data_json = response.read().decode('utf-8')
        chunked_docs = json.loads(chunked_data_json)

        logger.info(f"Loaded {len(chunked_docs)} chunks from {file_name}")
        return chunked_docs
    
    except Exception as e:
        logger.error(f"Error loading chunked documents from MinIO: {str(e)}")
        raise

def generate_and_track_embeddings(bucket_name: str, file_name: str):
    """Function to generate embeddings and track them with MLflow."""
    try:
        logger.info("Starting the embedding generation pipeline.")

        with mlflow.start_run(run_name="embedding_generation"):
            mlflow.log_param("bucket_name", bucket_name)
            mlflow.log_param("file_name", file_name)

            chunked_docs = load_chunked_docs_from_minio(bucket_name, file_name)

            # Generate OpenAI embeddings
            logger.info("Generating OpenAI embeddings")
            embedding_generator = OpenAIEmbeddings()
            openai_library = FAISS.from_texts([doc["text"] for doc in chunked_docs], embedding_generator)
            openai_library.save_local("/opt/airflow/embeddings/openai_faiss_index")

            # Generate ClinicalBERT embeddings
            # logger.info("Generating ClinicalBERT embeddings")
            # tokenizer = AutoTokenizer.from_pretrained("medicalai/ClinicalBERT")
            # model = AutoModel.from_pretrained("medicalai/ClinicalBERT")

            # clinicalbert_embeddings = []
            # for doc in chunked_docs:
            #     inputs = tokenizer(doc["text"], return_tensors="pt", truncation=True, padding=True)
            #     outputs = model(**inputs)
            #     embedding = outputs.last_hidden_state.mean(dim=1).detach().numpy()
            #     clinicalbert_embeddings.append(embedding)

            # clinicalbert_embeddings = np.array(clinicalbert_embeddings)
            # np.save("/opt/airflow/embeddings/clinicalbert_embeddings.npy", clinicalbert_embeddings)

            # Log embeddings as artifacts
            mlflow.log_artifact("/opt/airflow/embeddings/openai_faiss_index")
            # mlflow.log_artifact("/opt/airflow/embeddings/clinicalbert_embeddings.npy")

            logger.info("Embeddings generated and tracked with MLflow.")
    
    except Exception as e:
        logger.error(f"Error in embedding generation pipeline: {str(e)}")
        raise


default_args = {
    'owner': 'Tobi',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'processing_pipeline_v02',
    default_args=default_args,
    description='A DAG to read, split, and upload PDF chunks to Minio',
    schedule_interval=None,
    start_date=datetime(2025, 2, 7),
    catchup=False,
) as dag:
    data_ingestion_task = PythonOperator(
        task_id='data_ingestion_pipeline',
        python_callable=data_ingestion_pipeline,
        op_args=["data", "chunked_data.json", 500, 120], 
        dag=dag,
    )

    embedding_generation_task = PythonOperator(
        task_id='embedding_generation_pipeline',
        python_callable=generate_and_track_embeddings,
        op_args=["data", "chunked_data.json"], 
        dag=dag,
    )

    data_ingestion_task >> embedding_generation_task