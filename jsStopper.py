import maya.cmds as cmds
from pymel.all import *
######################
###jsStopper v1.0#####
######################

#By Joseph Szokoli
#sites.google.com/view/josephszokoli/
#Help: 
#To create shelf icon paste jsStopper.py to your scripts folder and assign the following command to the shelf
#import jsStopper
#reload(jsStopper)


def exposureStopper(value):
    conversionDict = {
    '-2/3':{'sign':'Negative','cValue':.66},
    '-1/3':{'sign':'Negative','cValue':.33},
    '+1/3':{'sign':'Positive','cValue':.33},
    '+2/3':{'sign':'Positive','cValue':.66},
    
    '-1':{'sign':'Negative','cValue':1},
    '-3/4':{'sign':'Negative','cValue':.75},
    '-1/2':{'sign':'Negative','cValue':.50},
    '-1/4':{'sign':'Negative','cValue':.25},    
    '+1/4':{'sign':'Positive','cValue':.25},
    '+1/2':{'sign':'Positive','cValue':.50},
    '+3/4':{'sign':'Positive','cValue':.75},
    '+1':{'sign':'Positive','cValue':1},
    }
    for origVal, convDict in conversionDict.iteritems():
        if value == origVal:
            gatherLightShapes(convDict['cValue'],convDict['sign'])

def gatherLightShapes(cValue,sign):
    aiLightType = ['aiAreaLight']
    otherTypes = []
    sel = cmds.ls(sl=1)
    for obj in sel:
        nodeTy = cmds.nodeType(obj)
        if nodeTy == 'transform':
            shapeNode = cmds.listRelatives(obj,s=1)[0]
            print shapeNode
            typeCheck = nodeTy = cmds.nodeType(shapeNode)
            print typeCheck
            if typeCheck in aiLightType:
                setExposure(shapeNode,'aiLight',cValue,sign)
            elif typeCheck in otherTypes:
                #tba
                pass

def setExposure(shapeNode,nodeSType,cValue,sign):
    if nodeSType == 'aiLight':
        origExposure = cmds.getAttr(shapeNode+'.aiExposure')
        print origExposure
        if sign == 'Positive':
            newExposure = origExposure+cValue
            cmds.warning( 'Increased Exposure of '+ shapeNode +' from '+ str(origExposure) +' to '+str(newExposure) )
        elif sign == 'Negative':
            newExposure = origExposure-cValue
            cmds.warning( 'Decreased Exposure of '+ shapeNode +' from '+ str(origExposure) +' to '+str(newExposure) )
        cmds.setAttr(shapeNode+'.aiExposure',newExposure)
        
    elif nodeSType == 'other':
        #tba
        pass
        
    
def ui_jsTopper(args=None):
    #If window exists delete 
    if cmds.window('jsTopper_ui', exists=True):
        cmds.deleteUI('jsTopper_ui')

    #Create Initial Window
    mainWindow = cmds.window('jsTopper_ui', title= 'jsTopper')
    gridSize= 30
    numberOfButtons=9
    cmds.gridLayout( numberOfColumns=numberOfButtons, cellWidthHeight=(gridSize, gridSize) )
    negativeButtons = ['-1','-3/4','-1/2','-1/4']
    for but in negativeButtons:
        cmds.button(l=but,command = Callback(exposureStopper,but) )
        
    cmds.iconTextStaticLabel( st='iconOnly', i1='pointlight.png')
    
    positiveButtons = ['+1/4','+1/2','+3/4','+1']
    for but in positiveButtons:
        cmds.button(l=but,command = Callback(exposureStopper,but) )
 
    cmds.setParent('..')
    
    cmds.showWindow( 'jsTopper_ui' )
    cmds.window('jsTopper_ui', edit=True, s = False, widthHeight=[gridSize*numberOfButtons, gridSize])
    #cmds.window('jsTopper_ui', query=True, widthHeight=True)

ui_jsTopper()
