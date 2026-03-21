from fastapi import FastAPI, HTTPException
from datetime import datetime, timezone
import httpx
import os
import socket

app = FastAPI(
    title="Gateway Service",
    description="API Gateway",
    version="1.0.0",
    openapi_url="/gateway/openapi.json",
    docs_url="/gateway/docs",
)

# This is the Kubernetes DNS name for items-service
# Format: <service-name>.<namespace>.svc.cluster.local
ITEMS_SERVICE_URL = os.getenv(
    "ITEMS_SERVICE_URL",
    "http://items-service.production.svc.cluster.local"
)

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pod": socket.gethostname()
    }

@app.get("/")
def root():
    return {
        "service": "gateway-service",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "environment": os.getenv("ENVIRONMENT", "unknown"),
        "pod": socket.gethostname(),
        "upstream": ITEMS_SERVICE_URL
    }

@app.get("/catalog")
def get_catalog(category: str = None):
    """
    Fetches items from items-service and enriches the response.
    This is the aggregation pattern — gateway calls upstream services.
    """
    try:
        params = {}
        if category:
            params["category"] = category

        # httpx is the async-friendly HTTP client for FastAPI
        with httpx.Client(timeout=5.0) as client:
            response = client.get(f"{ITEMS_SERVICE_URL}/items", params=params)
            response.raise_for_status()
            upstream_data = response.json()

        return {
            "gateway_pod": socket.gethostname(),
            "items_service_pod": upstream_data.get("served_by"),
            "environment": os.getenv("ENVIRONMENT", "unknown"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "catalog": upstream_data["items"],
            "total": upstream_data["count"]
        }

    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail=f"Cannot reach items-service at {ITEMS_SERVICE_URL}"
        )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="items-service timed out"
        )

@app.get("/catalog/{item_id}")
def get_catalog_item(item_id: int):
    """Proxy a single item lookup to items-service"""
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(f"{ITEMS_SERVICE_URL}/items/{item_id}")
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
            response.raise_for_status()
            return response.json()
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Cannot reach items-service")

@app.get("/health/upstream")
def upstream_health():
    """Check if items-service is reachable — useful for debugging"""
    try:
        with httpx.Client(timeout=3.0) as client:
            response = client.get(f"{ITEMS_SERVICE_URL}/health")
            upstream = response.json()
        return {
            "gateway": "healthy",
            "items_service": "healthy",
            "items_service_pod": upstream.get("pod"),
            "items_service_url": ITEMS_SERVICE_URL
        }
    except Exception as e:
        return {
            "gateway": "healthy",
            "items_service": "unreachable",
            "error": str(e),
            "items_service_url": ITEMS_SERVICE_URL
        }
# trigger gateway ci
# trigger gateway ci
# trigger gateway
