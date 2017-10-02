import maya.cmds as cmds

###########################
###js_aiShaderBlend v2.0###
###########################

#Author: Joseph Szokoli
#Website: cargocollective.com/josephSzokoli

#Help: 
#To create a shelf icon, move js_aiShaderBlend.py to your scripts folder and assign the following command to the shelf.
#import js_aiShaderBlend
#reload(js_aiShaderBlend)

#Version Number################
versionNumberBlend = 'v2.0'####
###############################

### ChangeLog: ################################################################################


# TO FIX
'''
Bump nodes don't get deleted on update blend shader

Add checks for fresnel use IOR and fresnel

Fix blending within namespaces





'''





###v2.0
#Updated to leave two source materials intact and added ability to continue tweaking source materials and update your BLENDED shader
#added Build Attr Library Function for source attr comparisons
#added Update Shader picker/ update selected shader
#added Ability to change names of created/source shaders, BLENDER and color blends update naming when updated
#Added update Blended Material to match attrs that are the same across both source shaders(connections, and values)
#Removed Blender Color Quick Edit
#Added Blend Color Containers



###v1.0 Initial
#changed to cmds.shadingNode from createNode
#Added BlendColor Quick Edit with cc dc tweak
#Added Bump Blend Support

##### End ChangeLog #####


### Template Attributes List ###
triple = ['.color', '.KsColor','.opacity', '.KtColor', '.KsssColor','.sssRadius','.KrColor', '.transmittance', '.opacity' , '.refractionExitColor', '.aiMatteColor', '.emissionColor'  ]
singleCheck = ['.Kd','.Kb','.diffuseRoughness','.Ks', '.specularRoughness', '.specularAnisotropy', '.specularRotation', '.Ksss', '.Ksn', '.Kr', '.Krn','.Kt', '.IOR','.refractionRoughness','.aiMatteColorA' , '.emission' ]
bumpCheck = ['.normalCamera']



#####FUNCTIONS#####

###Backbone Function###
#Returns a dictionary of the selected nodes attrs values ( connection / value )
def buildAttrLibrary(sourceNode):
    aiStandardAttrDict = {}
    aiStandardAttrs = [sourceNode]
    for i in aiStandardAttrs:
        aroDict ={}
        listAro = cmds.listAttr(i)
        for attr in listAro:
            try:
                connections=cmds.listConnections(i+'.'+attr,s=True,plugs=True)
                if connections:
                    attrVal=connections
                else:
                    attrVal = cmds.getAttr(i +'.' +attr)
                aroDict[attr] = attrVal
            except:
                pass
    return aroDict

#####Attribute Blend Functions#####
#Attr Blend Functions come in three varieties that execute essentially the same function. 
# Scalar, Triple, and Bump

#origNodeL, and origNodeR are the source shaders.
#blendShader is your new target shader
#blender is your input texture ramp for the blend attrs on blendcolors

#The command flow of the function is as follows

#Creates BlendColor Node and connects blend color to target shader
#Then connects values from source shaders to color1 and color2 of the blendcolor node
#Connects Texture Input Ramp to blender attr of BlendColor


