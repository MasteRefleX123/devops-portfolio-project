import jenkins.model.*
import java.util.logging.Logger

def logger = Logger.getLogger("")
def installed = false
def initialized = false

def pluginParameter = [
    "workflow-aggregator",
    "git",
    "github", 
    "credentials-binding",
    "pipeline-stage-view",
    "docker-workflow",
    "docker-plugin",
    "kubernetes-cli",
    "junit",
    "htmlpublisher",
    "email-ext",
    "blueocean",
    "workspace-cleanup",
    "timestamper",
    "ansicolor"
]

def plugins = pluginParameter.collect { it.split(':')[0] }

def instance = Jenkins.getInstance()
def pm = instance.getPluginManager()
def uc = instance.getUpdateCenter()

plugins.each {
    logger.info("Checking " + it)
    if (!pm.getPlugin(it)) {
        logger.info("Looking for " + it)
        if (!initialized) {
            uc.updateAllSites()
            initialized = true
        }
        def plugin = uc.getPlugin(it)
        if (plugin) {
            logger.info("Installing " + it)
            def installFuture = plugin.deploy()
            while(!installFuture.isDone()) {
                logger.info("Waiting for plugin install: " + it)
                sleep(3000)
            }
            installed = true
        }
    }
}

if (installed) {
    logger.info("Plugins installed, restarting...")
    instance.save()
    instance.restart()
}
