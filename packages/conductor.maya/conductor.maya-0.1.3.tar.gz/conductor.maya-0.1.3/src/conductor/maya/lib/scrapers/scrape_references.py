
"""
A scraper to return paths to referenced files.

"""
import pymel.core as pm


def run():
    result = [{"path": unicode(p)} for p in pm.listReferences(recursive=True)]
    result.append({"path": unicode(pm.sceneName())})
    return result
