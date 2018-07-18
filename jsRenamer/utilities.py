import maya.cmds as cmds
import sys

# delete all modules from sys.modules that contain the input string.
def deleteModules(packageName):
	# mods = sys.modules.keys()
	mods = sys.modules.items()
	mods.sort()

	for m, val in mods:
		if m.startswith(packageName) and val is not None and val.__name__ == m:
			print 'DELETED : %s' %(m)
			del sys.modules[m]


'''


import sys

renamer = '%/path%/'
sys.path.append(renamer)

import utilities
utilities.deleteModules('jsRenamer')

import jsRenamer
jsRenamer.launch_ui()






'''