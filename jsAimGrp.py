import maya.cmds as cmds

#####################
###jsAimGrp v1.1#####
#####################

#By Joseph Szokoli
#Website: cargocollective.com/josephSzokoli

#Help: 
#To create shelf icon paste jsAimGrp.py to your scripts folder and assign the following command to the shelf
#import jsAimGrp
#reload(jsAimGrp)

listCreate = cmds.ls(sl=1)
print listCreate
for each in listCreate:
    createLocator = cmds.spaceLocator(n='aimLocator'+each)
    cmds.scale(8,8,8, createLocator)
    cmds.aimConstraint( createLocator, each ,aim = [0,0,-1], wut = "vector" )
    cmds.group( createLocator, each , n='%s_aimLocator_GRP' %each )
