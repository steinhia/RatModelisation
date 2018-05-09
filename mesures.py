import maya.cmds as cmds
import maya.mel as mel
import math
import sys

sys.path.append("C:/Users/alexandra/Documents/alexandra/scripts")

path="C:/Users/alexandra/Documents/alexandra/scripts/"
execfile(path+"Short.py")

def SubVector(name1,name2):
    pos1=position(name1)
    pos2=position(name2)
    return sub(pos1,pos2)

def Hor():
    return SubVector('locatorPlane2','locatorPlane1')

def angleHB(v1,v2):
    angle1=RadToDeg(math.atan2(v1[1],v1[2]))
    angle2=RadToDeg(math.atan2(v2[1],v2[2]))
    return valPrincDeg(angle1-angle2)

def angleGD(v1,v2):
    angle1=RadToDeg(math.atan2(v1[0],v1[2]))
    angle2=RadToDeg(math.atan2(v2[0],v2[2]))
    return valPrincDeg(angle1-angle2)

def locator(i):
    return 'locatorAngle'+str(i)

def locatorPostureVector():
    v=SubVector(locator(1),locator(3))
    return v

def locatorPosture():
    return angleHB(locatorPostureVector(),[0,0,1]) # ou Hor()

def locatorPostureGD():
    return valPrincDeg(angleGD(locatorPostureVector(),[0,1,0])+90) # ou Hor()

def angleC():
    return angleHB(SubVector(locator(3),locator(4)),[0,0,1])

def angleComp():
    return angleHB(SubVector(locator(2),locator(3)),[0,0,1])

def angleCompGD():
    return angleGD(SubVector(locator(2),locator(3)),[0,0,1])

def angleD():
    return angleHB(SubVector(locator(1),locator(2)),[0,0,1])

def angleL():
    return angleHB(SubVector(locator(0),locator(1)),[0,0,1])

def angleCGD():
    return angleGD(SubVector(locator(3),locator(4)),[0,0,1])

def angleDGD():
    return angleGD(SubVector(locator(1),locator(2)),[0,0,1])

def angleLGD():
    return angleGD(SubVector(locator(0),locator(1)),[0,0,1])

def locatorLength():
    posC1=position(locator(0))
    posT1=position(locator(1))
    posT8=position(locator(2))
    posL3=position(locator(3))
    posL6=position(locator(4))
    length=0
    length+=distance(posC1,posT1)
    length+=distance(posT1,posT8)
    length+=distance(posT8,posL3)
    length+=distance(posL3,posL6)
    return length

def getLocatorCurvePosition(num=-1):
    if num==-1:
        return position(locator(2))
    else:
        return position(locator(2))[num]
    
