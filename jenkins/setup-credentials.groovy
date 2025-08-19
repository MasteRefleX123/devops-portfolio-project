import jenkins.model.*
import com.cloudbees.plugins.credentials.*
import com.cloudbees.plugins.credentials.common.*
import com.cloudbees.plugins.credentials.domains.*
import com.cloudbees.plugins.credentials.impl.*
import org.jenkinsci.plugins.plaincredentials.impl.*
import hudson.util.Secret

def jenkins = Jenkins.getInstance()
def domain = Domain.global()
def store = jenkins.getExtensionList('com.cloudbees.plugins.credentials.SystemCredentialsProvider')[0].getStore()

// Docker Hub Credentials
def dockerUser = new UsernamePasswordCredentialsImpl(
    CredentialsScope.GLOBAL,
    "docker-hub",
    "Docker Hub Credentials",
    "mastereflex123",
    "YOUR_DOCKER_PASSWORD"
)

// GitHub Token
def githubToken = new StringCredentialsImpl(
    CredentialsScope.GLOBAL,
    "github-token",
    "GitHub Personal Access Token",
    Secret.fromString("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")
)

// Add credentials
store.addCredentials(domain, dockerUser)
store.addCredentials(domain, githubToken)

println "Credentials configured successfully!"