def scalarBlend(origNodeL, origNodeR, typeCheck, blendShader, blender):
    
    blend = cmds.shadingNode('blendColors', n=typeCheck[1:]+'_'+ origNodeL + '_' +origNodeR + '_blender',asUtility = 1)
    cmds.addAttr(blend, sn='notes',nn = 'Notes', dt = "string" )
    cmds.setAttr(blend+'.notes', " Color1 = %s, Color 2 = %s" %(origNodeL, origNodeR),  type = "string" )
    
    try:
        cmds.connectAttr(blender+'.outValue', blend+'.blender',f=1)
    except:
        try:
            cmds.connectAttr(blender+'.outColorR', blend+'.blender',f=1)
        except:
            try:
                cmds.connectAttr(blender+'.outValueX', blend+'.blender',f=1)
            except:
                print 'none found'
                
    thisL = cmds.listConnections(origNodeL+typeCheck,p=1)
    if thisL == None:
        getVal = cmds.getAttr(origNodeL+typeCheck)
        cmds.setAttr(blend+'.color1R',getVal)
        cmds.setAttr(blend+'.color1G',getVal)
        cmds.setAttr(blend+'.color1B',getVal)      
    else:
        thisL=thisL[0]
        cmds.connectAttr(thisL, blend+'.color1R',f=1)
        cmds.connectAttr(thisL, blend+'.color1G',f=1)
        cmds.connectAttr(thisL, blend+'.color1B',f=1)
      
    thisR = cmds.listConnections(origNodeR+typeCheck,p=1)
    if thisR == None:
        getVal = cmds.getAttr(origNodeR+typeCheck)
        cmds.setAttr(blend+'.color2R',getVal)
        cmds.setAttr(blend+'.color2G',getVal)
        cmds.setAttr(blend+'.color2B',getVal)      
    else:
        thisR=thisR[0]
        cmds.connectAttr(thisR, blend+'.color2R',f=1)
        cmds.connectAttr(thisR, blend+'.color2G',f=1)
        cmds.connectAttr(thisR, blend+'.color2B',f=1)
    
    cmds.connectAttr(blend+'.outputR',blendShader+typeCheck,f=1)


def tripBlend(origNodeL, origNodeR, typeCheck, blendShader, blender):
    
    blend = cmds.shadingNode('blendColors', n=typeCheck[1:]+'_'+ origNodeL + '_' +origNodeR+'_blender', asUtility = 1)
    cmds.addAttr(blend, sn='notes',nn = 'Notes', dt = "string" )
    cmds.setAttr(blend+'.notes', " Color1 = %s, Color 2 = %s" %(origNodeL, origNodeR),  type = "string" )
    try:
        cmds.connectAttr(blender+'.outValue', blend+'.blender',f=1)
    except:
        try:
            cmds.connectAttr(blender+'.outColorR', blend+'.blender',f=1)
        except:
            try:
                cmds.connectAttr(blender+'.outValueX', blend+'.blender',f=1)
            except:
                print 'none found'
    thisL = cmds.listConnections(origNodeL+typeCheck,p=1)
    if thisL == None:
        getVal = cmds.getAttr(origNodeL+typeCheck)
        getVal = getVal[0]
        cmds.setAttr(blend+'.color1', getVal[0],getVal[1],getVal[2], type="double3")    
    else:
        thisL=thisL[0]
        cmds.connectAttr(thisL, blend+'.color1',f=1)
      
    thisR = cmds.listConnections(origNodeR+typeCheck,p=1)
    if thisR == None:
        getVal = cmds.getAttr(origNodeR+typeCheck)
        getVal = getVal[0]
        cmds.setAttr(blend+'.color2', getVal[0],getVal[1],getVal[2], type="double3")    
    else:
        thisR=thisR[0]
        cmds.connectAttr(thisR, blend+'.color2',f=1)
    cmds.connectAttr(blend+'.output',blendShader+typeCheck,f=1)

