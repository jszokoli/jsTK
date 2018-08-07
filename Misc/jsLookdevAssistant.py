import maya.cmds as cmds
import os
from datetime import datetime

###############################
###jsLookdevAssistant DEV #####
###############################

#Author: Joseph Szokoli
#Website: cargocollective.com/josephSzokoli

#Help: 
#To create a shelf icon, move jsLookdevAssistant.py to your scripts folder and assign the following command to the shelf.
#import jsLookdevAssistant
#reload(jsLookdevAssistant)

### ChangeLog: ################################################################################

#########4.0#########
###Changed Name to jsLookdevAssistant
#UI OVERHAUL
#Introduced Menu Bar
#REWRITE SHADERPACK INCOMING
###Aplhabetical listing with tabs in all exporter/importer/assigners
### Fixed bug in shader pack manager
#####LINE 277 FIX SG RENAMER WITH DISP


###3.2.0
#Changed Library Files to .mb 

###3.1.0
#Introduced Add Selected to textField Button "+' in materialApplicator
#Sorted listMat

###3.0.1
#Changed Rename SG function to filter to selection or do all

###3.0.0
#Introduced Shader Pack Manager.
#Squashed Dsp removal bugs.
#Added Check all to Import Materials
#Added Auto Import Materials Mentioned in shaderPacks
#Fixed Bug in Auto Import Only to Import Missing Shaders
#Fixed Close UI Bug

###2.2.0
#Added View All File Texture Paths Function

###2.1.2
#Fixed more than one nested Shader Removal

###v2.0 + v2.0.1 + v2.0.2
#Overall UI Overhaul.
#Introduced Texture Path Manager.
#Introduced Material Batch Applicator.
#Introduced Material Applicator Assignment Backups. Backups current assignments under storage node.
#Fixed publishing materials with namespace. Still not suggested.
#Added Batch Rename Shading Groups.
#Fixed bug publishing after additional shaders are created.
#Fixed bug on import. Deleting Top nodes blindly. Now focused only to Shading Groups.
#.1
#Nested Shaders no longer show up under publish
#Typo
#.2
#Added Try to ShadingGroupChanger
#Added Try to materialAssigner
#Nested Shaders no longer show up under Material Applicator
#Added Lambert1 back to material assigner

###v1.2 + v1.2.1
#Added Shading Group support.
#Added top folder for backups. 
#Added Storage Node Locks. 

###v1.1
#Intoduced Material Library.

###v1.0
#Initial Material Assignment System

#End ChangeLog.#################################################################################

#Begin Functions Area
#Initial Build Material List
listMat = cmds.ls( materials=True  )
dsp = cmds.ls(type = 'displacementShader')
if len(dsp)>0:
    for d in dsp:
        listMat.remove(d)
listMat.remove(u'particleCloud1')
matNumber = len(listMat)
sorted(listMat, key=lambda s: s.lower())


#####VERSION NUMBER#########################
#versionNumber = 'v4.0'
versionNumber = 'v4.0_DEV'
#############################################


def printNewMenuItem( item ):
    cmds.select(cmds.ls( sl=1 , tr=True )) 
    cmds.hyperShade( assign= item ) 
    updateIndividual()

def selection(*args):
    selectionName = cmds.textField('TFL_selection',q=True,text=True)
    selThis = cmds.ls('*%s*' %(selectionName), tr=1,r=1,type='mesh')
    if len(selThis) > 0:
        cmds.select(selThis)
    else:
        print 'Could not find object with name that matches: (%s)' %(selectionName)
         
def updateIndividual(args=None):
    listMat = cmds.ls( materials=True  )
    dsp = cmds.ls(type = 'displacementShader')
    if len(dsp)>0:
        for d in dsp:
            listMat.remove(d)
    listMat.remove(u'particleCloud1')
    matNumber = len(listMat)
    listMat = sorted(listMat, key=lambda s: s.lower())
    menuItems = cmds.optionMenu('individual', q=True, itemListLong=True) # itemListLong returns the children
    if menuItems:
        cmds.deleteUI(menuItems)
    for num in range(0,matNumber):
        cmds.menuItem(label= listMat [num],parent= 'individual' )
        
def applyChanges(args=None):       
    listMat = cmds.ls( materials=True  )
    listMat.remove(u'particleCloud1')
    for each in listMat:
        exists = cmds.textField('%s_ApplyField' %(each), query = True, exists=True)
        if exists == True:
            result = cmds.textField('%s_ApplyField' %(each), query = True, text=True)
            resultList = result.split()
            if len(resultList) > 0:
                for r in resultList:
                    try:
                        cmds.select(r)
                        cmds.hyperShade(assign=each)
                        cmds.select(d=1)
                    except:
                        pass
                    
def applyChangesSave(args=None):
    checkStorageNode = cmds.ls('materialLibraryDirectory_STORAGE')
    if not checkStorageNode:
        cmds.group(name = 'materialLibraryDirectory_STORAGE', em=True)
        cmds.addAttr('materialLibraryDirectory_STORAGE', sn='notes',nn = 'Notes', dt = "string" )
        cmds.setAttr('materialLibraryDirectory_STORAGE.notes', 'No Directory Currently Set',  type = "string",  )
         
    listMat = cmds.ls( materials=True  )
    listMat.remove(u'particleCloud1')
    for each in listMat:
        newName = cmds.ls(each)[0].rpartition(':')[2]
        exists = cmds.textField('%s_ApplyField' %(newName), query = True, exists=True)
        if exists == True:
            result = cmds.textField('%s_ApplyField' %(newName), query = True, text=True)
            testing = cmds.attributeQuery(newName, node='materialLibraryDirectory_STORAGE', ex=True )
            if testing == True:
                cmds.setAttr('materialLibraryDirectory_STORAGE.%s' %(newName), result ,type = "string" )
            else:
                cmds.addAttr('materialLibraryDirectory_STORAGE', sn=newName,nn = newName, dt = "string" )
                cmds.setAttr('materialLibraryDirectory_STORAGE.%s' %(newName), result ,type = "string" )
            resultList = result.split()
            if len(resultList) > 0:
                for r in resultList:
                    try:
                        cmds.select(r)
                        cmds.hyperShade(assign=each)
                        cmds.select(d=1)
                    except:
                        pass
                    
                                                       
def closeAssigner(args=None):
    cmds.deleteUI('materialBatchApply')
    
def addSelected(name):
    sel = cmds.ls(sl=1, tr=1)
    for each in sel:
        try:
            current = cmds.textField(name+'_ApplyField', query = True, text = True)
            if len(current) > 0:
                new = current + ' ' +each
            else:
                new = each
                cmds.textField(name+'_ApplyField', edit = True, text = new )
        except:
            pass      

def materialBatchApply(args=None):
    listMat = cmds.ls( materials=True  )
    listMatStart = cmds.ls( materials=True )
    downList = []
    for each in listMatStart:
        lowerNode = cmds.hyperShade(lun = each)
        underShader = cmds.ls(lowerNode, materials = True)
        #print underShader
        for x in underShader:
            downList.append(x)
    downList = remove_duplicates(downList)
    if len(downList) > 0:
        for z in downList:
            #print z
            listMat.remove(z)
    listMat.append(u'lambert1')
    listMat = sorted(listMat, key=lambda s: s.lower())
