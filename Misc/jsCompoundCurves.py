#compoundCurves
sel = cmds.ls(sl=1)
parentXform = sel[0]
newChildrenShapes = sel[1:]

for i in newChildrenShapes:
    curveChildShape = cmds.listRelatives(i,shapes = True)
    cmds.parent(curveChildShape,parentXform,relative=True,shape=True)


