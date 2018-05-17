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
    return GeneralCalculs(locatorList).PostureVector()

def locatorPosture():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs(locatorList).getPosture()

#def locatorPostureGD():
#    return valPrincDeg(angleGD(locatorPostureVector(),[0,1,0])) # ou Hor()

def angleC():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs(locatorList).angleCHB()

def angleCGD():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs(locatorList).angleCGD()

def angleD():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs(locatorList).angleDHB()

def angleDGD():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs(locatorList).angleDGD()

def angleL():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs(locatorList).angleLHB()

def angleLGD():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs(locatorList).angleLGD()

def angleComp():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs(locatorList).angleComp()

def angleCompGD():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs(locatorList).angleCompGD()


def locatorLength():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs(locatorList).getChainLength()

def getLocatorCurvePosition(num=-1):
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs(locatorList).getPosition(num)

def HalfChainLengthC():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs(locatorList).HalfChainLengthC()

def HalfChainLengtL():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs(locatorList).HalfChainLengthL()

def RapportChainLength():
    locatorList=[locator(i) for i in range(5)]
    return GeneralCalculs(locatorList).RapportChainLength()
    
