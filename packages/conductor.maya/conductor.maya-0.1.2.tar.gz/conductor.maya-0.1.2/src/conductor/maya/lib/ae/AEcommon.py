def printSetAttrCmd(attr):
    if attr.type() == "string":
        print 'setAttr -type "string" "{}" "{}";'.format(attr.name(), attr.get())
    else:
        print 'setAttr "{}" {};'.format(attr.name(), attr.get())