def bumpBlend(origNodeL, origNodeR, typeCheck, blendShader, blender):
    blend = cmds.shadingNode('blendColors', n='bumpValue' +'_'+ origNodeL + '_' +origNodeR +'_blender',asUtility = 1)
    cmds.addAttr(blend, sn='notes',nn = 'Notes', dt = "string" )
    cmds.setAttr(blend+'.notes', " Color1 = %s, Color 2 = %s" %(origNodeL, origNodeR),  type = "string" )
    try:
        cmds.connectAttr(blender+'.outValue', blend+'.blender',f=1)
    except:
        try:
            cmds.connectAttr(blender+'.outColorR', blend+'.blender',f=1)
        except:
            try:
                cmds.connectAttr(blender+'.outValueX', blend+'.blender',f=1)
            except:
                print 'none found'

    blend1 = cmds.shadingNode('blendColors', n=blendShader+'_bumpDepth'+'_blender',asUtility = 1)
    cmds.addAttr(blend1, sn='notes',nn = 'Notes', dt = "string" )
    cmds.setAttr(blend1+'.notes', " Color1 = %s, Color 2 = %s" %(origNodeL, origNodeR),  type = "string" )
    try:
        cmds.connectAttr(blender+'.outValue', blend1+'.blender',f=1)
    except:
        try:
            cmds.connectAttr(blender+'.outColorR', blend1+'.blender',f=1)
        except:
            try:
                cmds.connectAttr(blender+'.outValueX', blend1+'.blender',f=1)
            except:
                print 'none found'
    
    bump = cmds.shadingNode('bump2d', n=blendShader+'_bumpValue'+'_BUMP_BLENDED',asUtility = 1)

    nameL = cmds.listConnections(origNodeL+typeCheck,p=1)
    for i in nameL:   
        bumpNodeL = i.split('.')[0]
    thisL = cmds.listConnections(bumpNodeL + '.bumpValue',p=1)
    if thisL == None:
        getVal = cmds.getAttr(bumpNodeL+'.bumpValue')
        cmds.setAttr(blend+'.color1R',getVal)
        cmds.setAttr(blend+'.color1G',getVal)
        cmds.setAttr(blend+'.color1B',getVal)      
    else:
        thisL=thisL[0]
        cmds.connectAttr(thisL, blend+'.color1R',f=1)
        cmds.connectAttr(thisL, blend+'.color1G',f=1)
        cmds.connectAttr(thisL, blend+'.color1B',f=1)

    nameR = cmds.listConnections(origNodeR+typeCheck,p=1)
    for i in nameR:   
        bumpNodeR = i.split('.')[0]
    
    thisR = cmds.listConnections(bumpNodeR + '.bumpValue',p=1)
    if thisR == None:
        getVal = cmds.getAttr(bumpNodeR+'.bumpValue')
        cmds.setAttr(blend+'.color2R',getVal)
        cmds.setAttr(blend+'.color2G',getVal)
        cmds.setAttr(blend+'.color2B',getVal)      
    else:
        thisR=thisR[0]
        cmds.connectAttr(thisR, blend+'.color2R',f=1)
        cmds.connectAttr(thisR, blend+'.color2G',f=1)
        cmds.connectAttr(thisR, blend+'.color2B',f=1)


    getVal1 = cmds.getAttr(bumpNodeR+'.bumpDepth')
    getVal2 = cmds.getAttr(bumpNodeL+'.bumpDepth')
    if getVal1 == getVal2:
        cmds.delete(blend1)
        cmds.setAttr(bump+'.bumpDepth',getVal1)
    else:
        thisL1 = cmds.listConnections(bumpNodeL+'.bumpDepth',p=1)
        if thisL1 == None:
            getVal = cmds.getAttr(bumpNodeL+'.bumpDepth')
            cmds.setAttr(blend1+'.color1R',getVal)
            cmds.setAttr(blend1+'.color1G',getVal)
            cmds.setAttr(blend1+'.color1B',getVal)      
        else:
            thisL1=thisL1[0]
            cmds.connectAttr(thisL1, blend1+'.color1R',f=1)
            cmds.connectAttr(thisL1, blend1+'.color1G',f=1)
            cmds.connectAttr(thisL1, blend1+'.color1B',f=1)
    
        thisR1 = cmds.listConnections(bumpNodeR + '.bumpDepth',p=1)
        if thisR1 == None:
            getVal = cmds.getAttr(bumpNodeR+'.bumpDepth')
            cmds.setAttr(blend1+'.color2R',getVal)
            cmds.setAttr(blend1+'.color2G',getVal)
            cmds.setAttr(blend1+'.color2B',getVal)      
        else:
            thisR1=thisR1[0]
            cmds.connectAttr(thisR1, blend1+'.color2R',f=1)
            cmds.connectAttr(thisR1, blend1+'.color2G',f=1)
            cmds.connectAttr(thisR1, blend1+'.color2B',f=1)
        cmds.connectAttr(blend1+'.outputR',bump+'.bumpDepth',f=1)

    cmds.connectAttr(blend+'.outputR',bump+'.bumpValue',f=1)
    cmds.connectAttr(bump+'.outNormal',blendShader+'.normalCamera',force=1)

