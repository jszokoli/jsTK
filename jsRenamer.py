import maya.cmds as cmds
from functools import partial


####################
#jsRenamer DEV#####
####################




#Author: Joseph Szokoli
#Website: cargocollective.com/josephSzokoli




#Help:
#To create a shelf icon, move jsRenamer.py to your scripts folder and assign the following command to the shelf.
#import jsRenamer
#reload(jsRenamer)




#Version Number################
versionNumberRename = 'DEV'###
###############################




### ChangeLog: ################################################################################
###v1.0 Initial 
###v1.1
#Fixed Error in full renamer
##Changed Default name
##Added ability to rename without using ####.
###v1.2
###Fixed Name Clash Bug in replacer.






def checkTemplate(node):
    availPos = ['C','L','R','LF','RF','LB','RB','U','B']
    availSuf=['GES','GEP','PLY','NRB']
    #sel = cmds.ls(sl=1)
    #for node in sel:
    splitNode = node.split('_')
    #print splitNode
    #print splitNode[0][-3:]
    #check if correct amount of fields
    if len(splitNode) == 4:
        return True
        '''
        #check if material prefix ends in MTL
        if splitNode[0][-3:] == 'Mtl':
            #Check if field has 2 or less letters
            if splitNode[1] in availPos:
                if splitNode[3] in availSuf:
                    print splitNode[2][-4:]
            else:
                pass
        else:
            pass
        '''
    else:
        return False
        










###Full Renamer
def fullRenamer(args=None):
    renamerSel = cmds.ls(sl=1)
    wantedNaming = cmds.textField('fullRenamer',query = True, text = True)
    numPlace = wantedNaming.count('#')
    startNum = cmds.intSliderGrp('fullRenameStart',query = True, value = True)
    #print startNum
    for each in enumerate(renamerSel):
        listAmount = each[0]  
        if '|' in each[1]:
            oldName=each[1].split('|')[-1]
        else:
            oldName = each[1]
        newNumber = listAmount + startNum
        #print newNumber
        amountOfNew = len(str(newNumber))
        zeroBuffer = numPlace - amountOfNew
        #print zeroBuffer
        replacerZeroes = ('#'*numPlace)
        bufferNumber = ('0'*zeroBuffer+str(newNumber))
        #print bufferNumber
        if numPlace > 0:
            newNameFullRenamer = wantedNaming.replace(replacerZeroes,bufferNumber)
        else:
            newNameFullRenamer = wantedNaming
        #print newNameFullRenamer
        try:
            cmds.rename(each[1],newNameFullRenamer)
        except:
            pass
            
def templateRenamer(args=None):
    #Gather Field Information
    matField = cmds.textField('materialField',query=True,tx=1)
    posField = cmds.optionMenu('positionField',query=True,v=1)
    bodField = cmds.textField('bodyField',query=True,tx=1)
    numField = cmds.intField('numberField',query=True,v=1)
    sufField = cmds.optionMenu('suffixField',query=True,v=1)
        
    #List of currently selected geometry
    renamerSel = cmds.ls(sl=1)
    #Build Naming from Fields  
    firstPart = matField+'Mtl'+'_'+posField+'_'+bodField
    #print firstPart
    #Start Number
    startNum = str(numField)
    #Geo suffix naming
    endPart = '_'+sufField    
    numberBuffer=''
    #print startNum
        
    #Enumerated For loop of geo
    for each in enumerate(renamerSel):
        ###split | to resolve clash names and to have variables for both old and shortname
        listAmount = each[0]  
        if '|' in each[1]:
            oldName=each[1].split('|')[-1]
        else:
            oldName = each[1]   
        #New number is your startNumber +1 for each iteration of the for loop
        newNumber = listAmount + int(startNum)
        #print newNumber
        
        #Counts digits of your newNumber        
        amountOfNew = len(str(newNumber))
        #print amountOfNew
        #Template Name always has 4 digits        
        numPlace = 4
        #Calculates zeroes needed to buffer for 4 digits        
        zeroBuffer = numPlace - amountOfNew
       # print zeroBuffer
        #created buffer Number        
        bufferNumber = ('0'*zeroBuffer+str(newNumber))
        #print bufferNumber
        # If the field Displays -1 no numbering will occur
        if int(startNum) > -1:
            numCrunch =  bufferNumber
            #newNameFullRenamer = wantedNaming.replace(replacerZeroes,bufferNumber)
        else:
            numCrunch = ''
        newNameFullRenamer = firstPart+numCrunch+endPart
        #print newNameFullRenamer
        try:
            cmds.rename(each[1],newNameFullRenamer)
        except:
            pass


