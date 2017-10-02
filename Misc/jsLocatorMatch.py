import maya.cmds as cmds

target = cmds.ls(sl=True, fl=True)
for i in target:
    locator=cmds.spaceLocator()
    point = cmds.pointConstraint(i,locator,mo=0)
    orient = cmds.orientConstraint(i,locator,mo=0)
    scale = cmds.scaleConstraint(i,locator,mo=0)
    cmds.delete(point)
    cmds.delete(orient)
    cmds.delete(scale)
