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

def angleLoc(string):
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.angle(locatorList,string)

#def angleCHBLoc():
#    locatorList=[locator(i) for i in range(6)]
#    return GeneralCalculs.angleCHB(locatorList)

#def angleCGDLoc():
#    locatorList=[locator(i) for i in range(6)]
#    return GeneralCalculs.angleCGD(locatorList)

#def angleTHBLoc():
#    locatorList=[locator(i) for i in range(6)]
#    return GeneralCalculs.angleTHB(locatorList)

#def angleTGDLoc():
#    locatorList=[locator(i) for i in range(6)]
#    return GeneralCalculs.angleTGD(locatorList)

#def angleDHBLoc():
#    locatorList=[locator(i) for i in range(6)]
#    return GeneralCalculs.angleDHB(locatorList)

#def angleDGDLoc():
#    locatorList=[locator(i) for i in range(6)]
#    return GeneralCalculs.angleDGD(locatorList)

#def angleLHBLoc():
#    locatorList=[locator(i) for i in range(6)]
#    return GeneralCalculs.angleLHB(locatorList)

#def angleLGDLoc():
#    locatorList=[locator(i) for i in range(6)]
#    return GeneralCalculs.angleLGD(locatorList)

#def angleCompHBLoc():
#    locatorList=[locator(i) for i in range(6)]
#    return GeneralCalculs.angleCompHB(locatorList)

#def angleCompGDLoc():
#    locatorList=[locator(i) for i in range(6)]
#    return GeneralCalculs.angleCompGD(locatorList)

def HalfChainLengthC():
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.HalfChainLengthC(locatorList)

def HalfChainLengtL():
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.HalfChainLengthL(locatorList)

def RapportChainLength():
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.RapportChainLength(locatorList)

def createLocatorPlane(Cote=""):
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.createPlane(locatorList,Cote)

def projPoint3DLocator(p,Cote=""):
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.projPoint3D(p,locatorList,v,Cote)

def projPlanPostureLocator(v,Cote=""):
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.projPlanPosture(locatorList,v,Cote)

def projPlanPosture3DLocator(p1,p2,Cote=""):
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.projPlanPosture3D(locatorList,p1,p2,Cote)

def projPlanPosture2DLocator(p1,p2,Cote=""):
    locatorList=[locator(i) for i in range(6)]
    return GeneralCalculs.projPlanPosture2D(locatorList,p1,p2,Cote)
    
