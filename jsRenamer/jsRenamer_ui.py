import maya.cmds as cmds
from functools import partial

from . import custom_renamer
from . import field_replacer
from . import template_renamer
from . import bonus_tools
from . import renamer_settings as settings


######CollapseCommands#####################################################
###########################################################################
###########################################################################
class JsRenamer_ui(object):

    def __init__(self):
        print 'Initializing jsRenamer UI...'
        self.frp = field_replacer.FieldReplacer()
        self.trn = template_renamer.TemplateRenamer()
        self.crn = custom_renamer.CustomRenamer()
        self.btl = bonus_tools.BonusTools()
        self.mat_list = []

    def updatePreviewText(self,args=None):
        matField = cmds.textField('materialField',query=True,tx=1)
        posField = cmds.optionMenu('positionField',query=True,v=1)
        bodField = cmds.textField('bodyField',query=True,tx=1)
        numField = cmds.intField('numberField',query=True,v=1)
        sufField = cmds.optionMenu('suffixField',query=True,v=1)

        #Build Padded Number String      
        numPlace = 4
        countNum = len(str(numField))
        addZero = numPlace-countNum
        bufferNumber = ('0'*addZero+str(numField))

        #Updated name
        if numField == -1:
            postName = matField+'_'+posField+'_'+bodField+'_'+sufField
        else:
            postName = matField+'_'+posField+'_'+bodField+'_'+bufferNumber+'_'+sufField
        cmds.text('PreviewText', edit=1,
        label=postName )



    #UI Edits
    def closeBatch(self):
        cmds.frameLayout('batchRenamer',edit = True,h=20)
        checkCloseAdd = cmds.frameLayout('frameAdd',query = True,h=True)
        if checkCloseAdd == 20:
            cmds.window('jsRenamer', edit=True, height=202)     
        else:
            cmds.window('jsRenamer', edit=True, height=355)
         
    def expandBatch(self):
        cmds.frameLayout('batchRenamer',edit = True,h=100)
        checkCloseAdd = cmds.frameLayout('frameAdd',query = True,h=True)
        if checkCloseAdd == 20:
            cmds.window('jsRenamer', edit=True, height=285)
        else:
            cmds.window('jsRenamer', edit=True, height=435)    


    def closeAdd(self):
        cmds.frameLayout('frameAdd',edit = True,h=20)
        checkCloseAdd = cmds.frameLayout('batchRenamer',query = True,h=True)
        if checkCloseAdd == 20:
            cmds.window('jsRenamer', edit=True, height=202)
        else:
            cmds.window('jsRenamer', edit=True, height=285)
         
    def expandAdd(self):
        cmds.frameLayout('frameAdd',edit = True,h=202)
        checkCloseAdd = cmds.frameLayout('batchRenamer',query = True,h=True)
        if checkCloseAdd == 20:
            cmds.window('jsRenamer', edit=True, height=355)
        else:
            cmds.window('jsRenamer', edit=True, height=435)



    def getName(self,name,*args):
        cmds.textField('materialField',edit=True,tx=name)
        self.updatePreviewText()


    def clear_menu(self,menu,parent):
        print menu
        cmds.popupMenu(menu, edit=True, deleteAllItems=True)
        mat_scan = self.btl.material_scan()
        for new_mat in mat_scan:
            cmds.menuItem(l=new_mat, parent=menu, c=partial(self.getName,new_mat))


    def documentation(self,args=None):
        print settings.documentationString



    ###################________________________________________________________________________________________________________________________
    ######UI START#####________________________________________________________________________________________________________________________
    ###################________________________________________________________________________________________________________________________

    def renamer_ui(self):

        if cmds.window('jsRenamer',exists=True):
            cmds.deleteUI('jsRenamer')


        window = cmds.window('jsRenamer', 
            title= 'jsRenamer' , 
            w=330, 
            h=100,
            resizeToFitChildren = 1,
            menuBar=True)

        cmds.menu(label='Material Name Visualizer', tearOff=False)
        cmds.menuItem( label='Visualize Materials', c=self.btl.visualize_materials)
        cmds.menuItem( label='Delete Visualized Materials', c=self.btl.delete_visualizers)


        cmds.menu( label='Bonus Tools', tearOff=False )
        cmds.menuItem( label='Clean Selected xForm Intermediate Shapes', c=self.btl.cleanUpShapes )



        cmds.menu( label='Help', helpMenu=True )
        cmds.menuItem( label='Documentation',
        c=self.documentation)

        cmds.setParent('..')
        cmds.columnLayout('ParentLayout')




        ##### TEMPLATE RENAMER ################################################################
        #######################################################################################
        #######################################################################################


        cmds.frameLayout('moduleRenamer',label = "Template Renamer", w = 450, h=81)

        cmds.flowLayout()


        #material Naming
        cmds.columnLayout(w=150)

        cmds.text('Material Name:')

        cmds.flowLayout(w=150,h=20)
        cmds.textField('materialField',
        w=135,
        text='default',
        tcc=self.updatePreviewText )

        btn = cmds.nodeIconButton( style='iconOnly', image1='popupMenuIcon.png',h=19)



        #postMenuCommand
        popup = cmds.popupMenu('materials_popup', parent=btn, ctl=False, button=1, postMenuCommand=self.clear_menu)
        for mtl in settings.commonMtls:
            cmds.menuItem(mtl, l=mtl,parent='materials_popup', c=partial(self.getName,mtl))

        cmds.setParent('..')
        cmds.button('matRep',l='Replace', w=150,c=self.frp.replaceMaterial )
        cmds.setParent('..')





        #positon
        cmds.columnLayout(w=55)
        cmds.text('Position:',w=45)
        #availPos = ['C','L','R','F','B','U','D','CF','CB','CU','CD','LF','LB','LU','LD','RF','RB','RU','RD','FU','FD','BU','BD']
        cmds.optionMenu('positionField',w=52, cc=self.updatePreviewText)
        for pos in settings.availPos:
            cmds.menuItem( label=pos )


        cmds.button('posRep', l='Replace',w=52, c=self.frp.replacePosition)


        cmds.setParent('..')






        #BodyName
        cmds.columnLayout()
        cmds.text('Body Name:')
        cmds.textField('bodyField',
        text='default',
        w=110,
        tcc=self.updatePreviewText)


        cmds.button('bodRep',l='Replace',w=110, c=self.frp.replaceBody)


        cmds.setParent('..')






        ###Numbering_______________




        cmds.columnLayout(w=60)
        cmds.text('Numbering:')

        cmds.intField('numberField',
        minValue=-1,
        maxValue=9999,
        value=1,
        w=60,
        h=44,
        cc=self.updatePreviewText)

        #cmds.button('numRep',l='Replace',w=60)
        cmds.setParent('..')





        ###Suffix Naming


        #availSuffix=['GES','GEP','PLY','NRB']
        cmds.columnLayout(w=68)
        cmds.text('Suffix:')
        cmds.optionMenu('suffixField',w=65, cc=self.updatePreviewText)
        for suf in settings.availSuffix:
            cmds.menuItem(label = suf)
            


        cmds.button('sufRep',l='Replace',w=65,c=self.frp.replaceGeoSuffix )




        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')


        cmds.columnLayout(h=50)

        #cmds.textField('PreviewField',w=450,ed=0)
        cmds.text('PreviewText',
        label='default_C_default_0001_GES',
        bgc=[.2,.2,.2],
        w=450,
        h=25,
        fn='boldLabelFont')


        cmds.button('Template Rename', w=450,c=self.trn.exTemplateRenamer )
        #cmds.separator(hr=1, style='in',w=405)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')




        





        ##### Full Renamer##################################################################################################
        ####################################################################################################################
        ####################################################################################################################
        cmds.columnLayout()
        space ='                                                                       '

        cmds.frameLayout('batchRenamer',
        label = "Custom Renamer" + space + "# = Number Padding",
        w = 450,
        h=20,
        cl=1,
        cll=1,
        cc=self.closeBatch,
        ec = self.expandBatch )


        cmds.columnLayout( adjustableColumn=True, cal = 'left' )

        cmds.textField('fullRenamer',text = 'material_C_bodyName_####_GES')

        cmds.intSliderGrp('fullRenameStart', 
        field=True, 
        minValue=1, 
        maxValue=100,
        fmx = 100000, 
        v =1,
        cal = [1,'left'] )