#    listMat.remove(u'particleCloud1')
    
    if cmds.window('materialBatchApply', exists=True):
        
        cmds.deleteUI('materialBatchApply')
        
    
    cmds.window('materialBatchApply', title= 'jsMaterialApplicator')
        
    cmds.flowLayout()
    
    cmds.frameLayout(label = "Create Material Assignments:", borderStyle = "etchedIn",h=400,w=600 )
    cmds.scrollLayout(hst=16,vst=16)
    last = 'a'
    aExist =[]
    if listMat[0][0] == last:
        aExist.append('yes')
    if 'yes' in aExist:
        cmds.text('a'.capitalize()+':',fn = 'boldLabelFont')
    for each in listMat:
        if each[0] == last:
            newName = cmds.ls(each)[0].rpartition(':')[2]
            #cmds.rowLayout( nc=2, adjustableColumn=2, columnAlign=(1, 'left'), w= 580 )
            cmds.rowLayout( nc=3, adjustableColumn=3, columnAlign=(1, 'left'), w= 980 )
            cmds.button(newName,label = '+', c = 'jsLookdevAssistant.addSelected("%s")'%newName )
            cmds.text(label = '%s:' %(newName), font = "boldLabelFont",rs=1 )
            cmds.textField('%s_ApplyField' %(newName), w =200)
        else:
            cmds.text(label= each[0].capitalize()+':',fn = 'boldLabelFont')
            newName = cmds.ls(each)[0].rpartition(':')[2]
            #cmds.rowLayout( nc=2, adjustableColumn=2, columnAlign=(1, 'left'), w= 580 )
            cmds.rowLayout( nc=3, adjustableColumn=3, columnAlign=(1, 'left'), w= 980 )
            cmds.button(newName,label = '+', c = 'jsLookdevAssistant.addSelected("%s")'%newName )
            cmds.text(label = '%s:' %(newName), font = "boldLabelFont",rs=1 )
            cmds.textField('%s_ApplyField' %(newName), w =200)
            last = each[0]
        cmds.setParent('..') 
    
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.frameLayout(label = "Options:", borderStyle = "etchedIn",h=400,w=100 )
    cmds.columnLayout( adjustableColumn=True, cal = 'left' )
    cmds.button(label = 'Apply and Save:', c = applyChangesSave, h=125)
    cmds.button(label = 'Apply', c = applyChanges, h= 125 )   
    cmds.button(label = 'Close:', h =125, c = closeAssigner )
    
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.setParent('..')
    
    checkStorageNode = cmds.ls('materialLibraryDirectory_STORAGE')
    if len(checkStorageNode) > 0:
        for each in listMat:
            newName = cmds.ls(each)[0].rpartition(':')[2]
            testing = cmds.attributeQuery(newName, node='materialLibraryDirectory_STORAGE', ex=True )
            if testing == True:
                newSet = cmds.getAttr('materialLibraryDirectory_STORAGE.%s' %(newName) )
                cmds.textField('%s_ApplyField' %(newName),edit = True, text = newSet)
    cmds.showWindow( 'materialBatchApply' )
    cmds.window('materialBatchApply', edit=True, widthHeight=[700,400], s = False)
    
def renameShadingGroups(args=None):
    listMat = cmds.ls(sl=1, materials=True  )
    if not listMat:
        listMat = cmds.ls(materials=True)
        dsp = cmds.ls(type = 'displacementShader')
        if len(dsp)>0:
            for d in dsp:
                listMat.remove(d)
        listMat.remove(u'lambert1')
        listMat.remove(u'particleCloud1')
    if len(listMat) > 0:
        for each in listMat:
            try:
                upper = cmds.hyperShade(each, ldn = each)
                print 'upper =' + str(upper)
                SG = cmds.ls(upper, type = 'shadingEngine')
                print 'SG =' +str(SG)
                if len(SG) > 0:
                    cmds.rename(SG, '%sSG' %(each) )
                print 'Shading Group of %s has been changed from %s to [u\'%sSG\']' %(each,SG,each)
            except:
                pass

####TEXTURE PATH CODE#####__________________________________________________________________
def changeTexPath(Args = None):
    forwardSlash = '\\'
    backSlash = '/'
    textureNodes = cmds.ls( type = 'file')
    origDirPrefix = cmds.textField('oldDir', query = True, text = True)
    newDirPrefix = cmds.textField('newDir', query = True, text = True)
    origDirPrefix =  origDirPrefix.replace(forwardSlash,backSlash)
    newDirPrefix =  newDirPrefix.replace(forwardSlash,backSlash)
    for each in textureNodes:
        currentTexDir = cmds.getAttr('%s.ftn' %(each) )
        newDirName = currentTexDir.replace(origDirPrefix,newDirPrefix)
        cmds.setAttr('%s.ftn' %(each),"%s" %(newDirName), type = "string") 
        
def changeSelTexPath(Args = None):
    forwardSlash = '\\'
    backSlash = '/'
    textureNodes = cmds.ls( sl = 1, type = 'file')
    origDirPrefix = cmds.textField('oldDir', query = True, text = True)
    newDirPrefix = cmds.textField('newDir', query = True, text = True)
    origDirPrefix =  origDirPrefix.replace(forwardSlash,backSlash)
    newDirPrefix =  newDirPrefix.replace(forwardSlash,backSlash)
    for each in textureNodes:
        currentTexDir = cmds.getAttr('%s.ftn' %(each) )
        newDirName = currentTexDir.replace(origDirPrefix,newDirPrefix)
        cmds.setAttr('%s.ftn' %(each),"%s" %(newDirName), type = "string")     

def switchPortions(Args=None):
    oldOld= cmds.textField('oldDir', q=True, text = True)   
    oldNew = cmds.textField('newDir', q=True, text = True)
    cmds.textField('oldDir', edit=True, text = oldNew)   
    cmds.textField('newDir', edit=True, text = oldOld)  

def selectFtpNodes(args=None):
    ftpCheckOptions = []
    textureNodes = cmds.ls( type = 'file')
    for each in textureNodes:
        checkBoxExist = cmds.checkBox(each + '_ftpCheck', query=True, exists=True)
        if checkBoxExist == True:
            onOff = cmds.checkBox(each + '_ftpCheck', query=True, value=True)
        if onOff == True:
            ftpCheckOptions.append(each)
    cmds.select(ftpCheckOptions)
    
    
def closeTexPathUI(args=None):
    cmds.deleteUI('textureList')
    
def texturePathUI(args=None):
    textureNodes = cmds.ls( type = 'file')
    texturePaths = []
    for each in enumerate(textureNodes):
        currentTexDir = cmds.getAttr('%s.ftn' %(each[1]) )
        texturePaths.append(each[1]+'$'+currentTexDir)    
        if cmds.window('textureList', exists=True):
            cmds.deleteUI('textureList')
    cmds.window('textureList', title= 'Texture File Paths')
    cmds.flowLayout()
    cmds.frameLayout(label = "Texture File Paths:", borderStyle = "etchedIn",h=196,w=550)
    cmds.scrollLayout(hst=16,vst=16)
    for each in texturePaths:
        cmds.rowLayout( nc=2, adjustableColumn=2, columnAlign=(1, 'left'), w= 900 )
        cmds.checkBox(each.split('$',1)[0]+'_ftpCheck', l=each.split('$',1)[0]+':')
        cmds.textField(each.split('$',1)[1], tx = each.split('$',1)[1], ed = False, w=538)
        cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.frameLayout(label = "Functions:", borderStyle = "etchedIn",h=196,w=98)
    cmds.columnLayout( adjustableColumn=True, cal = 'left' )
    cmds.button('ftpNodeSelect', l= 'Select Nodes:', c = selectFtpNodes,h=86 )
    cmds.button('ftpUIClose', l='Close', c = closeTexPathUI,h=86)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.showWindow( 'textureList' )
    cmds.window('textureList', edit=True, widthHeight=[650,200], s = False)  

###TEXTUREPATH EDITOR

def texturePath(args=None):
    if cmds.window('jsTextureEditor',exists=True):
        cmds.deleteUI('jsTextureEditor')
    
    window = cmds.window('jsTextureEditor',menuBar=True, title= 'jsTexturePathEditor', w=330, h=100) #, s = False
    
    cmds.frameLayout(label = "jsTextureManager", borderStyle = "etchedIn", w = 320, h=260 )
    
    cmds.columnLayout(adj = 1)
    
    cmds.flowLayout(cs = 120,h=15)
    cmds.text(label = 'Old String Portion:',align='left' )
    cmds.button(label = 'Switch Old and New:',h=15, c=switchPortions)
    cmds.setParent('..')
    
    cmds.columnLayout(adj = 1)
    
    cmds.textField('oldDir', w = 315, h = 30)
    
    cmds.text(label = 'New String Portion:',align='left')
    
    cmds.textField('newDir', w=315, h= 30)
    
    cmds.frameLayout(label = "Change Texture Paths:", borderStyle = "etchedIn", w = 315, h=150)
    cmds.columnLayout(adj = 1)
    cmds.button(label= 'View All File Texture Paths:', c = texturePathUI, w = 312, h=42)
    cmds.button(label= 'Change All File Texture Paths:', c = changeTexPath, w = 312, h=42)
    cmds.button(label= 'Change Selected File Texture Path:', c = changeSelTexPath, w = 312, h=42)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.showWindow( window )
    cmds.window('jsTextureEditor', edit=True, widthHeight=[330,268], s = True)
    


####TEXTURE PATH END####____________________________________________________________________




####SetLibrary Area####______________________________________________________________________________________


