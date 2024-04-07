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


def test_stats_get_top_field_count():
    year = 109
    response = client.get(f"api/v1/stats/top_field?year={year}")
    assert response.status_code == 200
    data = response.json()
    assert data

def test_stats_get_institution_department():
    year = 109
    response = client.get(f"api/v1/stats/institution_department?year={year}")
    assert response.status_code == 200
    data = response.json()
    assert data
