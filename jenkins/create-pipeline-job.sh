#!/bin/bash

JENKINS_URL="http://localhost:8080"
USER="admin"
PASS="5b0b4d9541df4ef1a8e821673adec63d"
JOB_NAME="devops-portfolio"

echo "Creating Pipeline Job: $JOB_NAME"

# Create job XML
cat > /tmp/job-config.xml << 'JOBXML'
<?xml version='1.1' encoding='UTF-8'?>
<flow-definition plugin="workflow-job">
  <description>DevOps Portfolio CI/CD Pipeline</description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <org.jenkinsci.plugins.workflow.job.properties.PipelineTriggersJobProperty>
      <triggers>
        <hudson.triggers.SCMTrigger>
          <spec>H/5 * * * *</spec>
        </hudson.triggers.SCMTrigger>
      </triggers>
    </org.jenkinsci.plugins.workflow.job.properties.PipelineTriggersJobProperty>
  </properties>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition">
    <scm class="hudson.plugins.git.GitSCM">
      <configVersion>2</configVersion>
      <userRemoteConfigs>
        <hudson.plugins.git.UserRemoteConfig>
          <url>https://gitlab.com/MasteRefleX123/devops-portfolio-project.git</url>
        </hudson.plugins.git.UserRemoteConfig>
      </userRemoteConfigs>
      <branches>
        <hudson.plugins.git.BranchSpec>
          <name>*/feature/day2-docker-kubernetes</name>
        </hudson.plugins.git.BranchSpec>
      </branches>
    </scm>
    <scriptPath>Jenkinsfile</scriptPath>
    <lightweight>true</lightweight>
  </definition>
</flow-definition>
JOBXML

# Create the job
curl -X POST "$JENKINS_URL/createItem?name=$JOB_NAME" \
  --user $USER:$PASS \
  --header "Content-Type: application/xml" \
  --data-binary @/tmp/job-config.xml

echo ""
echo "✅ Job created: $JOB_NAME"
echo "🔗 View at: $JENKINS_URL/job/$JOB_NAME"
