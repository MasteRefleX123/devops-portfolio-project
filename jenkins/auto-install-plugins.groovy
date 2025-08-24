import jenkins.model.*
import java.util.logging.Logger

def logger = Logger.getLogger("")
def jenkins = Jenkins.getInstance()
def pluginManager = jenkins.getPluginManager()
def updateCenter = jenkins.getUpdateCenter()

def plugins = [
    "git",
    "github",
    "workflow-aggregator",
    "docker-workflow",
    "kubernetes-cli",
    "credentials-binding",
    "ws-cleanup"
]

logger.info("Starting plugin installation...")
updateCenter.updateAllSites()

plugins.each { pluginName ->
    if (!pluginManager.getPlugin(pluginName)) {
        logger.info("Installing plugin: ${pluginName}")
        def plugin = updateCenter.getPlugin(pluginName)
        if (plugin) {
            plugin.deploy()
        }
    } else {
        logger.info("Plugin already installed: ${pluginName}")
    }
}

logger.info("Plugin installation complete!")
jenkins.save()
