import maya.cmds as cmds

####################
#jsFileNode v1.1####
####################

#Author: Joseph Szokoli
#Website: cargocollective.com/josephSzokoli

#Help:
#To create a shelf icon, move jsRenamer.py to your scripts folder and assign the following command to the shelf.
#import jsFileNode
#reload(jsFileNode)


#Version Number#################
versionNumberTexture = 'v1.1'###
################################


### ChangeLog: ################################################################################
###v1.0 Initial 



def create2D(name):
    file1 = cmds.shadingNode('file',asTexture= 1, name = name)
    placement = cmds.shadingNode('place2dTexture',asUtility=1, name = name+'_place2DTexture')
    cmds.connectAttr( placement+'.coverage',  file1+'.coverage')
    cmds.connectAttr( placement+'.translateFrame',  file1+'.translateFrame')
    cmds.connectAttr( placement+'.rotateFrame',  file1+'.rotateFrame')
    cmds.connectAttr( placement+'.mirrorU',  file1+'.mirrorU')
    cmds.connectAttr( placement+'.mirrorV',  file1+'.mirrorV')
    cmds.connectAttr( placement+'.stagger',  file1+'.stagger')
    cmds.connectAttr( placement+'.wrapU',  file1+'.wrapU')
    cmds.connectAttr( placement+'.wrapV',  file1+'.wrapV')
    cmds.connectAttr( placement+'.repeatUV',  file1+'.repeatUV')
    cmds.connectAttr( placement+'.offset',  file1+'.offset')
    cmds.connectAttr( placement+'.rotateUV',  file1+'.rotateUV')
    cmds.connectAttr( placement+'.noiseUV',  file1+'.noiseUV')
    cmds.connectAttr( placement+'.vertexUvOne',  file1+'.vertexUvOne')
    cmds.connectAttr( placement+'.vertexUvTwo',  file1+'.vertexUvTwo')
    cmds.connectAttr( placement+'.vertexUvThree',  file1+'.vertexUvThree')
    cmds.connectAttr( placement+'.vertexCameraOne',  file1+'.vertexCameraOne')
    cmds.connectAttr( placement+'.outUV', file1+'.uv')
    cmds.connectAttr( placement+'.outUvFilterSize',  file1+'.uvFilterSize')
    return file1

def udimChecker(udimCheck):
    #udimCheck = textures
    udimTesting = []
    udimList = []
    singleList = []
    
    for i in udimCheck:
        splitName = i.split('.')
        bodyName = splitName[0]
        udimName = splitName[0]+'.'+'<udim>'+'.'+splitName[2]
        #print udimName
        if udimName in udimTesting:
            udimList.append(udimName)
            #print 'appended'
            udimTesting.remove(udimName)
        if udimName in udimList:
            pass
        else:
            udimTesting.append(udimName)
    
    for single in udimTesting:
        splitName = single.split('.')
        bodyName = splitName[0]
        for i in udimCheck:
            if bodyName in i:
                singleList.append(i)
    
    textureList = udimList+singleList
    return textureList


def createTextureNodes(args=None):    
    #filePath = '/job/comms/pipeline_testing_2015_1/sandbox/jszokoli/lighting/lighting/work/maya/data/udimTest'
    filePath = cmds.textField('texDirField',query=1,tx=1)
    
    fileType = cmds.optionMenu('fileType',query=1,v=1)
    if fileType == 'All':
        fileType='.*'
    
    textures = cmds.getFileList( folder=filePath, filespec='*?'+fileType )
    
    if cmds.checkBox('UdimOption',query=1,v=1) == True:
        textures = udimChecker(textures)
    
    
    for tex in textures:
        fileTex = create2D(tex)
        FullFilePath = filePath+'/'+tex
        print fileTex
        cmds.setAttr(fileTex+'.ftn',FullFilePath, type = "string")

def createTextureNodes1(args=None):    
    #filePath = '/job/comms/pipeline_testing_2015_1/sandbox/jszokoli/lighting/lighting/work/maya/data/udimTest'
    filePath = cmds.textField('texDirField',query=1,tx=1)
    print filePath


def selectDirectory(args=None):
    dialogDir = cmds.fileDialog2(dialogStyle=2, fm = 4, okc = 'Set Directory') or ['Directory']
    print dialogDir
    StringList = ''
    for i in dialogDir:
        StringList = StringList+',' + i
    print StringList
    cmds.textField('texDirField',edit=1,tx=StringList)





###################
######UI START#####
###################______________________________________________________________________________________________________________________________________________

if cmds.window('jsTextureManager',exists=True):
    cmds.deleteUI('jsTextureManager')

window = cmds.window('jsTextureManager', title= 'jsFileNode_%s' %versionNumberTexture , w=330, h=100,rtf = 1,menuBar = True)

'''
cmds.menu( label='Bonus Tools', tearOff=False )
cmds.menuItem( subMenu=True, label='Arnold Quick Settings', tearOff=False )
cmds.menuItem( label='Low Samples')
cmds.menuItem( divider=True )
cmds.menuItem( label='Motion Blur On')
cmds.menuItem( label='Motion Blur Off')
cmds.setParent( '..', menu=True )
cmds.menuItem( label='Rename Shading Groups')
'''


cmds.columnLayout()
##### Full Renamer
cmds.frameLayout('FileNodeLayout',label = "Texture Nodes from Path:", borderStyle = "etchedIn")
cmds.flowLayout(w=385)
cmds.columnLayout()



#cmds.flowLayout(w=300)
#cmds.text('Directory:')
cmds.textField('texDirField',tx='Directory',ed=0,w=300)

#cmds.setParent('..')

fileTypes = ['.tx', '.exr', '.tif', '.png', '.jpg','.tga','vrimg', '.tex','All']
cmds.separator(style='in',w=300)
cmds.flowLayout(w=300)
#cmds.gridLayout( numberOfColumns=3, cellWidthHeight=(100, 25) )
cmds.optionMenu('fileType',h=25)

#cmds.menuItem(label='tx')
for fileType in fileTypes:
    cmds.menuItem(label=fileType)

cmds.separator(hr=0, style='in',h=25)

cmds.checkBox('UdimOption',label='Udim',v=1,h=25)

cmds.separator(hr=0, style='in',h=25)
cmds.button('Set Directory',c=selectDirectory,h=25)

cmds.setParent('..')
cmds.setParent('..')
cmds.separator(hr=0, style='in',h=50)
cmds.button('Crate Nodes',w=75,h=50,c=createTextureNodes1)
cmds.setParent('..')

cmds.showWindow( window )
cmds.window('jsTextureManager', edit=True, widthHeight=[391,78], s = True)
#cmds.window('jsTextureManager', query=True, widthHeight=1)
