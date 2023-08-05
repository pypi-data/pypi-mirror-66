"""
Project data as a singleton.

Also has the ability to use fixtures for dev purposes.
"""
import json
import os

from conductor.core import api_client
from conductor.maya.lib import const as k
import pymel.core as pm

__data__ = None

def data(**kw):
    global __data__
    if (not __data__) or kw.get("force"):
        try:
            if k.USE_CACHES:
                module_path = pm.moduleInfo(path=True, moduleName="conductor")
                cache_path = os.path.join(module_path , "dev", "fixtures", "projects.json" )
                if os.path.isfile(cache_path):
                    with open(cache_path) as f:
                        __data__ = json.load(f)
                else:
                    __data__ = sorted(api_client.request_projects())
            else:
                __data__ = sorted(api_client.request_projects())
        except BaseException:
            __data__ = None
    return __data__
