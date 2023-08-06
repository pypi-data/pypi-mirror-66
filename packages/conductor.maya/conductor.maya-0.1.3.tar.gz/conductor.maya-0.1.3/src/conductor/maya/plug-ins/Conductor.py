import sys

# The template mut be imported before the plugin node.
import maya.api.OpenMaya as om

from conductor.maya.lib.ae import AEconductorRenderTemplate
from conductor.maya.lib import conductor_menu
from conductor.maya.lib.nodes.conductorRender import conductorRender


def maya_useNewAPI():
    pass


def initializePlugin(obj):
    plugin = om.MFnPlugin(obj, "Conductor", "1.0.0", "Any")
    try:
        plugin.registerNode(
            "conductorRender",
            conductorRender.id,
            conductorRender.creator,
            conductorRender.initialize,
            om.MPxNode.kDependNode,
        )
    except:
        sys.stderr.write("Failed to register conductorRender\n")
        raise

    conductor_menu.load()


def uninitializePlugin(obj):
    plugin = om.MFnPlugin(obj)

    try:
        plugin.deregisterNode(conductorRender.id)
    except:
        sys.stderr.write("Failed to deregister conductorRender\n")
        raise

    conductor_menu.unload()
