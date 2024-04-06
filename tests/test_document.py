import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient

from app.services.constants import _API_PREFIX
from main import app

client = TestClient(
    app=app
)

def test_get_document():
    response = client.get(f"{_API_PREFIX}/document/", params={"uid": "109THU00099005"})
    assert response.status_code == 200
    data = response.json()
    assert data["uid"] == "109THU00099005"
    assert "title" in data 

def test_get_document_similarity():
    response = client.get(f"{_API_PREFIX}/document/similarity", params={"uid": "109THU00099005"})
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "edges" in data
    assert "documents" in data