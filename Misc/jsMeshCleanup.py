import maya.cmds as cmds


path = "F:\job\proj\Xwing\\asset\Xwing\model\maya\data\clean\\"

print path


sel = cmds.ls(sl=1)

for i in sel:
    print i
    uuidNode = cmds.ls(i, uuid=True)
    print uuidNode
    parentNode = cmds.listRelatives(i, p=True)
    print parentNode
    cmds.parent( i, world=True )
    newNodeName = cmds.ls(uuidNode)
    print newNodeName
    
    cmds.select(newNodeName)
    newFile = cmds.file(path+'cleaner.obj',force=True, exportSelected=True, type="OBJexport")
    print 'EXPORTED'
    print i, newFile
    
    cmds.delete(newNodeName)
    cleanObj = cmds.file(path+'cleaner.obj', force=True, i=True, type="OBJexport", dns = True,rnn=True)
    
    for node in cleanObj:
        if cmds.nodeType(node) == 'mesh' or cmds.nodeType(node) == 'transform':
            if cmds.nodeType(node) == 'transform':
                xformNode = node
            
            
    print 'IMPORTED'
    print xformNode
    cmds.parent(xformNode, parentNode)
    
#cmds.nodeType('EngineVentExhaust_GRP1|FilthyEngineMetal_L_Exhaust_0009_GEP|FilthyEngineMetal_L_Exhaust_0009_GEPShape')
