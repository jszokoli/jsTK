###############################
###jsTopologyChecker v2.0:#####
###############################

Joseph Szokoli
https://sites.google.com/view/josephszokoli/


A tool to sanity check meshes for [History,Ngons,Triangles,Concave Faces,Non-Frozen Transforms, Lamina Faces, NonManifold Vertices, NonManifold Edges, and extra shape nodes]



Help: 
Clone jsTK to your maya/scripts/ folder and assign the following command to the shelf.

import sys
from os.path import expanduser
home = expanduser("~")
sys.path.append(home+"/maya/scripts/jsTK/jsTK")

import jsTopologyChecker.utilities
jsTopologyChecker.utilities.deleteModules('jsTopologyChecker')
import jsTopologyChecker
jsTopologyChecker.launch_ui()



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
