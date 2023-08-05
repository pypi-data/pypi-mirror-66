"""
Software data as a singleton.

Software is converted to a PackageTree containing only maya packages and
supported plugins.

Also has the ability to use fixtures for dev purposes.
"""

import json
import os
import re
from conductor.core import api_client
from conductor.core.package_tree import PackageTree
from conductor.maya.lib import const as k
import pymel.core as pm

__data__ = None


def data(**kw):
    global __data__
    if (__data__ == None) or kw.get("force"):
        try:
            if k.USE_CACHES:
                module_path = pm.moduleInfo(path=True, moduleName="conductor")
                cache_path = os.path.join(module_path , "dev", "fixtures", "software.json" )
                if os.path.isfile(cache_path):
                    with open(cache_path) as f:
                        all_packages = json.load(f)
                else:
                    all_packages = api_client.request_software_packages()
            else:
                all_packages = api_client.request_software_packages()
            __data__ = PackageTree(all_packages, product="maya-io")
        except BaseException:
            __data__ = None
    return __data__


def detect_host():
    version_parts = pm.about(iv=True).replace("Autodesk Maya", "").strip().split(".")
    if len(version_parts) < 2:
        version_parts.append("0")
    version_parts[1] = "SP{}".format(version_parts[1])
    return "maya-io {}".format(".".join(version_parts))

def detect_mtoa():
    try:
        version = pm.pluginInfo("mtoa", q=True, version=True)
    except RuntimeError:
        return
    parts = version.split(".")
    version = ".".join(parts + ['0'] * (4 - len(parts)))
    return "arnold-maya {}".format(version)
 
def detect_rfm():
    try:
        version = pm.pluginInfo("RenderMan_for_Maya", q=True, version=True)
    except RuntimeError:
        return
    parts = filter(None, re.split(r" |\.|@", version))
    version = ".".join(parts + ['0'] * (4 - len(parts)))
    return "renderman-maya {}".format(version)
