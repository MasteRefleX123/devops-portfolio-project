import jenkins.model.*
import hudson.plugins.git.*
import org.jenkinsci.plugins.workflow.job.WorkflowJob

def jenkins = Jenkins.getInstance()

// Update the Pipeline job to include Slack notifications
def jobName = "devops-portfolio"
def job = jenkins.getItem(jobName)

if (job != null && job instanceof WorkflowJob) {
    println("Adding Slack notification configuration to job: ${jobName}")
    
    // Add a description with Slack configuration instructions
    job.setDescription("""
    <h3>DevOps Portfolio Pipeline</h3>
    <p>This pipeline builds, tests, and deploys the portfolio application.</p>
    
    <h4>Slack Notifications:</h4>
    <p>To enable Slack notifications:</p>
    <ol>
        <li>Install the Slack Notification Plugin</li>
        <li>Configure Slack workspace in Jenkins global settings</li>
        <li>Add SLACK_CHANNEL environment variable to the job</li>
    </ol>
    
    <h4>Webhook Configuration:</h4>
    <p>GitHub webhook should point to: [ngrok-url]/github-webhook/</p>
    """)
    
    job.save()
    println("✅ Job description updated with Slack configuration")
} else {
    println("Job not found or not a Pipeline job: ${jobName}")
}
