"""
Handle the UI for extra assets:
"""

import pymel.core as pm
from conductor.maya.lib import const as k


class AEdestination(object):
    def __init__(self, aet):
        self.path_field = None
        self.browse_button = None

        aet.callCustom(self.new_ui, self.replace_ui, "destinationDirectory")

    def new_ui(self, node_attr):
        """Build static UI"""

        pm.rowLayout(
            numberOfColumns=3,
            adjustableColumn=2,
            columnWidth3=(k.AE_TEXT_WIDTH, 100, 25),
            columnAttach=((1, "both", 0), (2, "both", 0), (3, "both", 0)),
        )
        pm.text(label="Destination Directory")
        self.path_field = pm.textField()

        self.browse_button = pm.symbolButton(
            image="SP_DirClosedIcon.png", width=24, height=24
        )

        pm.setParent("..")

        self.replace_ui(node_attr)

    def replace_ui(self, node_attr):
        """Reconfigure UI for the current node"""

        attr = pm.Attribute(node_attr)
        pm.setUITemplate("attributeEditorTemplate", pushTemplate=True)

        path = attr.get()
        pm.textField(
            self.path_field,
            edit=True,
            text=path,
            changeCommand=pm.Callback(self.on_path_changed, attr),
        )

        pm.symbolButton(
            self.browse_button,
            edit=True,
            command=pm.Callback(self.on_browse_button, attr),
        )

        pm.setUITemplate(ppt=True)

    def on_browse_button(self, attr):
        path = browse_for_dest_directory()
        if path:
            attr.set(path)
            pm.textField(self.path_field, edit=True, text=path)

    def on_path_changed(self, attr):
        path = pm.textField(self.path_field, query=True, text=True)
        attr.set(path)


def browse_for_dest_directory():
    entries = pm.fileDialog2(
        caption="Choose Directory",
        okCaption="Choose",
        fileFilter="*",
        dialogStyle=2,
        fileMode=3,
        dir=pm.workspace.getPath(),
    )
    if entries:
        return entries[0]
    pm.displayWarning("No files Selected")
