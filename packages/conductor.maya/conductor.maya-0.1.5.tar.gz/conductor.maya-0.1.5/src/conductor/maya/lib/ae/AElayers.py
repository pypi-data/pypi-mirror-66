"""
Handle the UI for layers

"""
import pymel.core as pm
from conductor.maya.lib import const as k


class AElayers(object):
    def __init__(self, aet):
        self.menu = None
        aet.callCustom(self.new_ui, self.replace_ui, "renderLayers")

    def new_ui(self, node_attr):
        """Build static UI"""
        pm.rowLayout(
            numberOfColumns=2,
            columnWidth2=(k.AE_TEXT_WIDTH, 200),
            columnAttach=((1, "both", 0), (2, "both", 0)),
        )
        pm.text(label="Render Layers")

        self.menu = pm.attrEnumOptionMenu(label="", width=200, attribute=node_attr)

        pm.setParent("..")
        self.replace_ui(node_attr)

    def replace_ui(self, node_attr):
        """Reconfigure UI for the current node"""
        pm.setUITemplate("attributeEditorTemplate", pushTemplate=True)
        pm.attrEnumOptionMenu(self.menu, edit=True, attribute=node_attr)
        pm.setUITemplate(ppt=True)
