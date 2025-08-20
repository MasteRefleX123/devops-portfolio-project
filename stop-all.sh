#!/bin/bash

echo "🛑 Stopping DevOps Portfolio Project Services"
echo "============================================"

echo "Stopping port-forward..."
pkill -f "port-forward.*5001:80" 2>/dev/null

echo "Stopping ngrok..."
pkill ngrok 2>/dev/null

echo "Stopping Jenkins..."
cd jenkins && docker compose down

echo "✅ All services stopped!"
echo ""
echo "Note: Kubernetes deployments are still running."
echo "To stop them: kubectl delete namespace oriyan-portfolio"
