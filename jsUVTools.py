import maya.mel as mel
import maya.cmds as cmds
####################
#jsUVTools v1.1#####
####################

#Author: Joseph Szokoli
#Website: cargocollective.com/josephSzokoli

#Help: 
#To create a shelf icon, move jsRenamer.py to your scripts folder and assign the following command to the shelf.
#import jsUVTools
#reload(jsUVTools)

#Version Number################
versionNumberUV = 'v1.1'###
###############################

### ChangeLog: ################################################################################
###v1.1 Added Horizontal Vertical Order Switch

###v1.0 Initial Release
def repitionUnfold(Args=None):
    repeatUnfold = cmds.intSliderGrp('unfoldRepeatSlider', query = True, value = True)
    for num in range (0,repeatUnfold):
        cmds.unfold( i = 5000, ss = 0.001, gb = 0, gmb = 0.5, pub = 0,  ps = 0, oa = 1, us = False)
        cmds.unfold( i = 5000, ss = 0.001, gb = 0, gmb = 0.5, pub = 0,  ps = 0, oa = 2, us = False)

def repitionUnfoldHV(Args=None):
    repeatUnfold = cmds.intSliderGrp('unfoldRepeatSlider', query = True, value = True)
    for num in range (0,repeatUnfold):   
        cmds.unfold( i = 5000, ss = 0.001, gb = 0, gmb = 0.5, pub = 0,  ps = 0, oa = 2, us = False)
        cmds.unfold( i = 5000, ss = 0.001, gb = 0, gmb = 0.5, pub = 0,  ps = 0, oa = 1, us = False)

def repitionUnfoldVH(Args=None):
    repeatUnfold = cmds.intSliderGrp('unfoldRepeatSlider', query = True, value = True)
    for num in range (0,repeatUnfold):
        cmds.unfold( i = 5000, ss = 0.001, gb = 0, gmb = 0.5, pub = 0,  ps = 0, oa = 1, us = False)
        cmds.unfold( i = 5000, ss = 0.001, gb = 0, gmb = 0.5, pub = 0,  ps = 0, oa = 2, us = False)


def tubeUnfold(args=None):
    edgeSel = cmds.ls(sl=1)
    objName = edgeSel[0].split('.e')
    cmds.select(objName[0])
    cmds.polyForceUV( uni=True )
    cmds.select(edgeSel)
    mel.eval('invertSelection')
    cmds.polyMapSewMove(nf = 10, lps = 0 , ch = 1)
    cmds.polyLayoutUV(fr = 1, l = 2, sc = 1)
#    for num in range(1,10):
#        cmds.unfold( i = 5000, ss = 0.001, gb = 0, gmb = 0.5, pub = 0,  ps = 0, oa = 1, us = False)
#        cmds.unfold( i = 5000, ss = 0.001, gb = 0, gmb = 0.5, pub = 0,  ps = 0, oa = 2, us = False)
    cmds.polyLayoutUV(fr = 1, l = 2, sc = 1)
    cmds.select(objName[0])

def flipAllUV(args=None):
    sel = cmds.ls(sl=1)
    for each in sel:
        cmds.polyFlipUV(each, flipType = 0, local = False )
    mel.eval('PolySelectConvert(4)')
    cmds.polyEditUV( relative=True, uValue=1)
    cmds.select(sel)

def face2Edge(args=None):
    cmds.select(cmds.polyListComponentConversion( ff=True, te=True, bo=True),r = True)

def nudgeUp(args=None):
    value = cmds.floatField('nudgeField',query = True,value=True )
    sel =cmds.ls(sl=1)
    for each in sel:
        try:
            cmds.select(each)
            mel.eval('PolySelectConvert(4)') 
            cmds.polyEditUV( relative=True, vValue=value)
            cmds.select(each)
        except:
            pass
    cmds.select(sel)
    
def nudgeDown(args=None):
    value = cmds.floatField('nudgeField',query = True,value=True )
    sel =cmds.ls(sl=1)
    for each in sel:
        try:
            cmds.select(each)
            mel.eval('PolySelectConvert(4)') 
            cmds.polyEditUV( relative=True, vValue=-value)
            cmds.select(each)
        except:
            pass
    cmds.select(sel)