def saveDirectory(args = None):
 #needs create notes attr   
    checkStorageNode = cmds.ls('materialLibraryDirectory_STORAGE')
    if len(checkStorageNode) > 0:    
        findDir = cmds.textField('getDir',q=True,text=True)
        print findDir
        cmds.setAttr('materialLibraryDirectory_STORAGE.notes', "%s" %(findDir),  type = "string",  )
    else:
        print 'Storage Node does not exist. Creating Storage Node...'
        findDir = cmds.textField('getDir',q=True,text=True)
        cmds.group(name = 'materialLibraryDirectory_STORAGE', em=True)
        cmds.addAttr('materialLibraryDirectory_STORAGE', sn='notes',nn = 'Notes', dt = "string" )
        cmds.setAttr('materialLibraryDirectory_STORAGE.notes', "%s" %(findDir),  type = "string",  )


def loadDirectory(args = None):
    
    checkStorageNode = cmds.ls('materialLibraryDirectory_STORAGE')
    if len(checkStorageNode) > 0:
        dialogDir = cmds.fileDialog2(dialogStyle=2, fm = 3, okc = 'Set Directory')
        if dialogDir == None:
            print 'Operation Cancelled'
        else:
            for each in dialogDir:
                dialogDirStrip = each   
            cmds.setAttr('materialLibraryDirectory_STORAGE.notes', "%s" %(dialogDirStrip),  type = "string",  )
    else:
        dialogDir = cmds.fileDialog2(dialogStyle=2, fm = 3, okc = 'Set Directory')
        if not dialogDir:    
            print 'Operation Cancelled'
        else:
            for each in dialogDir:
                dialogDirStrip = each   
            cmds.group(name = 'materialLibraryDirectory_STORAGE', em=True)
            cmds.addAttr('materialLibraryDirectory_STORAGE', sn='notes',nn = 'Notes', dt = "string" )
            cmds.setAttr('materialLibraryDirectory_STORAGE.notes', "%s" %(dialogDirStrip),  type = "string",  )

    checkStorageNode = cmds.ls('materialLibraryDirectory_STORAGE')
    if len(checkStorageNode) > 0:    
        currentSet = cmds.getAttr('materialLibraryDirectory_STORAGE.notes')
    else:
        currentSet = 'No Directory Storage File Found'
    cmds.textField('getDir', edit = True, text = "%s" %(currentSet) )

####END SetLibrary Area####______________________________________________________________________________________


######EXPORT#####_________________________________________________________________________________________________
def remove_duplicates(li):
    my_set = set()
    res = []
    for e in li:
        if e not in my_set:
            res.append(e)
            my_set.add(e)
    return res
    
    
def closeExport(args = None):
    cmds.deleteUI('materialBatchExport')
    
def closeInport(args = None):
    cmds.deleteUI('materialBatchImport')
    
    
def exportCheckerUi(args = None):
    listMat = cmds.ls( materials=True  )
    listMatStart = cmds.ls( materials=True )
    listMat = sorted(listMat, key=lambda s: s.lower())
    downList = []
    for each in listMatStart:
        lowerNode = cmds.hyperShade(lun = each)
        underShader = cmds.ls(lowerNode, materials = True)
        #print underShader
        for x in underShader:
            downList.append(x)
    downList = remove_duplicates(downList)
    if len(downList) > 0:
        for z in downList:
            listMat.remove(z)
    dsp = cmds.ls(type = 'displacementShader')
    if len(dsp)>0:
        for d in dsp:
            try:
                listMat.remove(d)
            except:
                pass
    lowerNode = cmds.hyperShade(lun = each)
    if cmds.window('materialBatchExport', exists=True):
    
        cmds.deleteUI('materialBatchExport')
    
    cmds.window('materialBatchExport', title= 'jsMaterialLibraryPublish')
    cmds.flowLayout()
    cmds.frameLayout(label = "Select Materials to Export:", borderStyle = "etchedIn",h=350,w=250 )
    cmds.scrollLayout(hst=16,vst=16)
    cmds.columnLayout( adjustableColumn=True, cal = 'left' )
    last = 'a'
    aExist =[]
    if listMat[0][0] == last:
        cmds.text('a'.capitalize()+':',fn = 'boldLabelFont')
    for each in listMat:
        if each[0] == last:
            cmds.checkBox(each, l=each)
        else:
            cmds.text(label= each[0].capitalize()+':',fn = 'boldLabelFont')
            cmds.checkBox(each,l=each)
            last = each[0]  
    cmds.setParent('..') 
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.frameLayout(label = "Export Options:", borderStyle = "etchedIn",h=350)
    cmds.columnLayout( adjustableColumn=True, cal = 'left' )
    exportHeightButton = 108
    cmds.button(label = 'Export Selected:', command = exportCheckedOper, h=exportHeightButton)
    cmds.button(label = 'Export All:', command = batchExport, h=exportHeightButton)
    cmds.button(label = 'Cancel:', command = closeExport, h=exportHeightButton)
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.showWindow( 'materialBatchExport' )
    cmds.window('materialBatchExport', edit=True, widthHeight=[350,350], s = False)
    listMat.append(u'lambert1')

def exportCheckedOper(args = None):
    setDir = cmds.getAttr('materialLibraryDirectory_STORAGE.notes') 
    listMat = cmds.ls( materials=True  )
    listMat.remove(u'lambert1')
    listMat.remove(u'particleCloud1')
    dsp = cmds.ls(type = 'displacementShader')
    if len(dsp)>0:
        for d in dsp:
            listMat.remove(d)   
    checkOptions = []
    
    for each in listMat:
        newName = cmds.ls(each)[0].rpartition(':')[2]
        checkBoxExist = cmds.checkBox(each, query=True, exists=True)
        if checkBoxExist == True:
            onOff = cmds.checkBox(each, query=True, value=True)
            if onOff == True:
                checkOptions.append(each)
                print '%s was selected.' %(newName)
            else:
                print '%s was not selected.' %(newName)

        now = datetime.now()
        
        timeStamp = '%s.%s.%s_%s.%s.%s' % (now.month, now.day, now.year, now.hour, now.minute, now.second )
        
        if (os.path.exists("%s/_backup" %(setDir) )) == False:
            cmds.sysFile("%s/_backup/" %(setDir) , md=1)
        else:
            print "Backup Directory Exists"

    for each in checkOptions:
        newName = cmds.ls(each)[0].rpartition(':')[2]
        if (os.path.exists("%s/_backup/%s" %(setDir,newName) )) == False:
            cmds.sysFile("%s/_backup/%s" %(setDir,newName) , md=1)
        else:
            print "Backup Directory Exists"
        #cmds.select(each)
        SGHOLDER = cmds.polyPlane(n='MATERIALMANAGEREXPORTPLANEDELETETHIS_%s' %(newName), sx=1, sy=1)
        cmds.hyperShade(assign = each)
        cmds.select(SGHOLDER)  
        if (os.path.exists("%s/%s/" %(setDir,newName))) == False:
            cmds.sysFile("%s/%s/" %(setDir,newName) , md=1)
        else:
            cmds.sysFile( "%s/%s/" %(setDir,newName) , rename= "%s/_backup/%s/%s_backup_%s/" %(setDir,newName,newName,timeStamp) )
            cmds.sysFile("%s/%s/" %(setDir,newName) , md=1)
        cmds.file("%s/%s/%s" %(setDir,newName,newName), force=True, exportSelected=True, type="mayaBinary", pr = False)
        cmds.delete(cmds.ls('*MATERIALMANAGEREXPORTPLANEDELETETHIS*'))
        cmds.select(d=1)
        
    cmds.deleteUI('materialBatchExport')



