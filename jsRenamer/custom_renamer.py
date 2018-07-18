import maya.cmds as cmds

class CustomRenamer(object):

    def __init__(self):
        print 'Initializing jsRenamer CustomRenamer...'


    ###Full Renamer
    def customRename(self, args=None):
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
