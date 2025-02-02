import mlflow
import openai
import numpy as np
from dotenv import load_dotenv
from mlflow.models.signature import ModelSignature
from mlflow.types.schema import ColSpec, ParamSchema, ParamSpec, Schema, TensorSpec

load_dotenv()
mlflow.set_tracking_uri("http://localhost:5000")

# Path to saved FAISS embeddings
mlflow.set_experiment("embedding model tracking")

with mlflow.start_run():
    model_info = mlflow.openai.log_model(
        model="text-embedding-ada-002",
        task=openai.embeddings,
        artifact_path="model",
        signature=ModelSignature(
            inputs=Schema([ColSpec(type="string", name=None)]),
            outputs=Schema([TensorSpec(type=np.dtype("float64"), shape=(-1,))]),
            params=ParamSchema([ParamSpec(name="batch_size", dtype="long", default=1024)]),
        ),
    )

# Load the model in pyfunc format
model = mlflow.pyfunc.load_model(model_info.model_uri)
