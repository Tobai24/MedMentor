from fastapi import HTTPException, Depends, APIRouter
from fastapi.responses import Response
from sqlalchemy.orm import Session
from .database import get_db  
from .rag_pipeline import rag
from .schema import QueryInput

router = APIRouter(prefix="/generate-case", tags=["case"])

@router.post("", status_code=200)
def generate_case(query: QueryInput, db: Session = Depends(get_db)):
    try:
        response = rag(query.dict())  # Call the RAG pipeline
        
        # Ensure the response is plain text (removes JSON serialization issues)
        return Response(content=response, media_type="text/plain")  
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
