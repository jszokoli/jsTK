import maya.cmds as cmds
import os.path
import time

time_start = time.clock()
#path = "F:\job\proj\Xwing\\asset\Xwing\model\maya\data\clean\\"
projectDirectory = cmds.workspace(q=True, rd=True)
path = projectDirectory+'/data/'
#print path

sel = cmds.ls(sl=1,type='transform')
for i in sel:
    uuidNode = cmds.ls(i, uuid=True)
    
    parentNode = cmds.listRelatives(i, p=True)
    cmds.parent( i, world=True )
    newNodeName = cmds.ls(uuidNode)
    cmds.select(newNodeName)
    
    newFile = cmds.file(path+'SUCHALONGNAMENOONEELSEWOULDEVERUSE.obj',force=True, exportSelected=True, type="OBJexport")
    
    cmds.delete(newNodeName)
    cleanObj = cmds.file(path+'SUCHALONGNAMENOONEELSEWOULDEVERUSE.obj', force=True, i=True, type="OBJexport", dns = True,rnn=True)
    #print cleanObj
    
    importCleanupNodes = []    
    for node in cleanObj:
        #print node        
        if cmds.nodeType(node) == 'mesh' or cmds.nodeType(node) == 'transform':
            if cmds.nodeType(node) == 'transform':
                xformNode = node
        else:
            importCleanupNodes.append(node)
    if len(importCleanupNodes) > 0:
        cmds.delete(importCleanupNodes)
    
    cmds.select(xformNode)
    cmds.hyperShade(assign='initialShadingGroup')

    cmds.parent(xformNode, parentNode)

if os.path.exists(path+'SUCHALONGNAMENOONEELSEWOULDEVERUSE.obj') == True:
    cmds.sysFile(path+'SUCHALONGNAMENOONEELSEWOULDEVERUSE.obj', delete=True)
if os.path.exists(path+'SUCHALONGNAMENOONEELSEWOULDEVERUSE.mtl') == True:
    cmds.sysFile(path+'SUCHALONGNAMENOONEELSEWOULDEVERUSE.mtl', delete=True)
cmds.select(sel)

for cleanup in sel:
    print 'Cleaned up node: '+cleanup + ' | Assigned Lambert1'
time_elapsed = (time.clock() - time_start)
print 'Process took '+ str(time_elapsed) + ' seconds to complete.'