##########################################
#####REPLACE FIELD########################
##########################################


def replaceMaterial(args=None):
    prefixReplaceSel = cmds.ls(sl=1)
    prefixReplace = cmds.textField('materialField',query=True,tx=1)
    prefixReplace= prefixReplace+'Mtl'
    if prefixReplace == '':
        pass
    else:
        for each in prefixReplaceSel:
            if checkTemplate(each) == True:
                if '|' in each:
                    replacerOldName=each.split('|')[-1]
                else:
                    replacerOldName = each
                prefixSplit = replacerOldName.split('_',1)
                prefixReplaceName = prefixReplace+ '_' +str(prefixSplit[1])
                #print prefixReplaceName
                cmds.rename(each,prefixReplaceName)
            else:
                cmds.error(each+' does not match naming Template (defaultMtl_C_default0000_???)')






















###Replace GEO_Suffix
def replaceGeoSuffix(args=None):
    suffixReplaceSel = cmds.ls(sl=1)
    suffixReplace = cmds.optionMenu('suffixField',query=True,v=1)
    for each in suffixReplaceSel:
        if checkTemplate(each) == True:
            #print each
            if '|' in each:
                replacerOldName=each.split('|')[-1]
            else:
                replacerOldName = each
            suffixSplit = replacerOldName.rsplit('_',1)
            suffixReplaceName = suffixSplit[0] + '_' +suffixReplace
            #print suffixReplaceName
            cmds.rename(each,suffixReplaceName)
        else:
            cmds.error(each+' does not match naming Template (defaultMtl_C_default0000_???)')








      
###Replacer




def replacer(Args=None):
    replacerSel = cmds.ls(sl=1)
    replacerOld = cmds.textField('replacerOldField',query = True,text=True)
    replacerNew = cmds.textField('replacerNewField',query = True,text=True)
    for each in replacerSel:
        if '|' in each:
            replacerOldName=each.split('|')[-1]
        else:
            replacerOldName = each
        replacerNewName = replacerOldName.replace(replacerOld,replacerNew)
        print replacerNewName
        cmds.rename(each, replacerNewName)








         
###PrefixAdd
def addPrefix(args=None):
    prefixSel = cmds.ls(sl=1)
    prefixAddition = cmds.textField('addPrefixField',query = True,text=True)
    for each in prefixSel:
        newPrefixName = prefixAddition+each
        print newPrefixName
        cmds.rename(each,newPrefixName)




###Suffix Add
def addSuffix(args=None):
    suffixSel = cmds.ls(sl=1)
    suffixAddition = cmds.textField('addSuffixField',query = True,text=True)
    for each in suffixSel:
        newSuffixName = each+suffixAddition
        print newSuffixName
        cmds.rename(each,newSuffixName)
         
###Replace Prefix
def replacePrefix(args=None):
    prefixReplaceSel = cmds.ls(sl=1)
    prefixReplace = cmds.textField('replacePrefixField',query = True,text=True)
    if prefixReplace == '':
        pass
    else:
        for each in prefixReplaceSel:
            try:
                    if '|' in each:
                        replacerOldName=each.split('|')[-1]
                    else:
                        replacerOldName = each
                    prefixSplit = replacerOldName.split('_',1)
                    prefixReplaceName = prefixReplace+ '_' +str(prefixSplit[1])
                    print prefixReplaceName
                    cmds.rename(each,prefixReplaceName)
            except:
                    pass




         
         
