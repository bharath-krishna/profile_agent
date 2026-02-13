#!/bin/bash
# Build script for FamilyMan UI Docker image

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Building FamilyMan UI Docker image...${NC}"

# Get the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

cd "$PROJECT_ROOT"

# Default image name and tag
IMAGE_NAME="${IMAGE_NAME:-familyman-ui}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
REGISTRY="${REGISTRY:-}"

# Full image name
if [ -n "$REGISTRY" ]; then
    FULL_IMAGE_NAME="$REGISTRY/$IMAGE_NAME:$IMAGE_TAG"
else
    FULL_IMAGE_NAME="$IMAGE_NAME:$IMAGE_TAG"
fi

echo -e "${BLUE}Building image: $FULL_IMAGE_NAME${NC}"

# Build the image
docker build \
    --tag "$FULL_IMAGE_NAME" \
    --file Dockerfile \
    .

echo -e "${GREEN}✓ Successfully built: $FULL_IMAGE_NAME${NC}"

# Ask if user wants to push to registry
if [ -n "$REGISTRY" ]; then
    echo ""
    read -p "Push to registry $REGISTRY? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}Pushing image to registry...${NC}"
        docker push "$FULL_IMAGE_NAME"
        echo -e "${GREEN}✓ Successfully pushed: $FULL_IMAGE_NAME${NC}"
    fi
fi

# If using minikube or kind, offer to load the image
if command -v minikube &> /dev/null && minikube status &> /dev/null; then
    echo ""
    read -p "Load image into minikube? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}Loading image into minikube...${NC}"
        minikube image load "$FULL_IMAGE_NAME"
        echo -e "${GREEN}✓ Image loaded into minikube${NC}"
    fi
elif command -v kind &> /dev/null && kind get clusters &> /dev/null; then
    echo ""
    read -p "Load image into kind? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}Loading image into kind...${NC}"
        kind load docker-image "$FULL_IMAGE_NAME"
        echo -e "${GREEN}✓ Image loaded into kind${NC}"
    fi
fi

echo ""
echo -e "${GREEN}Build complete!${NC}"
echo -e "Image: ${BLUE}$FULL_IMAGE_NAME${NC}"
echo ""
echo "Next steps:"
echo "1. Create your secrets: cp k8s/base/secret-template.yaml k8s/base/secret.yaml"
echo "2. Edit k8s/base/secret.yaml with your base64-encoded secrets"
echo "3. Deploy to k8s: kubectl apply -k k8s/overlays/local"