def batchExport(args = None):
    listMat = cmds.ls( materials=True  )
    listMatStart = cmds.ls( materials=True  )
    for each in listMatStart:
        lowerNode = cmds.hyperShade(lun = each)
        underShader = cmds.ls(lowerNode, materials = True)
        if len(underShader) > 0:
            for z in underShader:
                try:
                    listMat.remove(z)
                except:
                    pass
    dsp = cmds.ls(type = 'displacementShader')
    if len(dsp)>0:
        for d in dsp:
            try:
                listMat.remove(d) 
            except:
                pass
    setDir = cmds.getAttr('materialLibraryDirectory_STORAGE.notes')
    for each in listMat:
        newName = cmds.ls(each)[0].rpartition(':')[2]
        if (os.path.exists("%s/_backup" %(setDir) )) == False:
            cmds.sysFile("%s/_backup/" %(setDir) , md=1)
        else:
            print "Backup Directory Exists"
        if (os.path.exists("%s/_backup/%s" %(setDir,newName) )) == False:
            cmds.sysFile("%s/_backup/%s" %(setDir,newName) , md=1)
        else:
            print "Backup Directory Exists"   
        now = datetime.now()
        
        timeStamp = '%s.%s.%s_%s.%s.%s' % (now.month, now.day, now.year, now.hour, now.minute, now.second )
        
    
    #print listMat
    for each in listMat:
        newName = cmds.ls(each)[0].rpartition(':')[2]
        #cmds.select(each)
        SGHOLDER = cmds.polyPlane(n='MATERIALMANAGEREXPORTPLANEDELETETHIS_%s' %(newName), sx=1, sy=1)
        cmds.hyperShade(assign = each)
        cmds.select(SGHOLDER)
       
        if (os.path.exists("%s/_backup/%s" %(setDir,newName) )) == False:
                cmds.sysFile("%s/_backup/%s" %(setDir,newName) , md=1)

        if (os.path.exists("%s/%s/" %(setDir,newName))) == False:
            cmds.sysFile("%s/%s/" %(setDir,newName) , md=1)
        else:
            cmds.sysFile( "%s/%s/" %(setDir,newName) , rename= "%s/_backup/%s/%s_backup_%s/" %(setDir,newName,newName,timeStamp) )
            cmds.sysFile("%s/%s/" %(setDir,newName) , md=1)
    
        cmds.file("%s/%s/%s" %(setDir,newName,newName), force=True, exportSelected=True, type="mayaBinary", pr = False)       
    cmds.delete(cmds.ls('*MATERIALMANAGEREXPORTPLANEDELETETHIS*'))
    cmds.select(d=1)
    
    listMat.append(u'lambert1')
    
    cmds.deleteUI('materialBatchExport')

######END EXPORT#####_________________________________________________________________________________________________


###### IMPORT #####_________________________________________________________________________________________________
def importCheckAll(args=None):
    setDir = cmds.getAttr('materialLibraryDirectory_STORAGE.notes')
          
    backupDir = os.path.abspath(".")
    
    os.chdir("%s" %(setDir) )
    
    allLibraryMaterials = [name for name in os.listdir(".") if os.path.isdir(name)]
    
    os.chdir("%s" %backupDir)
    
    try:
        allLibraryMaterials.remove('_backup')
    except:
        pass
    try:
        allLibraryMaterials.remove('_asset')
    except:
        pass
    for each in allLibraryMaterials:
        cmds.checkBox(each,edit=1,v=1)
    

def importCheckerUI(args = None):
#Batch Import
    if len(cmds.ls('materialLibraryDirectory_STORAGE')) == 0:
        return None
    setDir = cmds.getAttr('materialLibraryDirectory_STORAGE.notes')
          
    backupDir = os.path.abspath(".")
    
    os.chdir("%s" %(setDir) )
    
    allLibraryMaterials = [name for name in os.listdir(".") if os.path.isdir(name)]
    
    os.chdir("%s" %backupDir)
    
    try:
        allLibraryMaterials.remove('_backup')
    except:
        pass
    try:
        allLibraryMaterials.remove('_asset')
    except:
        pass
    allLibraryMaterials=sorted(allLibraryMaterials, key=lambda s: s.lower())
    if cmds.window('materialBatchImport', exists=True):
    
        cmds.deleteUI('materialBatchImport')
    
    cmds.window('materialBatchImport', title= 'jsMaterialLibraryImport')
    
    #cmds.columnLayout( adjustableColumn=True, cal = 'left' )
    cmds.flowLayout()
    cmds.frameLayout(label = "Select Materials to Import", borderStyle = "etchedIn", w=250,h=350)
    #cmds.columnLayout( adjustableColumn=True, cal = 'left' )
    cmds.scrollLayout(hst=16,vst=16)
    #cmds.gridLayout( numberOfColumns=4, cellWidthHeight=(150, 25) )
    
    last = 'a'
    aExist =[]
    if len(allLibraryMaterials) > 0:
        if allLibraryMaterials[0][0] == last:
            aExist.append('yes')
    if 'yes' in aExist:
        cmds.text('a'.capitalize()+':',fn = 'boldLabelFont')
    for each in allLibraryMaterials:
        if each[0] == last:
            cmds.checkBox(each, l=each)
        else:
            cmds.text(label= each[0].capitalize()+':',fn = 'boldLabelFont')
            cmds.checkBox(each,l=each)
            last = each[0]
        
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.frameLayout(label = "Import Options", borderStyle = "etchedIn") 
    #cmds.gridLayout( numberOfColumns=4,numberOfRows = 1, cellWidthHeight=(150, 25) )
    cmds.columnLayout( adjustableColumn=True, cal = 'left' )    
    importButtonHeight = 107
    cmds.button(label = 'Import Selected:', command = importCheckedOper, h = importButtonHeight)
    cmds.button(label = 'Check All', h = importButtonHeight, c=importCheckAll)
    cmds.button(label = 'Cancel:', command = closeInport, h = importButtonHeight)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.showWindow( 'materialBatchImport' )
    cmds.window('materialBatchImport', edit=True, widthHeight=[350,350], s = False)
    



def importCheckedOper(args = None):
    
    #import selected Button
    
    setDir = cmds.getAttr('materialLibraryDirectory_STORAGE.notes')
    
        
    backupDir = os.path.abspath(".")
    
    os.chdir("%s" %(setDir) )
    
    allLibraryMaterials = [name for name in os.listdir(".") if os.path.isdir(name)]
    
    os.chdir("%s" %backupDir)
      
    
    allLibraryMaterials.remove('_backup')
    
    checkOptions = []
    
    for each in allLibraryMaterials:
        checkBoxExist = cmds.checkBox(each, query=True, exists=True)
        if checkBoxExist == True:
            onOff = cmds.checkBox(each, query=True, value=True)
            if onOff == True:
                checkOptions.append(each)
                print '%s was selected.' %(each)
            else:
                print '%s was not selected.' %(each)
      
    for each in checkOptions:
        shaderExists = cmds.ls('*%s*' %(each), materials = 1)
        cmds.hyperShade(o = each)
        prevAssigned = cmds.ls(sl=1)
        cmds.select(d=1)
        lowerNode = cmds.hyperShade(lun = each)
        upperNode = cmds.hyperShade(ldn = each)
        if len(shaderExists) > 0:
                if len(lowerNode) > 0:
                    cmds.delete(lowerNode)
                if len(upperNode) > 0:
                    SG = cmds.ls(upperNode, type = 'shadingEngine')
                    cmds.delete(SG)
                cmds.delete(each)
        cmds.file("%s/%s/%s.mb" %(setDir,each,each), force=True, i=True, type="mayaBinary", dns = True)
        if len(prevAssigned) > 0:
            cmds.select(prevAssigned)
            cmds.hyperShade(assign = each)
            cmds.select(d=1)
    cmds.delete(cmds.ls('*MATERIALMANAGEREXPORTPLANEDELETETHIS*'))
    cmds.deleteUI('materialBatchImport')

######END IMPORT#####_________________________________________________________________________________________________


##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################

def createAssetDir(args=None):
    if len(cmds.ls('materialLibraryDirectory_STORAGE')) == 1:
        setDir = cmds.getAttr('materialLibraryDirectory_STORAGE.notes') 
        if (os.path.exists("%s/_asset" %(setDir) )) == False:
            cmds.sysFile("%s/_asset/" %(setDir) , md=1)
        else:
            print "Asset Directory Exists"
    else:
        print "No Directory is Set"

##################################################################################################################       
def closeImportAsset(args=None):
    cmds.deleteUI('materialAssetImport')


def importPacketMaterials(assetName):
    setDir = cmds.getAttr('materialLibraryDirectory_STORAGE.notes')
           
    backupDir = os.path.abspath(".")
        
    os.chdir("%s" %(setDir) )
        
    allLibraryMaterials = [name for name in os.listdir(".") if os.path.isdir(name)]
    os.chdir("%s" %backupDir)
        
    try:
        allLibraryMaterials.remove('_backup')
    except:
        pass
    materials = cmds.listAttr(assetName,ud=1)
    checkOptions = []
    for each in materials:
        #testing = cmds.attributeQuery(each,node = assetName)
        testing = cmds.getAttr(assetName+'.'+each,)
        if testing == '':
            pass
        else:
            checkOptions.append(each)
        
    for each in checkOptions:
        try:
            if cmds.objExists(each):
                print 'exists'
            else:
                    cmds.file("%s/%s/%s.ma" %(setDir,each,each), force=True, i=True, type="mayaAscii", dns = True)
                    cmds.delete(cmds.ls('*MATERIALMANAGEREXPORTPLANEDELETETHIS*'))
        except:
            pass




