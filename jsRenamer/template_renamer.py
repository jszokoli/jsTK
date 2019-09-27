import maya.cmds as cmds
from . import renamer_settings as settings

class TemplateRenamer(object):

    def __init__(self):
        print 'Initializing jsRenamer TemplateRenamer...'



    def templateRenamer(self,args=None):
        #Gather Field Information
        matField = cmds.textField('materialField',query=True,tx=1)
        posField = cmds.optionMenu('positionField',query=True,v=1)
        bodField = cmds.textField('bodyField',query=True,tx=1)
        numField = cmds.intField('numberField',query=True,v=1)
        sufField = cmds.optionMenu('suffixField',query=True,v=1)
            
        #List of currently selected geometry
        renamerSel = cmds.ls(sl=1)
        #Build Naming from Fields  
        #firstPart = matField+'Mtl'+'_'+posField+'_'+bodField
        firstPart = matField+'_'+posField+'_'+bodField
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
            #print zeroBuffer
            #created buffer Number        
            bufferNumber = ('0'*zeroBuffer+str(newNumber))
            #print bufferNumber
            # If the field Displays -1 no numbering will occur
            if int(startNum) > -1:
                numCrunch =  '_'+bufferNumber
                #newNameFullRenamer = wantedNaming.replace(replacerZeroes,bufferNumber)
            else:
                numCrunch = ''
            newNameFullRenamer = firstPart+numCrunch+endPart
            #print newNameFullRenamer
            try:
                cmds.rename(each[1],newNameFullRenamer)
            except:
                pass
        # if matField not in settings.commonMtls:
        #     settings.commonMtls.append(matField)
    def exTemplateRenamer(self,args=None):
        self.templateRenamer()
        self.templateRenamer()