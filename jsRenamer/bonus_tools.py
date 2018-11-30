import maya.cmds as cmds

class BonusTools(object):

    def __init__(self):
        print 'Initializing jsRenamer BonusTools...'

    def cleanUpShapes(self,args=None):
        sel = cmds.ls(sl=1,type='transform',l=True)

        for xform in sel:
            # print xform
            #print xform
            cmds.delete(xform,ch=1)
            correctShape = []
            intermediateShapes = []
            children = cmds.listRelatives(xform,c=1,f=True)
            # print children
            for shapeNode in children:
                # print shapeNode
                # print cmds.getAttr(shapeNode+'.intermediateObject')
                if cmds.getAttr(shapeNode+'.intermediateObject') == True:
                #if True in cmds.getAttr(shapeNode+'.intermediateObject'):
                    # print shapeNode
                    intermediateShapes.append(shapeNode)
                else:
                    correctShape.append(shapeNode)
            # print intermediateShapes
            # print correctShape 
            if len(intermediateShapes) > 0:
                cmds.delete(intermediateShapes)
            for origShapeName in correctShape:
                if origShapeName in xform+'Shape':
                    pass
                else: 
                    # print origShapeName
                    origShapeNameSplit = xform.split('|')[-1]
                    # print origShapeNameSplit
                    cmds.rename(origShapeName,origShapeNameSplit+'Shape')

            if len(intermediateShapes) > 0:
                print xform+' intermediate shapes nodes ('+str(intermediateShapes)+') have been deleted'

'''
    def cleanUpShapes(self,args=None):
        sel = cmds.ls(sl=1,type='transform')

        for xform in sel:
            #print xform
            cmds.delete(xform,ch=1)
            correctShape = []
            intermediateShapes = []
            children = cmds.listRelatives(xform,c=1)
            for shapeNode in children:
                #print shapeNode
                if cmds.getAttr(shapeNode+'.intermediateObject') == True:
                    intermediateShapes.append(shapeNode)
                else:
                    correctShape.append(shapeNode)
            #print intermediateShapes
            #print correctShape 
            if len(intermediateShapes) > 0:
                cmds.delete(intermediateShapes)
            
            for origShapeName in correctShape:
                if origShapeName in xform+'Shape':
                    pass
                else:            
                    cmds.rename(origShapeName,xform+'Shape')

            if len(intermediateShapes) > 0:
                print xform+' intermediate shapes nodes ('+str(intermediateShapes)+') have been deleted'
'''
                




        