def importAssetCheckedOper(args = None):
    

    setDir = cmds.getAttr('materialLibraryDirectory_STORAGE.notes')
    setDir = setDir+'/_asset/'
        
    backupDir = os.path.abspath(".")
    
    os.chdir("%s" %(setDir) )
    
    allLibraryMaterials = [name for name in os.listdir(".") if os.path.isdir(name)]
    
    os.chdir("%s" %backupDir)
        
    allLibraryMaterials.remove('_backup')
    
    checkOptions = []
    
    for each in allLibraryMaterials:
        checkBoxExist = cmds.checkBox(each, query=True, exists=True)
        if checkBoxExist == True:
            onOff = cmds.checkBox(each, query=True, value=True)
            if onOff == True:
                checkOptions.append(each)
                print '%s was selected.' %(each)
            else:
                print '%s was not selected.' %(each)
      
    for each in checkOptions:
        try:
            cmds.delete(each)
        except:
            pass
        cmds.file("%s/%s/%s.mb" %(setDir,each,each), force=True, i=True, type="mayaBinary", dns = True)
        cmds.parent( each, 'materialLibraryDirectory_STORAGE' )
        #importPacketMaterials(each)
    allStor = cmds.ls('materialLibraryDirectory_STORAGE*')
    allStor.remove('materialLibraryDirectory_STORAGE')
    cmds.delete(allStor)
    cmds.delete(cmds.ls('*MATERIALMANAGEREXPORTPLANEDELETETHIS*'))
    cmds.deleteUI('materialAssetImport')
    
    try:
        cmds.textScrollList('assetList',edit =1, ra=1 )
        underList = cmds.listRelatives('materialLibraryDirectory_STORAGE')
        assetList = []
        for each in underList:
            if 'Asset_STORAGE' in each:
                assetList.append(each)
        cmds.textScrollList('assetList',edit = 1, append = assetList,sii=1 )   
    except:
        pass





def importAssetUI(args = None):
    createAssetDir()
    setDir = cmds.getAttr('materialLibraryDirectory_STORAGE.notes')
    setDir = setDir+'/_asset/'
    backupDir = os.path.abspath(".")
    
    os.chdir("%s" %(setDir) )
    
    allLibraryMaterials = [name for name in os.listdir(".") if os.path.isdir(name)]
    
    os.chdir("%s" %backupDir)
    
    try:
        allLibraryMaterials.remove('_backup')
    except:
        pass
    allLibraryMaterials = sorted(allLibraryMaterials, key=lambda s: s.lower())
    if cmds.window('materialAssetImport', exists=True):
    
        cmds.deleteUI('materialAssetImport')
    
    cmds.window('materialAssetImport', title= 'jsShaderPackImport')
    
    #cmds.columnLayout( adjustableColumn=True, cal = 'left' )
    cmds.flowLayout()
    cmds.frameLayout(label = "Select Shader Packs to Import", borderStyle = "etchedIn", w=250,h=350)
    #cmds.columnLayout( adjustableColumn=True, cal = 'left' )
    cmds.scrollLayout(hst=16,vst=16)
    #cmds.gridLayout( numberOfColumns=4, cellWidthHeight=(150, 25) )
    
    for each in allLibraryMaterials:
        cmds.checkBox(each, l=each)
        #cmds.checkBox(each, l=each, onCommand = checkEach, offCommand = uncheckEach)
        
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.frameLayout(label = "Import Options", borderStyle = "etchedIn") 
    #cmds.gridLayout( numberOfColumns=4,numberOfRows = 1, cellWidthHeight=(150, 25) )
    cmds.columnLayout( adjustableColumn=True, cal = 'left' )    
    importButtonHeight = 160      
    cmds.button(label = 'Import Selected:', command = importAssetCheckedOper, h = importButtonHeight)
    cmds.button(label = 'Cancel:', command = closeImportAsset, h = importButtonHeight)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.showWindow( 'materialAssetImport' )
    cmds.window('materialAssetImport', edit=True, widthHeight=[350,350], s = False)

##################################################################################################################


def getMaterialsUsed(assetName):
    materials = cmds.listAttr(assetName,ud=1)
    checkOptions = []
    for each in materials:
        testing = cmds.getAttr(assetName+'.'+each,)
        if testing == '':
            pass
        else:
            shaderHolder = cmds.polyPlane(n='MATERIALMANAGEREXPORTPLANEDELETETHIS_%s' %(each), sx=1, sy=1)
            cmds.delete(ch=1)
            cmds.hyperShade(assign=each)
            checkOptions.append('MATERIALMANAGEREXPORTPLANEDELETETHIS_%s' %(each))  
    cmds.select(checkOptions, assetName)


def publishSelected(args=None):
    createAssetDir()
    allAssets = cmds.listRelatives('materialLibraryDirectory_STORAGE')
    setDir = cmds.getAttr('materialLibraryDirectory_STORAGE.notes')
    setDir = setDir+'/_asset/'
    checkOptions = []  
    for each in allAssets:
        checkBoxExist = cmds.checkBox(each, query=True, exists=True)
        if checkBoxExist == True:
            onOff = cmds.checkBox(each, query=True, value=True)
            if onOff == True:
                checkOptions.append(each) 
        now = datetime.now()
        
        timeStamp = '%s.%s.%s_%s.%s.%s' % (now.month, now.day, now.year, now.hour, now.minute, now.second )
        
        if (os.path.exists("%s/_backup" %(setDir) )) == False:
            cmds.sysFile("%s/_backup/" %(setDir) , md=1)
        else:
            print "Backup Directory Exists"
        if (os.path.exists("%s/_backup/%s" %(setDir,each) )) == False:
            cmds.sysFile("%s/_backup/%s" %(setDir,each) , md=1)
        else:
            print "Backup Directory Exists"
    
    for each in checkOptions:
        cmds.parent( each, world=True )
        getMaterialsUsed(each)        
        if (os.path.exists("%s/%s/" %(setDir,each))) == False:
            cmds.sysFile("%s/%s/" %(setDir,each) , md=1)
        else:
            cmds.sysFile( "%s/%s/" %(setDir,each) , rename= "%s/_backup/%s/%s_backup_%s/" %(setDir,each,each,timeStamp) )
            cmds.sysFile("%s/%s/" %(setDir,each) , md=1)    
        cmds.file("%s/%s/%s" %(setDir,each,each), force=True, exportSelected=True, type="mayaBinary", pr = False)
        cmds.parent(each,'materialLibraryDirectory_STORAGE')
    cmds.delete(cmds.ls('*MATERIALMANAGEREXPORTPLANEDELETETHIS*'))       
    cmds.deleteUI('assetsExport')







def publishAllAssets(args=None):
    createAssetDir()
    allAssets = cmds.listRelatives('materialLibraryDirectory_STORAGE')
    setDir = cmds.getAttr('materialLibraryDirectory_STORAGE.notes')
    setDir = setDir+'/_asset/'
    listMat = cmds.ls( materials=True  )
    checkOptions = []  
    now = datetime.now()
        
    timeStamp = '%s.%s.%s_%s.%s.%s' % (now.month, now.day, now.year, now.hour, now.minute, now.second )
    for each in allAssets:
        if (os.path.exists("%s/_backup" %(setDir) )) == False:
            cmds.sysFile("%s/_backup/" %(setDir) , md=1)
        else:
            print "Backup Directory Exists"
        if (os.path.exists("%s/_backup/%s" %(setDir,each) )) == False:
            cmds.sysFile("%s/_backup/%s" %(setDir,each) , md=1)
        else:
            print "Backup Directory Exists"
        
    for each in allAssets:
        cmds.parent( each, world=True )
        getMaterialsUsed(each)
        if (os.path.exists("%s/%s/" %(setDir,each))) == False:
            cmds.sysFile("%s/%s/" %(setDir,each) , md=1)
        else:
            cmds.sysFile( "%s/%s/" %(setDir,each) , rename= "%s/_backup/%s/%s_backup_%s/" %(setDir,each,each,timeStamp) )
            cmds.sysFile("%s/%s/" %(setDir,each) , md=1)    
        cmds.file("%s/%s/%s" %(setDir,each,each), force=True, exportSelected=True, type="mayaBinary", pr = False)
    cmds.delete(cmds.ls('*MATERIALMANAGEREXPORTPLANEDELETETHIS*'))     
    cmds.deleteUI('assetsExport')





