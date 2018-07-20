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


def getPostureVectorLoc(Cote=""):
    locatorList=locList()
    return GeneralCalculs.PostureVector(locatorList,Cote)

def getPostureLoc(Cote=""):
    locatorList=locList()
    return GeneralCalculs.getPosture(locatorList,Cote)

def getOrientationLoc(Cote=""):
    locatorList=locList()
    return GeneralCalculs.getOrientation(locatorList,Cote)

def getPositionLoc(num=-1,Cote=""):
    locatorList=locList()
    return GeneralCalculs.getPosition(locatorList,num,Cote)

def getXLoc(Cote=""):
    locatorList=locList()
    return GeneralCalculs.getX(locatorList,Cote)

def getYLoc(Cote=""):
    locatorList=locList()
    return GeneralCalculs.getY(locatorList,Cote)

def getZLoc(Cote=""):
    locatorList=locList()
    return GeneralCalculs.getZ(locatorList,Cote)

def getLengthLoc():
    locatorList=locList()
    return GeneralCalculs.getLength(locatorList)

def angleLoc(string):
    locatorList=locList()
    return GeneralCalculs.angle(locatorList,string)

def HalfChainLengthC():
    locatorList=locList()
    return GeneralCalculs.HalfChainLengthC(locatorList)

def HalfChainLengtL():
    locatorList=locList()
    return GeneralCalculs.HalfChainLengthL(locatorList)

def RapportChainLength():
    locatorList=locList()
    return GeneralCalculs.RapportChainLength(locatorList)

def createLocatorPlane(Cote=""):
    locatorList=locList()
    return GeneralCalculs.createPlane(locatorList,Cote)

def projPoint3DLocator(p,Cote=""):
    locatorList=locList()
    return GeneralCalculs.projPoint3D(p,locatorList,v,Cote)

def projPlanPostureLocator(v,Cote=""):
    locatorList=locList()
    return GeneralCalculs.projPlanPosture(locatorList,v,Cote)

def projPlanPosture3DLocator(p1,p2,Cote=""):
    locatorList=locList()
    return GeneralCalculs.projPlanPosture3D(locatorList,p1,p2,Cote)

def projPlanPosture2DLocator(p1,p2,Cote=""):
    locatorList=locList()
    return GeneralCalculs.projPlanPosture2D(locatorList,p1,p2,Cote)
    
