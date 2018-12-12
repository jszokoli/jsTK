import maya.cmds as cmds
from pymel.all import *
############################
###js_aiAOV_Editor v1.0#####
############################

#By Joseph Szokoli
#sites.google.com/view/josephszokoli/
#Help: 
#To create shelf icon paste js_aiAOV_Editor.py to your scripts folder and assign the following command to the shelf
#import js_aiAOV_Editor
#reload(js_aiAOV_Editor)


def aov_buildAovDict(args=None):
    sel = cmds.ls(type='aiAOV')
    allAovDict = {}
    for i in sel:
        currentAovDict = {}
        aovName = cmds.getAttr(i+'.name')
        aovType = cmds.getAttr(i+'.aovt')
        aovEnable = cmds.getAttr(i+'.aoven')

        currentAovDict['name'] = aovName
        #currentAovDict['aovt'] = aovType
        currentAovDict['aoven'] = aovEnable
        allAovDict[i] = currentAovDict
    return allAovDict

#buildAovDict()

def aov_enable(args=None):
    selectedFromList = cmds.textScrollList('AOVoperatorList',query=True,selectItem=True) or []

    for aovNode in selectedFromList:
        checkBoxBool = cmds.checkBox(aovNode+'_checkBox', edit=True, value=True)
        cmds.setAttr(aovNode+'.aoven',1)

def aov_disable(args=None):
    selectedFromList = cmds.textScrollList('AOVoperatorList',query=True,selectItem=True) or []
    for aovNode in selectedFromList:
        checkBoxBool = cmds.checkBox(aovNode+'_checkBox', edit=True, value=False)
        cmds.setAttr(aovNode+'.aoven',0)

def aov_enableToggle(aovNode):
    checkBoxBool = cmds.checkBox(aovNode+'_checkBox', query=True, value=True)
    cmds.setAttr(aovNode+'.aoven',checkBoxBool)



def aov_add2List(aovNode):
    currentInList = cmds.textScrollList('AOVoperatorList',query=True,allItems=True) or []
    if aovNode not in currentInList:
        cmds.textScrollList('AOVoperatorList',edit=True,append=aovNode)
    else:
        cmds.warning(aovNode+' currently in list.')

def aov_addAll2List(aovNodes):
    for aovNode in aovNodes:
        currentInList = cmds.textScrollList('AOVoperatorList',query=True,allItems=True) or []
        if aovNode not in currentInList:
            cmds.textScrollList('AOVoperatorList',edit=True,append=aovNode)
        else:
            cmds.warning(aovNode+' currently in list.')



def aov_clearList(args=None):
    cmds.textScrollList('AOVoperatorList',edit=True,removeAll=True)

def aov_clearSelected(args=None):
    selectedFromList = cmds.textScrollList('AOVoperatorList',query=True,selectItem=True) or []
    for node in selectedFromList:
        cmds.textScrollList('AOVoperatorList',edit=True,removeItem=node)


def aov_SoloSelect(aovNode):
    cmds.select(aovNode)

def aov_deleteSelected(args=None):
    selectedFromList = cmds.textScrollList('AOVoperatorList',query=True,selectItem=True) or []
    for aovNode in selectedFromList:
        cmds.textScrollList('AOVoperatorList',edit=True,removeItem=aovNode)
        try:
            cmds.delete(aovNode)  
        except:
            cmds.error('Could not delete '+aovNode)
        try:
            cmds.deleteUI(aovNode+'ColLay')
        except:
            pass


def aov_deleteAll(args=None):
    selectedFromList = cmds.textScrollList('AOVoperatorList',query=True,allItems=True) or []
    cmds.textScrollList('AOVoperatorList',edit=True,removeAll=True)
    for aovNode in selectedFromList:
        try:
            cmds.delete(aovNode)           
        except:
            cmds.error('Could not delete '+aovNode)
        try:
            cmds.deleteUI(aovNode+'ColLay')
        except:
            pass

#cmds.deleteUI('aiAOV_test'+'flowLay')

def aov_deleteDuplicates(args=None):
    selectedFromList = cmds.textScrollList('AOVoperatorList',query=True,allItems=True) or []
    duplicateChecker =[]
    correctAovNodes = []
    duplicateAovNodes = []

    for aovNode in selectedFromList:
        aovName = cmds.getAttr(aovNode+'.name')
        if aovName not in duplicateChecker:
            duplicateChecker.append(aovName)
            correctAovNodes.append(aovNode)
        else:
            duplicateAovNodes.append(aovNode)
    # print duplicateChecker
    # print correctAovNodes
    # print duplicateAovNodes
    for node in duplicateAovNodes:
        print node
        try:
            cmds.delete(node)
        except:
            pass
        try:
            cmds.deleteUI(aovNode+'ColLay')
        except:
            pass

