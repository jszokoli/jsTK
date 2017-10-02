import maya.cmds as cmds

########################
###jsBlendTools v1.0 ###
########################

#Author: Joseph Szokoli
#Website: cargocollective.com/josephSzokoli

#Help: 
#To create a shelf icon, move jsBlendTools.py to your scripts folder and assign the following command to the shelf.
#import jsBlendTools
#reload(jsBlendTools)

### ChangeLog: ################################################################################

###v1.0
#Initial Release jsBlendTools

#End ChangeLog.#################################################################################



#Begin Functions Area


origBrows = 'brow_lineUp brow_lineDown brow_lidUp brow_lidDown brow_massUp brow_massDown brow_slideOut brow_slideIn brow_lineScaleUp brow_lineScaleDown brow_lidScaleUp brow_lidScaleDown brow_insideUp brow_insideDown brow_middleUp brow_middleDown brow_outsideUp brow_outsideDown brow_bridgeCrease brow_crowsfeetDown'

brows = ['Brows','brow_lineUp', 'brow_lineDown', 'brow_lidUp', 'brow_lidDown', 'brow_massUp', 'brow_massDown', 'brow_slideOut', 'brow_slideIn', 'brow_lineScaleUp', 'brow_lineScaleDown', 'brow_lidScaleUp', 'brow_lidScaleDown', 'brow_insideUp', 'brow_insideDown', 'brow_middleUp', 'brow_middleDown', 'brow_outsideUp', 'brow_outsideDown', 'brow_bridgeCrease', 'brow_crowsfeetDown']


origCheeks = 'cheek_lineUp cheek_lineDown cheek_lidUp cheek_lidDown cheek_massUp cheek_massDown cheek_puffOut cheek_puffIn cheek_slideOut cheek_slideIn cheek_scaleUp cheek_scaleDown cheek_lidScaleUp cheek_lidScaleDown cheek_insideUp cheek_insideDown cheek_middleUp cheek_middleDown cheek_outsideUp cheek_outsideDown cheek_ridgeCrease'
cheeks = ['Cheeks','cheek_lineUp', 'cheek_lineDown', 'cheek_lidUp', 'cheek_lidDown', 'cheek_massUp', 'cheek_massDown', 'cheek_puffOut', 'cheek_puffIn', 'cheek_slideOut', 'cheek_slideIn', 'cheek_scaleUp', 'cheek_scaleDown', 'cheek_lidScaleUp', 'cheek_lidScaleDown', 'cheek_insideUp', 'cheek_insideDown', 'cheek_middleUp', 'cheek_middleDown', 'cheek_outsideUp', 'cheek_outsideDown', 'cheek_ridgeCrease']


origMouth = 'mouth_jawOpen mouth_jawClose mouth_jawUp mouth_jawDown mouth_jawLeft mouth_jawOut mouth_jawIn mouth_lipSlideLeft mouth_lipSlideRight mouth_lipWide mouth_lipNarrow mouth_lipTense mouth_lipRelease mouth_cornerUp mouth_cornerDown mouth_cornerOut mouth_cornerIn mouth_cornerPinch mouth_cornerRelease mouth_cornerCurlUp mouth_cornerCurlDown mouth_lipTopUp mouth_lipTopDown mouth_lipBottomUp mouth_lipBottomDown mouth_lipTopRollOut mouth_lipTopRollIn mouth_lipBottomRollOut mouth_lipBottomRollIn mouth_lipTopPushOut mouth_lipTopPushIn mouth_lipBottomPushOut mouth_lipBottomPushIn mouth_lipTopInsideUp mouth_lipTopInsideDown mouth_lipBottomInsideUp mouth_lipBottomInsideDown mouth_lipTopMiddleUp mouth_lipTopMiddleDown mouth_lipBottomMiddleUp mouth_lipBottomMiddleDown mouth_lipTopOutsideUp mouth_lipTopOutsideDown mouth_lipBottomOutsideUp mouth_lipBottomOutsideDown mouth_lipTopScaleUp mouth_lipTopScaleDown mouth_lipBottomScaleUp mouth_lipBottomScaleDown mouth_lipTopCreaseHarden mouth_lipTopCreaseSoften mouth_lipBottomCreaseHarden mouth_lipBottomCreaseSoften mouth_nostrilFlare mouth_nostrilContract mouth_nostrilUp mouth_nostrilDown mouth_noseSneer'

