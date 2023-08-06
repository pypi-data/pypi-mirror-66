"""
Handle the UI for projects:

"""
 
import pymel.core as pm
 
import json

class AEoutput(object):
    def __init__(self, aet):

        self.field = None
        self.attributeWatcher = None
        aet.callCustom(self.new_ui, self.replace_ui, "output")

    def new_ui(self, node_attr):
        """Build static UI"""

        self.field = pm.scrollField(height=250, editable=False, wordWrap=False)
        self.replace_ui(node_attr)

    def replace_ui(self, node_attr):
        """Reconfigure UI for the current node"""
 
        pm.setUITemplate("attributeEditorTemplate", pushTemplate=True)
        attr =  pm.Attribute(node_attr)
        val = json.dumps(json.loads(attr.get()), sort_keys=True, indent=4)
        pm.scrollField(self.field, edit=True, text=val)

        pm.scriptJob(attributeChange=(attr, pm.Callback(self.on_output_change, attr)), parent=self.field , replacePrevious=True)

        pm.setUITemplate(ppt=True)
 
    def on_output_change(self, attr):
        """
        Respond to menu change.
        """
        val = json.dumps(json.loads(attr.get()), sort_keys=True, indent=4)
        pm.scrollField(self.field, edit=True, text=val)
 