#!/bin/bash

# Jenkins CLI URL
JENKINS_URL="http://localhost:8080"
ADMIN_PASSWORD="5b0b4d9541df4ef1a8e821673adec63d"

# List of plugins to install
PLUGINS=(
    "workflow-aggregator"
    "git"
    "github"
    "credentials-binding"
    "pipeline-stage-view"
    "docker-workflow"
    "docker-plugin"
    "kubernetes-cli"
    "junit"
    "cobertura"
    "htmlpublisher"
    "email-ext"
    "slack"
    "blueocean"
    "dark-theme"
    "workspace-cleanup"
    "timestamper"
    "ansicolor"
    "matrix-auth"
    "role-strategy"
    "configuration-as-code"
)

echo "Installing Jenkins plugins..."

# Download Jenkins CLI
docker exec jenkins-server wget -O /var/jenkins_home/jenkins-cli.jar ${JENKINS_URL}/jnlpJars/jenkins-cli.jar

# Install plugins
for plugin in "${PLUGINS[@]}"
do
    echo "Installing plugin: $plugin"
    docker exec jenkins-server java -jar /var/jenkins_home/jenkins-cli.jar -s ${JENKINS_URL} -auth admin:${ADMIN_PASSWORD} install-plugin $plugin -restart || true
done

echo "Plugins installation initiated. Jenkins will restart..."
