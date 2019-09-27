import maya.cmds as cmds
from . import renamer_settings as settings

class FieldReplacer(object):

    def __init__(self):
        print 'Initializing jsRenamer FieldReplacer...'
        #replaceMaterial = self.replaceMaterial


    def checkTemplate(self,node):
        #availPos = ['C','L','R','LF','RF','LB','RB','U','B']
        #availSuf=['GES','GEP','PLY','NRB']


        #sel = cmds.ls(sl=1)
        #for node in sel:
        splitNode = node.split('_')
        #print splitNode
        #print splitNode[0][-3:]
        #check if correct amount of fields
        if len(splitNode) == 5:
            return True
        else:
            return False
            



    ##########################################
    #####REPLACE FIELD########################
    ##########################################


    def replaceMaterial(self, args=None):
        ReplaceSel = cmds.ls(sl=1)
        prefixReplace = cmds.textField('materialField',query=True,tx=1)
        prefixReplace= prefixReplace
        if prefixReplace == '':
            pass
        else:
            for each in ReplaceSel:
                if self.checkTemplate(each) == True:
                    if '|' in each:
                        replacerOldName=each.split('|')[-1]
                    else:
                        replacerOldName = each
                    prefixSplit = replacerOldName.split('_',1)
                    prefixReplaceName = prefixReplace+ '_' +str(prefixSplit[1])
                    #print prefixReplaceName
                    cmds.rename(each,prefixReplaceName)
                else:
                    cmds.error(each+' does not match naming Template (default_C_default_0000_???)')



    def replacePosition(self, args=None):
        ReplaceSel = cmds.ls(sl=1)
        positionReplace = cmds.optionMenu('positionField',query=True,v=1)
        for each in ReplaceSel:
            if self.checkTemplate(each) == True:
                #print each
                if '|' in each:
                    replacerOldName=each.split('|')[-1]
                else:
                    replacerOldName = each
                positionSplit = replacerOldName.split('_')
                newPosName = positionSplit[0]+'_'+positionReplace+'_'+positionSplit[2]+'_'+positionSplit[3]+'_'+positionSplit[4]
                #print newPosName
                cmds.rename(each,newPosName)
            else:
                cmds.error(each+' does not match naming Template (default_C_default_0000_???)')




    def replaceBody(self, args=None):
        ReplaceSel = cmds.ls(sl=1)
        bodyReplace = cmds.textField('bodyField',query=True,tx=1)
        for each in ReplaceSel:
            if self.checkTemplate(each) == True:
                #print each
                if '|' in each:
                    replacerOldName=each.split('|')[-1]
                else:
                    replacerOldName = each
                bodySplit = replacerOldName.split('_')
                newBodyName = bodySplit[0]+'_'+bodySplit[1]+'_'+bodyReplace+'_'+bodySplit[3]+'_'+bodySplit[4]
                #print newBodyName
                cmds.rename(each,newBodyName)
            else:
                cmds.error(each+' does not match naming Template (default_C_default_0000_???)')







    ###Replace GEO_Suffix
    def replaceGeoSuffix(self, args=None):
        ReplaceSel = cmds.ls(sl=1)
        suffixReplace = cmds.optionMenu('suffixField',query=True,v=1)
        for each in ReplaceSel:
            if self.checkTemplate(each) == True:
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
                cmds.error(each+' does not match naming Template (default_C_default_0000_???)')
















          
    ###Replacer




    def replacer(self, args=None):
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
    def addPrefix(self, args=None):
        prefixSel = cmds.ls(sl=1)
        prefixAddition = cmds.textField('addPrefixField',query = True,text=True)
        for each in prefixSel:
            newPrefixName = prefixAddition+each
            print newPrefixName
            cmds.rename(each,newPrefixName)




    ###Suffix Add
    def addSuffix(self, args=None):
        suffixSel = cmds.ls(sl=1)
        suffixAddition = cmds.textField('addSuffixField',query = True,text=True)
        for each in suffixSel:
            newSuffixName = each+suffixAddition
            print newSuffixName
            cmds.rename(each,newSuffixName)
             
    ###Replace Prefix
    def replacePrefix(self, args=None):
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
    def replaceSuffix(self, args=None):
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
















