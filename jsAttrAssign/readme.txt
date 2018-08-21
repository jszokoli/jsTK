import maya.cmds as cmds

############################
###jsAttrAssign v1.1.0 #####
############################

Joseph Szokoli
https://sites.google.com/view/josephszokoli/

Help: 
Clone jsTK to your maya/scripts/ folder and assign the following command to the shelf.

import sys
from os.path import expanduser
home = expanduser("~")
sys.path.append(home+"/maya/scripts/jsTK/jsTK")

import jsAttrAssign.utilities
jsAttrAssign.utilities.deleteModules('jsAttrAssign')
import jsAttrAssign
jsAttrAssign.launch_ui()





### ChangeLog: ################################################################################
###v1.1.0 Initial 

Added Shader Support
Added Multi Type Support

ToDo:
    Patch out Error Messages and replace with Warnings with Instructions.
"""
###v1.0.0 Initial 










 



























