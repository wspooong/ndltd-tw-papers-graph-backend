from typing import Dict, List, Union

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from src import Search
from src.classes import Document, Edge, Node


class NetworkData(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
    documents: Dict[str, Document]


app = FastAPI()
es_search = Search()


@app.get("/")
def redirect_root_to_docs():
    return RedirectResponse("/docs")


@app.get("/api/v1/search_document")
def search_document(uid: str) -> Document:
    return es_search.get_document_with_id(uid)


@app.get("/api/v1/search_similarity_network")
def search_similarity_network(
    uid: str = "109THU00099005", layer: int = Query(2), n_results: int = Query(5)
) -> NetworkData:
    node_list, edge_list, documents = es_search.get_document_similarity_network(
        uid=uid, layer=layer, n_results=n_results
    )
    return {"nodes": node_list, "edges": edge_list, "documents": documents}


@app.get("/api/v1/get_top_ten_field_count")
def get_top_ten_field_count(
    year: int = Query(109),
) -> Dict[str, List[Dict[str, Union[str, int]]]]:
    return es_search.get_top_ten_field_count(year=year)


@app.get("/api/v1/get_institution_department_stats")
def get_institution_department_stats(
    year: int = Query(109),
) -> List[Dict[str, Union[str, int]]]:
    return es_search.get_institution_department_stats(year=year)

@app.get("/api/v1/search_title")
def search_title(query: str) -> List[Document]:
    return es_search.search_title(query)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8777)
