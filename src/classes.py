from pydantic import BaseModel
from typing import List

class UIDwithScore(BaseModel):
    uid: str
    title: str
    score: float


class UIDwithEmbedding(BaseModel):
    uid: str
    embedding: List[float]


class Document(BaseModel):
    uid: str
    title: str
    abstract: str
    author: str
    degree: str
    institution: str
    department: str
    narrow_field:str
    detailed_field: str
    graduated_academic_year: int
    url: str
    keywords: List[str]
    types_of_paper: str
    language: str


class Edge(BaseModel):
    source: str
    target: str
    score: float


class Node(BaseModel):
    uid: str
    layer: int