##### Match Blend Functions #####
#The same as the blend functions these match blend funcs come in the same three varieties.
#These functions are used to match attrs from the sources to the target shader which are identical across the two source shaders .

def matchBlendSing(origNodeL, typeCheck, blendShader):
    connections=cmds.listConnections(origNodeL+typeCheck,s=True,plugs=True)
    if connections:
        cmds.connectAttr(connections[0], blendShader+typeCheck,force=1)
    else:
        RecAttr = cmds.getAttr(origNodeL+typeCheck)
        cmds.setAttr(blendShader+typeCheck, RecAttr)

def matchBlendBump(origNodeL, typeCheck, blendShader):
    connections=cmds.listConnections(origNodeL+typeCheck,s=True,plugs=True)
    if connections:
        cmds.connectAttr(connections[0], blendShader+typeCheck,force=1)

def matchBlendTrip(origNodeL, typeCheck, blendShader):
    connections=cmds.listConnections(origNodeL+typeCheck,s=True,plugs=True)
    if connections:
        cmds.connectAttr(connections[0], blendShader+typeCheck,force=1)
    else:
        RecAttr = cmds.getAttr(origNodeL+typeCheck)
        cmds.setAttr(blendShader+typeCheck, RecAttr[0][0],RecAttr[0][1],RecAttr[0][2] )


##### Create and Update Blend Shader Functions #####

###Command Flow is as follows###

#Available Blend Attr Lists#
#Create Dictionaries of the two source shaders
#Compare the two dictionaries for differences in the keys
#Create Target Bleneded Shader and the input texture ramp.
#If a key is different, run it through blend Attr functions, and if an attr is identical run it through match attr functions.

