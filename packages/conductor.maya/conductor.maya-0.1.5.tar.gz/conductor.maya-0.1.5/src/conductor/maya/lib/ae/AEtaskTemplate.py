"""
Handle the UI for extra assets:
"""

import pymel.core as pm
from conductor.maya.lib import const as k


class AEtaskTemplate(object):
    def __init__(self, aet):
        self.template_field = None
        self.popup = None

        aet.callCustom(self.new_ui, self.replace_ui, "taskTemplate")

    def new_ui(self, node_attr):
        """Build static UI"""

        self.template_field = pm.textFieldGrp(label="Task Template")
        label = pm.layout(self.template_field, query=True, childArray=True)[0]

        self.popup = pm.popupMenu(parent=label)
        pm.menuItem(label="Reset")

        self.replace_ui(node_attr)

    def replace_ui(self, node_attr):
        """Reconfigure UI for the current node"""
        attr = pm.Attribute(node_attr)
        text = attr.get()
        pm.setUITemplate("attributeEditorTemplate", pushTemplate=True)
        pm.textFieldGrp(
            self.template_field,
            edit=True,
            text=text,
            changeCommand=pm.Callback(self.on_text_changed, attr),
        )

        items = pm.popupMenu(self.popup, query=True, itemArray=True)
        pm.menuItem(items[0], edit=True, command=pm.Callback(self.on_reset, attr))
        pm.setUITemplate(ppt=True)

    def on_text_changed(self, attribute):
        template = pm.textFieldGrp(self.template_field, query=True, text=True)
        attribute.set(template)

    def on_reset(self, attribute):
        attribute.set(k.DEFAULT_TEMPLATE)
        pm.textFieldGrp(self.template_field, edit=True, text=k.DEFAULT_TEMPLATE)
