import maya.cmds as cmds

###############################
###jsTopologyChecker v2.0:#####
###############################

#Author: Joseph Szokoli
#Website: cargocollective.com/josephSzokoli
#____________________________________________________________________________________________________________________________________________________________________

#Help: 
#To create shelf icon paste jsTopologyChecker.py to your scripts folder and assign the following command to the shelf
#import jsTopologyChecker
#reload(jsTopologyChecker)

### ChangeLog: ################################################################################

### v2.0
#UI OVERHAUL
#Added Func
#Delete Key Funcs

### v1.2
# UI overhaul

###v1.1
# Introduce Multiple Object Check
 
###v1.0
#Initial topoCheck release

#End ChangeLog.#################################################################################

###TOPOLOGY CHECKERS###_______________________________________________________________________________________________________________________________________________
topoVersion = '2.0'
#TriangleChecker______________________________________________________________________________________________________________________________________________________
#RED = [.6,0,0]
#GREEN = [0,.6,0]

RED = [.463,.608,.747]
GREEN = [.2,.2,.2]

def findTris(args=None):
    origSel = cmds.ls(sl=1)
    cmds.polySelectConstraint( m=0,c =0)
    cmds.polySelectConstraint( m=3, t=8, sz=1 ) # to get triangles
    cmds.polySelectConstraint( m=0,c =0)
    faces = cmds.filterExpand(selectionMask =34)
    cmds.select(origSel)
    cmds.polySelectConstraint( m=0,c =0)
    return faces

def checkTris(args=None):
    faces = findTris()
    if not faces:
        cmds.textField('triField',edit = True, tx= 'Triangles:',  ebg = True, bgc = GREEN)
        cmds.textField('TrianglesField',edit = True,  ebg = True, bgc = GREEN)
        cmds.textScrollList('triCheck', edit = True, ra =1  )
        cmds.textScrollList('triCheck', edit = True, numberOfRows=8, append = 'No Triangles Detected', allowMultiSelection=True,h = 125 )
    else:
        cmds.textField('triField',edit = True, tx= 'Triangles:', ebg = True, bgc = RED )
        cmds.textField('TrianglesField',edit = True, ebg = True, bgc = RED )
        cmds.textScrollList('triCheck', edit = True,numberOfRows=8, allowMultiSelection=True, ra =1, h = 125  )
        cmds.textScrollList('triCheck', edit = True, numberOfRows=8, append = faces, allowMultiSelection=True,h = 125 )
    
def selectTriangles(args = None):
    try:
        triangleList = cmds.textScrollList('triCheck', q = True, si = True )
        cmds.select(triangleList)
    except:
        pass

def deleteSelectedTris():
    triangleList = cmds.textScrollList('triCheck', q = True, si = True )
    for i in triangleList:
        try:
            cmds.delete(i)
            cmds.textScrollList('triCheck',edit=True, ri = i)
        except:
            pass


#NGON CHECKER______________________________________________________________________________________________________________________________________________________
def findNgons(args=None):
    origSel = cmds.ls(sl=1)
    cmds.polySelectConstraint( m=0,c =0)
    cmds.polySelectConstraint( m=3, t=8, sz=3 ) # to get N-sided
    cmds.polySelectConstraint( m=0,c =0)
    faces = cmds.filterExpand(selectionMask =34)
    cmds.polySelectConstraint( m=0,c =0)
    cmds.select(origSel)
    return faces

def checkNgons(args=None):
    faces = findNgons()
    if not faces:
        cmds.textField('ngonField',edit = True, tx= 'Ngons:',  ebg = True, bgc = GREEN)
        cmds.textField('NgonsField',edit = True,  ebg = True, bgc = GREEN)
        cmds.textScrollList('ngonCheck', edit = True, ra =1  )
        cmds.textScrollList('ngonCheck', edit = True, numberOfRows=8, append = 'No Ngons Detected', allowMultiSelection=True, h = 125 )
    else:
        cmds.textField('ngonField',edit = True, tx= 'Ngons:', ebg = True, bgc = RED )
        cmds.textField('NgonsField',edit = True, ebg = True, bgc = RED ) 
        cmds.textScrollList('ngonCheck', edit = True,numberOfRows=8, allowMultiSelection=True, ra =1, h = 125  )
        cmds.textScrollList('ngonCheck', edit = True, numberOfRows=8, append = faces, allowMultiSelection=True,h = 125 )

