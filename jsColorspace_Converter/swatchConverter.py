import maya.cmds as cmds
from functools import partial
sys.path.append("/usr/lib64/python2.6/site-packages")
import PyOpenColorIO as ocio


###ACES to sRGB

def Aces2sRGB(R_in,G_in,B_in):
    config = ocio.GetCurrentConfig()
    proccessor = config.getProcessor("ACES - ACEScg", "Utility - Rec.709 - Display")
    
    postVal =  proccessor.applyRGB([R_in,G_in,B_in])
    
    proccessor2 = config.getProcessor("Utility - Rec.709 - Camera", "Utility - Linear - sRGB")
    postVal2 =  proccessor2.applyRGB([ postVal[0],postVal[1],postVal[2] ])
    return postVal2


def sRGB2Aces(R_in,G_in,B_in):
    config = ocio.GetCurrentConfig()
    proccessor = config.getProcessor("Utility - Linear - sRGB", "Utility - Rec.709 - Camera")
    
    postVal =  proccessor.applyRGB([R_in,G_in,B_in])
    
    proccessor2 = config.getProcessor("Utility - Rec.709 - Display","ACES - ACEScg")
    postVal2 =  proccessor2.applyRGB([ postVal[0],postVal[1],postVal[2] ])
    return postVal2




def attrList(node):
    vectorList = []
    sel = [node]
    for i in sel:
        attrGet = cmds.listAttr(i,
        output=False)
        for h in attrGet:
            if '.' in h:
                pass
            else:
                if cmds.attributeQuery(h,node=i,at=1) == 'compound':
                    compoundChildren = cmds.attributeQuery(h,node=i,lc=1)
                    numberChildren = cmds.getAttr(i+'.'+h,mi=1)
                    for child in compoundChildren:
                        for x in numberChildren:
                            try:
                                checker1=  cmds.getAttr(i+'.'+h+'['+str(x)+'].'+child)
                                if len(checker1[0]) == 3:
                                    vectorList.append(h+'['+str(x)+'].'+child)
                                else:
                                    pass
                            except:
                                pass
                            
                else:
                    attrType= cmds.attributeQuery(h,node=i,at=1)
                    if attrType == 'float3':
                        vectorList.append(h)
    return vectorList





def attrConverter(node):
    acesDict = {}
    rec709Dict = {}
    vectorAttrs = attrList(node)
    for attr in vectorAttrs:
        currentAttr =  node+'.'+attr
        if cmds.listConnections(node+'.'+attr) == None:
            val = cmds.getAttr(currentAttr)
            R_in = val[0][0]
            G_in = val[0][1]
            B_in = val[0][2]
            if cmds.radioButton('ACES_option', query = True, sl=True) == True:
                convertedVal = Aces2sRGB(R_in,G_in,B_in)
                cmds.setAttr(currentAttr,convertedVal[0],convertedVal[1],convertedVal[2], type="double3")
    
            if cmds.radioButton('rec709_option', query = True, sl=True) == True:
                convertedVal = sRGB2Aces(R_in,G_in,B_in)
                cmds.setAttr(currentAttr,convertedVal[0],convertedVal[1],convertedVal[2], type="double3")
        else:
            pass


def addSelected(args=None):
    sel = cmds.ls(sl=1)
    currentObjects = cmds.textScrollList('objectList',query=True,ai=True) or []
    for i in sel:
        if i in currentObjects:
            pass
        else:
            cmds.textScrollList( "objectList", edit=True, append=[i])


def convertSelected(args=None):
    selectedObjects = cmds.textScrollList('objectList',query=True,si=True) or []
    for i in selectedObjects:
        cmds.textScrollList('objectList',edit=True,ri=i)
        attrConverter(i)
        


def deleteSelected(args=None):
    selectedObjects = cmds.textScrollList('objectList',query=True,si=True)
    for i in selectedObjects:
        cmds.textScrollList('objectList',edit=True,ri=i)
        
def selectObjects(args=None):
    selectedObjects = cmds.textScrollList('objectList',query=True,si=True)
    cmds.select(selectedObjects)


def jsColorspace_Converter_ui(args=None):
    if cmds.window('jsColorspace_Converter_ui', exists=True):
        cmds.deleteUI('jsColorspace_Converter_ui')
    
    cmds.window('jsColorspace_Converter_ui', title= 'jsColorspace_Converter')
    
    cmds.columnLayout('ColMaster',
    adjustableColumn=True,
    cal = 'left',
    parent='jsColorspace_Converter_ui' )
    
    
    cmds.frameLayout('FrameMaster',l='jsColorspace_Converter',parent='ColMaster')

    cmds.flowLayout('Flow2')
    mode = cmds.radioCollection()
    cmds.text( label='Source Colorspace:', align='left' )
    cmds.radioButton('ACES_option', label = 'ACES',sl=1)
    cmds.radioButton('rec709_option', label = 'rec709')
    cmds.setParent('..')
    
    cmds.flowLayout('flow3')
    cmds.columnLayout('col2')
    
    cmds.textScrollList('objectList',
    numberOfRows=32,
    h = 250,
    allowMultiSelection=True,
    deleteKeyCommand=deleteSelected,
    selectCommand = selectObjects)
    
    cmds.setParent('..')
    cmds.columnLayout('col3')
    cmds.button('AddSelected',l='Add \n Selected \n Nodes',h=123,c=addSelected)
    cmds.button('BakeSelected',l='Convert \n Selected \n Nodes',h=123,c=convertSelected)
    
    cmds.setParent( '..' )
    cmds.setParent('..')
    
    cmds.showWindow( 'jsColorspace_Converter_ui' )
    cmds.window('jsColorspace_Converter_ui', edit=True, widthHeight=[322L, 300L], s = True)
    #cmds.window('lookdevManager_SwatchBaker_ui', query=True, widthHeight=True)


jsColorspace_Converter_ui()