def publishAssetWindow(Args=None):
    if cmds.window('assetsExport', exists=True):
        cmds.deleteUI('assetsExport')
    
    cmds.window('assetsExport', title= 'jsShaderPackPublish')
    #cmds.columnLayout( adjustableColumn=True, cal = 'left' )
    cmds.flowLayout()
    cmds.frameLayout(label = "Select Shader Packs to Publish:", borderStyle = "etchedIn",h=350,w=250 )
    cmds.scrollLayout(hst=16,vst=16)
    cmds.columnLayout( adjustableColumn=True, cal = 'left' )
    #cmds.gridLayout( numberOfColumns=4, cellWidthHeight=(150, 25) )
    allAssets = cmds.listRelatives('materialLibraryDirectory_STORAGE')
    if allAssets > 0:
        for each in allAssets:
            cmds.checkBox(each, l=each)
        
    cmds.setParent('..') 
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.frameLayout(label = "Export Options:", borderStyle = "etchedIn",h=350)
    #cmds.gridLayout( numberOfColumns=4,numberOfRows = 1, cellWidthHeight=(150, 25) )
    cmds.columnLayout( adjustableColumn=True, cal = 'left' )
    exportHeightButton = 108
    cmds.button(label = 'Export Selected:', h=exportHeightButton, c = publishSelected)
    cmds.button(label = 'Export All:', h=exportHeightButton, c = publishAllAssets)
    cmds.button(label = 'Cancel:', h=exportHeightButton,c="cmds.deleteUI('assetsExport')")
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.showWindow( 'assetsExport' )
    cmds.window('assetsExport', edit=True, widthHeight=[350,350], s = False)


###########################################################################################################################################

def createAssetPopUp(args=None):
    if cmds.window('jsAssetCreate', exists=True):
        cmds.deleteUI('jsAssetCreate')
    cmds.window('jsAssetCreate', title= 'jsShaderPackCreate')
    cmds.frameLayout(label = "Create New Shader Pack:", borderStyle = "etchedIn" )
    cmds.columnLayout( adjustableColumn=True, cal = 'center' )
    #cmds.text('Asset Name:')
    cmds.textField('assetNameField')
    cmds.button(label='Create Shader Pack:', c=createAsset,h=35 )
    cmds.showWindow( 'jsAssetCreate' )
    cmds.window('jsAssetCreate', edit=True, widthHeight=[200,80], s = False)
    


def createAsset(args=None):
    assetName = cmds.textField('assetNameField',query=1,text=1)
    checkExists=cmds.ls(assetName+'_Asset_STORAGE')
    if len(checkExists) >0:
        print 'Asset already exists'
        cmds.textField('assetNameField',edit=1,text='')
    else:
        if len(cmds.ls('materialLibraryDirectory_STORAGE')) > 0:
            cmds.group(em=True,name = assetName+'_Asset_STORAGE',parent = 'materialLibraryDirectory_STORAGE')
            cmds.textScrollList('assetList',edit =1, ra=1 )
            underList = cmds.listRelatives('materialLibraryDirectory_STORAGE')
            assetList = []
            for each in underList:
                if 'Asset_STORAGE' in each:
                    assetList.append(each)
                    cmds.textScrollList('assetList',edit = 1, ra=1 )
                    cmds.textScrollList('assetList',edit = 1, append = assetList,sii=1 )
        else:
            cmds.group(name = 'materialLibraryDirectory_STORAGE', em=True)
            cmds.addAttr('materialLibraryDirectory_STORAGE', sn='notes',nn = 'Notes', dt = "string" )
            cmds.setAttr('materialLibraryDirectory_STORAGE.notes', 'No Directory Currently Set',  type = "string",  )
            cmds.group(em=True,name = assetName+'_Asset_STORAGE',parent = 'materialLibraryDirectory_STORAGE')
            cmds.textScrollList('assetList',edit =1, ra=1 )
            underList = cmds.listRelatives('materialLibraryDirectory_STORAGE')
            assetList = []
            for each in underList:
                if 'Asset_STORAGE' in each:
                    assetList.append(each)
                    cmds.textScrollList('assetList',edit = 1, ra=1 )
                    cmds.textScrollList('assetList',edit = 1, append = assetList,sii=1 )
        cmds.deleteUI('jsAssetCreate')

##################################################################################################################

def saveAssetApply(args=None):
    listAsset = cmds.textScrollList('assetList', q = True, si = True )
    if listAsset > 0:
        for each in listAsset:
            assetName = each
    else:
        currentAsset = 'error'
    checkStorageNode = cmds.ls('materialLibraryDirectory_STORAGE')
    if not checkStorageNode:
        cmds.group(name = 'materialLibraryDirectory_STORAGE', em=True)
        cmds.addAttr('materialLibraryDirectory_STORAGE', sn='notes',nn = 'Notes', dt = "string" )
        cmds.setAttr('materialLibraryDirectory_STORAGE.notes', 'No Directory Currently Set',  type = "string",  )       
    listMat = cmds.ls( materials=True  )
    listMat.remove(u'particleCloud1')
    for each in listMat:
        newName = cmds.ls(each)[0].rpartition(':')[2]
        exists = cmds.textField('%s_AssetApplyField' %(newName), query = True, exists=True)
        if exists == True:
            result = cmds.textField('%s_AssetApplyField' %(newName), query = True, text=True)
            testing = cmds.attributeQuery(newName, node=assetName, ex=True )
            if testing == True:
                cmds.setAttr(str(assetName)+'.%s' %(newName), result ,type = "string" )
            else:
                cmds.addAttr(str(assetName), sn=newName,nn = newName, dt = "string" )
                cmds.setAttr(str(assetName)+'.%s' %(newName), result ,type = "string" )
            resultList = result.split()
            if len(resultList) > 0:
                for r in resultList:
                    try:
                        cmds.select(r)
                        cmds.hyperShade(assign=each)
                        cmds.select(d=1)
                    except:
                        pass

def saveAsset(args=None):
    listAsset = cmds.textScrollList('assetList', q = True, si = True )
    if listAsset > 0:
        for each in listAsset:
            assetName = each
    else:
        currentAsset = 'error'
    checkStorageNode = cmds.ls('materialLibraryDirectory_STORAGE')
    if not checkStorageNode:
        cmds.group(name = 'materialLibraryDirectory_STORAGE', em=True)
        cmds.addAttr('materialLibraryDirectory_STORAGE', sn='notes',nn = 'Notes', dt = "string" )
        cmds.setAttr('materialLibraryDirectory_STORAGE.notes', 'No Directory Currently Set',  type = "string",  )       
    listMat = cmds.ls( materials=True  )
    listMat.remove(u'particleCloud1')
    for each in listMat:
        newName = cmds.ls(each)[0].rpartition(':')[2]
        exists = cmds.textField('%s_AssetApplyField' %(newName), query = True, exists=True)
        if exists == True:
            result = cmds.textField('%s_AssetApplyField' %(newName), query = True, text=True)
            testing = cmds.attributeQuery(newName, node=assetName, ex=True )
            if testing == True:
                cmds.setAttr(str(assetName)+'.%s' %(newName), result ,type = "string" )
            else:
                cmds.addAttr(str(assetName), sn=newName,nn = newName, dt = "string" )
                cmds.setAttr(str(assetName)+'.%s' %(newName), result ,type = "string" )
            resultList = result.split()
def closeAssetAssigner(args=None):
    cmds.deleteUI('jsAssetAssigner')


def assignAssetTest(args=None):
    listAsset = cmds.textScrollList('assetList', q = True, si = True )
    if listAsset > 0:
        for each in listAsset:
            assetName = each
    else:
        currentAsset = 'error'   
    listMat = cmds.ls( materials=True  )
    listMat.remove(u'particleCloud1')
    for each in listMat:
        newName = cmds.ls(each)[0].rpartition(':')[2]
        exists = cmds.textField('%s_AssetApplyField' %(newName), query = True, exists=True)
        if exists == True:
            result = cmds.textField('%s_AssetApplyField' %(newName), query = True, text=True)
            resultList = result.split()
            if len(resultList) > 0:
                for r in resultList:
                    try:
                        cmds.select(r)
                        cmds.hyperShade(assign=each)
                        cmds.select(d=1)
                    except:
                        pass
                        
                        
##################################################################################################################
def addSelectedOther(name):
    sel = cmds.ls(sl=1, tr=1)  
    for each in sel:
        current = cmds.textField(name+'_AssetApplyField', query = True, text = True)
        if len(current) > 0:
            new = current + ' ' +each
        else:
            new = each
        cmds.textField(name+'_AssetApplyField', edit = True, text = new )