#       cmds.separator( height=5, style='in' )
        cmds.separator(height=5)
        cmds.button('fullRenamerExecute',label = 'Custom Rename', c = self.crn.customRename)
        cmds.setParent('..')
        cmds.setParent('..')










        ######Replacers######################################################################
        #####################################################################################
        #####################################################################################



        cmds.frameLayout('frameAdd',
        label = "Additional/Replacement Renamer",
        w = 450,
        h=20,
        cl=1,
        cll=1,
        cc=self.closeAdd,
        ec=self.expandAdd )

        cmds.columnLayout( adjustableColumn=True, cal = 'left' )




        ###Replacer
        cmds.separator( height=5, style='in' )
        cmds.flowLayout()
        cmds.text('Replace This: ')
        cmds.textField('replacerOldField',w=374)
        cmds.setParent('..')




        cmds.flowLayout()
        cmds.text('With This: ')
        cmds.textField('replacerNewField', w=288)
        cmds.button(label = 'Replace', w = 105, h=20,c=self.frp.replacer )
        cmds.setParent('..')
        cmds.separator( height=5)




        #####Adding#####




        ###Add Prefix
        cmds.flowLayout()
        cmds.text('Add Prefix: ')
        cmds.textField('addPrefixField', w=282)
        cmds.button(label = 'Add Prefix', w = 105, h=20,c=self.frp.addPrefix )
        cmds.setParent('..')
        ###Add Suffix
        cmds.flowLayout()
        cmds.text('Add Suffix: ')
        cmds.textField('addSuffixField', w=282)
        cmds.button(label = 'Add Suffix', w = 108, h=20,c=self.frp.addSuffix )
        cmds.setParent('..')
        cmds.separator( height=5)





        #####Replacing#####

        ###Replace Prefix
        cmds.flowLayout()
        cmds.text('Replace Prefix: ')
        cmds.textField('replacePrefixField', w=263)
        cmds.button(label = 'Replace', w = 105, h=20,c=self.frp.replacePrefix )
        cmds.setParent('..')








        ###Replace Suffix
        cmds.flowLayout()
        cmds.text('Replace Suffix: ')
        cmds.textField('replaceSuffixField', w=263)
        cmds.button(label = 'Replace', w = 105, h=20,c=self.frp.replaceSuffix )
        cmds.setParent('..')
        cmds.separator( height=5)




        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.showWindow( window )
        cmds.window('jsRenamer', edit=True, widthHeight=[454,202], s = False)

        #cmds.window('jsRenamer',query=True,widthHeight=True)



def launch_ui():
    uiObject = JsRenamer_ui()
    uiObject.renamer_ui()
