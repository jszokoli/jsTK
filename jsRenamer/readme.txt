################
###jsRenamer ###
################


Author: Joseph Szokoli
Website: sites.google.com/view/josephszokoli/home


Help:
To create a shelf icon, move jsRenamer.py to your scripts folder and assign the following command to the shelf.
import jsRenamer
reload(jsRenamer)


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






import sys

renamer = '/net/homes/jszokoli/maya/scripts/jsTK/jsTK/'
sys.path.append(renamer)

import utilities
utilities.deleteModules('jsRenamer')

import jsRenamer
jsRenamer.launch_ui()






 



























