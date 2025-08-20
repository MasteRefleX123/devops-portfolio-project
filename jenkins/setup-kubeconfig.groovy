import jenkins.model.*
import com.cloudbees.plugins.credentials.*
import com.cloudbees.plugins.credentials.domains.*
import org.jenkinsci.plugins.plaincredentials.impl.*
import hudson.util.Secret

def jenkins = Jenkins.getInstance()
def domain = Domain.global()
def store = jenkins.getExtensionList('com.cloudbees.plugins.credentials.SystemCredentialsProvider')[0].getStore()

// Read kubeconfig from host
def kubeconfigContent = """
apiVersion: v1
kind: Config
clusters:
- cluster:
    server: https://127.0.0.1:35375
    insecure-skip-tls-verify: true
  name: kind-devops-portfolio
contexts:
- context:
    cluster: kind-devops-portfolio
    user: kind-devops-portfolio
  name: kind-devops-portfolio
current-context: kind-devops-portfolio
users:
- name: kind-devops-portfolio
  user:
    client-certificate-data: # Will be populated from actual kubeconfig
    client-key-data: # Will be populated from actual kubeconfig
"""

def kubeconfigCredentials = new FileCredentialsImpl(
    CredentialsScope.GLOBAL,
    "kubeconfig",
    "Kubernetes Config",
    "kubeconfig.yaml",
    SecretBytes.fromBytes(kubeconfigContent.getBytes())
)

def existingKubeconfig = store.getCredentials(domain).find { it.id == "kubeconfig" }
if (existingKubeconfig == null) {
    store.addCredentials(domain, kubeconfigCredentials)
    println("✅ Kubeconfig credentials added")
} else {
    println("Kubeconfig already exists")
}

jenkins.save()