###Replace Geo Suffix
def replaceSuffix(args=None):
    suffixReplaceSel = cmds.ls(sl=1)
    suffixReplace = cmds.textField('replaceSuffixField',query = True,text=True)
    if suffixReplace == '':
        pass
    else:
        for each in suffixReplaceSel:
            try:
                    if '|' in each:
                        replacerOldName=each.split('|')[-1]
                    else:
                        replacerOldName = each
                    suffixSplit = replacerOldName.rsplit('_',1)
                    suffixReplaceName = suffixSplit[0] + '_' +suffixReplace
                    print suffixReplaceName
                    cmds.rename(each,suffixReplaceName)
            except:
                    pass






















######CollapseCommands#####################################################
###########################################################################
###########################################################################




def closeBatch(args=None):
    cmds.frameLayout('batchRenamer',edit = True,h=20)
    checkCloseAdd = cmds.frameLayout('frameAdd',query = True,h=True)
    if checkCloseAdd == 20:
        cmds.window('jsRenamer', edit=True, widthHeight=[409,178], s = False)     
    else:
        cmds.window('jsRenamer', edit=True, widthHeight=[409,332], s = False)
     
def expandBatch(args=None):
    cmds.frameLayout('batchRenamer',edit = True,h=100)
    checkCloseAdd = cmds.frameLayout('frameAdd',query = True,h=True)
    if checkCloseAdd == 20:
        cmds.window('jsRenamer', edit=True, widthHeight=[409,255], s = False)
    else:
        cmds.window('jsRenamer', edit=True, widthHeight=[409,412], s = False)    








def closeAdd(args=None):
    cmds.frameLayout('frameAdd',edit = True,h=20)
    checkCloseAdd = cmds.frameLayout('batchRenamer',query = True,h=True)
    if checkCloseAdd == 20:
        cmds.window('jsRenamer', edit=True, widthHeight=[409,178], s = False)
    else:
        cmds.window('jsRenamer', edit=True, widthHeight=[409,255], s = False)
     
def expandAdd(args=None):
    cmds.frameLayout('frameAdd',edit = True,h=173)
    checkCloseAdd = cmds.frameLayout('batchRenamer',query = True,h=True)
    if checkCloseAdd == 20:
        cmds.window('jsRenamer', edit=True, widthHeight=[409,327], s = False)
    else:
        cmds.window('jsRenamer', edit=True, widthHeight=[409,408], s = False)






def getName(name,*args):
    cmds.textField('materialField',edit=True,tx=name)
















###################________________________________________________________________________________________________________________________
######UI START#####________________________________________________________________________________________________________________________
###################________________________________________________________________________________________________________________________


if cmds.window('jsRenamer',exists=True):
    cmds.deleteUI('jsRenamer')




window = cmds.window('jsRenamer', title= 'jsRenamer_%s' %versionNumberRename , w=330, h=100,resizeToFitChildren = 1,menuBar=True)




cmds.menu( label='Bonus Tools', tearOff=False )
'''
cmds.menuItem( subMenu=True, label='Arnold Quick Settings', tearOff=False )
cmds.menuItem( label='Low Samples')
cmds.menuItem( divider=True )
cmds.menuItem( label='Motion Blur On')
cmds.menuItem( label='Motion Blur Off')
cmds.setParent( '..', menu=True )
'''
cmds.menuItem( label='Fix Shape Names')






cmds.menu( label='Help', helpMenu=True )
cmds.menuItem( label='Documentation')




cmds.setParent('..')
















cmds.columnLayout()




##### TEMPLATE RENAMER ################################################################
#######################################################################################
#######################################################################################