def selectNgons(args = None):
    try:
        ngonList = cmds.textScrollList('ngonCheck', q = True, si = True )
        cmds.select(ngonList)
    except:
        pass

def deleteSelectedNgons(args = None):
    ngonList = cmds.textScrollList('ngonCheck', q = True, si = True )
    for i in ngonList:
        try:
            cmds.delete(i)
            cmds.textScrollList('ngonCheck',edit=True, ri = i)
        except:
            pass
#History Checker______________________________________________________________________________________________________________________________________________________

def findHistory(args=None):
    origSel = cmds.ls(sl=1)
    history = cmds.listHistory()
    return history

def checkHistory(args=None):
    history = findHistory()
    amountHis = cmds.textScrollList('objectList',query=True,nsi = 1)
    if amountHis == 0:
        amountHis = 1
    if len(history) > amountHis:
        cmds.textField('historyField',edit = True, tx= 'History: History Detected', ed  = False, ebg = True, bgc = RED)
        cmds.textField('HistoryField',edit = True, ebg = True, bgc = RED )
        cmds.textScrollList('historyCheck', edit = True,numberOfRows=8, allowMultiSelection=True,ra =1, h = 125  )
        cmds.textScrollList('historyCheck', edit = True, numberOfRows=8, append = history, allowMultiSelection=True,h = 125 )
    else:
        cmds.textField('historyField',edit = True,  tx= 'History:', ed  = False, ebg = True, bgc = GREEN)
        cmds.textField('HistoryField',edit = True,  ebg = True, bgc = GREEN)
        cmds.textScrollList('historyCheck', edit = True,numberOfRows=8, allowMultiSelection=True,ra =1, h = 125  )
        cmds.textScrollList('historyCheck', edit = True,numberOfRows=8, allowMultiSelection=True,append = 'History is Clean', h = 125  )           


#concaveChecker______________________________________________________________________________________________________________________________________________________
def findConcave(args=None):
    origSel = cmds.ls(sl=1)
    cmds.polySelectConstraint( m=3, t=8, c=1, sz=0 ) # to get concave
    cmds.polySelectConstraint( m=0)
    faces = cmds.filterExpand(selectionMask =34)
    cmds.polySelectConstraint( m=0)
    cmds.select(origSel)
    return faces

def checkConcave(args=None):
    faces = findConcave()
    if not faces:
        cmds.textField('concaveField',edit = True, tx= 'Concave Faces:',  ebg = True, bgc = GREEN)
        cmds.textField('ConcaveField',edit = True,  ebg = True, bgc = GREEN)
        cmds.textScrollList('concaveCheck', edit = True, ra =1  )
        cmds.textScrollList('concaveCheck', edit = True, numberOfRows=8, append = 'No Concave Faces Detected', allowMultiSelection=True,h = 125 )
    else:   
        cmds.textField('concaveField',edit = True, tx= 'Concave Faces:', ebg = True, bgc = RED )
        cmds.textField('ConcaveField',edit = True, ebg = True, bgc = RED )
        cmds.textScrollList('concaveCheck', edit = True,numberOfRows=8, allowMultiSelection=True,ra =1, h = 125  )
        cmds.textScrollList('concaveCheck', edit = True, numberOfRows=8, append = faces, allowMultiSelection=True,h = 125 )
    
def selectConcave(args = None):
    try:
        concaveList = cmds.textScrollList('concaveCheck', q = True, si = True )
        cmds.select(concaveList)
    except:
        pass
        
def deleteSelectedConcave(args = None):
    ngonList = cmds.textScrollList('concaveCheck', q = True, si = True )
    cmds.delete(ngonList)
    for i in ngonList:
        try:
            cmds.delete(i)
            cmds.textScrollList('concaveCheck',edit=True, ri = i)
        except:
            pass


#TRANSLATION CHECK______________________________________________________________________________________________________________________________________________________

