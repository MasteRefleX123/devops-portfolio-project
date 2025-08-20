import jenkins.model.*
import hudson.plugins.git.*
import org.jenkinsci.plugins.workflow.job.WorkflowJob
import org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition
import hudson.triggers.SCMTrigger

def jenkins = Jenkins.getInstance()

// Check if job already exists
def jobName = "devops-portfolio"
def job = jenkins.getItem(jobName)

if (job == null) {
    println("Creating Pipeline job: ${jobName}")
    
    // Create new Pipeline job
    job = jenkins.createProject(WorkflowJob.class, jobName)
    
    // Configure Git repository
    def gitRepo = "https://github.com/MasteRefleX123/devops-portfolio-project.git"
    def gitBranch = "*/feature/day2-docker-kubernetes"
    def scriptPath = "Jenkinsfile"
    
    def scm = new GitSCM(gitRepo)
    scm.branches = [new BranchSpec(gitBranch)]
    
    def scmFlowDefinition = new CpsScmFlowDefinition(scm, scriptPath)
    job.setDefinition(scmFlowDefinition)
    
    // Add GitHub webhook trigger
    def githubTrigger = new SCMTrigger("")
    job.addTrigger(githubTrigger)
    
    job.save()
    println("✅ Pipeline job created successfully: ${jobName}")
} else {
    println("Job already exists: ${jobName}")
}
