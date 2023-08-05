"""
Handle the UI for 2 attributes:

1. hostSoftware (single value maya version)
2. pluginSoftware (multi value plugin name and version)

TODO: Try to move ALL the plugin/host compatibility logic out of this file. 
"""

import pymel.core as pm
from conductor.core import package_tree
from conductor.maya.lib import software as sw
from conductor.maya.lib import const as k
from . import AEcommon


class AEsoftware(object):
    def __init__(self, aet):
        aet.callCustom(self.new_ui, self.replace_ui, "hostSoftware")

        self.tree_data = None
        self.maya_menu = None
        self.add_btn = None
        self.plugin_col = None

    def has_data(self):
        return self.tree_data is not None

    def new_ui(self, node_attr):
        """Build static UI

        UI consists of a menu to set the Maya version (host), and a list of menu
        pairs to set plugin versions.
        """

        node = pm.Attribute(node_attr).node()
        pm.rowLayout(
            numberOfColumns=3,
            adjustableColumn=3,
            columnWidth3=(k.AE_TEXT_WIDTH, 200, 80),
            columnAttach=((1, "both", 0), (2, "both", 0), (3, "both", 0)),
        )
        pm.text(label="Maya Version")
        self.maya_menu = pm.optionMenu(acc=True)
        self.add_btn = pm.button(
            label="Add Plugin",
            height=18,
            command=pm.Callback(self.on_add_plugin_btn, node),
        )

        self.populate_host_software_menu()
        pm.setParent("..")
        self.plugin_col = pm.columnLayout(adj=True)
        self.replace_ui(node_attr)

    def replace_ui(self, node_attr):
        """Reconfigure UI for the current node"""
        node = pm.Attribute(node_attr).node()
        pm.setUITemplate("attributeEditorTemplate", pushTemplate=True)
        pm.optionMenu(
            self.maya_menu,
            edit=True,
            changeCommand=pm.Callback(self.set_host_software_value, node),
        )

        # Configure the Add button
        pm.button(
            self.add_btn, edit=True, command=pm.Callback(self.on_add_plugin_btn, node)
        )

        if not self.tree_data:
            return

        # Set host and plugin menu items to reflect attribute values.
        self.sync_host_software_menu_item(node)
        self.sync_plugin_software_menus(node)
        pm.setUITemplate(ppt=True)

    def populate_host_software_menu(self):
        """Put all the maya versions in the host menu."""
        for item in pm.optionMenu(self.maya_menu, query=True, itemListLong=True):
            pm.deleteUI(item)
        if self.tree_data:
            pm.setParent(self.maya_menu, menu=True)
            for mi in self.get_host_versions():
                pm.menuItem(label=mi)

    def get_host_versions(self):
        """Pluck host paths from the available software tree."""
        pathlist = self.tree_data.to_path_list()
        return sorted([p for p in pathlist if "/" not in p])

    def sync_host_software_menu_item(self, node):
        """
        Make sure host menu item reflects the attribute value.

        If the attribute is invalid, set it to the last valid version.
        """
        attr = node.attr("hostSoftware")
        value = attr.get()
        items = pm.optionMenu(self.maya_menu, query=True, itemListLong=True)
        if not items:
            return
        labels = [pm.menuItem(item, query=True, label=True) for item in items]
        try:
            index = labels.index(value)
        except ValueError:
            index = len(items) - 1
            attr.set(labels[index])
            AEcommon.printSetAttrCmd(attr)
        pm.optionMenu(self.maya_menu, edit=True, sl=(index + 1))

    def set_host_software_value(self, node):
        """
        Respond to host menu change.
        """
        num_items = pm.optionMenu(self.maya_menu, query=True, numberOfItems=True)
        if not num_items:
            return
        selected_value = pm.optionMenu(self.maya_menu, query=True, value=True)

        attr = node.attr("hostSoftware")
        attr.set(selected_value)
        AEcommon.printSetAttrCmd(attr)

        self.sync_plugin_software_menus(node)

    def on_add_plugin_btn(self, node):
        """Add an element to the pluginSoftware multi.

        Adding a multi element triggers a rebuiild of the AE automatically,
        which calls the replace func. For this reason, all we do here is add the
        attr.
        """
        if not self.tree_data:
            pm.warning("You must connect to Conductor to add plugins.")
            return
        indices = node.attr("pluginSoftware").getArrayIndices()
        next_available = next(a for a, b in enumerate(indices + [-1]) if a != b)
        node.attr("pluginSoftware")[next_available].set("something")

    def sync_plugin_software_menus(self, node):
        """
        Make sure plugin menu items reflect the pluginSoftware attribute values.

        We simply delete all UI and rebuild from scratch.
        """
        for widget in (
            pm.columnLayout(self.plugin_col, query=True, childArray=True) or []
        ):
            pm.deleteUI(widget)

        indices = node.attr("pluginSoftware").getArrayIndices()
        if not indices:
            return

        plugins = self.get_supported_plugins(node)
        if not plugins:
            return

        pm.setParent(self.plugin_col)
        for index in indices:
            self.build_plugin_option_menus(node, index, plugins)

    def get_supported_plugins(self, node):
        """Make sorted list of plugins.

        Each entry is an object with a 'plugin' and a 'versions' key.

        Example:
        plugins = [
            {"plugin": "arnold", "versions": ["1","2","3"]},
            {"plugin": "vray", "versions": ["1","2","3"]},
        ]
        """
        host = node.attr("hostSoftware").get()
        try:
            plugin_versions = self.tree_data.to_path_list(name=host)
        except TypeError:
            return

        if not plugin_versions:
            return

        plugin_dict = {}
        for plugin, version in [pv.split(" ") for pv in plugin_versions]:
            if plugin not in plugin_dict:
                plugin_dict[plugin] = []
            plugin_dict[plugin].append(version)

        plugins = []
        for key in plugin_dict:
            plugins.append({"plugin": key, "versions": sorted(plugin_dict[key])})

        return sorted(plugins, key=lambda k: k["plugin"])

    def build_plugin_option_menus(self, node, index, plugins):
        """
        Build 2 menus (plugin, version) for the one plugin at index.

        The plugin at node.attr("pluginSoftware")[index] is something like:
        "vray 1.2.3" so we check that it is supported by the current maya
        version, and if not we reset the attr to one that is. Then we build the
        two menus.
        1. plugin menu contains all plugin names supported by current maya
           version.
        2. version menu contains versions of the currently selected plugin.
        """
        valid_plugin = ensure_valid_selected_plugin(node, index, plugins)
        if not valid_plugin:
            return

        plugin, version = valid_plugin
        pm.setParent(self.plugin_col)
        pm.rowLayout(
            width=290,
            numberOfColumns=4,
            adjustableColumn=3,
            columnWidth4=(k.AE_TEXT_WIDTH, 200, 90, 30),
            columnAttach=(
                (1, "right", 0),
                (2, "both", 0),
                (3, "both", 0),
                (4, "both", 0),
            ),
        )
        pm.text(label="Plugin Version")
        plugin_menu = pm.optionMenu(acc=True)
        version_menu = pm.optionMenu(acc=True)
        remove_btn = pm.symbolButton(image="smallTrash.xpm", ann="Remove plugin")

        pm.optionMenu(
            plugin_menu,
            edit=True,
            changeCommand=pm.Callback(
                self.plugin_menu_change, node, index, plugins, plugin_menu, version_menu
            ),
        )
        pm.optionMenu(
            version_menu,
            edit=True,
            changeCommand=pm.Callback(
                self.version_menu_change, node, index, plugin_menu, version_menu
            ),
        )
        pm.symbolButton(
            remove_btn,
            edit=True,
            command=pm.Callback(self.on_remove_plugin, node, index),
        )
        pm.setParent("..")

        pm.setParent(plugin_menu, menu=True)
        for p in plugins:
            pm.menuItem(label=p["plugin"])

        sel_plugin_index = get_supported_plugin_index(plugin, plugins) + 1
        versions = get_versions_for_supported_plugin(plugin, plugins)

        pm.optionMenu(plugin_menu, edit=True, sl=sel_plugin_index)

        pm.setParent(version_menu, menu=True)
        for v in versions:
            pm.menuItem(label=v)

        sel_version_index = get_version_index(version, versions) + 1
        pm.optionMenu(version_menu, edit=True, sl=sel_version_index)

    def plugin_menu_change(self, node, index, plugins, plugin_menu, version_menu):
        """Callback when plugin menu item is selected.

        We rebuild the versions menu for this plugin, and select the last
        element.
        """
        plugin = pm.optionMenu(plugin_menu, query=True, value=True)
        versions = get_versions_for_supported_plugin(plugin, plugins)

        pm.setParent(version_menu, menu=True)
        for ui in pm.optionMenu(version_menu, query=True, itemListLong=True):
            pm.deleteUI(ui)
        for v in versions:
            pm.menuItem(label=v)
        pm.optionMenu(version_menu, edit=True, sl=len(versions))

        attr = node.attr("pluginSoftware")[index]
        attr.set("{} {}".format(plugin, versions[-1]))
        AEcommon.printSetAttrCmd(attr)

    def version_menu_change(self, node, index, plugin_menu, version_menu):
        """Callback when version menu item is selected.

        Set the attribute to the string combination of 'plugin version'
        """
        plugin = pm.optionMenu(plugin_menu, query=True, value=True)
        version = pm.optionMenu(version_menu, query=True, value=True)
        attr = node.attr("pluginSoftware")[index]
        attr.set("{} {}".format(plugin, version))
        AEcommon.printSetAttrCmd(attr)

    def on_remove_plugin(self, node, index):
        """Remove attr multi element.

        Redraw is triggered automatically.
        """
        pm.removeMultiInstance(node.attr("pluginSoftware")[index], b=True)

    def refresh_data(self, node_attr):
        """Fetch a fresh list of software from Conductor."""
        self.tree_data = sw.data(force=True)
        if self.maya_menu:
            self.populate_host_software_menu()
            self.replace_ui(node_attr)


