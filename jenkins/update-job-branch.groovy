import jenkins.model.*
import hudson.plugins.git.*

def jenkins = Jenkins.getInstance()
def job = jenkins.getItem("devops-portfolio")

if (job) {
    def scm = job.getDefinition().getScm()
    if (scm instanceof GitSCM) {
        // Update branch to new one
        scm.branches = [new BranchSpec("*/feature/day5-monitoring")]
        job.save()
        println("✅ Updated job to use branch: feature/day5-monitoring")
    }
} else {
    println("❌ Job not found")
}
