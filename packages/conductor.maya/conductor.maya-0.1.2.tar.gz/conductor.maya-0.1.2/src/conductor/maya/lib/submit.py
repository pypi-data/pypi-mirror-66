"""
Submit.

"""
import json
import os
import sys
import traceback
from contextlib import contextmanager

import pymel.core as pm
from conductor.core import conductor_submit
from conductor.core.expander import Expander
from conductor.maya.lib import const as k
from conductor.maya.lib import layer_utils, window


@contextmanager
def full_output(node):
    task_limit = node.attr("taskLimit").get()
    do_scrape = node.attr("doScrape").get()
    node.attr("taskLimit").set(-1)
    node.attr("doScrape").set(True)
    yield
    node.attr("taskLimit").set(task_limit)
    node.attr("doScrape").set(do_scrape)


@contextmanager
def transient_save(filepath, cleanup=True):
    original = pm.sceneName()
    pm.saveAs(filepath)
    yield
    pm.renameFile(original)
    if cleanup:
        try:
            os.remove(filepath) 
        except OSError:
            pm.displayWarning("Couldn't cleanup file: {}".format(filepath))
 

def submit(node, dry_run=False):
    validate(node)

    if node.attr("autosave").get():
        cleanup = node.attr("cleanupAutosave").get() and not node.attr("useUploadDaemon").get()
        filepath = _resolve_autosave_template(node)
        with transient_save(filepath, cleanup=cleanup):
            handle_submissions(node,dry_run )
        return

    filepath = pm.sceneName()
    if pm.isModified():
        filepath = browse_save_as()
        if not filepath:
            pm.warning('No file Selected')
            return
        pm.saveAs(filepath)
 
    handle_submissions(node,dry_run)

    
def handle_submissions(node, dry_run):
    submissions = get_submissions(node)
    if  dry_run:
        window.show_as_json( submissions, title="Dry run submissions", sort_keys=True, indent=2)
    else:
        responses = do_submissions(submissions)
        window.show_submission_responses(responses)


def get_submissions(node):

    submissions = []
    layer_policy = node.attr("renderLayers").get()

    if layer_policy == k.CURRENT_LAYER:
        submissions.append(get_submission(node))
    else:
        for layer in layer_utils.get_renderable_legacy_layers():
            with layer_utils.layer_context(layer):
                submissions.append(get_submission(node))
    return list(filter(None, submissions))


def do_submissions(submissions):
    results = []
    for submission in submissions:
        try:
            remote_job = conductor_submit.Submit(submission)
            response, response_code = remote_job.main()
            results.append({"code": response_code, "response": response})
        except BaseException:
            results.append(
                {
                    "code": "undefined",
                    "response": "".join(
                        traceback.format_exception(*sys.exc_info())
                    ),
                }
            )
    return results

def _resolve_autosave_template(node):
 
    scene_path = pm.sceneName()
    scene_name = os.path.splitext(os.path.split(scene_path)[1])[0]
    context = {
        "Scene": scene_name,
        "scene": scene_name
    }
    expander = Expander(**context)
    resolved_name = expander.evaluate(node.attr("autosaveTemplate").get())
    return os.path.join(os.path.dirname(scene_path), "{}.ma".format(resolved_name))


def browse_save_as():
    filters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"

    entries = pm.fileDialog2(
        caption="Save File As",
        okCaption="Save As",
        fileFilter=filters,
        dialogStyle=2,
        fileMode=0,
        dir=os.path.dirname(pm.sceneName()))

    if entries:
        return entries[0]


def get_submission(node):
    out_attr = pm.PyNode(node).attr("output")
    with full_output(node):
        pm.dgdirty(out_attr)
        result = out_attr.get()
        if result:
            return json.loads(result)


def validate(node):
    result = {}
    _extend_validation(result, validate_cameras())
    _extend_validation(result, validate_something())

    if "errors" in result:
        for entry in result["errors"]:
            print entry
        pm.error("Errors prevented your submission. See above.")
    if "warnings" in result:
        if not window.show_warnings(result["warnings"]) == "okay":
            pm.error("Submission cancelled by user.")


def _extend_validation(validation, more):
    if more:
        for key in more:
            if not key in validation:
                validation[key] = []
            validation[key] += more[key]


def validate_cameras():
    if any(cam.attr("renderable").get() for cam in pm.ls(type="camera")):
        return
    return {"warnings": ["No renderable cameras. Please make at least one camera renderable in Render Settings."]}


def validate_something():
    pass
 