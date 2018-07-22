from functools import partial
import maya.cmds as cmds
import maya.mel as mel
import math
import time
import sys

def HideListRest(args=[]):
    """ liste du corps du rat """
    HideList=[]
    HideList.append(cmds.ls('*Cote*',r=True))
    HideList.append(cmds.ls('*Costal*',r=True))
    HideList.append(cmds.ls('*Radius*',r=True))
    HideList.append(cmds.ls('*Clavicule*',r=True))
    HideList.append(cmds.ls('*Humerus*',r=True))
    HideList.append(cmds.ls('*Tibia*',r=True))
    HideList.append(cmds.ls('*Ulna*',r=True))
    HideList.append(cmds.ls('*Sternum*',r=True))
    HideList.append(cmds.ls('*Os*',r=True))
    HideList.append(cmds.ls('*Scapula*',r=True))
    HideList.append(cmds.ls('*Femur*',r=True))
    HideList.append(cmds.ls('*Patella*',r=True))
    HideList.append(cmds.ls('*Xyphoide*',r=True))
    HideList.append(cmds.ls('*Manubrium*',r=True))
    HideList.append(cmds.ls('*Tissue*',r=True))
    HideList.append(cmds.ls('*Vertebre*Vertebre*',r=True))
    HideList.append("obj58_Sacrum_VertebreL6")
    HideList.append("obj99_VerterbreL2_VertebreL3")
    HideList.append("obj102_VertebreL1_VerterbreL2")
    HideList.append("obj46_VertebreC1_Atlas_Crane")
    HideList.append(cmds.ls('*Cluster*',r=True))
    HideList.append(cmds.ls('*Caudale*',r=True))
    HideList.append(cmds.ls('*Sacrum*',r=True)) 
    return HideList

def HideListHead(args=[],*_):
    """ liste des objets de la tete """
    HideList=['obj8_Crane_Exterior','obj181_Mandibule_Exterior','obj182_Mandibule_Crane','obj109_OsHyoide_Exterior']
    return HideList  
                
def HideRestOfSkeleton(args=[],*_):
    """ cache le reste du squelette non modélisé """
    HideList=HideListRest([])
    for i in HideList :
        cmds.hide(i)
    if(cmds.objExists("curve1")):
        cmds.showHidden("curve1",a=True)
        
def ShowRestOfSkeleton(args=[],*_):
    """ montre le reste du squelette non modélisé """
    HideList=HideListRest([])
    for i in HideList :
        cmds.showHidden(i,a=True)
    
def HideHeadAndTail(args=[],*_):
    """ cache la tete """
    HideList=HideListHead([])
    for i in HideList :
        cmds.hide(i)

def ShowHeadAndTail(args=[],*_):
    """ montre la tete """
    HideList=HideListHead([])
    for i in HideList :
        cmds.showHidden(i,a=True)      
    
def HidePolygons(args=[],*_):
    """ cache le maillage """
    HideList=cmds.ls('*obj*',r=True)
    for i in HideList :
        if('joint' not in i):
            cmds.hide(i)
   
def ShowPolygons(args=[],*_):
    """ montre le maillage """
    HideList=cmds.ls('*obj*',r=True)
    for i in HideList :
        cmds.showHidden(i,a=True)
    HideRestOfSkeleton(args)
         
          
def HideSkeletonJoints(args=[],*_):
    """ cache les joints """
    for i in range(56) :
        if(cmds.objExists('joint'+str(i+1))):
            cmds.hide('joint'+str(i+1)) 
    
def ShowSkeletonJoints(args=[],*_):
    """ montre les joints """
    HideList=cmds.ls('*joint*',r=True)
    for i in HideList :
        cmds.showHidden(i,a=True)


def colorSkeleton(nameList,*_):
    """ colorie les mesh """
    mel.eval("shadingNode -asShader blinn -n blinn1;")
    mel.eval("sets -renderable true -noSurfaceShader true -empty -name blinn1SG;")
    mel.eval("connectAttr -f blinn1.outColor blinn1SG.surfaceShader;")
    
    mel.eval("shadingNode -asShader blinn -n blinn2;")
    mel.eval("sets -renderable true -noSurfaceShader true -empty -name blinn2SG;")
    mel.eval("connectAttr -f blinn2.outColor blinn2SG.surfaceShader;")

    mel.eval("shadingNode -asShader blinn -n blinn3;")
    mel.eval("sets-renderable true -noSurfaceShader true -empty -name blinn3SG;")
    mel.eval("connectAttr -f blinn3.outColor blinn3SG.surfaceShader;")

    cmds.select( clear=True )
    for i in range(6) :
        cmds.select(nameList[i],add=True)
    mel.eval("sets -e -forceElement blinn1SG;")
    mel.eval("setAttr \"blinn1.color\" -type double3 1 0 0 ;")
    cmds.select( clear=True)
    for i in range(6,19) :
        cmds.select(nameList[i],add=True)
    cmds.select('obj8_Crane_Exterior',add=True)
    cmds.select('obj181_Mandibule_Exterior',add=True)
    cmds.select('obj109_OsHyoide_Exterior',add=True)
    mel.eval("sets -e -forceElement blinn2SG;")
    mel.eval("setAttr \"blinn2.color\" -type double3 0 1 0 ;")
    cmds.select( clear=True )
    for i in range(19,26) :
        cmds.select(nameList[i],add=True)
    mel.eval("sets -e -forceElement blinn3SG;")
    mel.eval("setAttr \"blinn3.color\" -type double3 0 0 1 ;")
    cmds.select( clear=True )  

def HidePlane(*_):
    """ supprime le plan pour le cacher """
    if cmds.objExists('PosturePlane'):
        cmds.delete('PosturePlane')

def ShowPlane(paramList=[],*_):
    """ montre le plan """
    if paramList!=[] and paramList[2]=="On":
        Cote=paramList[1]
        if paramList==[] or paramList[0]=="Curve":
            createCurvePlane(Cote=Cote)
        elif paramList[0]=="Locator":
            createLocatorPlane(Cote=Cote)

def ShowPlaneOn(paramList,*_):
    """ callback 'on' """
    paramList[2]="On"
    ShowPlane(paramList)

def ClickCurve(paramList,*_):
    """ callback 'curve' """
    paramList[0]="Curve"
    ShowPlane(paramList)

def ClickLocator(paramList,*_):
    """ callback 'locator' """
    paramList[0]="Locator"
    ShowPlane(paramList)

def ClickN(paramList,*_):
    """ callback Cote='' """
    paramList[1]=""
    ShowPlane(paramList)

def ClickC(paramList,*_):
    """ callback Cote='C' """
    paramList[1]="C"
    ShowPlane(paramList)

def ClickL(paramList,*_):
    """ callback Cote='N' """
    paramList[1]="L"
    ShowPlane(paramList)

def ClickT(paramList,*_):
    """ callback Cote='T' """
    paramList[1]="T"
    ShowPlane(paramList)




 




