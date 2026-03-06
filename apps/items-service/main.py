from fastapi import FastAPI, HTTPException
from datetime import datetime
import os
import socket

app = FastAPI(
    title="Items Service",
    description="Manages items inventory",
    version="1.0.0"
)

# Simulated data store — no database needed for this lab
ITEMS = [
    {"id": 1, "name": "NGINX Ingress Controller", "category": "networking", "in_stock": True},
    {"id": 2, "name": "BIG-IP VE", "category": "load-balancer", "in_stock": True},
    {"id": 3, "name": "Grafana Dashboard", "category": "observability", "in_stock": True},
    {"id": 4, "name": "ArgoCD", "category": "gitops", "in_stock": False},
    {"id": 5, "name": "Prometheus", "category": "observability", "in_stock": True},
    {"id": 6, "name": "F5 CIS", "category": "networking", "in_stock": True},
]

@app.get("/health")
def health():
    """Kubernetes liveness + readiness probe endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "pod": socket.gethostname()
    }

@app.get("/")
def root():
    return {
        "service": "items-service",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "environment": os.getenv("ENVIRONMENT", "unknown"),
        "pod": socket.gethostname()
    }

@app.get("/items")
def get_items(category: str = None, in_stock: bool = None):
    """Get all items, optionally filtered"""
    results = ITEMS
    if category:
        results = [i for i in results if i["category"] == category]
    if in_stock is not None:
        results = [i for i in results if i["in_stock"] == in_stock]
    return {
        "count": len(results),
        "items": results,
        "served_by": socket.gethostname()
    }

@app.get("/items/{item_id}")
def get_item(item_id: int):
    """Get a single item by ID"""
    item = next((i for i in ITEMS if i["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return item

@app.get("/version")
def version():
    return {
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "environment": os.getenv("ENVIRONMENT", "unknown"),
        "pod_name": socket.gethostname(),
        "built_at": "2024-01-01T00:00:00"
    }
