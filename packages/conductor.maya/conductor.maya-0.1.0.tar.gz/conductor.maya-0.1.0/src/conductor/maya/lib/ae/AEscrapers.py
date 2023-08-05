"""
Handle the UI for extra assets:
"""

import ast
import imp
import os

import pymel.core as pm
from conductor.maya.lib  import const as k


def get_module_docstring(filepath):
    """
    Get module docstring.

    Optimizations:
    If not python file, no docstring.
    If first (non false) line is not three quotes, no docstring.
    If docstring has no content, no docstring.
    """
    result = "No doctring"
    if os.path.splitext(filepath)[1] != ".py":
        return result

    try:
        with open(filepath) as f:
            for line in f.readlines():
                stripped_line = line.strip()
                if stripped_line:
                    if not (stripped_line.startswith('"""') or stripped_line.startswith("'''")):
                        return result
                    break

        with open(filepath) as f:
            file_contents = f.read()

        module = ast.parse(file_contents)
        ds = ast.get_docstring(module)
        if ds:
            result = ds.strip()
    except BaseException:
        pass
    return result


class AEscrapers(object):
    def __init__(self, aet):
        self.test_btn = None

        aet.callCustom(self.new_ui, self.replace_ui, "assetScrapers")

    def new_ui(self, node_attr):
        """Build static UI"""

        node = pm.Attribute(node_attr).node()
        pm.rowLayout(numberOfColumns=3,
                     # adjustableColumn=2,
                     columnWidth3=(k.AE_TEXT_WIDTH, 210, 100),
                     columnAttach=((1, 'right', 0),
                                   (2, 'both', 0),
                                   (2, 'both', 0))
                     )

        pm.text(label="")
        self.add_btn = pm.button(
            label="Add Scraper", height=24
        )
        pm.text(label="")

        pm.setParent("..")
        pm.separator()

        self.col = pm.columnLayout(adj=True)
        pm.setParent("..")
        pm.separator()
        pm.rowLayout(width=290,
                     numberOfColumns=3,
                     adjustableColumn=1,
                     columnWidth3=(k.AE_TEXT_WIDTH, 25, 25),
                     columnAttach=((1, 'both', 0),
                                   (2, 'both', 0),
                                   (3, 'both', 0)
                                   )
                     )
        pm.text(label="")
        self.test_btn = pm.symbolButton(
            image="SP_FileIcon.png", ann="Test active scrapers", width=24, height=24)
        pm.text(label="")
        pm.setParent("..")

        self.replace_ui(node_attr)

    def replace_ui(self, node_attr):
        """Reconfigure UI for the current node"""
        # node = pm.Attribute(node_attr).node()
        attr = pm.Attribute(node_attr)
        pm.setUITemplate("attributeEditorTemplate", pushTemplate=True)
        pm.button(self.add_btn, edit=True,
                  command=pm.Callback(on_add_btn, attr)
                  )

        for widget in pm.columnLayout(self.col, query=True, childArray=True) or []:
            pm.deleteUI(widget)

        pm.setParent(self.col)
        for i, attr_el in enumerate(attr):
            pm.rowLayout(
                numberOfColumns=5,
                adjustableColumn=2,
                columnWidth5=(25, k.AE_TEXT_WIDTH, 25, 25, 25),
                columnAttach=((1, 'both', 0),
                              (2, 'both', 0),
                              (3, 'both', 0),
                              (4, 'both', 0),
                              (5, 'both', 0)
                              )
            )

            path_att = attr_el.attr("assetScraperPath")
            active_att = attr_el.attr("assetScraperActive")

            path = path_att.get()

            active = active_att.get()

            active_cb = pm.checkBox(value=active, label="")
            path_tf = pm.textField(text=path, enable=active,
                                   placeholderText="Path to scraper")

            set_docstring(path_tf)

            pm.symbolButton(image="SP_DirClosedIcon.png", width=24, height=24,
                            command=pm.Callback(on_browse_button, attr_el, path_tf, active_cb))

            pm.symbolButton(image="SP_FileIcon.png", ann="Test this scraper", width=24, height=24,
                            command=pm.Callback(on_test_scraper, attr_el))

            pm.symbolButton(image="smallTrash.xpm", width=24, height=24,
                            command=pm.Callback(on_remove_scraper, attr_el))

            pm.checkBox(active_cb, edit=True, changeCommand=pm.Callback(
                on_active_cb_changed, active_cb, path_tf, active_att))

            pm.textField(path_tf, edit=True, changeCommand=pm.Callback(
                on_path_changed, path_tf, path_att))

            pm.setParent(self.col)
        pm.setParent("..")

        pm.symbolButton(self.test_btn, edit=True,  command=pm.Callback(
            on_test_scraper, attr))

        pm.setUITemplate(ppt=True)


def on_add_btn(attr):
    indices = attr.getArrayIndices()
    next_available = indices[-1] + 1 if indices else 0
    script = browse_for_script()
    if script:
        attr[next_available].attr("assetScraperPath").set(script)


def on_browse_button(attr_el, path_tf, active_cb):
    script = browse_for_script()
    if script:
        attr_el.attr("assetScraperPath").set(script)
        attr_el.attr("assetScraperActive").set(True)
        pm.textField(path_tf, edit=True, text=script,
                     enable=True)
        pm.checkBox(active_cb, edit=True, value=True)

        pm.evalDeferred(pm.Callback(set_docstring, path_tf))

        # docstring = get_module_docstring(script)


def browse_for_script():
    entries = pm.fileDialog2(
        caption="Choose Script",
        okCaption="Choose",
        fileFilter="*",
        dialogStyle=2,
        fileMode=1,
        dir=pm.workspace.getPath())
    if entries:
        return entries[0]
    pm.displayWarning('No files Selected')


def on_test_scraper(attr):
    if attr.isArray():
        script_paths = [attr_el.attr("assetScraperPath").get(
        ) for attr_el in attr if attr_el.attr("assetScraperActive").get()]
    else:
        script_paths = [attr.attr("assetScraperPath").get()]

    for p in run_scrapers(script_paths):
        print p 



def on_path_changed(text_field, attribute):
    path = pm.textField(text_field, query=True, text=True)
    attribute.set(path)
    pm.evalDeferred(pm.Callback(set_docstring, text_field))


def set_docstring(text_field):
    path = pm.textField(text_field, query=True, text=True)
    docstring = get_module_docstring(path)
    pm.textField(text_field, edit=True, ann=docstring)


def on_active_cb_changed(checkbox, text_field, attribute):
    active = pm.checkBox(checkbox, query=True, value=True)
    pm.textField(text_field, edit=True, enable=active)
    attribute.set(active)


def on_remove_scraper(attribute):
    pm.removeMultiInstance(attribute, b=True)


def run_scrapers(paths):

    result = []
    for path in paths:
        try:
            mod_name = "conductor.maya.{}".format(
                os.path.splitext(os.path.basename(path))[0])
            scraper_module = imp.load_source(mod_name, path)
        except IOError:
            pm.warning(
                "Can't load the script '{}' as a Python module.".format(path))
            raise
        except SyntaxError:
            pm.warning("Syntax error in the scraper script: '{}'.".format(path))
            raise
        result += scraper_module.run()
    return result
