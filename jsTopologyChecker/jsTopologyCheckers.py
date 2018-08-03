import maya.cmds as cmds

from . import settings

class JsTopologyCheckers(object):
    def __init__(self):
        print 'Initializing jsTopologyCheckers...'

    def findTris(self, args=None):
        origSel = cmds.ls(sl=1)
        cmds.polySelectConstraint( m=0,c =0)
        cmds.polySelectConstraint( m=3, t=8, sz=1 ) # to get triangles
        cmds.polySelectConstraint( m=0,c =0)
        faces = cmds.filterExpand(selectionMask =34)
        cmds.select(origSel)
        cmds.polySelectConstraint( m=0,c =0)
        return faces

    def checkTris(self, args=None):
        faces = self.findTris()
        if not faces:
            cmds.textField('triField',edit = True, tx= 'Triangles:',  ebg = True, bgc = settings.color2)
            cmds.textField('TrianglesField',edit = True,  ebg = True, bgc = settings.color2)
            cmds.textScrollList('triCheck', edit = True, ra =1  )
            cmds.textScrollList('triCheck', edit = True, numberOfRows=8, append = 'No Triangles Detected', allowMultiSelection=True,h = 125 )
        else:
            cmds.textField('triField',edit = True, tx= 'Triangles:', ebg = True, bgc = settings.color1 )
            cmds.textField('TrianglesField',edit = True, ebg = True, bgc = settings.color1 )
            cmds.textScrollList('triCheck', edit = True,numberOfRows=8, allowMultiSelection=True, ra =1, h = 125  )
            cmds.textScrollList('triCheck', edit = True, numberOfRows=8, append = faces, allowMultiSelection=True,h = 125 )
        
    def selectTriangles(self, args = None):
        try:
            triangleList = cmds.textScrollList('triCheck', q = True, si = True )
            cmds.select(triangleList)
        except:
            pass

    def deleteSelectedTris(self, args=None):
        triangleList = cmds.textScrollList('triCheck', q = True, si = True )
        for i in triangleList:
            try:
                cmds.delete(i)
                cmds.textScrollList('triCheck',edit=True, ri = i)
            except:
                pass


    #NGON CHECKER______________________________________________________________________________________________________________________________________________________
    def findNgons(self, args=None):
        origSel = cmds.ls(sl=1)
        cmds.polySelectConstraint( m=0,c =0)
        cmds.polySelectConstraint( m=3, t=8, sz=3 ) # to get N-sided
        cmds.polySelectConstraint( m=0,c =0)
        faces = cmds.filterExpand(selectionMask =34)
        cmds.polySelectConstraint( m=0,c =0)
        cmds.select(origSel)
        return faces

    def checkNgons(self, args=None):
        faces = self.findNgons()
        if not faces:
            cmds.textField('ngonField',edit = True, tx= 'Ngons:',  ebg = True, bgc = settings.color2)
            cmds.textField('NgonsField',edit = True,  ebg = True, bgc = settings.color2)
            cmds.textScrollList('ngonCheck', edit = True, ra =1  )
            cmds.textScrollList('ngonCheck', edit = True, numberOfRows=8, append = 'No Ngons Detected', allowMultiSelection=True, h = 125 )
        else:
            cmds.textField('ngonField',edit = True, tx= 'Ngons:', ebg = True, bgc = settings.color1 )
            cmds.textField('NgonsField',edit = True, ebg = True, bgc = settings.color1 ) 
            cmds.textScrollList('ngonCheck', edit = True,numberOfRows=8, allowMultiSelection=True, ra =1, h = 125  )
            cmds.textScrollList('ngonCheck', edit = True, numberOfRows=8, append = faces, allowMultiSelection=True,h = 125 )

    def selectNgons(self, args = None):
        try:
            ngonList = cmds.textScrollList('ngonCheck', q = True, si = True )
            cmds.select(ngonList)
        except:
            pass

    def deleteSelectedNgons(self, args = None):
        ngonList = cmds.textScrollList('ngonCheck', q = True, si = True )
        for i in ngonList:
            try:
                cmds.delete(i)
                cmds.textScrollList('ngonCheck',edit=True, ri = i)
            except:
                pass
    #History Checker______________________________________________________________________________________________________________________________________________________

    def findHistory(self, args=None):
        origSel = cmds.ls(sl=1)
        history = cmds.listHistory()
        return history

    def checkHistory(self, args=None):
        history = self.findHistory()
        amountHis = cmds.textScrollList('objectList',query=True,nsi = 1)
        if amountHis == 0:
            amountHis = 1
        if len(history) > amountHis:
            cmds.textField('historyField',edit = True, tx= 'History: History Detected', ed  = False, ebg = True, bgc = settings.color1)
            cmds.textField('HistoryField',edit = True, ebg = True, bgc = settings.color1 )
            cmds.textScrollList('historyCheck', edit = True,numberOfRows=8, allowMultiSelection=True,ra =1, h = 125  )
            cmds.textScrollList('historyCheck', edit = True, numberOfRows=8, append = history, allowMultiSelection=True,h = 125 )
        else:
            cmds.textField('historyField',edit = True,  tx= 'History:', ed  = False, ebg = True, bgc = settings.color2)
            cmds.textField('HistoryField',edit = True,  ebg = True, bgc = settings.color2)
            cmds.textScrollList('historyCheck', edit = True,numberOfRows=8, allowMultiSelection=True,ra =1, h = 125  )
            cmds.textScrollList('historyCheck', edit = True,numberOfRows=8, allowMultiSelection=True,append = 'History is Clean', h = 125  )           


    #concaveChecker______________________________________________________________________________________________________________________________________________________
    def findConcave(self, args=None):
        origSel = cmds.ls(sl=1)
        cmds.polySelectConstraint( m=3, t=8, c=1, sz=0 ) # to get concave
        cmds.polySelectConstraint( m=0)
        faces = cmds.filterExpand(selectionMask =34)
        cmds.polySelectConstraint( m=0)
        cmds.select(origSel)
        return faces

    def checkConcave(self, args=None):
        faces = self.findConcave()
        if not faces:
            cmds.textField('concaveField',edit = True, tx= 'Concave Faces:',  ebg = True, bgc = settings.color2)
            cmds.textField('ConcaveField',edit = True,  ebg = True, bgc = settings.color2)
            cmds.textScrollList('concaveCheck', edit = True, ra =1  )
            cmds.textScrollList('concaveCheck', edit = True, numberOfRows=8, append = 'No Concave Faces Detected', allowMultiSelection=True,h = 125 )
        else:   
            cmds.textField('concaveField',edit = True, tx= 'Concave Faces:', ebg = True, bgc = settings.color1 )
            cmds.textField('ConcaveField',edit = True, ebg = True, bgc = settings.color1 )
            cmds.textScrollList('concaveCheck', edit = True,numberOfRows=8, allowMultiSelection=True,ra =1, h = 125  )
            cmds.textScrollList('concaveCheck', edit = True, numberOfRows=8, append = faces, allowMultiSelection=True,h = 125 )
        
    def selectConcave(self, args = None):
        try:
            concaveList = cmds.textScrollList('concaveCheck', q = True, si = True )
            cmds.select(concaveList)
        except:
            pass
            
    def deleteSelectedConcave(self, args = None):
        ngonList = cmds.textScrollList('concaveCheck', q = True, si = True )
        cmds.delete(ngonList)
        for i in ngonList:
            try:
                cmds.delete(i)
                cmds.textScrollList('concaveCheck',edit=True, ri = i)
            except:
                pass


    #TRANSLATION CHECK______________________________________________________________________________________________________________________________________________________

    def transformsCheck(self, args=None):
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
                cmds.textField('transformsField',edit = True, tx= 'Transforms:', ebg = True, bgc = settings.color2 )
                cmds.textField('xformField',edit = True,  ebg = True, bgc = settings.color2)
            else:
                cmds.textField('transformsField',edit = True, tx= 'Transforms:', ebg = True, bgc = settings.color1 )
                cmds.textField('xformField',edit = True, ebg = True, bgc = settings.color1 )

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

    def checkLamina(self, args=None):
        origSel = cmds.ls(sl=1)
        faces = cmds.polyInfo( lf=True )
        if not faces:
            cmds.textField('laminaField',edit = True, tx= 'Lamina Faces:',  ebg = True, bgc = settings.color2)
            cmds.textField('LaminaField',edit = True,  ebg = True, bgc = settings.color2)
            #print 'No Lamina Faces Detected' 
            cmds.textScrollList('laminaCheck', edit = True, ra =1  )
            cmds.textScrollList('laminaCheck', edit = True, numberOfRows=8, append = 'No Lamina Faces Detected', allowMultiSelection=True, h = 125 )
            cmds.select(origSel)
        else:
            #cmds.inViewMessage( amg='jsTopologyChecker: <hl> Triangles Detected & Selected </hl>', pos='topCenter', fade=True, fot = 25 )    
            cmds.textField('laminaField',edit = True, tx= 'Lamina Faces:', ebg = True, bgc = settings.color1)
            cmds.textField('LaminaField',edit = True, ebg = True, bgc = settings.color1)
            cmds.select(faces)
            lamina = cmds.filterExpand(selectionMask =34)
            cmds.textScrollList('laminaCheck', edit = True,numberOfRows=8, allowMultiSelection=True, ra =1, h = 125  )
            cmds.textScrollList('laminaCheck', edit = True, numberOfRows=8, append = lamina, allowMultiSelection=True,  h = 125 )
            cmds.select(origSel)
            
            
    def selectLamina(self, args = None):
        try:
            laminaList = cmds.textScrollList('laminaCheck', q = True, si = True )
            cmds.select(laminaList)
        except:
            pass

    def deleteSelectedLamina(self, args = None):
        ngonList = cmds.textScrollList('laminaCheck', q = True, si = True )
        for i in ngonList:
            try:
                cmds.delete(i)
                cmds.textScrollList('laminaCheck',edit=True, ri = i)
            except:
                pass


    #nonmanifoldVertexChecker________________________________________________________________________________________________________________________________________________

    def checkVtx(self, args=None):
        origSel = cmds.ls(sl=1)
        faces = cmds.polyInfo( nmv=True )
        if not faces:
            cmds.textField('vtxField',edit = True, tx= 'NonManifold Vertices:',  ebg = True, bgc = settings.color2)
            cmds.textField('NonVtxField',edit = True,  ebg = True, bgc = settings.color2)
            #print 'No NonManifold Vertices Detected' 
            cmds.textScrollList('vtxCheck', edit = True, ra =1  )
            cmds.textScrollList('vtxCheck', edit = True, numberOfRows=8, append = 'No NonManifold Vertices Detected', allowMultiSelection=True,  h = 125 )
            cmds.select(origSel)
        else: 
            cmds.textField('vtxField',edit = True, tx= 'NonManifold Vertices:', ebg = True, bgc = settings.color1)
            cmds.textField('NonVtxField',edit = True, ebg = True, bgc = settings.color1)
            cmds.select(faces)  
            vtx = cmds.filterExpand(selectionMask =31)
            cmds.textScrollList('vtxCheck', edit = True,numberOfRows=8, allowMultiSelection=True, ra =1, h = 125  )
            cmds.textScrollList('vtxCheck', edit = True, numberOfRows=8, append = vtx, allowMultiSelection=True,  h = 125 )
            cmds.select(origSel)
            
            
    def selectVtx(self, args = None):
        try:
            vtxList = cmds.textScrollList('vtxCheck', q = True, si = True )
            cmds.select(vtxList)
        except:
            pass

    #nonmanifoldEdgesChecker______________________________________________________________________________________________________________________________________________________

    def checkEdge(self, args=None):
        origSel = cmds.ls(sl=1)
        faces = cmds.polyInfo( nme=True )
        if not faces:
            cmds.textField('edgeField',edit = True, tx= 'NonManifold Edges:',  ebg = True, bgc = settings.color2)
            cmds.textField('NonEdgeField',edit = True,  ebg = True, bgc = settings.color2)
            #print 'No NonManifold Vertices Detected' 
            cmds.textScrollList('edgeCheck', edit = True, ra =1  )
            cmds.textScrollList('edgeCheck', edit = True, numberOfRows=8, append = 'No NonManifold Edges Detected', allowMultiSelection=True,h = 125 )
            cmds.select(origSel)
        else: 
            cmds.textField('edgeField',edit = True, tx= 'NonManifold Edges:', ebg = True, bgc = settings.color1)
            cmds.textField('NonEdgeField',edit = True, ebg = True, bgc = settings.color1)
            cmds.select(faces)  
            edges = cmds.filterExpand(selectionMask =32)
            cmds.textScrollList('edgeCheck', edit = True,numberOfRows=8, allowMultiSelection=True, ra =1, h = 125  )
            cmds.textScrollList('edgeCheck', edit = True, numberOfRows=8, append = edges, allowMultiSelection=True,h = 125 )
            cmds.select(origSel)
            
            
    def selectEdge(self, args = None):
        try:
            edgeList = cmds.textScrollList('edgeCheck', q = True, si = True )
            cmds.select(edgeList)
        except:
            pass

    #check clash shape Names____________________________________________________________________

    def findClashShapes(self, args=None):
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

    def checkShapeNames(self, args=None):
        faces = self.findClashShapes()
        faceList = []
        for i in faces:
            shapeOf = cmds.listRelatives(i ,s=1)
            faceList.append(shapeOf[0])
        if not faces:
            cmds.textField('shapeNameField',edit = True, tx= 'Shape Names:',  ebg = True, bgc = settings.color2)
            cmds.textField('ShapesField',edit = True,  ebg = True, bgc = settings.color2)
            cmds.textScrollList('shapeNameCheck', edit = True, ra =1  )
            cmds.textScrollList('shapeNameCheck', edit = True, numberOfRows=8, append = 'All Shape Names Correct', allowMultiSelection=True, h = 125 )
        else:
            cmds.textField('shapeNameField',edit = True, tx= 'Shape Names:', ebg = True, bgc = settings.color1)
            cmds.textField('ShapesField',edit = True, ebg = True, bgc = settings.color1)
            cmds.textScrollList('shapeNameCheck', edit = True,numberOfRows=8, allowMultiSelection=True,ra =1, h = 125  )
            cmds.textScrollList('shapeNameCheck', edit = True, numberOfRows=8, append = faceList, allowMultiSelection=True, h = 125 )
            

    def fixShapeNames(self, args=None):
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

    def checkClicked(self, args=None):
        #cmds.progressBar(progressControl, edit=True, pr = 0)
        currentSel = cmds.textScrollList('objectList', q = True, si = True )  
        cmds.select(currentSel)
        bakeString = '|'.join(currentSel)
     #   cmds.textField('idvField', edit = True, tx = bakeString)
        self.checkHistory()
        self.checkNgons()
        self.checkTris()
        self.checkConcave()
        self.transformsCheck()
        self.checkLamina()
        self.checkVtx()
        self.checkEdge()
        self.checkShapeNames()

    def groupLister(self, args = None):
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
            self.checkHistory()
            self.checkNgons()
            self.checkTris()
            self.checkConcave()
            self.transformsCheck()
            self.checkLamina()
            self.checkVtx()
            self.checkEdge()
            self.checkShapeNames()
            cmds.select(d=1)   