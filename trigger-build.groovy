import jenkins.model.*
def job = Jenkins.getInstance().getItem("devops-portfolio")
if (job) {
    def cause = new hudson.model.Cause.UserIdCause()
    job.scheduleBuild(0, cause)
    println("Build triggered!")
} else {
    println("Job not found")
}
