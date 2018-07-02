import sys
import numpy as np
#sys.path.append("C:/Users/alexa/Documents/alexandra/scripts")

path="C:/Users/alexa/Documents/alexandra/scripts/"
execfile(path+"Short.py")

def placeLocator(num=-1):
    if num==-1:
        result = cmds.promptDialog(message='Num of Locator:',button=['OK', 'Cancel'],\
		defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
        if result == 'OK' :
	        num=int(cmds.promptDialog(query=True, text=True))
    if num!=-1:
        # ray1
        posC=position('camX1|ptC')
        posCam=position('camX1|cmrkX1')
        # ray 2
        posC2=position('camX2|ptC')
        posCam2=position('camX2|cmrkX2')
        
        dir1=sub(posCam,posC)    
        dir2=sub(posCam2,posC2)   
        CD=sub(posC2,posC)   

        q=norm(np.cross(dir2,CD))/norm(np.cross(dir2,dir1))
        M=sum(posC,pdt(q,dir1))
        cmds.select(locator(num))
        cmds.move(M[0],M[1],M[2],r=False)
        string='setKeyframe -breakdown 0 -hierarchy none -controlPoints 0 -shape 0 {"locatorAngle'+str(num)+'"};'
        mel.eval(string)
    return num
    
placeLocator()