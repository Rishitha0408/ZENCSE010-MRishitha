import pytest
import unittest.mock
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.config import settings

# Setup Test Client
client = TestClient(app)

# Create a mock DB that behaves asynchronously
class AsyncMockDB:
    def __init__(self):
        self.certificates = unittest.mock.AsyncMock()
        self.verification_logs = unittest.mock.AsyncMock()

mock_db = AsyncMockDB()

def override_get_db():
    return mock_db

app.dependency_overrides[get_db] = override_get_db

def test_unauthorized_issuance():
    """Test: POST /api/v1/certificates without X-API-Key returns 401"""
    response = client.post("/api/v1/certificates/", json={})
    assert response.status_code == 401

def test_verify_non_existent():
    """Test: GET /api/v1/verify/non-existent-id returns NOT_FOUND"""
    # Setup mock to return None for get_certificate
    mock_db.certificates.find_one = unittest.mock.AsyncMock(return_value=None)
    
    response = client.get("/api/v1/verify/CERT-999999")
    assert response.status_code == 200
    assert response.json()["result"] == "NOT_FOUND"

def test_issue_success():
    """Test: POST /api/v1/certificates returns 201 with QR"""
    headers = {"X-API-Key": settings.api_key}
    payload = {
        "recipient_name": "Integration Tester",
        "recipient_email": "test@example.com",
        "course_title": "Integration Course",
        "skills": ["Python"],
        "issue_date": "2024-03-15"
    }
    
    # Mock insert_one
    mock_db.certificates.insert_one = unittest.mock.AsyncMock()
    
    response = client.post("/api/v1/certificates/", json=payload, headers=headers)
    assert response.status_code == 201
    assert "certificate_id" in response.json()
    assert "qr_code_base64" in response.json()

def test_revoke_success():
    """Test: PUT /api/v1/certificates/{id}/revoke returns 200"""
    headers = {"X-API-Key": settings.api_key}
    
    # Mock update_one to simulate success
    mock_db.certificates.update_one = unittest.mock.AsyncMock(return_value=unittest.mock.Mock(modified_count=1))
    
    response = client.put("/api/v1/certificates/CERT-123/revoke", headers=headers)
    assert response.status_code == 200
