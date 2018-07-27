for i in range(5) :
	cm.spaceLocator(n='locatorAngle%d'%i)

path = "C:/Users/alexa/Documents/alexandra/scripts/"
path = 'D:/users/reveret/usr/src/dev/maya/spine/'

import numpy as np
import maya.cmds as cmds
sys.path.append(path)

cm.group(em=1,n='camGroup')
for i in range(2) : cm.parent('camX%d'%(1+i),'camGroup',r=1)
