import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(
    app=app
)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_document():
    response = client.get("/api/v1/document", params={"uid": "109THU00099005"})
    assert response.status_code == 200
    data = response.json()
    assert data["uid"] == "109THU00099005"
    assert "title" in data 

def test_get_document_similarity():
    response = client.get("/api/v1/document/similarity", params={"uid": "109THU00099005"})
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "edges" in data
    assert "documents" in data