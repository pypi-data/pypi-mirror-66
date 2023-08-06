"""
Handle the UI for emails:
"""

import pymel.core as pm
from conductor.maya.lib import const as k


class AEemails(object):
    def __init__(self, aet):
        self.add_btn = None
        self.col = None
        aet.callCustom(self.new_ui, self.replace_ui, "emailAddresses")

    def new_ui(self, node_attr):
        """Build static UI"""
        node = pm.Attribute(node_attr).node()
        pm.rowLayout(
            numberOfColumns=2,
            columnWidth2=(k.AE_TEXT_WIDTH, 210),
            columnAttach=((1, "right", 0), (2, "both", 0)),
        )

        pm.text(label="")
        self.add_btn = pm.button(
            label="Add Email Address", height=24, command=pm.Callback(on_add_btn, node)
        )
        pm.setParent("..")
        pm.separator()

        self.col = pm.columnLayout(adj=True)
        self.replace_ui(node_attr)

    def replace_ui(self, node_attr):
        """Reconfigure UI for the current node"""
        node = pm.Attribute(node_attr).node()
        pm.setUITemplate("attributeEditorTemplate", pushTemplate=True)
        pm.button(self.add_btn, edit=True, command=pm.Callback(on_add_btn, node))

        for widget in pm.columnLayout(self.col, query=True, childArray=True) or []:
            pm.deleteUI(widget)

        pm.setParent(self.col)
        for i, attr in enumerate(pm.Attribute(node_attr)):
            pm.rowLayout(
                numberOfColumns=4,
                adjustableColumn=2,
                columnWidth4=(k.AE_TEXT_WIDTH, 150, 36, 24),
                columnAttach=(
                    (1, "both", 0),
                    (2, "both", 0),
                    (3, "both", 0),
                    (4, "both", 0),
                ),
            )

            address_att = attr.attr("emailAddress")
            active_att = attr.attr("emailAddressActive")

            active = active_att.get()
            address = address_att.get()

            pm.text(label="Email: {:d}".format(i + 1))

            address_tf = pm.textField(
                text=address, enable=active, placeholderText="Email Address"
            )
            active_cb = pm.checkBox(value=active, label="")

            pm.symbolButton(
                image="smallTrash.xpm", command=pm.Callback(on_remove_email, attr)
            )

            pm.textField(
                address_tf,
                edit=True,
                changeCommand=pm.Callback(on_text_changed, address_tf, address_att),
            )

            pm.checkBox(
                active_cb,
                edit=True,
                changeCommand=pm.Callback(
                    on_active_cb_changed, active_cb, address_tf, active_att
                ),
            )

            pm.setParent(self.col)

        pm.setUITemplate(ppt=True)


def on_add_btn(node):
    indices = node.attr("emailAddresses").getArrayIndices()
    next_available = next(a for a, b in enumerate(indices + [-1]) if a != b)
    node.attr("emailAddresses")[next_available].attr("emailAddress").set("")


def on_text_changed(text_field, attr):
    val = pm.textField(text_field, query=True, text=True)
    attr.set(val)


def on_active_cb_changed(checkbox, text_field, attr):
    active = pm.checkBox(checkbox, query=True, value=True)
    pm.textField(text_field, edit=True, enable=active)
    attr.set(active)


def on_remove_email(attr):
    pm.removeMultiInstance(attr, b=True)
