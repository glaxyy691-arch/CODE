from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_emergency():
    response = client.post(
        "/api/emergency/test",
        json={
            "caller": "+91XXXXXXXXXX",
            "message": "Earthquake test alert",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["incident"]["status"] == "ACTIVE"
    assert data["incident"]["priority"] == "HIGH"
