import maya.cmds as cmds
import math as math
sel = cmds.ls(sl=1)
for lgt in sel:
    Intensity = cmds.getAttr(lgt+'.intensity')
    Exposure = cmds.getAttr(lgt+'.aiExposure')
    print Intensity,Exposure
    expCalc = 2**Exposure
    oldBrightness = Intensity*expCalc
    print oldBrightness
    newExposure = math.log(oldBrightness,2)
    cmds.setAttr(lgt+'.intensity',1)
    cmds.setAttr(lgt+'.aiExposure',newExposure)