def blendShader(args=None):
    triple = ['.color', '.KsColor','.opacity', '.KtColor', '.KsssColor','.sssRadius','.KrColor', '.transmittance', '.opacity' , '.refractionExitColor', '.aiMatteColor', '.emissionColor'  ]
    singleCheck = ['.Kd','.Kb','.diffuseRoughness','.Ks', '.specularRoughness', '.specularAnisotropy', '.specularRotation', '.Ksss', '.Ksn', '.Kr', '.Krn','.Kt', '.IOR','.refractionRoughness','.aiMatteColorA' , '.emission' ]
    bumpCheck = ['.normalCamera']
    
    singleCheckList = []
    tripleCheck = []
    bumpCheckList = []

    singleSameList = []
    tripleSameList = []
    bumpSameList = []

    origNodeL= cmds.textField('SetL',query=True, tx=True)
    origNodeR=cmds.textField('SetR',query=True, tx=True)
    if origNodeL == origNodeR:
        pass
    blendNodeWhiteDict = buildAttrLibrary(origNodeL)
    blendNodeBlackDict = buildAttrLibrary(origNodeR)
    
    keys = []
    
    for k,v in blendNodeWhiteDict.iteritems():
        keys.append(k)
           
    for key in keys:
        if blendNodeWhiteDict[key] != blendNodeBlackDict[key]:
            if '.'+key in triple:
                tripleCheck.append('.'+key)
            
            if '.'+key in singleCheck:
                singleCheckList.append('.'+key)
                
            if '.'+key in bumpCheck:
                bumpCheckList.append('.'+key)
        else:
            if '.'+key in singleCheck:
                singleSameList.append('.'+key)
            if '.'+key in triple:
                tripleSameList.append('.'+key)
            if '.'+key in bumpCheck:
                bumpSameList.append('.'+key)

    blender = cmds.shadingNode('ramp',n = 'BLENDER_'+origNodeL+'_'+origNodeR, asTexture = 1)
    cmds.setAttr (blender+".colorEntryList[0].position", 0)
    cmds.setAttr(blender+'.colorEntryList[0].color', 0,0,0 )
    
    #create Blended Shader
    blendShader= cmds.shadingNode('aiStandard', n = origNodeL + '_' +origNodeR + '_BLENDED_SHD', asShader=True)

    cmds.addAttr(blendShader, sn='jsBlendedShader', at="float")
    cmds.setAttr(blendShader+'.jsBlendedShader', 1)

    cmds.addAttr(blendShader, sn='whiteShader',at="float")
    cmds.addAttr(blendShader, sn='blackShader',at="float")
    cmds.addAttr(blendShader, sn='blenderRamp',at="float")

    cmds.addAttr(blendShader, sn='blendsContainer',at="float")

    cmds.connectAttr(origNodeL+'.message', blendShader+'.whiteShader',f=1)
    cmds.connectAttr(origNodeR+'.message', blendShader+'.blackShader',f=1)
    cmds.connectAttr(blender+'.message', blendShader+'.blenderRamp',f=1)
    
    ###Blends Attributes Functions
    for typeCheck in tripleCheck:
        tripBlend(origNodeL, origNodeR, typeCheck, blendShader,blender)
    for typeCheck in singleCheckList:
        scalarBlend(origNodeL, origNodeR, typeCheck, blendShader,blender)
    for typeCheck in bumpCheckList:
        bumpBlend(origNodeL, origNodeR, typeCheck, blendShader,blender)
    
    for typeCheck in singleSameList:
        matchBlendSing(origNodeL, typeCheck, blendShader)
        
    for typeCheck in tripleSameList:
        matchBlendTrip(origNodeL, typeCheck, blendShader)
        
    for typeCheck in bumpSameList:
        matchBlendBump(origNodeL, typeCheck, blendShader)       
    
    availableBlends = []
    underNodes = cmds.listConnections(blendShader)
    for i in underNodes:
        if '_blender' in i:
            availableBlends.append(i)
    if len(availableBlends) > 0:
        blendCont = cmds.container(name = origNodeL+'_'+origNodeR+'_blend_CONTAINER', addNode=availableBlends,includeNetwork=False,includeHierarchyBelow=False)

    cmds.connectAttr(blendCont+'.message', blendShader+'.blendsContainer',f=1)

def UpdateBlendedIfFunc(args=None):
    findBlended = []

    filterForBlended = cmds.ls(mat=1, r=1,sl=1)
    if len(filterForBlended) > 0:
        for i in filterForBlended:
            try:
                if cmds.getAttr(i+'.jsBlendedShader') == 1:
                    findBlended.append(i)
            except:
                pass
            if len(findBlended) > 0:
                blendShaderUpdate(findBlended)
            else:
                pickToUpdate()
    else:
        pickToUpdate()


def pickToUpdate(args=None):
    if cmds.window('js_pickUpdate',exists=True):
        cmds.deleteUI('js_pickUpdate')
    window = cmds.window('js_pickUpdate',menuBar=True, title= 'Update Picker') #, s = False
    cmds.flowLayout()
    cmds.frameLayout(label = "Update Picker:", borderStyle = "etchedIn",w=300,h=175)
    cmds.scrollLayout(cr=1,h=155)
    cmds.columnLayout(adj=1)
    findBlended = []
    filterForBlended = cmds.ls(mat=1, r=1)
    for i in filterForBlended:
        try:
            if cmds.getAttr(i+'.jsBlendedShader') == 1:
                findBlended.append(i)
        except:
            pass
    for each in findBlended:
        eachButton = cmds.checkBox(each,l=each,h=20)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.frameLayout(label = "Functions:", borderStyle = "etchedIn",w=100,h=175)
    cmds.columnLayout(adj=1)
    funcButtonsHeight= 75
    cmds.button(l='Update Selected:', c=updateSelectedShaders, h = funcButtonsHeight)
    cmds.button(l='Close:', c="cmds.deleteUI('js_pickUpdate')", h=funcButtonsHeight)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.showWindow( window )
    cmds.window('js_pickUpdate', edit=True, widthHeight=[403, 179], s = True)
    #cmds.window('js_pickUpdate', query=True, widthHeight=True)
    
 
