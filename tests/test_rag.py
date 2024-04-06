import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient


from main import app

client = TestClient(
    app=app
)

# def test_generate_summary_google():
#     response = client.get("/api/v1/genai/summary/", params={"llm_service": "google"})
#     assert response.status_code == 200
#     assert response.text