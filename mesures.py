import maya.cmds as cmds
import maya.mel as mel
import math
import sys

sys.path.append("C:/Users/alexandra/Documents/alexandra/scripts")

path="C:/Users/alexandra/Documents/alexandra/scripts/"
execfile(path+"Short.py")
execfile(path+"GeneralCalculs.py")

#def Hor():
#    return SubVector('locatorPlane2','locatorPlane1')

def locator(i):
    return 'locatorAngle'+str(i)

def locatorPostureVector():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs.PostureVector(locatorList)

def locatorPosture():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs.getPosture(locatorList)

#def locatorPostureGD():
#    return valPrincDeg(angleGD(locatorPostureVector(),[0,1,0])) # ou Hor()

def angleC():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs.angleCHB(locatorList)

def angleCGD():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs.angleCGD(locatorList)

def angleD():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs.angleDHB(locatorList)

def angleDGD():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs.angleDGD(locatorList)

def angleL():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs.angleLHB(locatorList)

def angleLGD():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs.angleLGD(locatorList)

def angleComp():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs.angleComp(locatorList)

def angleCompGD():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs.angleCompGD(locatorList)


def locatorLength():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs.getChainLength(locatorList)

def getLocatorCurvePosition(num=-1):
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs.getPosition(locatorList,num)

def HalfChainLengthC():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs.HalfChainLengthC(locatorList)

def HalfChainLengtL():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs.HalfChainLengthL(locatorList)

def RapportChainLength():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs.RapportChainLength(locatorList)
    
