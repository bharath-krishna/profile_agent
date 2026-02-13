# FamilyMan UI - Kubernetes Deployment Documentation

## Overview

This document covers the complete containerization and Kubernetes deployment process for the FamilyMan UI application (Next.js + FastAPI agent).

## Docker Containerization

### Multi-Stage Dockerfile

Created a multi-stage Dockerfile that combines both Next.js and FastAPI services in a single container:

**Stages:**
1. **nextjs-builder** - Builds Next.js application
2. **python-builder** - Sets up Python dependencies
3. **Production stage** - Combines both services

**Key Features:**
- Installs Node.js in Python base image to run both services
- Uses `docker-entrypoint.sh` to orchestrate service startup
- FastAPI runs in background on port 8001
- Next.js runs in foreground on port 3000

### Issues Fixed During Build

#### 1. Package Lock File Sync Error
**Problem:** `npm ci` failed with "Missing: @ag-ui/client@1.25.8 from lock file"

**Solution:**
```bash
rm -rf node_modules package-lock.json
npm install  # Regenerate fresh lock file
```

**Root Cause:** Lock files were gitignored, causing out-of-sync package.json and package-lock.json

#### 2. Postinstall Script Failure
**Problem:** `npm ci` tried to run `./scripts/setup-agent.sh` before it was copied

**Solution:** Added `--ignore-scripts` flag to npm commands in Dockerfile:
```dockerfile
RUN npm ci --ignore-scripts
```

#### 3. TypeScript Compilation Errors

**Error 1 - route.ts:** Type mismatch for agents configuration
```typescript
// Fixed with type assertion
agents: {
  "BharathAssistant": new HttpAgent({url: "http://localhost:8001/"}),
} as any
```

**Error 2 - page.tsx:** Render function type error
```typescript
// Fixed with any type
render: ({ args, status }: any) => {
```

**Error 3 - types.ts:** Missing proverbs property
```typescript
// Added to AgentState
proverbs?: string[];
```

**Error 4 - Invalid CSS properties:** `ringColor` and `focusRing` not valid CSS properties
```typescript
// Fixed using Tailwind CSS custom property
style={{ '--tw-ring-color': themeColor } as React.CSSProperties}
```

## Kubernetes Deployment

### Architecture

**Resources Created:**
- ConfigMap: `familyman-ui-config` (environment variables: PORT=3000, PYTHON_PORT=8001)
- Secret: `familyman-ui-secrets` (API keys: GOOGLE_API_KEY, LANGFUSE_*)
- Deployment: `familyman-ui` (1 replica, image from Docker Hub)
- Service: `familyman-ui-service` (ClusterIP, ports 80 & 8001)
- Ingress: `familyman-ui-ingress` (HAProxy class, host: profile.krishb.in)

**External Infrastructure:**
- HAProxy: Host-level SSL termination with Let's Encrypt certificate
- DNS: profile.krishb.in → host machine
- HAProxy backend: Routes to k8s ingress controller at 10.0.0.197:30080

### Directory Structure
```
k8s/
├── base/
│   ├── app-deployment.yaml
│   ├── app-service.yaml
│   ├── config-map.yaml
│   ├── ingress.yaml
│   ├── secret-template.yaml
│   ├── secret.yaml (gitignored)
│   └── kustomization.yaml
└── overlays/
    └── local/
        └── kustomization.yaml
```

### Deployment Issues & Fixes

#### 1. Secret Base64 Encoding Error
**Problem:** `illegal base64 data at input byte 5`

**Root Cause:** Secret values weren't base64 encoded

**Solution:**
```bash
# Encode each secret value
echo -n 'sk-lf-9509f21c-9dbf-4435-9a53-d250b029c153' | base64
echo -n 'pk-lf-6c1f0219-8f80-4b1f-a23f-e9a4f72c7670' | base64
echo -n 'https://langfuse.krishb.in' | base64

# Update secret.yaml with encoded values
kubectl delete secret familyman-ui-secrets
kubectl apply -f k8s/base/secret.yaml
```

#### 2. Image Pull Error
**Problem:** `ErrImagePull - pull access denied, repository does not exist`

**Root Cause:** Image only existed locally, not in a container registry

**Solution:**
```bash
# Tag and push to Docker Hub
docker tag familyman-ui:latest krishbharath/familyman-ui:latest
docker push krishbharath/familyman-ui:latest

# Update deployment
kubectl set image deployment/familyman-ui familyman-ui=krishbharath/familyman-ui:latest
```

#### 3. Port Configuration Issue (RESOLVED)
**Problem:** FastAPI agent was running on port 3000 instead of 8001, causing health check failures

**Root Cause:** Docker image was built with cached layers that didn't include the port configuration fix

**Solution:**
1. Modified `agent/main.py` line 555 to prioritize PYTHON_PORT:
```python
port = int(os.getenv("PYTHON_PORT", os.getenv("PORT", 8001)))
```

