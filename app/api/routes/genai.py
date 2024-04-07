from typing import Annotated

from fastapi import APIRouter, Header, Query

from app.services.rag import RagSummary
from app.services import os_search

router = APIRouter()

@router.get("/summary")
def generate_summary(
    llm_service: str = Query("google"),
    model_name: str = Query("gemini-1.0-pro"),
    target_uid: str = Query("109THU00099005"),
    n_results: int = Query(6),
    genai_api_key: Annotated[str | None, Header()] = None
) -> dict:
    rag = RagSummary(
        llm_service=llm_service, 
        model_name=model_name, 
        api_key=genai_api_key, 
        target_uid=target_uid, 
        n_results=n_results
    )
    
    answer = rag.run()
    return answer
