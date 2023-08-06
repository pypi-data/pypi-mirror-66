"""
Handle the UI for environment:
"""

import pymel.core as pm
from conductor.maya.lib import const as k


class AEenvironment(object):
    def __init__(self, aet):
        self.add_btn = None
        self.col = None
        aet.callCustom(self.new_ui, self.replace_ui, "extraEnvironment")

    def new_ui(self, node_attr):
        """Build static UI"""
        node = pm.Attribute(node_attr).node()
        pm.rowLayout(
            width=290,
            numberOfColumns=2,
            columnWidth2=(k.AE_TEXT_WIDTH, 210),
            columnAttach=((1, "right", 0), (2, "both", 0)),
        )

        pm.text(label="")
        self.add_btn = pm.button(
            label="Add Environment Variable",
            height=24,
            command=pm.Callback(on_add_btn, node),
        )
        pm.setParent("..")
        pm.separator()
        pm.rowLayout(
            width=290,
            numberOfColumns=4,
            adjustableColumn=2,
            columnWidth4=(k.AE_TEXT_WIDTH, 150, 36, 24),
            columnAttach=(
                (1, "both", 6),
                (2, "both", 6),
                (3, "both", 6),
                (4, "both", 0),
            ),
        )
        pm.text(label="Key", align="left")
        pm.text(label="Value", align="left")
        pm.text(label="Excl", align="left")
        pm.text(label="")
        pm.setParent("..")

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
        for attr in pm.Attribute(node_attr):
            pm.rowLayout(
                width=290,
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

            key_att = attr.attr("extraEnvironmentKey")
            val_att = attr.attr("extraEnvironmentValue")
            exc_att = attr.attr("extraEnvironmentExclusive")

            key_tf = pm.textField(text=key_att.get(), placeholderText="VAR_NAME")
            val_tf = pm.textField(text=val_att.get(), placeholderText="Value")
            exc_cb = pm.checkBox(value=exc_att.get(), label="")
            pm.symbolButton(
                image="smallTrash.xpm", command=pm.Callback(on_remove_var, attr)
            )

            pm.textField(
                key_tf,
                edit=True,
                changeCommand=pm.Callback(on_text_changed, key_tf, key_att),
            )
            pm.textField(
                val_tf,
                edit=True,
                changeCommand=pm.Callback(on_text_changed, val_tf, val_att),
            )
            pm.checkBox(
                exc_cb,
                edit=True,
                changeCommand=pm.Callback(on_excl_cb_changed, exc_cb, exc_att),
            )

            pm.setParent(self.col)

        pm.setUITemplate(ppt=True)


def on_add_btn(node):
    indices = node.attr("extraEnvironment").getArrayIndices()
    next_available = next(a for a, b in enumerate(indices + [-1]) if a != b)
    node.attr("extraEnvironment")[next_available].attr("extraEnvironmentKey").set("")
    node.attr("extraEnvironment")[next_available].attr("extraEnvironmentValue").set("")


def on_text_changed(text_field, attribute):
    val = pm.textField(text_field, query=True, text=True)
    attribute.set(val)


def on_excl_cb_changed(checkbox, attribute):
    val = pm.checkBox(checkbox, query=True, value=True)
    attribute.set(val)


def on_remove_var(attribute):
    pm.removeMultiInstance(attribute, b=True)