def assignAssetWindow(args=None):
    if len(cmds.ls('*_Asset_STORAGE')) >0:
        assignAssetWindowFunc()
    else:
        print 'No Asset Storage Nodes Exist'

def assignAssetWindowFunc(args=None):
    listAsset = cmds.textScrollList('assetList', q = True, si = True )
    if listAsset > 0:
        for each in listAsset:
            currentAsset = each
    else:
        currentAsset = 'error'
    listMat = cmds.ls( materials=True  )
    listMatStart = cmds.ls( materials=True )
    downList = []
    for each in listMatStart:
        lowerNode = cmds.hyperShade(lun = each)
        underShader = cmds.ls(lowerNode, materials = True)
        for x in underShader:
            downList.append(x)
    downList = remove_duplicates(downList)
    if len(downList) > 0:
        for z in downList:
            listMat.remove(z)
    listMat.append(u'lambert1')  
    
    listMat=sorted(listMat, key=lambda s: s.lower())
    if cmds.window('jsAssetAssigner', exists=True):
        
        cmds.deleteUI('jsAssetAssigner')
        
    
    cmds.window('jsAssetAssigner', title= currentAsset+' Assignments')
        
    cmds.columnLayout( adjustableColumn=True, cal = 'left' )

    
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.flowLayout()
    cmds.frameLayout(label = "Create Material Assignments for " +str(currentAsset)+":", borderStyle = "etchedIn",h=400,w=600 )
    cmds.scrollLayout(hst=16,vst=16)
    last = 'a'
    aExist =[]
    if listMat[0][0] == last:
        aExist.append('yes')
    if 'yes' in aExist:
        cmds.text('a'.capitalize()+':',fn = 'boldLabelFont')
    for each in listMat:
        if each[0] == last:
            newName = cmds.ls(each)[0].rpartition(':')[2]
            #cmds.rowLayout( nc=2, adjustableColumn=2, columnAlign=(1, 'left'), w= 580 )
            cmds.rowLayout( nc=3, adjustableColumn=3, columnAlign=(1, 'left'), w= 980 )
            cmds.button(newName,label = '+', c = 'jsLookdevAssistant.addSelectedOther("%s")'%newName )
            cmds.text(label = '%s:' %(newName), font = "boldLabelFont",rs=1 )
            cmds.textField('%s_AssetApplyField' %(newName), w =200)
            cmds.setParent('..')
        else:
            cmds.text(label= each[0].capitalize()+':',fn = 'boldLabelFont')
            newName = cmds.ls(each)[0].rpartition(':')[2]
            #cmds.rowLayout( nc=2, adjustableColumn=2, columnAlign=(1, 'left'), w= 580 )
            cmds.rowLayout( nc=3, adjustableColumn=3, columnAlign=(1, 'left'), w= 980 )
            cmds.button(newName,label = '+', c = 'jsLookdevAssistant.addSelectedOther("%s")'%newName )
            cmds.text(label = '%s:' %(newName), font = "boldLabelFont",rs=1 )
            cmds.textField('%s_AssetApplyField' %(newName), w =200)
            last = each[0]
            cmds.setParent('..')

    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.frameLayout(label = "Options:", borderStyle = "etchedIn",h=400,w=100 )
    cmds.columnLayout( adjustableColumn=True, cal = 'left' )
    evenHeight = 93
    cmds.button(label = 'Assign and Save:', c = saveAssetApply, h = evenHeight)
    cmds.button(label = 'Test Assignments:', c = assignAssetTest, h = evenHeight)
    cmds.button(label = 'Save Current:', c = saveAsset, h = evenHeight )
    cmds.button(label = 'Close', c= closeAssetAssigner, h = evenHeight)
    
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.setParent('..')
    
    cmds.showWindow( 'jsAssetAssigner' )
    cmds.window('jsAssetAssigner', edit=True, widthHeight=[705,400], s = False)
    
    for each in listMat:
        newName = cmds.ls(each)[0].rpartition(':')[2]
        testing = cmds.attributeQuery(newName, node=currentAsset, ex=True )
        if testing == True:
            newSet = cmds.getAttr('%s.%s' %(currentAsset, newName) )
            cmds.textField('%s_AssetApplyField' %(newName),edit = True, text = newSet)


def applyAsset(args=None):
    assignAssetWindow()
    assignAssetTest()
    closeAssetAssigner()
    
################################################################################################################################
 

def createAssetWindow(args=None):     
    if cmds.window('jsAssetManager', exists=True):       
        cmds.deleteUI('jsAssetManager')
    
    cmds.window('jsAssetManager', title= 'jsShaderPackManager')
    cmds.frameLayout(label = "jsShaderPackManager:", borderStyle = "etchedIn" )
    
    
    cmds.flowLayout()
    cmds.frameLayout(label = "Shader Packs in Scene:", borderStyle = "etchedIn",w=200 )

    cmds.columnLayout( adjustableColumn=True, cal = 'left' )
    if len(cmds.ls('materialLibraryDirectory_STORAGE')) == 0:
        cmds.textScrollList('assetList', numberOfRows=8, allowMultiSelection=False,  h = 250,append = '',sii =1 )
    else:
        underList = cmds.listRelatives('materialLibraryDirectory_STORAGE')
        if underList > 0:
            assetList = []
            for each in underList:
                if 'Asset_STORAGE' in each:
                    assetList.append(each)
            cmds.textScrollList('assetList', numberOfRows=8, allowMultiSelection=False,  h = 250, append = assetList,sii = 1 )       
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.frameLayout(label = "Asset Functions:", borderStyle = "etchedIn",h=275 )
    cmds.button(label='Create:',c = createAssetPopUp)
    cmds.button(label='Edit:', c= assignAssetWindow)
    cmds.button(label='Import:',c=importAssetUI)
    cmds.button(label='Publish:',c=publishAssetWindow)
    cmds.button(label='Apply Asset:',c=applyAsset)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.showWindow( 'jsAssetManager' )
    cmds.window('jsAssetManager', edit=True, widthHeight=[305,300], s = 0)
######################################################################################



######Arnold Quick Settings#################################################################################
############################################################################################################
############################################################################################################
############################################################################################################

def lowSamples(args=None):
    cmds.setAttr("defaultArnoldRenderOptions.AA_samples", 2)
    cmds.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples",2)
    cmds.setAttr("defaultArnoldRenderOptions.GIGlossySamples",1)
    cmds.setAttr("defaultArnoldRenderOptions.GI_refraction_samples",1)
    cmds.setAttr("defaultArnoldRenderOptions.sss_bssrdf_samples",1)
    cmds.setAttr("defaultArnoldRenderOptions.volume_indirect_samples",1)
    cmds.setAttr("defaultArnoldDriver.tiled", True)
    cmds.setAttr("defaultArnoldDriver.preserveLayerName", True)
    cmds.setAttr("defaultArnoldDriver.halfPrecision", True)

def midSamples(args=None):
    cmds.setAttr("defaultArnoldRenderOptions.AA_samples", 3)
    cmds.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples",2)
    cmds.setAttr("defaultArnoldRenderOptions.GIGlossySamples",2)
    cmds.setAttr("defaultArnoldRenderOptions.GI_refraction_samples",2)
    cmds.setAttr("defaultArnoldRenderOptions.sss_bssrdf_samples",2)
    cmds.setAttr("defaultArnoldRenderOptions.volume_indirect_samples",2)
    cmds.setAttr("defaultArnoldDriver.tiled", True)
    cmds.setAttr("defaultArnoldDriver.preserveLayerName", True)
    cmds.setAttr("defaultArnoldDriver.halfPrecision", True)

def highSamples(args=None):
    cmds.setAttr("defaultArnoldRenderOptions.AA_samples", 5)
    cmds.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples",4)
    cmds.setAttr("defaultArnoldRenderOptions.GIGlossySamples",3)
    cmds.setAttr("defaultArnoldRenderOptions.GI_refraction_samples",2)
    cmds.setAttr("defaultArnoldRenderOptions.sss_bssrdf_samples",2)
    cmds.setAttr("defaultArnoldRenderOptions.volume_indirect_samples",2)
    cmds.setAttr("defaultArnoldDriver.tiled", True)
    cmds.setAttr("defaultArnoldDriver.preserveLayerName", True)
    cmds.setAttr("defaultArnoldDriver.halfPrecision", True)


def mBlurOn(args=None):
    cmds.setAttr("defaultArnoldRenderOptions.mb_en",1)

def mBlurOff(args=None):
    cmds.setAttr("defaultArnoldRenderOptions.mb_en",0)


