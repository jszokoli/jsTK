import maya.cmds as cmds

###########################
###js_aiAreaProxyPreview###
###########################

#Author: Joseph Szokoli
#Website: cargocollective.com/josephSzokoli

#Help: 
#To create a shelf icon, move js_aiShaderBlend.py to your scripts folder and assign the following command to the shelf.
#import js_aiAreaProxyPreview
#reload(js_aiAreaProxyPreview)


### ChangeLog: ################################################################################

###v1.0 Initial

##### End ChangeLog #####


def deleteProxyNodes(args=None):
    searchNodes = cmds.ls('*MAYA_PROXY*', r=1)
    proxyNodes = []
    for node in searchNodes:
        try:
            if cmds.getAttr(node+'.ProxyNode') == 1:
                proxyNodes.append(node)
        except:
            pass
    cmds.delete(proxyNodes)

def createProxyLight(args=None):
    sel = cmds.ls(sl=1)
    aiLights = []
    for i in sel:
        shapes = cmds.listRelatives(i, s=1) or []
        for shape in shapes:
            if len(cmds.ls(shape, type='aiAreaLight')) > 0:
                aiLights.append(i)
    
    for aiLight in aiLights:
        
        mayaLight = cmds.shadingNode('areaLight', asLight=1)
        
        point = cmds.pointConstraint(aiLight,mayaLight,mo=0)
        orient = cmds.orientConstraint(aiLight,mayaLight,mo=0)
        scale = cmds.scaleConstraint(aiLight,mayaLight,mo=0)
        
        
        toggle = ['.aiCastShadows', '.emitDiffuse', '.emitSpecular','.aiCastVolumetricShadows','.aiAffectVolumetrics']
        for togs in toggle:
            cmds.setAttr(mayaLight+togs, 0)
        cmds.setAttr(mayaLight+'.decayRate', 2)
        
        BUILD = cmds.shadingNode('multiplyDivide', asUtility=1, n = aiLight+'_MAYA_PROXY_Mult_POWER')
        RESULT = cmds.shadingNode('multiplyDivide', asUtility=1, n = aiLight+'_MAYA_PROXY_Mult_RESULT')
        cmds.setAttr(BUILD+'.operation', 3)
        
        cmds.setAttr(BUILD+'.input1Y',2)
        cmds.connectAttr(aiLight+'.aiExposure',BUILD+'.input2Y')
        
        cmds.connectAttr(BUILD+'.outputY', RESULT+'.input2X')
        
        cmds.connectAttr(aiLight+'.intensity',RESULT+'.input1X')
        
        cmds.connectAttr(RESULT+'.outputX', mayaLight+'.intensity')
        cmds.setAttr(mayaLight+'.lodVisibility',0)
        
        cmds.delete(point)
        cmds.delete(orient)   
        cmds.delete(scale)      
        cmds.parent(mayaLight,aiLight)
        allCreated = [BUILD, RESULT, mayaLight]
        for node in allCreated:
            cmds.addAttr(node, sn='ProxyNode', at="float")
            cmds.setAttr(node+'.ProxyNode', 1)
            
        cmds.sets( mayaLight, rm='defaultLightSet' )
        cmds.rename(mayaLight,aiLight+'_MAYA_PROXY')


def buildProxyLightUI(args=None):
    if cmds.window('aiAreaLightProxy',exists=True):
        cmds.deleteUI('aiAreaLightProxy')
    
    window = cmds.window('aiAreaLightProxy',menuBar=True, title= 'aiAreaLightProxy' , w=330, h=100) #, s = False
    
    
    cmds.columnLayout(adj=1)
    
    cmds.frameLayout(label = 'aiAreaLight Light Proxies')
    cmds.columnLayout(adj=1)
    buttH=35
    addProxyButt = cmds.button(h=buttH,l='Add Proxy to Selected Light:',c=createProxyLight)
    cmds.button(h=buttH,l='Delete Proxy Nodes:',c=deleteProxyNodes)
        
    cmds.showWindow( window )
    cmds.window('aiAreaLightProxy', edit=True, widthHeight=[200, 100], s = False)#409
    #cmds.window('wrinkleCenter', query=True, widthHeight=True)
buildProxyLightUI()