cmds.frameLayout('moduleRenamer',label = "Template Renamer", borderStyle = "etchedIn", w = 405, h=81)


cmds.flowLayout()




#material Naming
cmds.columnLayout()




cmds.text('Material Name:')
#cmds.frameLayout('materials',w=150,h=150)
#cmds.columnLayout()
commonMtls = ['metal','plastic','leather','glass','chrome','wood','stone','rubber']


cmds.flowLayout()
cmds.textField('materialField',w=96,text='default')
btn = cmds.nodeIconButton( style='iconOnly', image1='popupMenuIcon.png')




popup = cmds.popupMenu(parent=btn, ctl=False, button=1)
#item1 = cmds.menuItem(l='Item1', c="print btname")
#cmds.menuItem(l='Item2', c="print 'btname'")
for mtl in commonMtls:
    cmds.menuItem(l=mtl, c=partial(getName,mtl))
cmds.setParent('..')
#cmds.setParent('..')
cmds.button('matRep',l='Replace', w=110,c=replaceMaterial)
#cmds.setParent('..')
cmds.setParent('..')
#cmds.setParent('..')
#cmds.setParent('..')




cmds.separator(hr=0, style='in',h=150)








#positon
cmds.columnLayout(w=45)
cmds.text('Position:',w=45)
availPos = ['C','L','R','F','B','U','D','CF','CB','CU','CD','LF','LB','LU','LD','RF','RB','RU','RD','FU','FD','BU','BD']
cmds.optionMenu('positionField',w=45)
for pos in availPos:
    cmds.menuItem( label=pos )
'''
cmds.menuItem( label='C' )
cmds.menuItem( label='L' )
cmds.menuItem( label='R' )
cmds.menuItem( label='LF' )
cmds.menuItem( label='RF' )
cmds.menuItem( label='LB' )
cmds.menuItem( label='RB' )
cmds.menuItem( label='U' )
cmds.menuItem( label='B' )
'''


cmds.button('posRep', l='Replace',w=45)




cmds.setParent('..')




cmds.separator(hr=0, style='in',h=150)




#BodyName
cmds.columnLayout()
cmds.text('Body Name:')
cmds.textField('bodyField',text='default',w=110)


cmds.button('bodRep',l='Replace',w=110)


cmds.setParent('..')


cmds.separator(hr=0, style='in',h=150)








###Numbering_______________




cmds.columnLayout(w=60)
cmds.text('Numbering:')
#cmds.flowLayout()
#cmds.intSliderGrp('fullRenameStart', field=True, minValue=-1, maxValue=100,fmx = 100000, v =1 , cal = [1,'left'],w=150 )
'''
cmds.optionMenu('numberOrder')
for i in range(-1,500):
     cmds.menuItem( label=i )
cmds.optionMenu('numberOrder',edit=True,select=3)
'''


cmds.intField('numberField', minValue=-1, maxValue=9999, value=1,w=60 )
#cmds.textField('numberField',text='1')
#cmds.textField()
#cmds.setParent('..')
cmds.button('numRep',l='Replace',w=60)
cmds.setParent('..')




cmds.separator(hr=0, style='in',h=150)








###Suffix Naming










availSuffix=['GES','GEP','PLY','NRB']
cmds.columnLayout(w=50)
cmds.text('Suffix:')
cmds.optionMenu('suffixField',w=50)
for suf in availSuffix:
    cmds.menuItem(label = suf)
    
'''
cmds.menuItem( label='GES' )
cmds.menuItem( label='GEP' )
cmds.menuItem( label='PLY' )
cmds.menuItem( label='NRB' )
'''


cmds.button('sufRep',l='Replace',w=50,c=replaceGeoSuffix)




cmds.setParent('..')




#cmds.separator(hr=0, style='in',h=150)




cmds.setParent('..')


cmds.setParent('..')


cmds.columnLayout(h=26)


