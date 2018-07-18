import maya.cmds as cmds

class BonusTools(object):

    def __init__(self):
        print 'Initializing jsRenamer BonusTools...'

    def cleanUpShapes(self,args=None):
        sel = cmds.ls(sl=1,type='transform')

        for xform in sel:
            print xform
            correctShape = []
            children = cmds.listRelatives(xform,c=1)
            for childShape in children:
                if cmds.listConnections(childShape+'.instObjGroups') == None:
                    print 'deleted ' + childShape
                    cmds.delete(childShape)
                else:
                    correctShape.append(childShape)
                        
            for origShapeName in correctShape:
                cmds.rename(origShapeName,xform+'Shape')
                print xform+'Shape'