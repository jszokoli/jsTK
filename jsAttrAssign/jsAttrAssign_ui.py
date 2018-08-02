import maya.cmds as cmds
from functools import partial

from . import attrAssign
from . import settings


class JsAttrAssign_ui(object):

    def __init__(self):
        print 'Initialized JsAttrAssign_ui'
        self.ata = attrAssign.AttrAssigner()


    def applyAttr(self, args=None):
        attr= cmds.textField('attrName',query =1,tx=1)
        val= cmds.textField('attrValue',query =1,tx=1)
        if len(cmds.ls(sl=1)) > 0:
            self.ata.attrAssign(attr,val)

    def getName(self, name,*args):
        cmds.textField('attrName',edit=True,tx=name)

    def finalSelect(self, args=None):
        choosenAttr = cmds.textScrollList('commonSelector',query=1, si = True )
        if choosenAttr == None:
            pass
        else:
            choosenAttr = choosenAttr[0]
            cmds.textField('attrName',edit=True,tx=choosenAttr)
            cmds.deleteUI('ChooserForm')
            cmds.window('JS_attrLoop', edit=True, widthHeight=[331L,49L], s = False)
        
    def cancelSelect(self, args=None):
        cmds.deleteUI('ChooserForm')
        cmds.window('JS_attrLoop', edit=True, widthHeight=[331L,49L], s = False)



    def listCommonUI(self, args=None):
        cmds.window('JS_attrLoop', edit=True, widthHeight=[331L, 270L], s = False)
        if cmds.columnLayout('ChooserForm', exists= True):
            cmds.deleteUI('ChooserForm')
            
        cmds.columnLayout('ChooserForm', parent= 'multiPickerForm',adj=1)
        
        cmds.columnLayout('innerForm', parent= 'ChooserForm',adj=1)
        cmds.textScrollList('commonSelector', parent = 'ChooserForm', dkc = self.finalSelect )
        cmds.setParent('..')
        
        cmds.flowLayout()
        cmds.button('apply',l='Pick Attribute', c=self.finalSelect, w=250)
        cmds.button('cancel',l='Cancel', c=self.cancelSelect, w=73)
        
        cmds.setParent('..')
        
        cmds.setParent('..')
        
        commonAttrs = self.ata.commonAttrFunc()
        if commonAttrs == None:
            cmds.textScrollList('commonSelector', edit = True,append = 'Select an Object to list available attributes.')
        else:
            commonAttrs = sorted( self.ata.commonAttrFunc() )
            cmds.textScrollList('commonSelector', edit = True,append = commonAttrs)
        

    def jsAttrPrimeUI(self, args=None):

        if cmds.window('JS_attrLoop', exists=True):
            cmds.deleteUI('JS_attrLoop')
        
        #WINDOW START
        cmds.window('JS_attrLoop', title= 'jsAttrAssign %s' %(settings.versionNumber) )
        
        cmds.columnLayout('COLMaster', adjustableColumn=True, cal = 'left' )
        
        MasterFrame = cmds.frameLayout('frameMaster',l='| Attribute Name:                              | Value:')


        cmds.flowLayout()
        cmds.textField('attrName',w=175,h=25)
        commonAttrBtn = cmds.nodeIconButton('commonAttrBtn', style='iconOnly', image1='popupMenuIcon.png', c=self.listCommonUI )
        
        
        cmds.textField('attrValue', w=75,h=25)
        cmds.button(l='Apply',w=63,h=25, c=self.applyAttr)

        cmds.setParent('..')
        cmds.setParent('..')
        
        cmds.columnLayout('multiPickerForm', adjustableColumn=True, cal = 'left' )
        cmds.setParent('..')
        
        cmds.showWindow( 'JS_attrLoop' )
        cmds.window('JS_attrLoop', edit=True, widthHeight=[331L,49L], s = False)
        cmds.window('JS_attrLoop', query=True, widthHeight=True)

def launch_ui():
    uiObject = JsAttrAssign_ui()
    uiObject.jsAttrPrimeUI()