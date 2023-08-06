"""
Handle the UI for projuse custom frames and use scout frames:

"""

import pymel.core as pm

constants = {
    "useCustomRange": {
        "text_label": "Custom Range",
        "annotation": "Specifies a set of frames to render. Provide a comma-separated list of progressions. Example 1,7,10-20,30-60x3,1001.",
        "value_attr": "customRange",
    },
    "useScoutFrames": {
        "text_label": "Scout Frames",
        "annotation": "Specifies a set of frames to test render on Conductor before other frames. Provide a comma-separated list of progressions. Example 1,7,10-20,30-60x3,1001.",
        "value_attr": "scoutFrames",
    },
}


def _on_bool_change(attr, widget):
    pm.frameLayout(widget, edit=True, visible=attr.get())


def _on_text_changed(attr, widget):
    attr.set(pm.textFieldGrp(widget, query=True, text=True))


class AEframes(object):
    def __init__(self, aet):
        self.widgets = {
            "useCustomRange": {"checkbox": None, "textfield": None, "frame": None},
            "useScoutFrames": {"checkbox": None, "textfield": None, "frame": None},
        }
        self.current_node = None
        aet.callCustom(self.new_ui, self.replace_ui, "useCustomRange")
        aet.addSeparator()
        aet.callCustom(self.new_ui, self.replace_ui, "useScoutFrames")

    def new_ui(self, node_attr):
        """Build static UI"""
        key = node_attr.split(".")[1]
        ann = constants[key]["annotation"]
        label = constants[key]["text_label"]

        self.widgets[key]["checkbox"] = pm.attrControlGrp(attribute=node_attr)
        self.widgets[key]["frame"] = pm.frameLayout(
            visible=False, lv=False, cl=False, cll=False
        )

        self.widgets[key]["textfield"] = pm.textFieldGrp(label=label, ann=ann)

        pm.setParent("..")
        self.replace_ui(node_attr)

    def replace_ui(self, node_attr):
        """Reconfigure UI for the current node-attr"""
        self.current_node = pm.Attribute(node_attr).node()

        key = node_attr.split(".")[1]
        bool_attr = pm.Attribute(node_attr)

        pm.setUITemplate("attributeEditorTemplate", pushTemplate=True)
        value_attr = self.current_node.attr(constants[key]["value_attr"])
        value_widget = self.widgets[key]["textfield"]
        frame = self.widgets[key]["frame"]

        pm.attrControlGrp(
            self.widgets[key]["checkbox"],
            edit=True,
            attribute=node_attr,
            changeCommand=pm.Callback(_on_bool_change, bool_attr, frame),
        )

        pm.textFieldGrp(
            value_widget,
            edit=True,
            text=value_attr.get(),
            changeCommand=pm.Callback(_on_text_changed, value_attr, value_widget),
        )

        _on_bool_change(bool_attr, frame)

        pm.setUITemplate(ppt=True)
