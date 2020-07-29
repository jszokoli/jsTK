def screenShotCurrent(dir, name):
    oldFormat = cmds.getAttr('defaultRenderGlobals.imageFormat')
    oldGrid = cmds.grid(toggle=True, q=True)
    cmds.grid(toggle=0)
    cmds.setAttr('defaultRenderGlobals.imageFormat', 8)
    cmds.playblast(frame=1, format='image', cf=dir + name + '.jpg', v=0, wh=[1280, 720], p=100)
    cmds.setAttr('defaultRenderGlobals.imageFormat', oldFormat)
    cmds.grid(toggle=oldGrid)


screenShotCurrent('/net/homes/jszokoli/Desktop/', 'test')

target = cmds.ls(sl=True, fl=True)
for i in target:
    locator = cmds.spaceLocator()
    point = cmds.pointConstraint(i, locator, mo=0)
    cmds.delete(point)

import os

scriptPath = os.environ['MAYA_SCRIPT_PATH']
print scriptPath

sel = cmds.ls(sl=1)
createdNodes = []
for z in sel:
    getKeyable = cmds.listAttr(z, k=1)
    infoNode = cmds.group(name=z + '_infoNode', em=1)
    print infoNode
    createdNodes.append(infoNode)
    for i in getKeyable:
        typeAttr = cmds.attributeQuery(i, node=z, at=1)
        saveAttr = cmds.getAttr(z + '.' + i)
        print i + ' ' + str(saveAttr)
        print typeAttr
        cmds.addAttr(infoNode, longName=i + '_info', attributeType=typeAttr)
        cmds.setAttr(infoNode + '.' + i + '_info', saveAttr)
print createdNodes
cmds.group(createdNodes, name='asset')

sel = cmds.ls('*_infoNode')
for z in sel:
    new = z.split('_')[0]
    udAttr = cmds.listAttr(z, ud=1)
    for i in udAttr:
        get = cmds.getAttr(z + '.' + i)
        shortAttr = i.split('_')[0]
        cmds.setAttr(new + '.' + shortAttr, get)

sel = cmds.ls(sl=1)
for i in sel:
    cmds.setAttr(i + '.primaryVisibility', 0)

cmds.listAttr()

cmds.listRelatives(cmds.ls(sl=1), s=1)
sel = cmds.ls(sl=1)
for each in sel:
    print each