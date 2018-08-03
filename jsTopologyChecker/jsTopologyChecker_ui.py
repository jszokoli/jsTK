import maya.cmds as cmds
from . import jsTopologyCheckers
from . import settings

###TOPOLOGY CHECKERS###

#TriangleChecker______________________________________________________________________________________________________________________________________________________
#RED = [.6,0,0]
#GREEN = [0,.6,0]

#color1 = [.463,.608,.747] #red
#color2 = [.2,.2,.2] #green


class JsTopologyChecker_ui(object):

    def __init__(self):
        print 'Initializing jsTopologyCheck_ui'
        self.tpc = jsTopologyCheckers.JsTopologyCheckers()
    def topoCheckCollapse(self,args=None):
        windowSize = cmds.window('jsTopologyCheck', query=True, widthHeight=1)
        if windowSize == [490,525]:
            cmds.window('jsTopologyCheck', edit=True, widthHeight=[220,23], s = False)
        else:
            cmds.window('jsTopologyCheck', edit=True, widthHeight=[490,525], s = False)


    def topoChecker_ui(self,args=None):
        if cmds.window('jsTopologyCheck', exists=True):
            cmds.deleteUI('jsTopologyCheck')

        #WINDOW START
        cmds.window('jsTopologyCheck', title= 'jsTopologyChecker %s' %(settings.topoVersion) )


        cmds.columnLayout( adjustableColumn=True, cal = 'left' )
        cmds.frameLayout(label = "jsTopologyChecker:", borderStyle = "etchedIn",cll=1,cc=self.topoCheckCollapse,ec=self.topoCheckCollapse)

        #STATUS FIELDS
        cmds.flowLayout( columnSpacing=5 )

        #cmds.textField('idvField', tx= '', ed  = False, w = 200,ebg = 0,bgc = [.2,.2,.2] )
        cmds.textField('idvField', tx= '', ed  = False, w = 380,ebg = 0,bgc = [.2,.2,.2] )

        #cmds.button('sel', label = 'Check Selected Geometry / Group:', c = groupLister, h = 24, w =200)
        cmds.button('sel', label = 'Check Selected:', c = self.tpc.groupLister, h = 24, w =100)
        #LIST FOUND RESULTS
        cmds.setParent('..')


        listOfSearches = 'History', 'Ngons','Triangles','Concave','xform','Lamina','NonVtx','NonEdge','Shapes'
        widthField = 52
        cmds.flowLayout( columnSpacing=2)
        for i in listOfSearches:
            fieldName = i+'Field'
            cmds.textField(fieldName, tx= i, ed  = False, w = widthField,ebg = 0,bgc = [.2,.2,.2], fn = 'smallBoldLabelFont' )
        cmds.setParent('..')


        ###OBJECT LIST ADDITION################################
        cmds.flowLayout( )

        cmds.frameLayout(label = "Object List:", borderStyle = "etchedIn",w = 200, h =446 )
        cmds.textScrollList('objectList', numberOfRows=32, allowMultiSelection=True,h = 250,sc = self.tpc.checkClicked )
        cmds.setParent('..')



        ############# RESULTS AREA

           
        cmds.frameLayout(label = "Result List:", borderStyle = "etchedIn",w = 287, h =446 )
        #cmds.gridLayout( numberOfColumns=3, numberOfRows = 3, cellWidthHeight=(200, 150) )
        scrollLayout = cmds.scrollLayout(w=200,h=150)
        cmds.columnLayout( adjustableColumn=True, cal = 'left' )
        #HISTORY PRINT

        cmds.columnLayout( adjustableColumn=True, cal = 'left' )
        cmds.textField('historyField', tx= 'History:', ed  = False, ebg = True)
        cmds.textScrollList('historyCheck', numberOfRows=8, allowMultiSelection=True, h = 125 )
        cmds.setParent('..')

        #TRIANGLE PRINTS
        cmds.columnLayout( adjustableColumn=True, cal = 'left' )
        cmds.textField('triField', tx= 'Triangles:', ed  = False, ebg = True)
        cmds.textScrollList('triCheck', numberOfRows=8, allowMultiSelection=True,sc= self.tpc.selectTriangles, h = 125, dkc=self.tpc.deleteSelectedTris )
        cmds.setParent('..')

        #NGON PRINTS
        cmds.columnLayout( adjustableColumn=True, cal = 'left' )
        cmds.textField('ngonField', tx= 'Ngons:', ed  = False)
        cmds.textScrollList('ngonCheck', numberOfRows=8, allowMultiSelection=True,sc= self.tpc.selectNgons,  h = 125,dkc = self.tpc.deleteSelectedNgons)
        cmds.setParent('..')

        #concave Prints
        cmds.columnLayout( adjustableColumn=True, cal = 'left' )
        cmds.textField('concaveField', tx= 'Concave Faces:', ed  = False)
        cmds.textScrollList('concaveCheck', numberOfRows=8, allowMultiSelection=True, sc= self.tpc.selectConcave,  h = 125,dkc = self.tpc.deleteSelectedConcave )
        cmds.setParent('..')

        #Transforms Prints
        cmds.columnLayout( adjustableColumn=True, cal = 'left' )
        cmds.textField('transformsField', tx= 'Transforms:', ed  = False)
        cmds.textScrollList('transformsCheck', numberOfRows=8, allowMultiSelection=True, h = 125 )
        cmds.setParent('..')

        #Lamina Prints
        cmds.columnLayout( adjustableColumn=True, cal = 'left' )
        cmds.textField('laminaField', tx= 'Lamina Faces:', ed  = False)
        cmds.textScrollList('laminaCheck', numberOfRows=8, allowMultiSelection=True, h = 125 , sc = self.tpc.selectLamina,dkc=self.tpc.deleteSelectedLamina)
        cmds.setParent('..')

        #Vtx Prints
        cmds.columnLayout( adjustableColumn=True, cal = 'left' )
        cmds.textField('vtxField', tx= 'NonManifold Vertices:', ed  = False)
        cmds.textScrollList('vtxCheck', numberOfRows=8, allowMultiSelection=True, h = 125 , sc = self.tpc.selectVtx)
        cmds.setParent('..')

        #Edge Prints
        cmds.columnLayout( adjustableColumn=True, cal = 'left' )
        cmds.textField('edgeField', tx= 'NonManifold Edges:', ed  = False)
        cmds.textScrollList('edgeCheck', numberOfRows=8, allowMultiSelection=True, h = 125 , sc = self.tpc.selectEdge)
        cmds.setParent('..')

        #shapeNames
        cmds.columnLayout( adjustableColumn=True, cal = 'left' )
        cmds.textField('shapeNameField', tx= 'Shape Names:', ed  = False)
        cmds.textScrollList('shapeNameCheck', numberOfRows=8, allowMultiSelection=True, h = 125,dkc = self.tpc.fixShapeNames)
        cmds.setParent('..')


        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')

        cmds.showWindow( 'jsTopologyCheck' )
        cmds.window('jsTopologyCheck', edit=True, widthHeight=[490,525], s = False)


def launch_ui():
    uiObject = JsTopologyChecker_ui()
    uiObject.topoChecker_ui()