"""
Handle the UI for extra assets:
"""

import pymel.core as pm
from conductor.maya.lib import const as k


class AEextraAssets(object):
    def __init__(self, aet):
        self.manage_btn = None
        self.form = None
        self.clear_sel_btn = None
        self.clear_all_btn = None
        self.browse_file_btn = None
        self.browse_dir_btn = None
        self.scroll_list = None
        aet.callCustom(self.new_ui, self.replace_ui, "extraAssets")

    def new_ui(self, node_attr):
        """Build static UI"""

        self.form = pm.formLayout(nd=100, height=200)
        self.clear_all_btn = pm.button(label="Clear All", height=24)
        self.clear_sel_btn = pm.button(label="Remove Selection", height=24)
        self.browse_file_btn = pm.button(label="Browse Files", height=24)
        self.browse_dir_btn = pm.button(label="Browse Folder", height=24)

        self.scroll_list = pm.textScrollList(numberOfRows=10, allowMultiSelection=True)

        self.form.attachForm(self.clear_all_btn, "left", 2)
        self.form.attachPosition(self.clear_all_btn, "right", 2, 25)
        self.form.attachForm(self.clear_all_btn, "top", 2)
        self.form.attachNone(self.clear_all_btn, "bottom")

        self.form.attachPosition(self.clear_sel_btn, "left", 2, 25)
        self.form.attachPosition(self.clear_sel_btn, "right", 2, 50)
        self.form.attachForm(self.clear_sel_btn, "top", 2)
        self.form.attachNone(self.clear_sel_btn, "bottom")

        self.form.attachPosition(self.browse_file_btn, "left", 2, 50)
        self.form.attachPosition(self.browse_file_btn, "right", 2, 75)
        self.form.attachForm(self.browse_file_btn, "top", 2)
        self.form.attachNone(self.browse_file_btn, "bottom")

        self.form.attachPosition(self.browse_dir_btn, "left", 2, 75)
        self.form.attachForm(self.browse_dir_btn, "right", 2)
        self.form.attachForm(self.browse_dir_btn, "top", 2)
        self.form.attachNone(self.browse_dir_btn, "bottom")

        self.form.attachForm(self.scroll_list, "left", 2)
        self.form.attachForm(self.scroll_list, "right", 2)
        self.form.attachControl(self.scroll_list, "top", 2, self.clear_sel_btn)
        self.form.attachForm(self.scroll_list, "bottom", 2)

        pm.textScrollList(self.scroll_list, edit=True, append=("1", "2", "3"))

        pm.setParent("..")

        self.replace_ui(node_attr)

    def replace_ui(self, node_attr):
        """Reconfigure UI for the current node"""
        # node = pm.Attribute(node_attr).node()
        pm.setUITemplate("attributeEditorTemplate", pushTemplate=True)

        pm.textScrollList(self.scroll_list, edit=True, removeAll=True)
        paths = [asset_attr.get() for asset_attr in pm.Attribute(node_attr)]
        pm.textScrollList(self.scroll_list, edit=True, append=paths)

        pm.button(
            self.clear_all_btn,
            edit=True,
            command=pm.Callback(self.on_clear_all_btn, node_attr),
        )
        pm.button(
            self.clear_sel_btn,
            edit=True,
            command=pm.Callback(self.on_clear_sel_btn, node_attr),
        )
        pm.button(
            self.browse_file_btn,
            edit=True,
            command=pm.Callback(self.on_browse_btn, node_attr, 4),
        )
        pm.button(
            self.browse_dir_btn,
            edit=True,
            command=pm.Callback(self.on_browse_btn, node_attr, 3),
        )

        pm.setUITemplate(ppt=True)

    def on_clear_all_btn(self, node_attr):
        for asset_attr in pm.Attribute(node_attr):
            pm.removeMultiInstance(asset_attr, b=True)

    def on_clear_sel_btn(self, node_attr):
        attr = pm.Attribute(node_attr)
        sel_indices = [
            i - 1
            for i in pm.textScrollList(
                self.scroll_list, query=True, selectIndexedItem=True
            )
        ]
        logical_indices = pm.Attribute(node_attr).getArrayIndices()
        for i in sel_indices:
            pm.removeMultiInstance(attr[logical_indices[i]], b=True)

    def on_browse_btn(self, node_attr, mode):
        attr = pm.Attribute(node_attr)
        caption = "Choose Files" if mode == 4 else "Choose Folder"

        entries = pm.fileDialog2(
            caption=caption,
            okCaption="Choose",
            fileFilter="*",
            dialogStyle=2,
            fileMode=mode,
            dir=pm.workspace.getPath(),
        )
        if entries:
            logical_indices = attr.getArrayIndices()
            index = logical_indices[-1] + 1 if logical_indices else 0
            for entry in entries:
                attr[index].set(entry)
                index += 1
            return
        pm.displayWarning("No files Selected")
