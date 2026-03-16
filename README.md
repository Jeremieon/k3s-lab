# K3s Lab — FastAPI Microservices on Kubernetes

## Current Architecture
```
Client (Browser / curl)
        │
        │ HTTPS (TLS via cert-manager)
        ▼
┌─────────────────────────────────────┐
│  NGINX Plus Ingress Controller      │
│  External (nginx-external)          │
│  IP: 192.168.0.55/56                │
│  Rate limiting, Active health checks│
│  Live dashboard: node:30080         │
└─────────────────────────────────────┘
        │
        ├── fastapi.lab.local/items   → items-service-v2 (via VirtualServerRoute)
        ├── fastapi.lab.local/catalog → gateway-service  (via VirtualServerRoute)
        ├── items.lab.local           → items-service-v2
        └── gateway.lab.local         → gateway-service
                                              │
                                              └──► items-service-v2

┌─────────────────────────────────────┐
│  NGINX Plus Ingress Controller      │
│  Internal (nginx-internal)          │
│  NodePort: 192.168.0.X:30444        │
└─────────────────────────────────────┘
        │
        └── admin.lab.local           → gateway/items swagger docs
```

## Cluster Nodes

| Node | Role | IP |
|---|---|---|
| jeremy-control | control-plane | 192.168.0.49 |
| jeremyk3swrk | worker | 192.168.0.55 |
| jeremyk3swrk2 | worker | 192.168.0.56 |

## Helm Releases

| Release | Namespace | Chart | Purpose |
|---|---|---|---|
| nginx-plus | nginx-ingress | nginx-ingress 2.4.4 | External NGINX Plus IC |
| nginx-internal | nginx-ingress | nginx-ingress 2.4.4 | Internal NGINX Plus IC |
| cert-manager | cert-manager | cert-manager | TLS certificate automation |
| fastapi-production | production | fastapi-chart | Application (production) |
| fastapi-dev | dev | fastapi-chart | Application (dev) |
| fastapi-staging | staging | fastapi-chart | Application (staging) |
| ingress-release | production | ingress-chart | Ingress routing config |

## Hostnames

| Hostname | Controller | Purpose |
|---|---|---|
| fastapi.lab.local | external | Main entry — path routing to all services |
| items.lab.local | external | Direct items-service access |
| gateway.lab.local | external | Direct gateway-service access |
| admin.lab.local:30444 | internal | Admin/swagger docs (internal only) |

## Services

### items-service (v2.0.0)
- 7 items in catalogue
- Endpoints: `GET /health` `GET /items` `GET /items/{id}` `GET /version`
- Image: YOURDOCKERHUBUSERNAME/items-service:2.0.0

### gateway-service (v1.0.0)
- Calls items-service upstream
- Endpoints: `GET /health` `GET /catalog` `GET /catalog/{id}` `GET /health/upstream`
- Image: YOURDOCKERHUBUSERNAME/gateway-service:1.0.0

## Quick Commands
```bash
# Deploy application
helm upgrade fastapi-production fastapi-chart/ \
  -n production -f helm-values/values-production.yaml

# Deploy ingress config
helm upgrade ingress-release ingress-chart/ -n production

# Check everything
kubectl get pods -A | grep -v Running
kubectl get virtualserver -n production
helm list -A

# Test routing
curl -sk https://fastapi.lab.local/catalog
```

## Roadmap

- [x] Phase 1 — Foundations (K3s, kubectl, Deployments, Helm)
- [x] Phase 2 — NGINX Plus Ingress Controller
- [ ] Phase 3 — CI/CD (GitHub Actions + ArgoCD)
- [ ] Phase 4 — Observability (Prometheus + Grafana + Loki)
- [ ] Phase 5 — F5 CIS + BIG-IP VE
- [ ] Phase 6 — Production Hardening
