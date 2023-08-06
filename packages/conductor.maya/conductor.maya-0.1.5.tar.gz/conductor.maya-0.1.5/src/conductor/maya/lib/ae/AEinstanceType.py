"""
Handle the UI for instanceTypes:

"""

import maya.app.renderSetup.model.renderSetup as rs
import maya.app.renderSetup.views.overrideUtils as ov_utils
import pymel.core as pm

from conductor.maya.lib import instance_types as ity
from conductor.maya.lib import const as k
from conductor.maya.lib.ae import AEcommon


class AEinstanceType(object):
    def __init__(self, aet):
        self.instance_type_data = None
        self.menu = None
        self.popup = None
        self.label = None
        self.row = None
        self.current_node = None
        aet.callCustom(self.new_ui, self.replace_ui, "instanceTypeName")

    def has_data(self):
        return self.instance_type_data is not None

    def new_ui(self, node_attr):
        """Build static UI"""
        self.row = pm.rowLayout(
            numberOfColumns=2,
            columnWidth2=(k.AE_TEXT_WIDTH, 200),
            columnAttach=((1, "right", 0), (2, "both", 0)),
        )

        self.label = pm.text(label="Instance Type Name")
        self.menu = pm.optionMenu(
            acc=True, changeCommand=pm.Callback(self.set_instance_type_value)
        )

        self.create_popup_menu()
        self.populate_menu()
        pm.setParent("..")

        pm.scriptJob(
            event=(
                "renderLayerManagerChange",
                pm.Callback(self.on_render_layer_change),
            ),
            parent=self.menu,
        )

        self.replace_ui(node_attr)

    def replace_ui(self, node_attr):
        """Reconfigure UI for the current node"""

        self.current_node = pm.Attribute(node_attr).node()
        pm.setUITemplate("attributeEditorTemplate", pushTemplate=True)

        pm.rowLayout(self.row, edit=True, enable=bool(self.instance_type_data))
        if not self.instance_type_data:
            if not ity.valid():
                pm.setParent(self.menu, menu=True)
                pm.menuItem(label="Not connected")
                return
            self.refresh_data(False)

        self.sync_instance_type_menu_item()
        # Configure the popup menuItem
        self.configure_popup_menu()

        self.set_label_color()

        pm.setUITemplate(ppt=True)

    def populate_menu(self):
        for item in pm.optionMenu(self.menu, query=True, itemListLong=True):
            pm.deleteUI(item)
        if self.instance_type_data:
            pm.setParent(self.menu, menu=True)
            for mi in self.instance_type_data:
                pm.menuItem(label=mi["description"])

    def sync_instance_type_menu_item(self):
        """
        Set selected menu item to reflect the attribute value.

        If the attribute is invalid, set it to the first valid instance type.
        """
        if not self.instance_type_data:
            return
        attr = self.current_node.attr("instanceTypeName")
        name = attr.get()
        index_el = self.get_index_and_element_from_name(name)
        if not index_el:
            index, el = (0, self.instance_type_data[0])
            attr.set(el["name"])
        else:
            index, _ = index_el
        pm.optionMenu(self.menu, edit=True, sl=(index + 1))

    def get_index_and_element_from_name(self, name):
        return next(
            (
                (i, x)
                for i, x in enumerate(self.instance_type_data)
                if x["name"] == name
            ),
            None,
        )

    def set_instance_type_value(self):
        """
        Respond to menu change.
        """
        num_items = pm.optionMenu(self.menu, query=True, numberOfItems=True)
        if not num_items:
            return
        index = pm.optionMenu(self.menu, query=True, sl=True) - 1
        attr = self.current_node.attr("instanceTypeName")
        attr.set(self.instance_type_data[index]["name"])
        AEcommon.printSetAttrCmd(attr)

    def create_popup_menu(self):
        self.popup = pm.popupMenu(parent=self.label)
        pm.menuItem(
            label="Refresh Instance Types", command=pm.Callback(self.refresh_data)
        )
        pm.menuItem(
            label="Create Absolute Override for Visible Layer",
            command=pm.Callback(self.on_create_layer_override),
        )

    def configure_popup_menu(self):
        items = pm.popupMenu(self.popup, query=True, itemArray=True)
        enable_override = (
            pm.editRenderLayerGlobals(query=True, currentRenderLayer=True)
            != "defaultRenderLayer"
        )
        pm.menuItem(items[1], edit=True, en=enable_override)

    def on_create_layer_override(self):
        # node = pm.Attribute(node_attr).node()
        ov_utils.createAbsoluteOverride(str(self.current_node), "instanceTypeName")
        self.set_label_color()

    def set_label_color(self):
        """By convention, label is orange if attr has an override."""
        has_override = rs.hasOverrideApplied(str(self.current_node), "instanceTypeName")
        text = "Instance Type Name"
        label = "<font color=#ec6a17>{}</font>".format(text) if has_override else text
        pm.text(self.label, edit=True, label=label)

    def refresh_data(self, force=True):
        """Fetch a fresh list of instance types from Conductor."""
        self.instance_type_data = ity.data(force=force)
        if self.menu:
            self.populate_menu()
            self.replace_ui(str(self.current_node.attr("instanceTypeName")))

    def on_render_layer_change(self):
        if self.current_node:
            self.replace_ui(str(self.current_node.attr("instanceTypeName")))
