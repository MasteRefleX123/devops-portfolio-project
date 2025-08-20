import jenkins.model.*
import org.jenkinsci.plugins.workflow.job.WorkflowJob
import com.cloudbees.jenkins.GitHubPushTrigger
import hudson.plugins.git.*

def jenkins = Jenkins.getInstance()
def job = jenkins.getItem("devops-portfolio")

if (job != null && job instanceof WorkflowJob) {
    println("Fixing Pipeline job triggers...")
    
    // Clear existing triggers
    job.triggers.clear()
    
    // Add GitHub push trigger
    def githubPushTrigger = new GitHubPushTrigger()
    job.addTrigger(githubPushTrigger)
    
    // Save the job
    job.save()
    
    println("✅ Pipeline job fixed - GitHub webhook trigger added")
} else {
    println("❌ Job not found: devops-portfolio")
}