#quickSettings End  ########################################################################################
############################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
def helpWindow(args=None):
    if cmds.window('jsLookDevAssistantReadMe',exists=True):
        cmds.deleteUI('jsLookDevAssistantReadMe')
    
    window = cmds.window('jsLookDevAssistantReadMe',menuBar=True, title= 'ReadMe',bgc=[.25,.25,.25]) #, s = False
    cmds.scrollLayout(hst=16,vst=16, cr=1)
    cmds.text('jsLookDevAssistant\'s Super Exciting Read Me:', fn = "boldLabelFont")
    cmds.separator( height=10, style='in' )
    
    cmds.text('General Overview:', fn = "boldLabelFont", al="left")
    cmds.text('jsLookDevAssistant is a tool designed to speed up the management and application of shaders. In the General Overview I will only cover the two most important points.' , al="left", ww=1)
    cmds.text('Which are... First - All material assignments in every material applicator in the script are made via gemommetry naming and wildcards. Material Applications can be made to groups and or individual geo in any combination. Secondly is the general existance of the "STORAGE_NODE". The storage node is what stores all of your saved data. Library Paths, Material assignments, etc. To use any "Library" function sucesfully you need to set a directory using "Load Directory". Understanding these two main factors you can basically jump right in and it\'s very straight forward. If you need a more in depth explanation of individual tools, you can find them below. ', al="left", ww=1)
    cmds.separator( height=20, style='in' )
    
    cmds.text('Primary Tools:', fn = "boldLabelFont")
    cmds.separator( height=20, style='in' )
    
    cmds.text('Material Applicator:', fn = "boldLabelFont", al="left")
    cmds.text('Material Applicator does stuff', al="left", ww=1)
    
    cmds.separator( height=15, style='in' )
    
    cmds.text('Shader Pack Manager:', fn = "boldLabelFont", al="left")
    cmds.text('ShaderPackManager does stuff', al="left", ww=1)
    
    cmds.separator( height=15, style='in' )
    
    cmds.text('Load Directory:', fn = "boldLabelFont", al="left")
    cmds.text('Used to set the directory where all exported materials, and asset shaderPacks are exported to.', al="left", ww=1)
    
    cmds.separator( height=15, style='in' )
    
    cmds.text('Import Material from Library:', fn = "boldLabelFont", al="left")
    cmds.text('Opens a UI to choose which materials to import from the library directory.', al="left", ww=1)
    
    cmds.separator( height=15, style='in' )
    
    cmds.text('Publish Material to Library:', fn = "boldLabelFont", al="left")
    cmds.text('Opens a UI to choose which materials to publish into the library directory.', al="left", ww=1)
    
    cmds.separator( height=20, style='in' )

    cmds.text('Bonus Tools:', fn = "boldLabelFont")
    cmds.separator( height=20, style='in' )
    
    cmds.text('Arnold Quick Setting:', fn = "boldLabelFont", al="left")
    cmds.text('Arnold Render Setting Presets created to allow quick changes to predefined low, mid, and High Settings. As well as toggle motion blur.', al="left", ww=1)
    
    cmds.separator( height=15, style='in' )
    
    cmds.text('Rename Shading Groups:', fn = "boldLabelFont", al="left")
    cmds.text('A one click script. Depending on your selection will either... Rename the Shading Groups of the selected materials. Or if no materials are selected rename ALL shading Groups to match the materialNames +"SG"', al="left", ww=1)
    
    cmds.separator( height=15, style='in' )
    
    cmds.text('Texture Path Editor:', fn = "boldLabelFont", al="left")
    cmds.text('A simple tool to replace parts of the file path string. Use "View All File Texture Paths" to view, and select Nodes that you wish to edit. ', al="left", ww=1)
    
    cmds.separator( height=15, style='in' )
    
    cmds.setParent('..')
    cmds.showWindow( window )
    cmds.window('jsLookDevAssistantReadMe', edit=True, widthHeight=[525,400], s = False)
    
####Help Ends   
############################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################


####UI Section Begins####_____________________________________________________________________
if cmds.window('jsLookDevAssistant',exists=True):
    cmds.deleteUI('jsLookDevAssistant')

window = cmds.window('jsLookDevAssistant',menuBar=True, title= 'jsLookdevAssistant %s' %(versionNumber) , w=330, h=100) #, s = False
cmds.columnLayout()

form = cmds.formLayout()
tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)


cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )

cmds.menu( label='Primary Tools', tearOff=True )
cmds.menuItem( label='Load Directory' , c = loadDirectory)
cmds.menuItem( divider=True )
cmds.menuItem( label='Material Manager',c= materialBatchApply)
cmds.menuItem( divider=True )
cmds.menuItem( label='Import Materials', c=importCheckerUI )
cmds.menuItem( label='Publish Materials', c =exportCheckerUi )
cmds.menuItem( divider=True )
cmds.menuItem( label='Shader Pack Manager', c=createAssetWindow )


cmds.menu( label='Bonus Tools', tearOff=True )
cmds.menuItem( subMenu=True, label='Arnold Quick Settings', tearOff=True )
cmds.menuItem( label='Low Samples',c=lowSamples )
cmds.menuItem( label='Mid Samples',c=midSamples )
cmds.menuItem( label='High Samples', c =highSamples)
cmds.menuItem( divider=True )
cmds.menuItem( label='Motion Blur On', c=mBlurOn )
cmds.menuItem( label='Motion Blur Off', c=mBlurOff )
cmds.setParent( '..', menu=True )
cmds.menuItem( label='Rename Shading Groups', c = renameShadingGroups )
cmds.menuItem( label='Texture Path Editor', c=texturePath )

cmds.menu( label='Help', helpMenu=True )
cmds.menuItem( label='Documentation', c = helpWindow )

############ MATERIAL MANAGER UI:############################################_________________________________________________________________________________
child1 = cmds.rowColumnLayout(numberOfColumns=3)


cmds.frameLayout(label = "jsMaterialManager", borderStyle = "etchedIn", w = 320 )


cmds.columnLayout(adj = 1)

cmds.flowLayout(h=32, wr=1)
cmds.textField('TFL_selection', enterCommand= selection, tx= 'Geometry Picker',h=30,w=263,aie = 1)
cmds.button(label='Select:', command= selection,w=50,h=30)
cmds.setParent('..')

cmds.flowLayout(h=32)
cmds.optionMenu('individual', label='Individual Assignment:', changeCommand=printNewMenuItem , h=30,w=263)#optionMenuCommand
for num in range(0,matNumber):
    cmds.menuItem(label= listMat [num] )
cmds.button(label='Update:', command = updateIndividual, h=30)
cmds.setParent('..') 
cmds.setParent('..')


cmds.frameLayout(label = "Material Assignment Tools:", borderStyle = "etchedIn", w = 310)
cmds.columnLayout(adj = 1, rs = 2)
cmds.button(label='Material Applicator:', c = materialBatchApply, h=44)
cmds.button(label = 'Shader Pack Manager:', c = createAssetWindow, h=43)
cmds.setParent('..')

cmds.setParent('..')

cmds.setParent('..')
cmds.setParent('..')


############MATERIAL LIBRARY UI##########_______________________________________________________________________________________________________
child2 = cmds.rowColumnLayout(numberOfColumns=3)

checkStorageNode = cmds.ls('materialLibraryDirectory_STORAGE')
if len(checkStorageNode) > 0: 
    testing = cmds.attributeQuery('notes', node='materialLibraryDirectory_STORAGE', ex=True )
    if testing == True:
        currentSet = cmds.getAttr('materialLibraryDirectory_STORAGE.notes')
else:
    currentSet = 'No Directory Storage File Found'

cmds.columnLayout( adjustableColumn=True, cal = 'left' )

cmds.frameLayout(label = "jsMaterialLibrary", borderStyle = "etchedIn", w = 320 )
cmds.columnLayout( adjustableColumn=True, cal = 'left' )
typeDir = cmds.textField('getDir', text = currentSet, h=30)
cmds.button(label = 'Load Directory:', command = loadDirectory, h=35)
cmds.setParent('..')

cmds.frameLayout(label = "jsPublishMaterial", borderStyle = "etchedIn", w = 300)
cmds.columnLayout(adj = 1, rs = 2)
cmds.button(label = 'Import Material from Library:', command = importCheckerUI, h=44)
cmds.button(label = 'Publish Material to Library:', command = exportCheckerUi, h=44)
cmds.setParent( '..' )


cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'Material Manager'), (child2, 'Material Library')) ) 

cmds.showWindow( window )
cmds.window('jsLookDevAssistant', edit=True, widthHeight=[330,259], s = False)

