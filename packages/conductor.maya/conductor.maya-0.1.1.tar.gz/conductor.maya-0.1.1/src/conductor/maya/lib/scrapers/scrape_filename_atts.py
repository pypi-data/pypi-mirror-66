"""
A basic scraper to collect paths from Maya filename attributes.

If an attribute is intended to contain a filename, it should have the
usedAsFilename flag set. This scraper returns the value for all such attributes
in the scene, including those contained in 3rd party plugins.
"""

import maya.api.OpenMaya as om
import pymel.core as pm
import re

# nodetypes that can always be safely ignored
BLACKLIST = [
    "partition",
    "shadingEngine",
    "objectSet",
    "script",
    "objectRenderFilter",
    "objectMultiFilter",
    "objectAttrFilter",
    "objectNameFilter",
    "objectScriptFilter",
    "objectTypeFilter",
    "nodeGraphEditorInfo",
    "renderSettingsCollection",
    "simpleSelector",
    "partition",
    "conductorRender",
    "displayLayer",
    "defaultLightList",
    "renderGlobals",
    "renderLayer",
    "renderQuality",
    "defaultRenderUtilityList",
    "defaultRenderingList",
    "resolution",
    "defaultShaderList",
    "defaultTextureList",
    "dof",
    "dynController",
    "globalCacheControl",
    "hardwareRenderGlobals",
    "hardwareRenderingGlobals",
    "hikSolver",
    "hyperGraphInfo",
    "hyperLayout",
    "ikRPsolver",
    "ikSCsolver",
    "ikSplineSolver",
    "ikSystem",
    "materialInfo",
    "displayLayerManager",
    "lightLinker",
    "lightList",
    "polyMergeEdge",
    "polyMergeFace",
    "poseInterpolatorManager",
    "renderGlobalsList",
    "renderLayerManager",
    "renderSetup",
    "selectionListOperator",
    "sequenceManager",
    "shapeEditorManager",
    "strokeGlobals",
    "multilisterLight",
    "time",
    "aiOptions",
    "hwRenderGlobals",
]


def run():
    """
    Find values in attributes that have usedAsFilename flag set.

    Test all nodes in the scene.

    For optimization purposes: As we find nodes with NO usedAsFilename atts, we
    add the typename to a blacklist. Aw we find nodes WITH usedAsFilename atts,
    we add the atts to a whitelist object, keyed on the typename. In this way,
    we can quickly eliminate a node (if it's type is in the blacklist), or know
    which attributes are viable filename candidates.

    """
    blacklist = []
    whitelist = {}
    result = []

    sel = om.MSelectionList()
    sel.add("*")
    num = sel.length()

    for i in xrange(num):
        dn_obj = sel.getDependNode(i)
        fn_node = om.MFnDependencyNode(dn_obj)
        typename = fn_node.typeName
        if typename in BLACKLIST or typename in blacklist:
            continue
        if typename not in whitelist:  # yet
            atts = get_potential_filename_atts(fn_node)

            if atts:
                whitelist[typename] = atts
            else:
                blacklist.append(typename)

        if typename in whitelist:
            attnames = whitelist[typename]

            result += get_filename_paths_for_node(fn_node, attnames)

    for r in result:
        r["path"] = re.sub("<f>", "*", r["path"])
    return result


def get_potential_filename_atts(fn_node):
    """
    Get the list of atts for a node that are probably filenames.

    They either have usedAsFilename set. Or they are string/stringArray and
    their name contains the word file or path.
    """
    result = []
    num_atts = fn_node.attributeCount()
    for a in range(num_atts):
        att_obj = fn_node.attribute(a)
        if att_obj.hasFn(om.MFn.kTypedAttribute):
            fn_attr = om.MFnTypedAttribute(att_obj)
            attr_type = fn_attr.attrType()
            attr_name = fn_attr.name
            if fn_attr.usedAsFilename:
                result.append(attr_name)
            elif (
                attr_type == om.MFnData.kString or attr_type == om.MFnData.kStringArray
            ):
                attr_name_lower = attr_name.lower()
                if "file" in attr_name_lower or "path" in attr_name_lower:
                    result.append(attr_name)

    return result


def get_filename_paths_for_node(fn_node, attnames):
    """
    Get filename values for usedAsFilename plugs.

    When we get a node's plug from the att name, it may be a child of a compound
    array plug (or even nested seveal levels). In this case the name will be of
    the form node_name.parentPlug[-1].childPlug This (-1) is a nonexistent plug.
    If any plugs do exist the index wil be >= 0. In order to get the actual plug
    elements, if they exist, we use a SelectionList. We add a wildcard name to
    the selectionlist and iterate through the real plugs it contains.

    The [-1] indicator is only used for array parent plugs, not leaf level array
    plugs.

    If the leaf level plug is an array, then we find out with isArray() and
    iterate over its elements.
    """
    ws = pm.Workspace()
    result = []
    for attname in attnames:
        plug = fn_node.findPlug(attname, False)
        plug_selection_list = om.MSelectionList()
        try:
            plug_selection_list.add(plug.name().replace("[-1]", "[*]"))
        except RuntimeError:
            continue

        num_plugs = plug_selection_list.length()
        for p in xrange(num_plugs):
            real_plug = plug_selection_list.getPlug(p)
            if real_plug.isArray:
                for physical_index in xrange(real_plug.numElements()):
                    child_plug = plug.elementByPhysicalIndex(physical_index)
                    value = child_plug.asString()
                    if value:
                        result.append(
                            {"path": ws.expandName(value), "plug": child_plug.name()}
                        )
            else:
                value = real_plug.asString()
                if value:
                    result.append(
                        {"path": ws.expandName(value), "plug": real_plug.name()}
                    )
    return result
