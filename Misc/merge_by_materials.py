from collections import defaultdict


sel = cmds.ls(sl=1)


matDict = defaultdict(list)
for i in sel:
    print i
    shapesInSel = cmds.listRelatives(i,shapes = True)
    # get shading groups from shapes:
    shadingGrps = cmds.listConnections(shapesInSel,type='shadingEngine')
    # get the shaders:
    shaders = cmds.ls(cmds.listConnections(shadingGrps),materials=1)
    print shaders[0]
    currentList =  matDict[shaders[0]]
    currentList.append(i)


print matDict



for key, value in matDict.iteritems():
    print key, value
    cmds.select(value)
    cmds.polyUnite( value, n=key+'_GEP' )
