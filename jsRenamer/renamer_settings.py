#versionNumberRename = 'v003'

commonMtls = ['metal','plastic','leather','glass','chrome','wood','stone','rubber']

availPos = ['C','L','R','F','B','U','D','CF','CB','CU','CD','LF','LB','LU','LD','RF','RB','RU','RD','FU','FD','BU','BD']

availSuffix=['GES','GEP','PLY','NRB','GED','GEV']


documentationString = '''

########################################################################################################################################################################
########################################################################################################################################################################
########################################################################################################################################################################


################
###jsRenamer ###
################


Author: Joseph Szokoli
Website: sites.google.com/view/josephszokoli/home


Help:
To create a shelf icon, move jsRenamer.py to your scripts folder and assign the following command to the shelf.

import sys

renamer = '%/Your Path%/'
sys.path.append(renamer)

import utilities
utilities.deleteModules('jsRenamer')

import jsRenamer
jsRenamer.launch_ui()



##################
### ChangeLog: ###
##################



##v3.0
#Module Class re-write


##v2.0
#Template Ui


##v1.2
##Fixed Name Clash Bug in replacer.


##v1.1
Fixed Error in full renamer
#Changed Default name
#Added ability to rename without using ####.


##v1.0 Initial 




########################################################################################################################################################################
########################################################################################################################################################################
########################################################################################################################################################################



'''


































