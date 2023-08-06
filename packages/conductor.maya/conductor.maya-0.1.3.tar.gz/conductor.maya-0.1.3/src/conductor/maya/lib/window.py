"""
Submit.

"""
import json

import pymel.core as pm
from conductor.core import  CONFIG
import urlparse

def show_as_json(data, **kw):
    """Not modal, as"""
    title = kw.get("title", "Json Window")
    indent = kw.get("indent", 2)
    sort_keys= kw.get("sort_keys", True)
    result_json = json.dumps(data, indent=indent, sort_keys=sort_keys)
    pm.window(width=600, height=800, title=title)
    pm.frameLayout(cll=False, lv=False)
    pm.scrollField(text=result_json, editable=False, wordWrap=False)
    pm.showWindow()



def _dismiss():
    pm.layoutDialog(dismiss="abort")

def _okay():
    pm.layoutDialog(dismiss="okay")


def warnings_layout(warnings):

    form = pm.setParent(query=True)
    pm.formLayout(form, edit=True, width=300)

    text = pm.text(label="Warnings")
    b1 = pm.button(label="Abort", command=pm.Callback(_dismiss))
    b2 = pm.button(label="Continue", command=pm.Callback(_okay))

    scroll = pm.scrollLayout(bv=True)
    pm.setParent("..")

    form.attachForm(text, 'left', 2)
    form.attachForm(text, 'right', 2)
    form.attachForm(text, 'top', 2)
    form.attachNone(text, 'bottom')

    form.attachForm(scroll, 'left', 2)
    form.attachForm(scroll, 'right', 2)
    form.attachControl(scroll, 'top', 2, text)
    form.attachControl(scroll, 'bottom', 2, b1)

    form.attachForm(b1, 'left', 2)
    form.attachPosition(b1, 'right',  2, 50)
    form.attachNone(b1, 'top')
    form.attachForm(b1, 'bottom', 2)

    form.attachPosition(b2, 'left',  2, 50)
    form.attachForm(b2, 'right', 2)
    form.attachNone(b2, 'top')
    form.attachForm(b2, 'bottom', 2)

    pm.setParent(scroll)
    pm.columnLayout()
    for w in warnings:
        pm.text(label=w)

    pm.setParent(form)
 

def show_warnings(warnings):
    return pm.layoutDialog(ui=pm.Callback(warnings_layout, warnings))


 
def submission_responses_layout(responses):


    print "-------- RESPONSES ------------"
    print responses
    print "-" * 30


    form = pm.setParent(query=True)
    pm.formLayout(form, edit=True, width=300)

    text = pm.text(label="Submission results")

    b1 = pm.button(label="Close", command=pm.Callback(_okay))

    scroll = pm.scrollLayout(bv=True)
    pm.setParent("..")

    form.attachForm(text, 'left', 2)
    form.attachForm(text, 'right', 2)
    form.attachForm(text, 'top', 2)
    form.attachNone(text, 'bottom')

    form.attachForm(scroll, 'left', 2)
    form.attachForm(scroll, 'right', 2)
    form.attachControl(scroll, 'top', 2, text)
    form.attachControl(scroll, 'bottom', 2, b1)

    form.attachForm(b1, 'left', 2)
    form.attachForm(b1, 'right',  2)
    form.attachNone(b1, 'top')
    form.attachForm(b1, 'bottom', 2)
 
    pm.setParent(scroll)
    pm.columnLayout()


 
    for success_uri in [
        response["response"]["uri"].replace("jobs", "job")
        for response in responses
        if response.get("code") <= 201
    ]:
        job_url = urlparse.urljoin(CONFIG['auth_url'], success_uri)
        label = "<a href=\"{}\"><font  color=#ec6a17 size=4>{}</font></a>".format(job_url,job_url)

 
        print label

  
        pm.text( hl=True, label=label )

    num_failed = len([r for r in responses if r.get("code") > 201])

    if num_failed:
        pm.text(label="Number of failed submissions: {:d}".format(num_failed))
 
    pm.setParent(form)
 
def show_submission_responses(responses):
    return pm.layoutDialog(ui=pm.Callback(submission_responses_layout, responses))


 