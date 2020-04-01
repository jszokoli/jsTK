import maya.cmds as cmds
import random
import textwrap

class BonusTools():

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

    def visualize_materials(self,*args):
        missingMaterialList = []
        origSel = cmds.ls(sl=1)
        modelGRP = cmds.ls('*_GE?')
        candidate_meshes = cmds.listRelatives(modelGRP, ad=1, typ="mesh")
        for mesh in candidate_meshes:
            mtlName = mesh.split('_')[0]
            if mtlName not in missingMaterialList:
                if 'Mtl' in mtlName:
                    missingMaterialList.append(mtlName)
                else:
                    missingMaterialList.append(mtlName)
        print missingMaterialList
        for mtl in missingMaterialList:
            print mtl
            fbxProxyMtl = cmds.shadingNode('lambert', n=mtl, asShader=True)
            cmds.addAttr(fbxProxyMtl, sn='FBXshader', at="float")
            cmds.setAttr(fbxProxyMtl + '.FBXshader', 1)
            removeMtl = mtl[0:-3]
            print removeMtl
            divNum = len(removeMtl) / 3
            print divNum
            splitMtl = textwrap.wrap(removeMtl, divNum)
            print splitMtl
            random.seed(splitMtl[0])
            redC = random.random()
            random.seed(splitMtl[1])
            greenC = random.random()
            if len(splitMtl) == 3:
                random.seed(splitMtl[2])
            else:
                compoundSplit = splitMtl[2] + splitMtl[3]
                print compoundSplit
                random.seed(compoundSplit)
            blueC = random.random()
            print redC, greenC, blueC
            cmds.setAttr(fbxProxyMtl + '.color', redC, greenC, blueC, type='double3')
            cmds.select(mtl + '*')
            cmds.hyperShade(a=fbxProxyMtl)

    def delete_visualizers(self,*args):
        origSel = cmds.ls(sl=1)
        allMats = cmds.ls(mat=1)
        for mtl in allMats:
            if cmds.attributeQuery('FBXshader', n=mtl, exists=1) == 1:
                print mtl
                cmds.hyperShade(o=mtl)
                appliedMeshes = cmds.ls(sl=1)
                print appliedMeshes
                upper = cmds.hyperShade(mtl, ldn=mtl)
                SG = cmds.ls(upper, type='shadingEngine')
                cmds.delete(mtl)
                cmds.delete(SG)
                cmds.select(appliedMeshes)
                cmds.hyperShade(a='lambert1')
        cmds.select(origSel)
    @classmethod
    def material_scan(self):
        candidate_meshes = cmds.ls('*_GE?')
        children = cmds.listRelatives(candidate_meshes, ad=1, typ="mesh")
        material_list = []
        for mesh in children:
            mtl_name = mesh.split('_')[0]
            if mtl_name not in material_list:
                if 'Mtl' in mtl_name:
                    material_list.append(mtl_name)
                else:
                    material_list.append(mtl_name)
        return material_list