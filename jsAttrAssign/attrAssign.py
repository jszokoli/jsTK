import maya.cmds as cmds

class AttrAssigner(object):

    def __init__(self):
        print 'Initialized AttrAssigner'

    def commonAttrFunc(self,args=None):
        sel = cmds.ls(sl=1)
        selShapes = []
        #Convert Selection to shapes
        if sel != []:
            for obj in sel:
                nodeTy = cmds.nodeType(obj)
                if nodeTy == 'transform':
                    shape = cmds.listRelatives(obj,s=1)
                    selShapes.append(shape)
                else:
                    selShapes.append(obj)
               
            print selShapes   
            #Compare and output Lists for attrs
            commonAttr = []
            commonAttrCheck =[]
            #Build Initial List of attrs
            availFirstAttrs = cmds.listAttr(selShapes[0],v=1,se=1)
            for start in availFirstAttrs:
                commonAttrCheck.append(start)
            #print commonAttrCheck
            #Compare attrs to remainder of selection
            for i in selShapes:
                availAttrs = cmds.listAttr(i,v=1,se=1)
                for x in availAttrs:
                    if x in commonAttrCheck:
                        if x not in commonAttr:
                            commonAttr.append(x)
            return commonAttr


    def attrAssign(self, attr,val):
        sel = cmds.ls(sl=1)    
        if sel != []:
            for obj in sel:
                nodeTy = cmds.nodeType(obj)[0]
                if nodeTy == 'transform':
                    obj = cmds.listRelatives(obj,s=1)
                attrType = cmds.getAttr(obj+'.'+attr,type=1)
                
                #For Float
                if attrType == 'float':
                    val = float(val)
                    if val != None:
                        cmds.setAttr(obj+'.'+attr,val)
                    
                #For Vector
                elif attrType == 'float3':            
                    val = val.split(',')
                    if len(val) == 3:
                        confirmList = []
                        for i in val:
                            confirmList.append( float(i) )
                        val = confirmList
                    else:
                        cmds.warning('Vectors must be typed \"Value,Value,Value\"')
                        val = None
                    if val != None:
                        print val[0]
                        print val[1]
                        print val[2]
                        print val
                        cmds.setAttr('aiStandard3.color', val[0],val[1],val[2] ,type='double3' )
                #For Bool
                elif attrType == 'bool':
                    val = int(float(val))
                    if val != None:
                        cmds.setAttr(obj+'.'+attr,val)
                    
                    
                #For Enum
                elif attrType == 'enum':
                    val = int(float(val))
                    if val != None:
                        cmds.setAttr(obj+'.'+attr,val)
                    
                #For String
                elif attrType == 'string':
                    val = val
                    if val != None:
                        cmds.setAttr(obj+'.'+attr,val,type='string')
        print ''




