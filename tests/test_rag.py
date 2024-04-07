import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from dotenv import load_dotenv

load_dotenv()

GEMINI_PRO_API_KEY = os.getenv("GEMINI_PRO_API_KEY")

from main import app

client = TestClient(
    app=app
)

def test_generate_summary_google():
    target_uid = "109THU00099005"
    params = {
        "llm_service": "google",
        "model_name": "gemini-1.0-pro",
        "target_uid": target_uid,
        "n_results": 6
    }
    response = client.get("/api/v1/genai/summary/", params=params, headers={"genai-api-key": GEMINI_PRO_API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["target_uid"] == target_uid
