#!/bin/bash

echo "🚀 Starting DevOps Portfolio Project - All Services"
echo "=================================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}[1/5]${NC} Starting Jenkins..."
cd jenkins && docker compose up -d
sleep 10

echo -e "${GREEN}[2/5]${NC} Checking Kubernetes cluster..."
kubectl get nodes > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Creating kind cluster...${NC}"
    kind create cluster --name devops-portfolio
    kubectl create namespace oriyan-portfolio
fi

echo -e "${GREEN}[3/5]${NC} Checking Kubernetes deployments..."
kubectl get all -n oriyan-portfolio --no-headers | grep -q "deployment"
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Deploying application to Kubernetes...${NC}"
    kubectl apply -f k8s/
fi

echo -e "${GREEN}[4/5]${NC} Starting port-forward to application..."
pkill -f "port-forward.*5001:80" 2>/dev/null
kubectl port-forward -n oriyan-portfolio service/portfolio-service 5001:80 > /dev/null 2>&1 &
echo "✅ Application available at: http://localhost:5001"

echo -e "${GREEN}[5/5]${NC} Starting ngrok tunnel..."
pkill ngrok 2>/dev/null
sleep 2
./ngrok http 8080 > /dev/null 2>&1 &
sleep 5

# Get ngrok URL
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | grep -o '"public_url":"[^"]*' | cut -d'"' -f4 | head -1)

echo ""
echo "=========================================="
echo "✅ All services are running!"
echo "=========================================="
echo "📦 Jenkins: http://localhost:8080"
echo ""
echo "🌐 Application: http://localhost:5001"
echo ""
if [ ! -z "$NGROK_URL" ]; then
    echo "🔗 Ngrok URL: $NGROK_URL"
    echo "   Webhook: ${NGROK_URL}/github-webhook/"
else
    echo "⚠️  Ngrok URL not found. Check: http://localhost:4040"
fi
echo "=========================================="
