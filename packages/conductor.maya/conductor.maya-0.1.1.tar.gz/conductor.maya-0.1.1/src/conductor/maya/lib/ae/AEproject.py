"""
Handle the UI for projects:

"""

import pymel.core as pm
from conductor.maya.lib import projects as prj
from conductor.maya.lib import const as k
from . import AEcommon


class AEproject(object):
    def __init__(self, aet):

        self.project_data = None
        self.menu = None
        self.row = None
        self.label = None
        self.popup = None
        aet.callCustom(self.new_ui, self.replace_ui, "projectName")

    def has_data(self):
        return self.project_data is not None

    def new_ui(self, node_attr):
        """Build static UI"""
        self.row = pm.rowLayout(
            numberOfColumns=2,
            columnWidth2=(k.AE_TEXT_WIDTH, 200),
            columnAttach=((1, "right", 0), (2, "both", 0)),
        )

        self.label = pm.text(label="Project name")
        self.menu = pm.optionMenu(acc=True)

        self.create_popup_menu()

        self.populate_menu()
        pm.setParent("..")

        self.replace_ui(node_attr)

    def replace_ui(self, node_attr):
        """Reconfigure UI for the current node"""
        node = pm.Attribute(node_attr).node()
        pm.setUITemplate("attributeEditorTemplate", pushTemplate=True)
        pm.optionMenu(
            self.menu,
            edit=True,
            changeCommand=pm.Callback(self.set_project_value, node),
        )

        pm.rowLayout(self.row, edit=True, enable=bool(self.project_data))
        if not self.project_data:
            pm.setParent(self.menu, menu=True)
            pm.menuItem(label="Not connected")
            return

        self.sync_project_menu_item(node)

        self.configure_popup_menu(node_attr)

        pm.setUITemplate(ppt=True)

    def populate_menu(self):
        for item in pm.optionMenu(self.menu, query=True, itemListLong=True):
            pm.deleteUI(item)
        if self.project_data:
            pm.setParent(self.menu, menu=True)
            for mi in self.project_data:
                pm.menuItem(label=mi)

    def sync_project_menu_item(self, node):
        """
        Make sure menu item reflects the attribute value.

        If the attribute is invalid, set it to the first valid project.
        """
        value = node.attr("projectName").get()
        items = pm.optionMenu(self.menu, query=True, itemListLong=True)
        if not items:
            return
        labels = [pm.menuItem(item, query=True, label=True) for item in items]
        try:
            index = labels.index(value)
        except ValueError:
            index = 0
            node.attr("projectName").set(labels[index])
        pm.optionMenu(self.menu, edit=True, sl=(index + 1))

    def set_project_value(self, node):
        """
        Respond to menu change.
        """
        num_items = pm.optionMenu(self.menu, query=True, numberOfItems=True)
        if not num_items:
            return
        selected_value = pm.optionMenu(self.menu, query=True, value=True)
        attr = node.attr("projectName")
        attr.set(selected_value)
        AEcommon.printSetAttrCmd(attr)

    def create_popup_menu(self):
        self.popup = pm.popupMenu(parent=self.label)
        pm.menuItem(label="Refresh Projects")

    def configure_popup_menu(self, node_attr):
        items = pm.popupMenu(self.popup, query=True, itemArray=True)
        pm.menuItem(
            items[0], edit=True, command=pm.Callback(self.refresh_data, node_attr)
        )

    def refresh_data(self, node_attr):
        """Fetch a fresh list of projects from Conductor."""
        self.project_data = prj.data(force=True)
        if self.menu:
            self.populate_menu()
            self.replace_ui(node_attr)
