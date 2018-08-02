import maya.cmds as cmds

####################
###jsAttrAssign#####
####################    

#Author: Joseph Szokoli
#Website: cargocollective.com/josephSzokoli

#Help:
#To create a shelf icon, move jsRenamer.py to your scripts folder and assign the following command to the shelf.
#import jsAttrAssign
#reload(jsAttrAssign)

#Version Number################
versionNumberAttr = 'v1.1.0'###
###############################

### ChangeLog: ################################################################################
###v1.1.0 Initial 
"""
Added Shader Support
Added Multi Type Support

ToDo:
    Patch out Error Messages and replace with Warnings with Instructions.
"""
###v1.0.0 Initial 






import sys

attrAssign = '/net/homes/jszokoli/maya/scripts/jsTK/jsTK/'
sys.path.append(attrAssign)

import jsAttrAssign.utilities
jsAttrAssign.utilities.deleteModules('jsAttrAssign')

import jsAttrAssign
jsAttrAssign.launch_ui()











 



























