import maya.cmds as cmds

####################
###jsAttrAssign#####
####################

#Author: Joseph Szokoli
#Website: cargocollective.com/josephSzokoli

#Help:
#To create a shelf icon, move jsRenamer.py to your scripts folder and assign the following command to the shelf.
#import jsAttrAssign
#reload(jsAttrAssign)

#Version Number################
versionNumberAttr = 'v1.0.0'###
###############################

### ChangeLog: ################################################################################
###v1.0 Initial 





def commonAttrFunc(args=None):
    sel = cmds.ls(sl=1)
    selShapes = []
    #Convert Selection to shapes
    if sel != []:
        for obj in sel:
            shape = cmds.listRelatives(obj,s=1)
            selShapes.append(shape)
        
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



def applyAttr(args=None):
    attr= cmds.textField('attrName',query =1,tx=1)
    val= cmds.textField('attrValue',query =1,tx=1)
    if len(cmds.ls(sl=1)) > 0:
        attrAssign(attr,val)


def attrAssign(attr,val):
    sel = cmds.ls(sl=1)
    for i in sel:
        shape = cmds.listRelatives(i,s=1)[0]
        val = float(val)
        cmds.setAttr(shape+'.'+attr,val)

def getName(name,*args):
    cmds.textField('attrName',edit=True,tx=name)


def finalSelect(args=None):
    choosenAttr = cmds.textScrollList('commonSelector',query=1, si = True )
    if choosenAttr == None:
        pass
    else:
        choosenAttr = choosenAttr[0]
        cmds.textField('attrName',edit=True,tx=choosenAttr)
        cmds.deleteUI('ChooserForm')
        cmds.window('JS_attrLoop', edit=True, widthHeight=[331L,49L], s = False)
    
def cancelSelect(args=None):
    cmds.deleteUI('ChooserForm')
    cmds.window('JS_attrLoop', edit=True, widthHeight=[331L,49L], s = False)



def listCommonUI(args=None):
    cmds.window('JS_attrLoop', edit=True, widthHeight=[331L, 270L], s = False)
    if cmds.columnLayout('ChooserForm', exists= True):
        cmds.deleteUI('ChooserForm')
        
    cmds.columnLayout('ChooserForm', parent= 'multiPickerForm',adj=1)
    
    cmds.columnLayout('innerForm', parent= 'ChooserForm',adj=1)
    cmds.textScrollList('commonSelector', parent = 'ChooserForm', dkc = finalSelect )
    cmds.setParent('..')
    
    cmds.flowLayout()
    cmds.button('apply',l='Pick Attribute', c=finalSelect, w=250)
    cmds.button('cancel',l='Cancel', c=cancelSelect, w=73)
    '''
    cmds.button('apply', parent = 'ChooserForm',l='Pick Attribute', c="finalSelect()")
    cmds.button('cancel', parent = 'ChooserForm',l='Cancel', c="cancelSelect()")
    '''
    
    cmds.setParent('..')
    
    cmds.setParent('..')
    
    commonAttrs = commonAttrFunc()
    if commonAttrs == None:
        cmds.textScrollList('commonSelector', edit = True,append = 'Select an Object to list available attributes.')
    else:
        commonAttrs = sorted( commonAttrFunc() )
        cmds.textScrollList('commonSelector', edit = True,append = commonAttrs)
    

def buildPrimeUI(args=None):

    if cmds.window('JS_attrLoop', exists=True):
        cmds.deleteUI('JS_attrLoop')
    
    #WINDOW START
    cmds.window('JS_attrLoop', title= 'jsAttrAssign %s' %(versionNumberAttr) )
    
    cmds.columnLayout('COLMaster', adjustableColumn=True, cal = 'left' )
    
    MasterFrame = cmds.frameLayout('frameMaster',l='| Attribute Name:                              | Value:')


    cmds.flowLayout()
    cmds.textField('attrName',w=175,h=25)
    commonAttrBtn = cmds.nodeIconButton('commonAttrBtn', style='iconOnly', image1='popupMenuIcon.png', c=listCommonUI )
    
    
    cmds.textField('attrValue', w=75,h=25)
    cmds.button(l='Apply',w=63,h=25, c=applyAttr)

    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.columnLayout('multiPickerForm', adjustableColumn=True, cal = 'left' )
    cmds.setParent('..')
    
    cmds.showWindow( 'JS_attrLoop' )
    cmds.window('JS_attrLoop', edit=True, widthHeight=[331L,49L], s = False)
    cmds.window('JS_attrLoop', query=True, widthHeight=True)
    

buildPrimeUI()


