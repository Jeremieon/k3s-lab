from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "gateway-service"

def test_catalog_upstream_unreachable():
    """When items-service is down gateway should return 503"""
    with patch("httpx.Client") as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value.__enter__.return_value = mock_instance
        import httpx
        mock_instance.get.side_effect = httpx.ConnectError("Connection refused")
        response = client.get("/catalog")
        assert response.status_code == 503

def test_upstream_health_check():
    """upstream health endpoint should always return gateway status"""
    with patch("httpx.Client") as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value.__enter__.return_value = mock_instance
        mock_instance.get.return_value.json.return_value = {
            "status": "healthy",
            "pod": "test-pod"
        }
        response = client.get("/health/upstream")
        assert response.status_code == 200
        assert response.json()["gateway"] == "healthy"