def transformsCheck(args=None):
    cmds.textScrollList('transformsCheck', edit = True,numberOfRows=8, allowMultiSelection=True,ra =1, h = 125  )
    origSel = cmds.ls(sl=1)
    if len(origSel) == 1:
        translateC = cmds.xform(query = True, t = True)
        rotateC = cmds.xform(query = True, ro = True)
        scaleC = cmds.xform(query = True, s = True, r=True)
        translateTest = [0,0,0]
        rotateTest = [0,0,0]
        scaleTest = [1,1,1]

        if translateC == translateTest and rotateC == rotateTest and scaleC == scaleTest:
            cmds.textField('transformsField',edit = True, tx= 'Transforms:', ebg = True, bgc = GREEN )
            cmds.textField('xformField',edit = True,  ebg = True, bgc = GREEN)
        else:
            cmds.textField('transformsField',edit = True, tx= 'Transforms:', ebg = True, bgc = RED )
            cmds.textField('xformField',edit = True, ebg = True, bgc = RED )

        if translateC == translateTest:
            #print 'Translate Passed'
            cmds.textScrollList('transformsCheck', edit = True, numberOfRows=8, append = 'All Translate Values Frozen', allowMultiSelection=True,h = 125 )
        else:   
            cmds.textScrollList('transformsCheck', edit = True, numberOfRows=8, append = 'Unfrozen Translate Detected', allowMultiSelection=True,h = 125 )
            
        if rotateC == rotateTest:
            #print 'Rotate Passed'
            cmds.textScrollList('transformsCheck', edit = True, numberOfRows=8, append = 'All Rotate Values Frozen', allowMultiSelection=True,h = 125 )
        else:       
            cmds.textScrollList('transformsCheck', edit = True, numberOfRows=8, append = 'Unfrozen Rotate Detected', allowMultiSelection=True,h = 125 )
            
        if scaleC == scaleTest:
            #print 'Scale Passed'
            cmds.textScrollList('transformsCheck', edit = True, numberOfRows=8, append = 'All Scale Values Frozen', allowMultiSelection=True,h = 125 )
        else:
            cmds.textScrollList('transformsCheck', edit = True, numberOfRows=8, append = 'Unfrozen Scale Detected', allowMultiSelection=True, h = 125 )
    else:
        cmds.textField('transformsField',edit = True, tx= 'Transforms:', ebg = False, bgc = [.5,.5,.5] )
        cmds.textField('xformField',edit = True, ebg = True, bgc = [.5,.5,.5] )
        pass



#laminaChecker______________________________________________________________________________________________________________________________________________________

def checkLamina(args=None):
    origSel = cmds.ls(sl=1)
    faces = cmds.polyInfo( lf=True )
    if not faces:
        cmds.textField('laminaField',edit = True, tx= 'Lamina Faces:',  ebg = True, bgc = GREEN)
        cmds.textField('LaminaField',edit = True,  ebg = True, bgc = GREEN)
        #print 'No Lamina Faces Detected' 
        cmds.textScrollList('laminaCheck', edit = True, ra =1  )
        cmds.textScrollList('laminaCheck', edit = True, numberOfRows=8, append = 'No Lamina Faces Detected', allowMultiSelection=True, h = 125 )
        cmds.select(origSel)
    else:
        #cmds.inViewMessage( amg='jsTopologyChecker: <hl> Triangles Detected & Selected </hl>', pos='topCenter', fade=True, fot = 25 )    
        cmds.textField('laminaField',edit = True, tx= 'Lamina Faces:', ebg = True, bgc = RED)
        cmds.textField('LaminaField',edit = True, ebg = True, bgc = RED)
        cmds.select(faces)
        lamina = cmds.filterExpand(selectionMask =34)
        cmds.textScrollList('laminaCheck', edit = True,numberOfRows=8, allowMultiSelection=True, ra =1, h = 125  )
        cmds.textScrollList('laminaCheck', edit = True, numberOfRows=8, append = lamina, allowMultiSelection=True,  h = 125 )
        cmds.select(origSel)
        
        
def selectLamina(args = None):
    try:
        laminaList = cmds.textScrollList('laminaCheck', q = True, si = True )
        cmds.select(laminaList)
    except:
        pass

