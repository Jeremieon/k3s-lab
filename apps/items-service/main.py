from fastapi import FastAPI, HTTPException
from datetime import datetime, timezone
import os
import socket

app = FastAPI(
    title="Items Service",
    description="Manages items inventory",
    version="2.0.0",
    openapi_url="/items/openapi.json",
    docs_url="/items/docs",
    redoc_url="/items/redoc",
)

ITEMS = [
    {"id": 1, "name": "NGINX Ingress Controller", "category": "networking", "in_stock": True},
    {"id": 2, "name": "BIG-IP VE", "category": "load-balancer", "in_stock": True},
    {"id": 3, "name": "Grafana Dashboard", "category": "observability", "in_stock": True},
    {"id": 4, "name": "ArgoCD", "category": "gitops", "in_stock": False},
    {"id": 5, "name": "Prometheus", "category": "observability", "in_stock": True},
    {"id": 6, "name": "F5 CIS", "category": "networking", "in_stock": True},
    {"id": 7, "name": "Loki", "category": "observability", "in_stock": True},
]

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pod": socket.gethostname(),
        "version": "2.0.0"
    }

@app.get("/")
def root():
    return {
        "service": "items-service",
        "version": os.getenv("APP_VERSION", "2.0.0"),
        "environment": os.getenv("ENVIRONMENT", "unknown"),
        "pod": socket.gethostname()
    }

@app.get("/items")
def get_items(category: str = None, in_stock: bool = None):
    results = ITEMS
    if category:
        results = [i for i in results if i["category"] == category]
    if in_stock is not None:
        results = [i for i in results if i["in_stock"] == in_stock]
    return {
        "count": len(results),
        "items": results,
        "served_by": socket.gethostname(),
        "version": "2.0.0"
    }

@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = next((i for i in ITEMS if i["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return item

@app.get("/version")
def version():
    return {
        "version": os.getenv("APP_VERSION", "2.0.0"),
        "environment": os.getenv("ENVIRONMENT", "unknown"),
        "pod_name": socket.gethostname()
    }
# trigger ci
# verify fix Sat Mar 21 09:46:42 PM UTC 2026
# trigger dev pipeline
# trigger dev pipeline
# sync fix
