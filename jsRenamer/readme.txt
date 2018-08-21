################
###jsRenamer ###
################


Joseph Szokoli
https://sites.google.com/view/josephszokoli/


Help: 
Clone jsTK to your maya/scripts/ folder and assign the following command to the shelf.

import sys
from os.path import expanduser
home = expanduser("~")
sys.path.append(home+"/maya/scripts/jsTK/jsTK")

import jsRenamer.utilities
jsRenamer.utilities.deleteModules('jsRenamer')
import jsRenamer
jsRenamer.launch_ui()


##################
### ChangeLog: ###
##################



##v1.2
##Fixed Name Clash Bug in replacer.


##v1.1
Fixed Error in full renamer
#Changed Default name
#Added ability to rename without using ####.


##v1.0 Initial 





 



























