# K3s Lab — FastAPI Microservices on Kubernetes

## Architecture
```
Client
  │
  ▼
[Phase 2: NGINX Ingress Controller]  ← coming next
  │
  ├──► gateway-service (ClusterIP)
  │         │
  │         └──► items-service (ClusterIP)
  │
[Phase 5: BIG-IP VE + F5 CIS]        ← coming later
```

## Cluster

| Node | Role | IP |
|---|---|---|
| jeremy-control | control-plane | 192.168.0.49 |
| jeremyk3swrk | worker | 192.168.0.55 |
| jeremyk3swrk2 | worker | 192.168.0.56 |

## Environments

| Environment | Namespace | Replicas | Log Level |
|---|---|---|---|
| dev | dev | 1 | debug |
| staging | staging | 1 | info |
| production | production | 2 | info |

## Services

### items-service
- Owns item data
- Endpoints: `GET /health` `GET /items` `GET /items/{id}` `GET /version`

### gateway-service
- API gateway — calls items-service upstream
- Endpoints: `GET /health` `GET /catalog` `GET /catalog/{id}` `GET /health/upstream`

## Deploy
```bash
# Install
helm install fastapi-production fastapi-chart/ \
  --namespace production \
  -f helm-values/values-production.yaml

# Upgrade (new image version)
helm upgrade fastapi-production fastapi-chart/ \
  --namespace production \
  -f helm-values/values-production.yaml \
  --set itemsService.image.tag=2.0.0

# Rollback
helm rollback fastapi-production 1 -n production

# Diff before upgrade
helm diff upgrade fastapi-production fastapi-chart/ \
  --namespace production \
  -f helm-values/values-production.yaml
```

## Roadmap

- [x] Phase 1 — Foundations (K3s, kubectl, Deployments, Helm)
- [ ] Phase 2 — NGINX Ingress Controller
- [ ] Phase 3 — CI/CD (GitHub Actions + ArgoCD)
- [ ] Phase 4 — Observability (Prometheus + Grafana + Loki)
- [ ] Phase 5 — F5 CIS + BIG-IP VE
- [ ] Phase 6 — Production Hardening