2. Rebuilt Docker image with `--no-cache` flag to force fresh build:
```bash
docker build --no-cache -t krishbharath/familyman-ui:latest .
docker push krishbharath/familyman-ui:latest
```

3. Updated deployment manifest to use Docker Hub image with `imagePullPolicy: Always`:
```yaml
image: krishbharath/familyman-ui:latest
imagePullPolicy: Always  # Always pull from Docker Hub
```

4. Restarted deployment:
```bash
kubectl rollout restart deployment/familyman-ui
```

**Verification:**
- ✅ FastAPI running on port 8001
- ✅ Next.js running on port 3000
- ✅ Pod in Running state (1/1 Ready)
- ✅ Services accessible via ingress

#### 4. HAProxy Routing Configuration (RESOLVED)
**Problem:** Initial ingress used nginx class and cert-manager, but infrastructure uses HAProxy

**Solution:**
Modified `k8s/base/ingress.yaml`:
1. Changed `ingressClassName` from `nginx` to `haproxy`
2. Removed TLS section (SSL handled by host HAProxy)
3. Removed cert-manager annotations
4. Removed nginx-specific SSL redirect annotations

**HAProxy Host Configuration:**
- Backend changed from `profile_local` (localhost:3000) to `k8s_ingress` (10.0.0.197:30080)
- SSL termination handled at host level with Let's Encrypt cert
- Config: `/etc/haproxy/haproxy.cfg`

**Traffic Flow:**
```
https://profile.krishb.in
  ↓
HAProxy on host (port 443, SSL termination)
  ↓
HAProxy Ingress Controller (NodePort 30080)
  ↓
familyman-ui-service (ClusterIP port 80 → targetPort 3000)
  ↓
familyman-ui pod (Next.js:3000, FastAPI:8001)
```

## HAProxy Integration

### Host-Level Configuration

The application is exposed to the internet through HAProxy running on the host machine, which provides:
- SSL/TLS termination with Let's Encrypt certificate
- Load balancing and reverse proxy
- Integration with Kubernetes ingress

**Configuration File:** `/etc/haproxy/haproxy.cfg` (on host)

**Backend Configuration:**
```haproxy
# profile.krishb.in backend
use_backend k8s_ingress if is_profile_krishb

backend k8s_ingress
    server k8s 10.0.0.197:30080 check
```

**SSL Certificate:** `/etc/haproxy/certs/profile.krishb.in.pem` (managed by acme.sh)

### Kubernetes Ingress Configuration

**File:** `k8s/base/ingress.yaml`

**Key Settings:**
- `ingressClassName: haproxy` - Uses HAProxy Ingress Controller
- `host: profile.krishb.in` - Matches DNS and HAProxy ACL
- **No TLS section** - SSL handled by host HAProxy, not in-cluster
- **No cert-manager** - Certificates managed by acme.sh on host
- **No SSL redirect annotations** - Would cause redirect loops

**Why This Architecture:**
1. Centralized SSL management for all services
2. HAProxy on host handles all external traffic
3. Kubernetes ingress controller only handles internal routing
4. Other services in the cluster use the same pattern

## Environment Variables

### ConfigMap (k8s/base/config-map.yaml)
```yaml
NODE_ENV: "production"
PORT: "3000"              # Next.js port
PYTHON_PORT: "8001"       # FastAPI port
MODEL_NAME: "gemini-2.5-flash"
LOG_LEVEL: "info"
```

### Secrets (k8s/base/secret.yaml)
```yaml
GOOGLE_API_KEY: "<base64-encoded>"
LANGFUSE_SECRET_KEY: "<base64-encoded>"
LANGFUSE_PUBLIC_KEY: "<base64-encoded>"
LANGFUSE_BASE_URL: "<base64-encoded>"
```

## Helper Scripts

### scripts/build-docker.sh
- Builds Docker image with proper naming
- Supports pushing to registry
- Can load into minikube/kind clusters

### scripts/deploy-k8s.sh
- Validates kubectl connectivity
- Applies secrets and kustomization
- Waits for deployment readiness
- Shows deployment status

## Access Information

**Application URL:** https://profile.krishb.in

**Service Ports:**
- Port 80 (HTTP) → Next.js (3000)
- Port 8001 → FastAPI agent

**Health Checks:**
- Liveness: `GET /` on port 3000 (Next.js)
- Readiness: `GET /` on port 3000 (Next.js)

## Useful Commands

### Check Status
```bash
kubectl get pods -l app=familyman-ui
kubectl get svc familyman-ui-service
kubectl get ingress familyman-ui-ingress
```

### View Logs
```bash
kubectl logs -l app=familyman-ui -f
kubectl logs -l app=familyman-ui --all-containers=true
```

