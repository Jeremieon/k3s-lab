from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "items-service"

def test_get_items():
    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "count" in data
    assert data["count"] > 0

def test_get_item_by_id():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_get_item_not_found():
    response = client.get("/items/999")
    assert response.status_code == 404

def test_filter_by_category():
    response = client.get("/items?category=networking")
    assert response.status_code == 200
    data = response.json()
    for item in data["items"]:
        assert item["category"] == "networking"

def test_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert "version" in response.json()
