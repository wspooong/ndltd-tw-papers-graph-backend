from typing import List

from fastapi import APIRouter, Query

from app.services.classes import Document, NetworkData
from app.services import os_search

router = APIRouter()

@router.get("/")
def search_document(uid: str) -> Document:
    return os_search.get_document_with_id(uid)

@router.get("/similarity")
def search_similarity_network(
    uid: str = "109THU00099005", layer: int = Query(2), n_results: int = Query(5)
) -> NetworkData:
    node_list, edge_list, documents = os_search.get_document_similarity_network(
        uid=uid, layer=layer, n_results=n_results
    )
    return NetworkData(nodes=node_list, edges=edge_list, documents=documents)


@router.get("/title")
def search_title(query: str) -> List[Document]:
    return os_search.search_title(query)