def deleteSelectedLamina(args = None):
    ngonList = cmds.textScrollList('laminaCheck', q = True, si = True )
    for i in ngonList:
        try:
            cmds.delete(i)
            cmds.textScrollList('laminaCheck',edit=True, ri = i)
        except:
            pass


#nonmanifoldVertexChecker________________________________________________________________________________________________________________________________________________

def checkVtx(args=None):
    origSel = cmds.ls(sl=1)
    faces = cmds.polyInfo( nmv=True )
    if not faces:
        cmds.textField('vtxField',edit = True, tx= 'NonManifold Vertices:',  ebg = True, bgc = GREEN)
        cmds.textField('NonVtxField',edit = True,  ebg = True, bgc = GREEN)
        #print 'No NonManifold Vertices Detected' 
        cmds.textScrollList('vtxCheck', edit = True, ra =1  )
        cmds.textScrollList('vtxCheck', edit = True, numberOfRows=8, append = 'No NonManifold Vertices Detected', allowMultiSelection=True,  h = 125 )
        cmds.select(origSel)
    else: 
        cmds.textField('vtxField',edit = True, tx= 'NonManifold Vertices:', ebg = True, bgc = RED)
        cmds.textField('NonVtxField',edit = True, ebg = True, bgc = RED)
        cmds.select(faces)  
        vtx = cmds.filterExpand(selectionMask =31)
        cmds.textScrollList('vtxCheck', edit = True,numberOfRows=8, allowMultiSelection=True, ra =1, h = 125  )
        cmds.textScrollList('vtxCheck', edit = True, numberOfRows=8, append = vtx, allowMultiSelection=True,  h = 125 )
        cmds.select(origSel)
        
        
def selectVtx(args = None):
    try:
        vtxList = cmds.textScrollList('vtxCheck', q = True, si = True )
        cmds.select(vtxList)
    except:
        pass

#nonmanifoldEdgesChecker______________________________________________________________________________________________________________________________________________________

def checkEdge(args=None):
    origSel = cmds.ls(sl=1)
    faces = cmds.polyInfo( nme=True )
    if not faces:
        cmds.textField('edgeField',edit = True, tx= 'NonManifold Edges:',  ebg = True, bgc = GREEN)
        cmds.textField('NonEdgeField',edit = True,  ebg = True, bgc = GREEN)
        #print 'No NonManifold Vertices Detected' 
        cmds.textScrollList('edgeCheck', edit = True, ra =1  )
        cmds.textScrollList('edgeCheck', edit = True, numberOfRows=8, append = 'No NonManifold Edges Detected', allowMultiSelection=True,h = 125 )
        cmds.select(origSel)
    else: 
        cmds.textField('edgeField',edit = True, tx= 'NonManifold Edges:', ebg = True, bgc = RED)
        cmds.textField('NonEdgeField',edit = True, ebg = True, bgc = RED)
        cmds.select(faces)  
        edges = cmds.filterExpand(selectionMask =32)
        cmds.textScrollList('edgeCheck', edit = True,numberOfRows=8, allowMultiSelection=True, ra =1, h = 125  )
        cmds.textScrollList('edgeCheck', edit = True, numberOfRows=8, append = edges, allowMultiSelection=True,h = 125 )
        cmds.select(origSel)
        
        
def selectEdge(args = None):
    try:
        edgeList = cmds.textScrollList('edgeCheck', q = True, si = True )
        cmds.select(edgeList)
    except:
        pass

#check clash shape Names____________________________________________________________________

def findClashShapes(args=None):
    sel = cmds.ls(sl=1)
    shapeNames = []
    for i in enumerate(sel):
        shapeSel = cmds.listRelatives( i[1] ,s=1)
        #if shapeSel[0]== str(i[1])+'Shape':
        #if i[1] in shapeSel[0] and shapeSel[0][-5:]== 'Shape':
        if shapeSel[0][:-5] in i[1] and shapeSel[0][-5:]== 'Shape':
            pass
        else:
            shapeNames.append(i[1])
    return shapeNames