def updateSelectedShaders(args=None):
    findBlended = []
    filterForBlended = cmds.ls(mat=1, r=1)
    for i in filterForBlended:
        try:
            if cmds.getAttr(i+'.jsBlendedShader') == 1:
                findBlended.append(i)
        except:
            pass
    updateTheseShaders = []
    for each in findBlended:
        eachButton = cmds.checkBox(each,query=True, v=1)
        if eachButton == 1:
            updateTheseShaders.append(each)

    blendShaderUpdate(updateTheseShaders)



def blendShaderUpdate(findBlended):
    triple = ['.color', '.KsColor','.opacity', '.KtColor', '.KsssColor','.sssRadius','.KrColor', '.transmittance', '.opacity' , '.refractionExitColor', '.aiMatteColor', '.emissionColor'  ]
    singleCheck = ['.Kd','.Kb','.diffuseRoughness','.Ks', '.specularRoughness', '.specularAnisotropy', '.specularRotation', '.Ksss', '.Ksn', '.Kr', '.Krn','.Kt', '.IOR','.refractionRoughness','.aiMatteColorA' , '.emission' ]
    bumpCheck = ['.normalCamera']
    
    singleCheckList = []
    tripleCheck = []
    bumpCheckList = []

    for i in findBlended:
        singleCheckList = []
        tripleCheck = []
        bumpCheckList = []      

        singleSameList = []
        tripleSameList = []
        bumpSameList = []

        blendShader = i
        origNodeL = cmds.listConnections(i+'.whiteShader')[0]
        origNodeR = cmds.listConnections(i+'.blackShader')[0]
        
        blendsContainer = cmds.listConnections(i+'.blendsContainer')[0]



        blendNodeWhiteDict = buildAttrLibrary(origNodeL)
        blendNodeBlackDict = buildAttrLibrary(origNodeR)
        
        keys = []
        
        for k,v in blendNodeWhiteDict.iteritems():
            keys.append(k)
        print keys  
        for key in keys:
            if blendNodeWhiteDict[key] != blendNodeBlackDict[key]:
                if '.'+key in triple:
                    tripleCheck.append('.'+key)
                
                if '.'+key in singleCheck:
                    singleCheckList.append('.'+key)
                    
                if '.'+key in bumpCheck:
                    bumpCheckList.append('.'+key) 
            else:
                if '.'+key in singleCheck:
                    singleSameList.append('.'+key)
                if '.'+key in triple:
                    tripleSameList.append('.'+key)
                if '.'+key in bumpCheck:
                    bumpSameList.append('.'+key)
                   
                    
        mergedBlendNames = origNodeL+'_' + origNodeR
        
        blender = cmds.listConnections(i+'.blenderRamp')[0]
        
        if blender != 'BLENDER_' + mergedBlendNames:
            blender = cmds.rename(blender, 'BLENDER_' + mergedBlendNames)

        #availableBlends = []
        #underNodes = cmds.listConnections(findBlended)
        #for i in underNodes:
        #    if '_blender' in i:
        #        availableBlends.append(i)
        #if len(availableBlends) > 0:
        #    cmds.delete(availableBlends)

        cmds.delete(blendsContainer)
        #checked that blends available blendColor nodes
        ###Blends Attributes Functions
        for typeCheck in tripleCheck:
            tripBlend(origNodeL, origNodeR, typeCheck, blendShader,blender)
        for typeCheck in singleCheckList:
            scalarBlend(origNodeL, origNodeR, typeCheck, blendShader,blender)
        for typeCheck in bumpCheckList:
            bumpBlend(origNodeL, origNodeR, typeCheck, blendShader,blender)
            
        
        for typeCheck in singleSameList:
            matchBlendSing(origNodeL, typeCheck, blendShader)
            
        for typeCheck in tripleSameList:
            matchBlendTrip(origNodeL, typeCheck, blendShader)

        for typeCheck in bumpSameList:
            matchBlendBump(origNodeL, typeCheck, blendShader) 

        availableBlends = []
        underNodes = cmds.listConnections(i)
        for under in underNodes:
            if '_blender' in under:
                availableBlends.append(under)
        if len(availableBlends) > 0:
            blendCont = cmds.container(name = origNodeL+'_'+origNodeR+'_blend_CONTAINER', addNode=availableBlends,includeNetwork=False,includeHierarchyBelow=False)

        cmds.connectAttr(blendCont+'.message', i+'.blendsContainer',f=1)