def get_versions_for_supported_plugin(plugin, plugins):
    return next((x["versions"] for x in plugins if x["plugin"] == plugin), None)


def get_supported_plugin_index(plugin, plugins):
    return next((i for i, x in enumerate(plugins) if x["plugin"] == plugin), None)


def get_version_index(version, versions):
    return next((i for i, x in enumerate(versions) if x == version), None)


def ensure_valid_selected_plugin(node, index, plugins):
    if not plugins:
        return
    attr = node.attr("pluginSoftware")[index]
    sel = attr.get()
    try:
        sel_plugin, sel_version = sel.split(" ")
        found_plugin = next((x for x in plugins if x["plugin"] == sel_plugin), None)
        if found_plugin:
            found_version = next(
                (x for x in found_plugin["versions"] if x == sel_version), None
            )
            if not found_version:
                sel_version = found_plugin["versions"][-1]
        else:
            sel_plugin = plugins[0]["plugin"]
            sel_version = plugins[0]["versions"][-1]
    except (ValueError, AttributeError):
        sel_plugin = plugins[0]["plugin"]
        sel_version = plugins[0]["versions"][-1]

    attr.set("{} {}".format(sel_plugin, sel_version))
    AEcommon.printSetAttrCmd(attr)

    return (sel_plugin, sel_version)
