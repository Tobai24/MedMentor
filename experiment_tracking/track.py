import mlflow
import mlflow.pyfunc
from langchain_community.embeddings import OpenAIEmbeddings
from transformers import AutoTokenizer, AutoModel
from langchain_community.vectorstores import FAISS
from langchain.vectorstores import VectorStore
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter


def read_split_doc(directory: str, chunk_size: int = 500, chunk_overlap: int = 120) -> list[str]:
    """Function to read the PDFs from a directory.

    Args:
        directory (str): The path of the directory where the PDFs are stored.

    Returns:
        list[str]: A list of text in the PDFs.
    """
    # Initialize a PyPDFDirectoryLoader object with the given directory
    file_loader = PyPDFDirectoryLoader(directory)
    
    # Load PDF documents from the directory
    documents = file_loader.load()
    
    #did not use the recursive text splitter because it did not give a good result
    document_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    
    document_chunk = document_splitter.split_documents(documents)
    
    return document_chunk

print("starting the document chunking")
chunked_document = read_split_doc("../data/")
print("finished chunking the document")

mlflow.set_tracking_uri("http://localhost:5000")


with mlflow.start_run():

    
    embeddings_list = []

    tokenizer1 = AutoTokenizer.from_pretrained("medicalai/ClinicalBERT")
    model1 = AutoModel.from_pretrained("medicalai/ClinicalBERT")
    embeddings_list.append(('ClinicalBERT', tokenizer1, model1))

    
    tokenizer2 = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
    model2 = AutoModel.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
    embeddings_list.append(('Bio_ClinicalBERT', tokenizer2, model2))


    embedding_generator = OpenAIEmbeddings()
    embeddings_list.append(('OpenAIEmbeddings', embedding_generator))


    # Initialize FAISS index for OpenAI embeddings
    openai_library = FAISS.from_documents(chunked_document, embedding_generator)
    
    # Save FAISS index locally
    faiss_path = "../embeddings"
    openai_library.save_local(faiss_path)

    # Log the saved embeddings to MLflow
    mlflow.log_param("faiss_path", faiss_path)

    # Log models and tokenizers
    for name, tokenizer, model in embeddings_list:
        mlflow.log_param(f"{name}_tokenizer", str(tokenizer))
        mlflow.log_param(f"{name}_model", str(model))
    
    # Log a custom artifact (you could save the embeddings as a file or other data)
    mlflow.log_artifact(faiss_path)
    

    faiss_stats = openai_library.index.research()  
    mlflow.log_metric("faiss_stats", faiss_stats)

    print(f"Embeddings tracked and saved under MLflow run {mlflow.active_run().info.run_id}")