def addSelectedFieldMat(field):
    sel = cmds.ls(sl=1,type='aiStandard')
    if len(sel) > 0:
        cmds.textField(field,edit=True, tx=sel[0])

def addSelectedFieldMatW(args=None):
    sel = cmds.ls(sl=1,type='aiStandard')
    if len(sel) > 0:
        cmds.textField('SetL',edit=True, tx=sel[0])

def addSelectedFieldMatB(args=None):
    sel = cmds.ls(sl=1,type='aiStandard')
    if len(sel) > 0:
        cmds.textField('SetR',edit=True, tx=sel[0])


def buildShaderBlendUI(versionNumberBlend):
    if cmds.window('js_aiShaderBlend',exists=True):
        cmds.deleteUI('js_aiShaderBlend')
    
    window = cmds.window('js_aiShaderBlend',menuBar=True, title= 'js_aiShaderBlend %s' %(versionNumberBlend) , w=330, h=100) #, s = False
    
    
    cmds.columnLayout(adj=1)
    
    child1 = cmds.columnLayout(adj=1)
    
    cmds.frameLayout(label = "Select Shading Nodes:", borderStyle = "etchedIn")
    
    fieldHeights = 35
    fieldWidth = 250
    cmds.flowLayout()
    cmds.textField('SetL', ed=0,h=fieldHeights, w=fieldWidth,pht="Set Target Shader 1 (White)")
    #cmds.button(label = 'W.Shader:',h=fieldHeights,w=70, c = "addSelectedFieldMat('SetL')" )
    cmds.button(label = 'W.Shader:',h=fieldHeights,w=70, c = addSelectedFieldMatW )
    cmds.setParent('..')
    
    cmds.flowLayout()
    cmds.textField('SetR', ed=0,h=fieldHeights, w=fieldWidth,pht="Set Target Shader 2 (Black)")
    #cmds.button(label = 'B.Shader:',h=fieldHeights,w=70, c= "addSelectedFieldMat('SetR')" )
    cmds.button(label = 'B.Shader:',h=fieldHeights,w=70, c= addSelectedFieldMatB )
    cmds.setParent('..')
    
    cmds.setParent('..')
    
    dualButtonHeight = 50 #55
    cmds.frameLayout(label = "Create Shader:", borderStyle = "etchedIn")
    cmds.columnLayout(adj=1)
    createBut = cmds.button(label = 'Create Blended Shader:',h=dualButtonHeight, c=blendShader )
    #cmds.button(label = 'Update Blended Shaders:',h=dualButtonHeight, c=blendShaderUpdate )
    cmds.button(label = 'Update Blended Shaders:',h=dualButtonHeight, c=UpdateBlendedIfFunc )
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.setParent('..')
    
    cmds.showWindow( window )
    cmds.window('js_aiShaderBlend', edit=True, widthHeight=[330, 230], s = False)
    cmds.setFocus(createBut)
    #cmds.window('js_aiShaderBlend', query=True, widthHeight=True)

buildShaderBlendUI(versionNumberBlend)