def checkShapeNames(args=None):
    faces = findClashShapes()
    faceList = []
    for i in faces:
        shapeOf = cmds.listRelatives(i ,s=1)
        faceList.append(shapeOf[0])
    if not faces:
        cmds.textField('shapeNameField',edit = True, tx= 'Shape Names:',  ebg = True, bgc = GREEN)
        cmds.textField('ShapesField',edit = True,  ebg = True, bgc = GREEN)
        cmds.textScrollList('shapeNameCheck', edit = True, ra =1  )
        cmds.textScrollList('shapeNameCheck', edit = True, numberOfRows=8, append = 'All Shape Names Correct', allowMultiSelection=True, h = 125 )
    else:
        cmds.textField('shapeNameField',edit = True, tx= 'Shape Names:', ebg = True, bgc = RED)
        cmds.textField('ShapesField',edit = True, ebg = True, bgc = RED)
        cmds.textScrollList('shapeNameCheck', edit = True,numberOfRows=8, allowMultiSelection=True,ra =1, h = 125  )
        cmds.textScrollList('shapeNameCheck', edit = True, numberOfRows=8, append = faceList, allowMultiSelection=True, h = 125 )
        

def fixShapeNames(args=None):
    clashShapes = cmds.textScrollList('shapeNameCheck', q = True, si = True )
    for i in clashShapes:
        try:
            transformList = cmds.listRelatives(i, parent=True)
            newShapeName = str(transformList[0])+'Shape'
            cmds.rename(i,newShapeName)
            cmds.textScrollList('shapeNameCheck',edit=True, ri = i)
        except:
            pass
#CHECKALL BUTTON______________________________________________________________________________________________________________________________________________________

def checkClicked(args=None):
    #cmds.progressBar(progressControl, edit=True, pr = 0)
    currentSel = cmds.textScrollList('objectList', q = True, si = True )  
    cmds.select(currentSel)
    bakeString = '|'.join(currentSel)
 #   cmds.textField('idvField', edit = True, tx = bakeString)
    checkHistory()
    checkNgons()
    checkTris()
    checkConcave()
    transformsCheck()
    checkLamina()
    checkVtx()
    checkEdge()
    checkShapeNames()

def groupLister(args = None):
    chooser = cmds.ls(sl=1)
    if len(chooser) == 0:
        print 'None Selected'
    else:
        appenderList = []
        cleanList = []
        for each in chooser:
            children = cmds.listRelatives(each,ad=1,s=0)
            if not children:
                print 'Empty Group Selected... Skipping...'            
            else:
                meshKids = cmds.listRelatives(each,ad=1,s=0, type = "mesh")
                if len(meshKids) > 1:
                    tr = cmds.filterExpand(each, sm=12 )
                    for x in tr:
                        appenderList.append(x)
                else:
                    tr = cmds.filterExpand(each, sm=12 )
                    for z in tr:
                        appenderList.append(z)           
        print appenderList
        for each in appenderList:
            clean = each
            cleanList.append(clean)
        cmds.textScrollList('objectList', edit = True, ra = 1 )
        cmds.textScrollList('objectList', edit = True, append = cleanList )
        fieldText = ''
        if len(chooser) > 1:
            for i in chooser:
                fieldText = fieldText+i+' '
        else:
            fieldText = chooser[0]
        cmds.textField('idvField', edit = True, tx = fieldText)
        cmds.select(d=1)   
        cmds.select(appenderList[0])
        checkHistory()
        checkNgons()
        checkTris()
        checkConcave()
        transformsCheck()
        checkLamina()
        checkVtx()
        checkEdge()
        checkShapeNames()
        cmds.select(d=1)   


def topoCheckCollapse():
    windowSize = cmds.window('jsTopologyCheck', query=True, widthHeight=1)
    if windowSize == [490,525]:
        cmds.window('jsTopologyCheck', edit=True, widthHeight=[220,23], s = False)
    else:
        cmds.window('jsTopologyCheck', edit=True, widthHeight=[490,525], s = False)

#UI START______________________________________________________________________________________________________________________________________________________

if cmds.window('jsTopologyCheck', exists=True):
    cmds.deleteUI('jsTopologyCheck')

#WINDOW START
cmds.window('jsTopologyCheck', title= 'jsTopologyChecker %s' %(topoVersion) )