def ui_refreshAOV(allAovDict):
    aovDict = aov_buildAovDict()
    #print allAovDict
    cmds.textScrollList('AOVoperatorList',edit=True,removeAll=True)
    
    for node, descriptionDict in sorted(allAovDict.iteritems(), key=lambda (k,v): (v,k)):
        try:
            cmds.deleteUI(node+'ColLay')
        except:
            pass
    
    lightGrey = .17
    
    for node, descriptionDict in sorted(aovDict.iteritems(), key=lambda (k,v): (v,k)):
        cmds.columnLayout(node+'ColLay',parent = 'AOVparentScroll')
        cmds.flowLayout(node+'flowLay',w=490,h=20)
        cmds.checkBox(node+'_checkBox',l='Enable AOV',value=descriptionDict['aoven'],changeCommand=Callback(aov_enableToggle,node) )
        cmds.textField(text=descriptionDict['name'],w=150,ed=0,bgc=[lightGrey,lightGrey,lightGrey])
        cmds.textField(text=node,w=200,ed=0,bgc=[lightGrey,lightGrey,lightGrey])
        cmds.button('+',w=25, command=Callback(aov_add2List,node))
        cmds.button('Sel ',w=25, command=Callback(aov_SoloSelect,node) ) 
        cmds.setParent('..')
        cmds.separator(node+'Separator')
        cmds.setParent('..')
    


def ui_deleteAOV(allAovDict):
    #If window exists delete 
    if cmds.window('DeleteAOV', exists=True):
        cmds.deleteUI('DeleteAOV')

    #Create Initial Window
    mainWindow = cmds.window('DeleteAOV', title= 'js_aiAOV_BatchEditor')

    cmds.flowLayout()


    cmds.frameLayout('Operator List',w=215)
    cmds.columnLayout()
    cmds.textScrollList('AOVoperatorList', numberOfRows=20, allowMultiSelection=True,showIndexedItem=4,h=337 ,w=210)

    cmds.gridLayout( numberOfColumns=2, cellWidthHeight=(105, 25) )

    cmds.button('Enable Selected',command= aov_enable)
    cmds.button('Disable Selected',command= aov_disable)

    cmds.button('Remove from List', command = aov_clearSelected)
    cmds.button('Delete Selected',command = aov_deleteSelected)

    cmds.button('Clear List',command = aov_clearList )
    cmds.button('Delete All',command = aov_deleteAll )
    cmds.button('Delete Duplicates',command = aov_deleteDuplicates)
    cmds.button('Refresh',command= Callback(ui_refreshAOV, allAovDict) )

    cmds.setParent('..')


    cmds.setParent('..')
    cmds.setParent('..')
    allList = []
    for node, descriptionDict in sorted(allAovDict.iteritems(), key=lambda (k,v): (v,k)):
        allList.append(node)
    cmds.frameLayout('Current AOVs',w=515,h=462L)
    darkGrey = .1
    cmds.flowLayout(w=500,h=20)
    cmds.textField(text='AOV Status',w=87,ed=0,bgc=[darkGrey,darkGrey,darkGrey])
    cmds.textField(text='AOV Name',w=150,ed=0,bgc=[darkGrey,darkGrey,darkGrey])
    cmds.textField(text='AOV Node',w=200,ed=0,bgc=[darkGrey,darkGrey,darkGrey])

    cmds.button('Add All',w=74,command=Callback(aov_addAll2List,allList))

    cmds.setParent('..')
    
    cmds.scrollLayout('AOVparentScroll')
    #cmds.columnLayout(w=1000)
    lightGrey = .17
    for node, descriptionDict in sorted(allAovDict.iteritems(), key=lambda (k,v): (v,k)):
        cmds.columnLayout(node+'ColLay')
        cmds.flowLayout(node+'flowLay',w=490,h=20)
        cmds.checkBox(node+'_checkBox',l='Enable AOV',value=descriptionDict['aoven'],changeCommand=Callback(aov_enableToggle,node) )
        cmds.textField(text=descriptionDict['name'],w=150,ed=0,bgc=[lightGrey,lightGrey,lightGrey])
        cmds.textField(text=node,w=200,ed=0,bgc=[lightGrey,lightGrey,lightGrey])
        cmds.button('+',w=25, command=Callback(aov_add2List,node))
        cmds.button('Sel ',w=25, command=Callback(aov_SoloSelect,node) ) 
        cmds.setParent('..')
        cmds.separator(node+'Separator')
        cmds.setParent('..')

    cmds.setParent('..')

    cmds.setParent('..')
    cmds.showWindow( 'DeleteAOV' )
    cmds.window('DeleteAOV', edit=True, s = False, widthHeight=[732L, 462L])
    #cmds.window('DeleteAOV', query=True, widthHeight=True)

ui_deleteAOV( aov_buildAovDict() )

#print cmds.window('DeleteAOV', query=True, widthHeight=True)
