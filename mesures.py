# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import math
import sys

sys.path.append("C:/Users/alexa/Documents/alexandra/scripts")

path="C:/Users/alexa/Documents/alexandra/scripts/"
execfile(path+"Short.py")
execfile(path+"GeneralCalculs.py")

#def Hor():
#    return SubVector('locatorPlane2','locatorPlane1')

def locator(i):
    return 'locatorAngle'+str(i)

def locatorPostureVector(Cote=""):
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.PostureVector(locatorList,Cote)

def locatorPosture(Cote=""):
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.getPosture(locatorList,Cote)

def locatorOrientation(Cote=""):
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.getOrientation(locatorList,Cote)

def getLocatorCurvePosition(num=-1,Cote=""):
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.getPosition(locatorList,num,Cote)

def locatorLength():
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.getChainLength(locatorList)

def angleCHBLoc():
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.angleCHB(locatorList)

def angleCGDLoc():
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.angleCGD(locatorList)

def angleTHBLoc():
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.angleTHB(locatorList)

def angleTGDLoc():
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.angleTGD(locatorList)

def angleDHBLoc():
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.angleDHB(locatorList)

def angleDGDLoc():
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.angleDGD(locatorList)

def angleLHBLoc():
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.angleLHB(locatorList)

def angleLGDLoc():
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.angleLGD(locatorList)

def angleCompLoc():
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.angleComp(locatorList)

def angleCompGDLoc():
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.angleCompGD(locatorList)

def HalfChainLengthC():
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.HalfChainLengthC(locatorList)

def HalfChainLengtL():
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.HalfChainLengthL(locatorList)

def RapportChainLength():
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.RapportChainLength(locatorList)

def createLocatorPlane():
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.createPlane(locatorList)
    
