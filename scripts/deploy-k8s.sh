#!/bin/bash
# Deployment script for FamilyMan UI to Kubernetes

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

cd "$PROJECT_ROOT"

# Default overlay
OVERLAY="${1:-local}"

echo -e "${BLUE}Deploying FamilyMan UI to Kubernetes (overlay: $OVERLAY)...${NC}"

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}Error: kubectl is not installed or not in PATH${NC}"
    exit 1
fi

# Check if cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED}Error: Cannot connect to Kubernetes cluster${NC}"
    exit 1
fi

# Check if secret exists
if [ ! -f "k8s/base/secret.yaml" ]; then
    echo -e "${YELLOW}Warning: k8s/base/secret.yaml not found!${NC}"
    echo "Please create it from the template:"
    echo "  cp k8s/base/secret-template.yaml k8s/base/secret.yaml"
    echo "  # Edit secret.yaml and add your base64-encoded secrets"
    echo ""
    read -p "Continue without applying secrets? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo -e "${BLUE}Applying secrets...${NC}"
    kubectl apply -f k8s/base/secret.yaml
    echo -e "${GREEN}✓ Secrets applied${NC}"
fi

# Apply kustomization
echo -e "${BLUE}Applying kustomization from k8s/overlays/$OVERLAY...${NC}"
kubectl apply -k "k8s/overlays/$OVERLAY"

echo -e "${GREEN}✓ Deployment applied${NC}"

# Wait for deployment to be ready
echo -e "${BLUE}Waiting for deployment to be ready...${NC}"
kubectl wait --for=condition=available --timeout=300s deployment/familyman-ui

echo -e "${GREEN}✓ Deployment is ready!${NC}"

# Show status
echo ""
echo -e "${BLUE}Deployment status:${NC}"
kubectl get pods -l app=familyman-ui
echo ""
kubectl get svc familyman-ui-service
echo ""
kubectl get ingress familyman-ui-ingress

# Get ingress URL
echo ""
echo -e "${GREEN}Application deployed successfully!${NC}"
echo -e "Access at: ${BLUE}https://profile.krishb.in${NC}"
echo ""
echo "Useful commands:"
echo "  View logs:    kubectl logs -l app=familyman-ui -f"
echo "  Get pods:     kubectl get pods -l app=familyman-ui"
echo "  Describe pod: kubectl describe pod -l app=familyman-ui"
echo "  Port forward: kubectl port-forward svc/familyman-ui-service 3000:80 8001:8001"
echo "  Delete:       kubectl delete -k k8s/overlays/$OVERLAY"
