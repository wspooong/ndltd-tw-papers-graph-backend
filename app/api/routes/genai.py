from typing import Annotated, List

from fastapi import APIRouter, Header, Query
from fastapi.responses import StreamingResponse

from app.services.rag import RagSummary
from app.services.search import Search

router = APIRouter()
os_search = Search()

@router.get("/summary")
def generate_summary(
    llm_service: str = Query("google"),
    model_name: str = Query("gemini-1.0-pro"),
    target_uid: str = Query("109THU00099005"),
    n_results: int = Query(6),
    genai_api_key: Annotated[str | None, Header()] = None
) -> str:
    rag = RagSummary(
        os_search=os_search, 
        llm_service=llm_service, 
        model_name=model_name, 
        api_key=genai_api_key, 
        target_uid=target_uid, 
        n_results=n_results
    )
    return StreamingResponse(rag.run())
