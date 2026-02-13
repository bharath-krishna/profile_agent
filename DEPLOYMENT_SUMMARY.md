# FamilyMan UI - Deployment Quick Reference

## ✅ What Was Completed

1. **Docker Containerization**
   - Multi-stage Dockerfile created
   - Single container runs both Next.js (port 3000) and FastAPI (port 8001)
   - Image built and pushed to Docker Hub: `krishbharath/familyman-ui:latest`
   - Image digest: sha256:6280b90e7e9b17363c4061e2a4827ad34607d9d2c1ef9cb61a224270cc50e863

2. **Kubernetes Manifests**
   - Complete k8s structure with base + overlays
   - ConfigMap, Secret, Deployment, Service, Ingress
   - HAProxy Ingress Controller integration for https://profile.krishb.in

3. **Issues Fixed**
   - ✅ Package lock file sync issues
   - ✅ TypeScript compilation errors (5 files)
   - ✅ Secret base64 encoding
   - ✅ Docker image registry access
   - ✅ Port configuration (FastAPI on 8001, Next.js on 3000)
   - ✅ Image pull policy (using Docker Hub with Always policy)
   - ✅ HAProxy routing configuration

## 🎉 Current Status: FULLY DEPLOYED

**Application:** ✅ Running at https://profile.krishb.in/

**Services:**
- Next.js frontend: Port 3000 ✅
- FastAPI agent: Port 8001 ✅
- Pod status: Running (1/1 Ready) ✅

**Routing:**
- SSL termination: HAProxy on host (Let's Encrypt cert)
- Ingress class: haproxy (NodePort 30080)
- Backend routing: HAProxy → k8s ingress → service → pod

## 🚀 Quick Start Commands

### Build and Deploy
```bash
# Build and push image (use --no-cache to ensure latest code)
docker build --no-cache -t krishbharath/familyman-ui:latest .
docker push krishbharath/familyman-ui:latest

# Deploy to Kubernetes
kubectl apply -f k8s/base/secret.yaml
./scripts/deploy-k8s.sh

# Restart deployment to pull latest image
kubectl rollout restart deployment/familyman-ui
kubectl rollout status deployment/familyman-ui
```

### Check Status
```bash
# Pod status
kubectl get pods -l app=familyman-ui

# View logs (both services)
kubectl logs -l app=familyman-ui -f

# Check service endpoints
kubectl get svc familyman-ui-service
kubectl get ingress familyman-ui-ingress

# Describe pod for detailed info
kubectl describe pod -l app=familyman-ui
```

### Verify Services
```bash
# Check environment variables
kubectl exec <pod> -- env | grep PORT

# Verify port bindings in container
kubectl exec <pod> -- netstat -tlnp | grep -E "(3000|8001)"

# Test endpoints
curl https://profile.krishb.in/          # Next.js frontend
kubectl port-forward <pod> 8001:8001
curl http://localhost:8001/docs          # FastAPI docs
```

## 📂 Key Files

- `Dockerfile` - Multi-stage build
- `scripts/docker-entrypoint.sh` - Service startup orchestration
- `k8s/base/secret.yaml` - API keys (gitignored)
- `k8s/base/config-map.yaml` - Environment variables (PORT=3000, PYTHON_PORT=8001)
- `k8s/base/app-deployment.yaml` - Deployment with imagePullPolicy: Always
- `k8s/base/ingress.yaml` - HAProxy ingress configuration
- `agent/main.py` - Line 555: Port configuration prioritizes PYTHON_PORT

## 🔑 Secrets Required

```bash
# Encode secrets
echo -n 'your-google-api-key' | base64

# Apply to cluster
kubectl apply -f k8s/base/secret.yaml
```

## 🌐 Access

**URL:** https://profile.krishb.in

**Docker Hub:** https://hub.docker.com/r/krishbharath/familyman-ui

## 🏗️ Infrastructure

**HAProxy Configuration:**
- Host: HAProxy handles SSL termination with Let's Encrypt cert
- Backend: Routes to k8s ingress controller (10.0.0.197:30080)
- Config: `/etc/haproxy/haproxy.cfg` on host

**Traffic Flow:**
```
Internet → HAProxy (443, SSL) → HAProxy Ingress (30080) → Service (80) → Pod (3000/8001)
```

## 📝 Future Improvements

1. Add dedicated health check endpoints to avoid 405 errors
2. Consider splitting into separate containers for easier scaling
3. Implement horizontal pod autoscaling based on traffic
4. Add monitoring and alerting (Prometheus/Grafana)

See `DEPLOYMENT.md` for complete documentation.