cmds.columnLayout( adjustableColumn=True, cal = 'left' )
cmds.frameLayout(label = "jsTopologyChecker:", borderStyle = "etchedIn",cll=1,cc=topoCheckCollapse,ec=topoCheckCollapse)

#STATUS FIELDS
cmds.flowLayout( columnSpacing=5 )

#cmds.textField('idvField', tx= '', ed  = False, w = 200,ebg = 0,bgc = [.2,.2,.2] )
cmds.textField('idvField', tx= '', ed  = False, w = 380,ebg = 0,bgc = [.2,.2,.2] )

#cmds.button('sel', label = 'Check Selected Geometry / Group:', c = groupLister, h = 24, w =200)
cmds.button('sel', label = 'Check Selected:', c = groupLister, h = 24, w =100)
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
cmds.textScrollList('objectList', numberOfRows=32, allowMultiSelection=True,h = 250,sc = checkClicked )
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
cmds.textScrollList('triCheck', numberOfRows=8, allowMultiSelection=True,sc= selectTriangles, h = 125, dkc=deleteSelectedTris )
cmds.setParent('..')

#NGON PRINTS
cmds.columnLayout( adjustableColumn=True, cal = 'left' )
cmds.textField('ngonField', tx= 'Ngons:', ed  = False)
cmds.textScrollList('ngonCheck', numberOfRows=8, allowMultiSelection=True,sc= selectNgons,  h = 125,dkc = deleteSelectedNgons)
cmds.setParent('..')

#concave Prints
cmds.columnLayout( adjustableColumn=True, cal = 'left' )
cmds.textField('concaveField', tx= 'Concave Faces:', ed  = False)
cmds.textScrollList('concaveCheck', numberOfRows=8, allowMultiSelection=True, sc= selectConcave,  h = 125,dkc = deleteSelectedConcave )
cmds.setParent('..')

#Transforms Prints
cmds.columnLayout( adjustableColumn=True, cal = 'left' )
cmds.textField('transformsField', tx= 'Transforms:', ed  = False)
cmds.textScrollList('transformsCheck', numberOfRows=8, allowMultiSelection=True, h = 125 )
cmds.setParent('..')

#Lamina Prints
cmds.columnLayout( adjustableColumn=True, cal = 'left' )
cmds.textField('laminaField', tx= 'Lamina Faces:', ed  = False)
cmds.textScrollList('laminaCheck', numberOfRows=8, allowMultiSelection=True, h = 125 , sc = selectLamina,dkc=deleteSelectedLamina)
cmds.setParent('..')

#Vtx Prints
cmds.columnLayout( adjustableColumn=True, cal = 'left' )
cmds.textField('vtxField', tx= 'NonManifold Vertices:', ed  = False)
cmds.textScrollList('vtxCheck', numberOfRows=8, allowMultiSelection=True, h = 125 , sc = selectVtx)
cmds.setParent('..')

#Edge Prints
cmds.columnLayout( adjustableColumn=True, cal = 'left' )
cmds.textField('edgeField', tx= 'NonManifold Edges:', ed  = False)
cmds.textScrollList('edgeCheck', numberOfRows=8, allowMultiSelection=True, h = 125 , sc = selectEdge)
cmds.setParent('..')

#shapeNames
cmds.columnLayout( adjustableColumn=True, cal = 'left' )
cmds.textField('shapeNameField', tx= 'Shape Names:', ed  = False)
cmds.textScrollList('shapeNameCheck', numberOfRows=8, allowMultiSelection=True, h = 125,dkc = fixShapeNames)
cmds.setParent('..')


cmds.setParent('..')
cmds.setParent('..')
cmds.setParent('..')

cmds.showWindow( 'jsTopologyCheck' )
cmds.window('jsTopologyCheck', edit=True, widthHeight=[490,525], s = False)




#testOrig = 'eyeOuterReferenceMtl_L_eyeOuter0002_PLY1'
#testName = 'eyeOuterReferenceMtl_L_eyeOuter0002_PLY1Shape'

#print testName[-5:]
#if testOrig in testName and testName[-5:] == 'Shape':
#    print 'yesy'