cmds.button('Template Rename', w=405,c=templateRenamer)
cmds.separator(hr=1, style='in',w=405)
cmds.setParent('..')
cmds.setParent('..')
cmds.setParent('..')
cmds.setParent('..')




cmds.setParent('..')


cmds.columnLayout()


##### Full Renamer##################################################################################################
####################################################################################################################
####################################################################################################################
space ='                                                              '
#cmds.frameLayout('batchRenamer',label = "Custom Renamer" + space + "# = Zero Buffer", borderStyle = "etchedIn", w = 405, h=95,cl=1,cll=1,cc=closeBatch, ec = expandBatch)
cmds.frameLayout('batchRenamer',label = "Custom Renamer" + space + "# = Zero Buffer", borderStyle = "etchedIn", w = 405, h=20,cl=1,cll=1,cc=closeBatch, ec = expandBatch)
cmds.columnLayout( adjustableColumn=True, cal = 'left' )
cmds.textField('fullRenamer',text = 'defaultMtl_bodyName####_GES')
cmds.intSliderGrp('fullRenameStart', field=True, minValue=1, maxValue=100,fmx = 100000, v =1,cal = [1,'left'] )
cmds.separator( height=5, style='in' )
cmds.button('fullRenamerExecute',label = 'Custom Rename', c = fullRenamer)
cmds.setParent('..')
cmds.setParent('..')


















######Replacers######################################################################
#####################################################################################
#####################################################################################




#cmds.frameLayout('frameAdd',label = "Additional/Replacement Renamer", borderStyle = "etchedIn", w = 405, h=173,cll=1,cc=closeAdd, ec = expandAdd )
cmds.frameLayout('frameAdd',label = "Additional/Replacement Renamer", borderStyle = "etchedIn", w = 405, h=20,cl=1,cll=1,cc=closeAdd, ec = expandAdd )
cmds.columnLayout( adjustableColumn=True, cal = 'left' )




###Replacer
cmds.separator( height=5, style='in' )
cmds.flowLayout()
cmds.text('Replace This: ')
cmds.textField('replacerOldField',w=332)
cmds.setParent('..')




cmds.flowLayout()
cmds.text('With This: ')
cmds.textField('replacerNewField', w=288)
cmds.button(label = 'Replace', w = 60, h=20,c=replacer)
cmds.setParent('..')
cmds.separator( height=5, style='in' )




#####Adding#####




###Add Prefix
cmds.flowLayout()
cmds.text('Add Prefix: ')
cmds.textField('addPrefixField', w=282)
cmds.button(label = 'Add Prefix', w = 60, h=20,c=addPrefix)
cmds.setParent('..')
###Add Suffix
cmds.flowLayout()
cmds.text('Add Suffix: ')
cmds.textField('addSuffixField', w=282)
cmds.button(label = 'Add Suffix', w = 60, h=20,c=addSuffix)
cmds.setParent('..')
cmds.separator( height=5, style='in' )








#####Replacing#####




###Replace Prefix
cmds.flowLayout()
cmds.text('Replace Prefix: ')
cmds.textField('replacePrefixField', w=263)
cmds.button(label = 'Replace', w = 60, h=20,c=replacePrefix)
cmds.setParent('..')








###Replace Suffix
cmds.flowLayout()
cmds.text('Replace Suffix: ')
cmds.textField('replaceSuffixField', w=263)
cmds.button(label = 'Repalce', w = 60, h=20,c=replaceSuffix)
cmds.setParent('..')
cmds.separator( height=5, style='in' )




cmds.setParent('..')




cmds.setParent('..')
cmds.setParent('..')
cmds.setParent('..')
cmds.setParent('..')
cmds.showWindow( window )
cmds.window('jsRenamer', edit=True, widthHeight=[409,178], s = True)


#[409,378]
#cmds.window('jsRenamer',query=True,widthHeight=True)

