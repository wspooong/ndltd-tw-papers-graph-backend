from typing import List

from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse

from src import Search
from src.classes import Document, NetworkData

app = FastAPI()
os_search = Search()


@app.get("/")
def redirect_root_to_docs():
    return RedirectResponse("/docs")

@app.get("/api/v1/search_document")
def search_document(uid: str) -> Document:
    return os_search.get_document_with_id(uid)

@app.get("/api/v1/search_similarity_network")
def search_similarity_network(
    uid: str = "109THU00099005", layer: int = Query(2), n_results: int = Query(5)
) -> NetworkData:
    node_list, edge_list, documents = os_search.get_document_similarity_network(
        uid=uid, layer=layer, n_results=n_results
    )
    return {"nodes": node_list, "edges": edge_list, "documents": documents}

@app.get("/api/v1/search_title")
def search_title(query: str) -> List[Document]:
    return os_search.search_title(query)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8777)
