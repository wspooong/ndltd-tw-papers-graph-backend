from typing import List, Optional, Annotated

from fastapi import FastAPI, Query, Header
from fastapi.responses import RedirectResponse, StreamingResponse

from src import Search, RagSummary
from src.classes import Document, NetworkData

app = FastAPI()
os_search = Search()


@app.get("/")
def redirect_root_to_docs():
    return RedirectResponse("/docs")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/v1/document", tags=["document"])
def search_document(uid: str) -> Document:
    return os_search.get_document_with_id(uid)

@app.get("/api/v1/document/similarity", tags=["document"])
def search_similarity_network(
    uid: str = "109THU00099005", layer: int = Query(2), n_results: int = Query(5)
) -> NetworkData:
    node_list, edge_list, documents = os_search.get_document_similarity_network(
        uid=uid, layer=layer, n_results=n_results
    )
    return NetworkData(nodes=node_list, edges=edge_list, documents=documents)

@app.get("/api/v1/document/title", tags=["document"])
def search_title(query: str) -> List[Document]:
    return os_search.search_title(query)

@app.get("/api/v1/genai/summary/", tags=["genai"])
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8777)
