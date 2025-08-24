#!/bin/bash
echo "Starting ngrok tunnel to Jenkins (port 8080)..."
./ngrok http 8080 &
NGROK_PID=$!
echo "Ngrok PID: $NGROK_PID"
echo "Waiting for ngrok to start..."
sleep 5
echo ""
echo "==================================="
echo "Ngrok Tunnel Information:"
echo "==================================="
echo "To see the ngrok web interface, open:"
echo "http://localhost:4040"
echo ""
echo "Your public URL will be shown there."
echo "Use it in GitHub webhook as: https://YOUR-URL.ngrok.io/github-webhook/"
echo "==================================="
echo ""
echo "Press Ctrl+C to stop ngrok"
wait $NGROK_PID
