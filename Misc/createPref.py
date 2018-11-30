'''
import maya.cmds as cmds

def attachPRef(connect=True):
    connectList=[]
    for refObj in cmds.ls('*_REFERENCE',r=True):
        renderObj=refObj.replace('_REFERENCE','')
        try:
            refObjShape=cmds.listRelatives(refObj,s=True)[0]
            renderObjShape=cmds.listRelatives(renderObj,s=True)[0]

            if connect==True:
                if not cmds.isConnected(refObjShape+'.message',renderObjShape+'.referenceObject'):
                    cmds.connectAttr(refObjShape+'.message',renderObjShape+'.referenceObject')
                    connectList.append(renderObj)
                else:
                    cmds.warning(refObj+' is already connected as reference to '+renderObj)

            if connect==False:
                if cmds.isConnected(refObjShape+'.message',renderObjShape+'.referenceObject'):
                    cmds.disconnectAttr(refObjShape+'.message',renderObjShape+'.referenceObject')
                    connectList.append(renderObj)
        except:
            pass

    if connect==True:
        print 'The following objects were connected to their reference:'
    if connect==False:
        print 'The following objects were disconnected from their reference:'
    for x in connectList:
        print ' '+x

attachPRef()
'''

import maya.cmds as cmds

def createPref(connect=True):
    sel = cmds.ls(sl=True)
    for renderObj in sel:
        print renderObj
        renderShape=cmds.listRelatives(renderObj,s=True)[0]
        refObj = cmds.duplicate(renderObj,n=renderObj+'_REFERENCE')[0]
        refShape=cmds.listRelatives(refObj,s=True)[0]
        cmds.setAttr(refObj+'.v',False)
        print refObj
        print refShape
        cmds.connectAttr(refShape+'.message',renderShape+'.referenceObject')
        print renderObj+' pref connection made to '+refObj

    sel2 = cmds.ls('*_REFERENCE')
    cmds.group(sel2,n='reference_GRP')



createPref()