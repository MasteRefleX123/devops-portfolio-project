#!/usr/bin/env bash
set -euo pipefail
IMAGE_NAME=${IMAGE_NAME:-jenkins-agent-local}
IMAGE_TAG=${IMAGE_TAG:-latest}
DOCKER_BUILDKIT=1 docker build -t "$IMAGE_NAME:$IMAGE_TAG" -f "$(dirname "$0")/Dockerfile-agent" "$(dirname "$0")"
echo "Built $IMAGE_NAME:$IMAGE_TAG"