mouth1 = ['Mouth_Row_1','mouth_jawOpen', 'mouth_jawClose', 'mouth_jawUp', 'mouth_jawDown', 'mouth_jawLeft', 'mouth_jawOut', 'mouth_jawIn', 'mouth_lipSlideLeft', 'mouth_lipSlideRight', 'mouth_lipWide', 'mouth_lipNarrow', 'mouth_lipTense', 'mouth_lipRelease', 'mouth_cornerUp', 'mouth_cornerDown', 'mouth_cornerOut', 'mouth_cornerIn', 'mouth_cornerPinch', 'mouth_cornerRelease', 'mouth_cornerCurlUp', 'mouth_cornerCurlDown']
mouth2 = ['Mouth_Row_2','mouth_lipTopUp', 'mouth_lipTopDown', 'mouth_lipBottomUp', 'mouth_lipBottomDown', 'mouth_lipTopRollOut', 'mouth_lipTopRollIn', 'mouth_lipBottomRollOut', 'mouth_lipBottomRollIn', 'mouth_lipTopPushOut', 'mouth_lipTopPushIn', 'mouth_lipBottomPushOut', 'mouth_lipBottomPushIn', 'mouth_lipTopInsideUp', 'mouth_lipTopInsideDown', 'mouth_lipBottomInsideUp', 'mouth_lipBottomInsideDown', 'mouth_lipTopMiddleUp']
mouth3= ['Mouth_Row_3','mouth_lipTopMiddleDown', 'mouth_lipBottomMiddleUp', 'mouth_lipBottomMiddleDown', 'mouth_lipTopOutsideUp', 'mouth_lipTopOutsideDown', 'mouth_lipBottomOutsideUp', 'mouth_lipBottomOutsideDown', 'mouth_lipTopScaleUp', 'mouth_lipTopScaleDown', 'mouth_lipBottomScaleUp', 'mouth_lipBottomScaleDown', 'mouth_lipTopCreaseHarden', 'mouth_lipTopCreaseSoften', 'mouth_lipBottomCreaseHarden', 'mouth_lipBottomCreaseSoften', 'mouth_nostrilFlare', 'mouth_nostrilContract', 'mouth_nostrilUp', 'mouth_nostrilDown', 'mouth_noseSneer']


def nudgeShape(origShape,shapeList):
    listNew = []
    startNudge = 0
    objectSize = cmds.xform(origShape,query=True,bb=1)
    widthX = objectSize[3] - objectSize[0]
    widthY = objectSize[4] - objectSize[1]
    widthZ = objectSize[5] - objectSize[2]    
    shapeType = shapeList[0]
    for i in shapeList[1:]:
        cmds.select(origShape)
        startNudge=startNudge+1
        newShape = cmds.duplicate(n = '%s_%s'%(origShape,i))#sel change
        pos = cmds.xform(newShape,q=1,ws=1,rp=1)
        newY = objectSize[1] + widthY+widthY/3
        newPos = [pos[0],newY,pos[2]]
        cmds.select(newShape)
        anno = cmds.annotate(newShape, tx=i, p = newPos)#selChange
        cmds.setAttr(anno+'.displayArrow',0)
        newGRP = cmds.group(newShape,anno, n=i+'_GRP')#selChange
        XnudgeValue = widthX+widthX/1    
        XnudgeValue = XnudgeValue*startNudge
        cmds.xform(r=1,t=[-XnudgeValue,0,0] )  
        listNew.append(newGRP)
    print listNew
    cmds.group(listNew, n=shapeType+'_BLENDS_GRP')


def createShapes(Shape,brows,cheeks,mouth1,mouth2,mouth3):
    objectSize = cmds.xform(Shape,query=True,bb=1)
    widthX = objectSize[3] - objectSize[0]
    widthY = objectSize[4] - objectSize[1]
    widthZ = objectSize[5] - objectSize[2]  
     
    nudgeShape(Shape,brows)
    browsSel = cmds.ls(sl=1)
    
    nudgeShape(Shape,cheeks) 
    cheeksSel = cmds.ls(sl=1)  
     
    nudgeShape(Shape,mouth1)
    mouth1Sel = cmds.ls(sl=1)
    
    nudgeShape(Shape,mouth2)
    mouth2Sel = cmds.ls(sl=1)
    
    nudgeShape(Shape,mouth3)
    mouth3Sel = cmds.ls(sl=1)

    YnudgeValue = widthY+widthY/2
    cmds.select(mouth2Sel)
    cmds.xform(r=1,t=[0,YnudgeValue,0] )
    cmds.select(mouth1Sel)
    cmds.xform(r=1,t=[0,YnudgeValue*2,0] )    
    cmds.select(cheeksSel)
    cmds.xform(r=1,t=[0,YnudgeValue*3,0] )
    cmds.select(browsSel)
    cmds.xform(r=1,t=[0,YnudgeValue*4,0] )
    
    mouthGrouped = cmds.group(mouth1Sel,mouth2Sel,mouth3Sel,n='Mouth_BLENDS_GRP')
    cmds.group(browsSel,cheeksSel,mouthGrouped,n='BLENDSHAPES_GRP')
    cmds.addAttr('BLENDSHAPES_GRP', sn='basemesh',nn = 'BaseMesh', dt = "string" )
    cmds.setAttr('BLENDSHAPES_GRP.basemesh',Shape,  type = "string",  )