def nudgeRight(args=None):
    value = cmds.floatField('nudgeField',query = True,value=True )
    sel =cmds.ls(sl=1)
    for each in sel:
        try:
            cmds.select(each)
            mel.eval('PolySelectConvert(4)') 
            cmds.polyEditUV( relative=True, uValue=value)
            cmds.select(each)
        except:
            pass
    cmds.select(sel)

def nudgeLeft(args=None):
    value = cmds.floatField('nudgeField',query = True,value=True )
    sel =cmds.ls(sl=1)
    for each in sel:
        try:
            cmds.select(each)
            mel.eval('PolySelectConvert(4)') 
            cmds.polyEditUV( relative=True, uValue=-value)
            cmds.select(each)
        except:
            pass
    cmds.select(sel)



def closeUV(args=None):
    cmds.window('jsUV', edit=True, widthHeight=[300,25], s = False)      

    
def expandUV(args=None):
    cmds.window('jsUV', edit=True, widthHeight=[300,140], s = False)   

if cmds.window('jsUV', exists=True):
    cmds.deleteUI('jsUV')

cmds.window('jsUV', title= 'jsUVTools '+versionNumberUV)

cmds.frameLayout(label = "jsUVTools:", borderStyle = "etchedIn",cll=1,cc=closeUV, ec = expandUV)

cmds.columnLayout( adjustableColumn=True, cal = 'left' )

cmds.rowLayout( nc=2, adjustableColumn=2, columnAlign=(1, 'left'), w= 300 )
cmds.text('Unfold Reptitions: ')
cmds.intSliderGrp('unfoldRepeatSlider', field=True, minValue=1, maxValue=10, v =1,cal = [1,'left'] )
cmds.setParent('..')

#cmds.rowLayout( nc=2, adjustableColumn=2, columnAlign=(1, 'left'), w= 300 )
cmds.flowLayout()
'''
cmds.iconTextButton(label = 'Unfold HV:',
image = 'textureEditorUnfoldUVsLarge.png',
style =  "iconAndTextHorizontal",
fla = 0,
mh = 20, mw = 50,
c=repitionUnfoldHV,
w=147 )

cmds.iconTextButton(label = 'Unfold VH:',
image = 'textureEditorUnfoldUVsLarge.png',
style =  "iconAndTextHorizontal",
fla = 0,
mh = 20, mw = 50,
c=repitionUnfoldVH,w=147 )
'''
cmds.button(label = 'Unfold HV:',
c=repitionUnfoldHV,
w=147 )

cmds.button(label = 'Unfold VH:',
c=repitionUnfoldVH,w=147 )


cmds.setParent('..')


cmds.separator( height=5, style='in' )
cmds.flowLayout()

cmds.button(label = 'Flip UV:',
c=flipAllUV )

cmds.button(label = 'Tube Unfold:',
c=tubeUnfold )

cmds.button(label = 'Face to Edge:',
c=face2Edge )


cmds.setParent('..')

cmds.separator( height=5, style='in' )
cmds.gridLayout( numberOfColumns=2, cellWidthHeight=(150, 37) )

cmds.rowLayout( nc=2, adjustableColumn=2, columnAlign=(1, 'left'), w= 300 )
cmds.text('UV Nudge Value: ')
cmds.floatField('nudgeField',precision=4, step=.01, v=1 )
cmds.setParent('..')

cmds.gridLayout( numberOfColumns=4, cellWidthHeight=(36, 36) )
cmds.iconTextButton(image = 'arrowUp.png', style =  "iconOnly", fla = 0,c=nudgeUp)
cmds.iconTextButton(image = 'arrowDown.png', style =  "iconOnly", fla = 0,c=nudgeDown)
cmds.iconTextButton(image = 'arrowLeft.png', style =  "iconOnly", fla = 0,c=nudgeLeft)
cmds.iconTextButton(image = 'arrowRight.png', style =  "iconOnly", fla = 0,c=nudgeRight)

cmds.setParent('..')
cmds.setParent('..')
cmds.separator( height=5, style='in' )
cmds.setParent('..')
cmds.setParent('..')
cmds.setParent('..')
cmds.showWindow( 'jsUV' )
cmds.window('jsUV', edit=True, widthHeight=[300,140], s = False)
