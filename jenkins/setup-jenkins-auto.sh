#!/bin/bash

echo "🚀 Automated Jenkins Setup Script"
echo "================================="

JENKINS_URL="http://localhost:8080"
ADMIN_PASS="5b0b4d9541df4ef1a8e821673adec63d"
JENKINS_CLI="/var/jenkins_home/jenkins-cli.jar"

# Download Jenkins CLI
echo "📥 Downloading Jenkins CLI..."
docker exec jenkins-server wget -q -O $JENKINS_CLI $JENKINS_URL/jnlpJars/jenkins-cli.jar 2>/dev/null

# Install essential plugins
echo "🔌 Installing plugins..."
PLUGINS=(
    "github"
    "git"
    "workflow-aggregator"
    "pipeline-stage-view"
    "docker-workflow"
    "credentials-binding"
    "ws-cleanup"
)

for plugin in "${PLUGINS[@]}"; do
    echo "  Installing: $plugin"
    docker exec jenkins-server java -jar $JENKINS_CLI -s $JENKINS_URL -auth admin:$ADMIN_PASS install-plugin $plugin -deploy 2>/dev/null || true
done

echo "✅ Plugins installed!"
echo "🔄 Restarting Jenkins..."
docker exec jenkins-server java -jar $JENKINS_CLI -s $JENKINS_URL -auth admin:$ADMIN_PASS safe-restart 2>/dev/null || true

echo "⏳ Waiting for Jenkins to restart (60 seconds)..."
sleep 60

echo "✅ Setup complete!"
