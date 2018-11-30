import maya.cmds as cmds
import random
import textwrap

def createFBXProxies(args=None):
    origSel = cmds.ls(sl=1)
    modelGRP = cmds.ls('high_model_GRP')
    children = cmds.listRelatives(modelGRP,ad=1,typ="mesh")
    missingMaterialList = []
    for mesh in children:
        mtlName =  mesh.split('_')[0]
        if mtlName not in missingMaterialList:
            if 'Mtl' in mtlName:
                missingMaterialList.append(mtlName)
            else:
                 missingMaterialList.append(mtlName)
    print missingMaterialList
    for mtl in missingMaterialList:
        fbxProxyMtl= cmds.shadingNode('lambert', n = mtl, asShader=True)
        cmds.addAttr(fbxProxyMtl, sn='FBXshader', at="float")
        cmds.setAttr(fbxProxyMtl+'.FBXshader', 1)
        removeMtl = mtl[0:-3]
        print removeMtl
        divNum = len(removeMtl)/3
        print divNum
        splitMtl = textwrap.wrap(removeMtl,divNum)
        print splitMtl
        random.seed(splitMtl[0])
        redC = random.random()
        random.seed(splitMtl[1])
        greenC = random.random()
        if len(splitMtl)==3:
            random.seed(splitMtl[2])
        else:
            compoundSplit = splitMtl[2]+splitMtl[3]
            print compoundSplit
            random.seed(compoundSplit)
        blueC = random.random()
        print redC,greenC,blueC
        
        cmds.setAttr(fbxProxyMtl+'.color',redC,greenC,blueC,type='double3')
        cmds.select(mtl+'*')
        cmds.hyperShade(a=fbxProxyMtl)
    cmds.select(origSel)

def createFBXProxiesUI(args=None):
    origSel = cmds.ls(sl=1)
    textFieldAns= cmds.textField('searchField',q=1,tx=1)
    modelGRP = cmds.ls(textFieldAns)
    children = cmds.listRelatives(modelGRP,ad=1,typ="mesh")
    missingMaterialList = []
    for mesh in children:
        mtlName =  mesh.split('_')[0]
        if mtlName not in missingMaterialList:
            if 'Mtl' in mtlName:
                missingMaterialList.append(mtlName)
            else:
                missingMaterialList.append(mtlName) 
    print missingMaterialList
    for mtl in missingMaterialList:
        fbxProxyMtl= cmds.shadingNode('lambert', n = mtl, asShader=True)
        cmds.addAttr(fbxProxyMtl, sn='FBXshader', at="float")
        cmds.setAttr(fbxProxyMtl+'.FBXshader', 1)
        removeMtl = mtl[0:-3]
        print removeMtl
        divNum = len(removeMtl)/3
        print divNum
        splitMtl = textwrap.wrap(removeMtl,divNum)
        print splitMtl
        random.seed(splitMtl[0])
        redC = random.random()
        random.seed(splitMtl[1])
        greenC = random.random()
        if len(splitMtl)==3:
            random.seed(splitMtl[2])
        else:
            compoundSplit = splitMtl[2]+splitMtl[3]
            print compoundSplit
            random.seed(compoundSplit)
        blueC = random.random()
        print redC,greenC,blueC
        
        cmds.setAttr(fbxProxyMtl+'.color',redC,greenC,blueC,type='double3')
        cmds.select(mtl+'*')
        cmds.hyperShade(a=fbxProxyMtl)
    cmds.select(origSel)



def deleteFBXProxies(args=None):
    origSel = cmds.ls(sl=1)
    allMats = cmds.ls(mat=1)
    for mtl in allMats:
        if cmds.attributeQuery('FBXshader', n=mtl, exists=1) == 1:
            print mtl
            cmds.hyperShade(o=mtl)
            appliedMeshes = cmds.ls(sl=1)
            print appliedMeshes
            upper = cmds.hyperShade(mtl, ldn = mtl)
            SG = cmds.ls(upper, type = 'shadingEngine')            
            cmds.delete(mtl)
            cmds.delete(SG)
            cmds.select(appliedMeshes)
            cmds.hyperShade(a='lambert1')
    cmds.select(origSel)           
#createFBXProxies()
#deleteFBXProxies()

def buildMatProxyUI(args=None):
    if cmds.window('FBXMaterials',exists=True):
        cmds.deleteUI('FBXMaterials')
    
    window = cmds.window('FBXMaterials',menuBar=True, title= 'FBXMaterials' , w=330, h=100) #, s = False
    
    
    cmds.columnLayout(adj=1)
    
    cmds.frameLayout(label = 'Material Prefix Proxy Materials')
    cmds.columnLayout(adj=1)
    cmds.textField('searchField', tx='model_GRP')
    buttH=35
    addProxyButt = cmds.button(h=buttH,l='Create Prefix Materials:',c=createFBXProxiesUI)
    cmds.button(h=buttH,l='Delete Proxy Nodes:',c=deleteFBXProxies)
        
    cmds.showWindow( window )
    cmds.window('FBXMaterials', edit=True, widthHeight=[200, 118], s = False)#409
    #cmds.window('wrinkleCenter', query=True, widthHeight=True)
buildMatProxyUI()