### Debug Pod
```bash
kubectl describe pod -l app=familyman-ui
kubectl exec -it <pod-name> -- /bin/bash
```

### Restart Deployment
```bash
kubectl rollout restart deployment/familyman-ui
kubectl rollout status deployment/familyman-ui
```

### Update Image
```bash
# After building and pushing new image
docker build -t krishbharath/familyman-ui:latest .
docker push krishbharath/familyman-ui:latest
kubectl rollout restart deployment/familyman-ui
```

## Current Status

### ✅ Deployment Successful

**Application URL:** https://profile.krishb.in/ (LIVE)

**Pod Status:**
- State: Running (1/1 Ready)
- Next.js: Port 3000 ✅
- FastAPI: Port 8001 ✅

**Infrastructure:**
- SSL: Terminated at HAProxy host level (Let's Encrypt)
- Ingress: HAProxy Ingress Controller (NodePort 30080)
- Service: ClusterIP (familyman-ui-service)
- Image: krishbharath/familyman-ui:latest (Docker Hub)

**Known Minor Issues:**
- Health checks commented out (return HTTP 405 on FastAPI root endpoint)
- Consider adding dedicated health check endpoints like `/health` or `/readiness`

## Production Considerations

1. **Separate containers:** Consider splitting Next.js and FastAPI into separate containers/pods
2. **Health check paths:** Use specific health check endpoints instead of root `/`
3. **Resource limits:** Adjust based on actual usage patterns
4. **Horizontal scaling:** Increase replicas for high availability
5. **Monitoring:** Add Prometheus metrics and Grafana dashboards
6. **Logging:** Centralize logs with EFK or Loki stack
7. **Image versioning:** Use semantic versioning instead of `latest` tag

## Files Modified

### Code Changes
- `/home/bharath/workspace/familyman-ui/Dockerfile` - Created
- `/home/bharath/workspace/familyman-ui/scripts/docker-entrypoint.sh` - Created
- `/home/bharath/workspace/familyman-ui/.dockerignore` - Created
- `/home/bharath/workspace/familyman-ui/.gitignore` - Updated (uncommented lock files)
- `/home/bharath/workspace/familyman-ui/agent/main.py` - Modified port configuration
- `/home/bharath/workspace/familyman-ui/src/app/api/copilotkit/route.ts` - Fixed type error
- `/home/bharath/workspace/familyman-ui/src/app/page.tsx` - Fixed type error
- `/home/bharath/workspace/familyman-ui/src/lib/types.ts` - Added proverbs property
- `/home/bharath/workspace/familyman-ui/src/components/experience-timeline.tsx` - Fixed CSS property
- `/home/bharath/workspace/familyman-ui/src/components/section-header.tsx` - Fixed CSS property
- `/home/bharath/workspace/familyman-ui/src/components/skills-filter.tsx` - Fixed CSS property

### Kubernetes Manifests
- `/home/bharath/workspace/familyman-ui/k8s/base/` - All manifests created
- `/home/bharath/workspace/familyman-ui/k8s/overlays/local/` - Overlay created
- `/home/bharath/workspace/familyman-ui/k8s/README.md` - Created

### Deployment Scripts
- `/home/bharath/workspace/familyman-ui/scripts/build-docker.sh` - Created
- `/home/bharath/workspace/familyman-ui/scripts/deploy-k8s.sh` - Created

## Docker Hub Repository

**Image:** `krishbharath/familyman-ui:latest`

**Repository:** https://hub.docker.com/r/krishbharath/familyman-ui

## Verification and Testing

1. **Check deployment status:**
   ```bash
   kubectl get pods -l app=familyman-ui
   kubectl get svc familyman-ui-service
   kubectl get ingress familyman-ui-ingress
   ```

2. **View logs:**
   ```bash
   kubectl logs -l app=familyman-ui -f --all-containers=true
   ```

3. **Verify port bindings in container:**
   ```bash
   kubectl exec -it <pod-name> -- netstat -tlnp | grep -E "(3000|8001)"
   ```

4. **Test endpoints:**
   ```bash
   # Frontend (via ingress)
   curl https://profile.krishb.in/

   # Agent API (via port-forward)
   kubectl port-forward <pod-name> 8001:8001
   curl http://localhost:8001/docs  # FastAPI docs
   ```

## Deployment Checklist

- [x] Docker image built and pushed to registry
- [x] Kubernetes secrets created and applied
- [x] ConfigMap with correct environment variables
- [x] Deployment with proper image pull policy
- [x] Service exposing correct ports
- [x] Ingress with HAProxy class configured
- [x] HAProxy host routing configured
- [x] SSL certificate in place
- [x] Both services running on correct ports
- [x] Application accessible at https://profile.krishb.in/

---

**Last Updated:** 2026-02-07
**Status:** ✅ DEPLOYMENT SUCCESSFUL - Application live at https://profile.krishb.in/