#mirrorBlend

def mirrorBlendShape(baseShape, selectedBlend):
    for i in selectedBlend:
        if 'Right' in i:
            flipName = i.replace('Right','Left')
        else:
            flipName = i
        if 'Left' in i:
            flipName = i.replace('Left','Right')
        else:
            flipName = i  
        translateMatch = cmds.xform(i, query=True,t=1)
        rotateMatch = cmds.xform(i, query=True,ro=1)
        scaleMatch = cmds.xform(i, query=True,s=1)    
        cmds.duplicate(baseShape,name='wrap_DELETE')
        cmds.duplicate(baseShape,name='blend_DELETE')
        cmds.duplicate(i,name='sourceBlend_DELETE')
        cmds.select('wrap_DELETE','blend_DELETE','sourceBlend_DELETE')
        cmds.xform(t=[0,0,0],scale = [1,1,1])
        cmds.blendShape('sourceBlend_DELETE','blend_DELETE')
        cmds.blendShape('blend_DELETE','wrap_DELETE')
        cmds.xform('blend_DELETE',s=[-1,1,1] )
        cmds.select('wrap_DELETE','blend_DELETE')
        mel.eval('CreateWrap;')
        cmds.blendShape( 'blend_DELETE', edit=True, w=[(0, 1)] )
        flippedBlend = cmds.duplicate('wrap_DELETE', n=flipName)
        cmds.xform(flippedBlend,t=translateMatch,ro=rotateMatch,s=scaleMatch)
        cmds.delete('wrap_DELETE','sourceBlend_DELETE','blend_DELETE')
        objectSize = cmds.xform(flippedBlend,query=True,bb=1)
        widthX = objectSize[3] - objectSize[0]
        XnudgeValue = widthX+widthX/4
        cmds.xform(flippedBlend,r=1,t=[-XnudgeValue,0,0] )
    
def setBaseMesh(sel):
    cmds.textField('BaseShapeField', edit = True, tx = sel[0])


#mirrorBlendShape(cmds.ls(sl=1))
#createShapes('HEAD',brows,cheeks,mouth1,mouth2,mouth3)


versionNumber = 'v1.0'
if cmds.window('jsBlendTools',exists=True):
    cmds.deleteUI('jsBlendTools')

window = cmds.window('jsBlendTools',menuBar=True, title= 'jsBlendTools %s' %(versionNumber) , w=330, h=100) #, s = False

#cmds.menu( label='Primary Tools', tearOff=True )
#cmds.menuItem( label='Set Selected as Base Mesh:' , c = 'setBaseMesh(cmds.ls(sl=1))')
#cmds.menuItem( divider=True )
#cmds.menuItem( label='Build Blend Shape Layout:' , c = "createShapes(cmds.textField('BaseShapeField', query = True, tx= True),brows,cheeks,mouth1,mouth2,mouth3)" )
#cmds.menuItem( label='Mirror Selected Shape:' , c = "mirrorBlendShape(cmds.textField('BaseShapeField', query = True, tx= True),cmds.ls(sl=1) )")

cmds.columnLayout(adj=1)
tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)

child1 = cmds.columnLayout(adj=1)

cmds.frameLayout(label = "Select Base Mesh:", borderStyle = "etchedIn")
cmds.columnLayout(adj=1)
cmds.textField('BaseShapeField', ed=0,h=25,pht="Base Mesh")
cmds.button(label = 'Set Selected as Base Mesh:',h=30, c='setBaseMesh(cmds.ls(sl=1))' )
cmds.setParent('..')
cmds.setParent('..')


dualButtonHeight = 55
cmds.frameLayout(label = "BlendShape Tools:", borderStyle = "etchedIn")
cmds.columnLayout(adj=1)
cmds.button(label = 'Build BlendShape Layout:',h=dualButtonHeight,  c = "createShapes(cmds.textField('BaseShapeField', query = True, tx= True),brows,cheeks,mouth1,mouth2,mouth3)" )
cmds.button(label = 'Mirror Selected Shape:',h=dualButtonHeight, c = "mirrorBlendShape(cmds.textField('BaseShapeField', query = True, tx= True),cmds.ls(sl=1) )" )
cmds.setParent('..')
cmds.setParent('..')

if len(cmds.ls('BLENDSHAPES_GRP')) > 0:
    test = cmds.attributeQuery('basemesh', node = 'BLENDSHAPES_GRP', ex=True)
    if test ==True:
        PreSet = cmds.getAttr('BLENDSHAPES_GRP.basemesh')
    else:
        PreSet = ''
else:
    PreSet = ''
cmds.textField('BaseShapeField', edit= True, tx= PreSet)
print PreSet



cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'jsBlendTools:') ) )
cmds.showWindow( window )
cmds.window('jsBlendTools', edit=True, widthHeight=[330,248], s = False)
