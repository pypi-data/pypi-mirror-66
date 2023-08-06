"""
Entry point for the conductorRender Attribute Editor UI.

Generally, there's one attributeEditor instance for the conductorRender node type. When different nodes of that
type are selected, the same AE is shown and its contents replaced to reflect the current node.

AE templates build interfaces to each attribute in one of 2 ways: 
Simple: e.g. self.addControl("preemptible") 
Custom: e.g. self.callCustom(new_func, replace_func, "preemptible")

new_func builds the UI the first time the template is run. replace_func
reconfigures the template based on the current node. The purpose is efficiency -
so that the template doesn't need to rebuild everything everytime.

We call out to separate files (classes) to build each section if it uses a custom UI. 
e.g. AEsoftware() is a class containing a new_func and a replace_func to manage the software
section.

"""
from conductor.maya.lib.ae.AEdestination import AEdestination
from conductor.maya.lib.ae.AEemails import AEemails
from conductor.maya.lib.ae.AEenvironment import AEenvironment
from conductor.maya.lib.ae.AEextraAssets import AEextraAssets
from conductor.maya.lib.ae.AEframes import AEframes
from conductor.maya.lib.ae.AEinstanceType import AEinstanceType
from conductor.maya.lib.ae.AElayers import AElayers
from conductor.maya.lib.ae.AEmetadata import AEmetadata
from conductor.maya.lib.ae.AEoutput import AEoutput
from conductor.maya.lib.ae.AEproject import AEproject
from conductor.maya.lib.ae.AEscrapers import AEscrapers
from conductor.maya.lib.ae.AEsoftware import AEsoftware
from conductor.maya.lib.ae.AEtaskTemplate import AEtaskTemplate
from conductor.maya.lib import const as k
from conductor.maya.lib import submit
from conductor.maya.lib import projects, software, instance_types

import pymel.core as pm


class AEconductorRenderTemplate(pm.ui.AETemplate):
    def __init__(self, node_name):
        """Define the high level arrangement of AE sections"""
        pm.ui.AETemplate.__init__(self, node_name)

        self.reload_button = None
        self.connect_button = None
        self.submit_button = None
        self.dry_run_button = None

        self.beginScrollLayout()

        self.callCustom(self.new_button_row, self.replace_button_row, "title")

        self.beginLayout("General Attributes", collapse=False)
        self.addControl("title")
        self.ae_project = AEproject(self)
        self.ae_layers = AElayers(self)

        self.addSeparator()
        self.ae_instance_type = AEinstanceType(self)
        self.addControl("preemptible")
        self.addSeparator()
        self.ae_destination = AEdestination(self)
        self.endLayout()

        self.beginLayout("Software", collapse=False)
        self.ae_software = AEsoftware(self)
        self.endLayout()

        self.beginLayout("Frame range")
        self.addControl("chunkSize")
        self.ae_frames = AEframes(self)
        self.endLayout()

        self.beginLayout("Info", collapse=False)
        self.addControl("frameSpec", label="Frame Spec")
        self.addControl("frameCount")
        self.addControl("taskCount")
        self.addControl("scoutTaskCount")
        self.endLayout()

        self.beginLayout("Assets", collapse=False)
        self.addControl("useUploadDaemon", changeCommand=self.updateUseUploadDaemon)
        self.addControl("uploadOnly")
        self.beginLayout("Asset Scrapers")
        self.ae_scrapers = AEscrapers(self)
        self.endLayout()
        self.beginLayout("Extra Assets")
        self.ae_extra_assets = AEextraAssets(self)
        self.endLayout()
        self.endLayout()

        self.beginLayout("Notifications")
        self.ae_emails = AEemails(self)
        self.endLayout()

        self.beginLayout("Task Command")
        self.addControl("maxTasksPerJob")
        self.ae_task_template = AEtaskTemplate(self)
        self.endLayout()

        self.beginLayout("Metadata")
        self.ae_metadata = AEmetadata(self)
        self.endLayout()

        self.beginLayout("Extra Environment")
        self.ae_environment = AEenvironment(self)
        self.endLayout()

        self.beginLayout("Automatic Retries")
        self.addControl("retriesWhenPreempted")
        self.addControl("retriesWhenFailed")
        self.endLayout()

        self.beginLayout("Submission Preview")
        self.addControl("doScrape", label="Display Scraped Assets")
        self.addControl("taskLimit", label="Display Tasks")
        self.ae_output = AEoutput(self)
        self.endLayout()

        self.beginLayout("Autosave")
        self.addControl("autosave")
        self.addControl("autosaveTemplate")
        self.addControl("cleanupAutosave")
        self.endLayout()

        self.beginLayout("Diagnostics")
        self.addControl("dryRun")
        self.endLayout()

        self.addExtraControls()

        for att in k.SUPPRESS_EXTRA_ATTS:
            self.suppress(att)

        self.endScrollLayout()

    def updateUseUploadDaemon(self, nodeName):
        useDaemon = pm.PyNode(nodeName).attr("useUploadDaemon").get()
        self.dimControl(nodeName, "cleanupAutosave", useDaemon)

    def new_button_row(self, node_attr):
        """Build row for action buttons."""
        but_width = k.AE_TOTAL_WIDTH / 3
        pm.setUITemplate("attributeEditorTemplate", pushTemplate=True)
        pm.rowLayout(numberOfColumns=3, cw3=(but_width, but_width, but_width))

        self.connect_button = pm.button(
            label="Connect to Conductor",
            ann="Connect to Conductor and update instance types, projects, and packages",
            w=but_width,
        )

        self.submit_button = pm.button(
            label="Submit", ann="Submit Job", w=but_width, en=False
        )
        self.dry_run_button = pm.button(
            label="Show Scripts",
            ann="This is effectively a dry run",
            w=but_width,
            en=False,
        )

        pm.setParent("..")
        self.replace_button_row(node_attr)
        pm.setUITemplate(ppt=True)

    def replace_button_row(self, node_attr):
        """Reconfigure action buttons when node changes."""
        node = pm.Attribute(node_attr).node()
        pm.setUITemplate("attributeEditorTemplate", pushTemplate=True)
        pm.button(
            self.connect_button, edit=True, command=pm.Callback(self.on_connect, node)
        )
        pm.button(self.submit_button, edit=True, command=pm.Callback(on_submit, node))
        pm.button(self.dry_run_button, edit=True, command=pm.Callback(on_dry_run, node))

        self.set_button_enabled_state()

        pm.setUITemplate(ppt=True)

    def on_connect(self, node):
        self.ae_project.refresh_data()
        self.ae_software.refresh_data()
        self.ae_instance_type.refresh_data()
        self.set_button_enabled_state()

    def set_button_enabled_state(self):
        can_submit = projects.valid() and software.valid() and instance_types.valid()
        pm.button(self.submit_button, edit=True, en=can_submit)
        pm.button(self.dry_run_button, edit=True, en=can_submit)


def on_submit(node):
    submit.submit(node)


def on_dry_run(node):
    submit.submit(node, dry_run=True)
