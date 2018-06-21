# create Model

#from functools import partial
#import maya.cmds as cmds
#import maya.mel as mel
#import math
import sys

sys.path.append("C:/Users/alexa/Documents/alexandra/scripts")


path="C:/Users/alexa/Documents/alexandra/scripts/"
execfile(path+"Calculs.py")

def clearVariables(nameList=[]):
    for i,name in enumerate(nameList):
        if(name not in cmds.listRelatives('objGroup')):        
            cmds.parent(name,'objGroup')
    for i in range(40):
        string='joint'+str(i+1)
        if(cmds.objExists(string)):
            cmds.delete(string)   
    #locatorList=cmds.ls('*locator*')
    #for i in locatorList:
    #    if(cmds.objExists(i)):
    #        cmds.delete(i)
    CircleList=cmds.ls('*Circle')  
    for i in CircleList:
        if(cmds.objExists(i)):
            cmds.delete(i)
    ClusterList=cmds.ls('*Cluster*')  
    for i in ClusterList:
        if(cmds.objExists(i)):
            cmds.delete(i)  
    POCList=cmds.ls('*POC*')  
    for i in POCList:
        if(cmds.objExists(i)):
            cmds.delete(i)   
    if(cmds.objExists('ikHandle')):
        cmds.delete('ikHandle')  
    curveList=cmds.ls('*curve*')
    for i in curveList:
        if cmds.objExists(i):
            cmds.delete(i)
    #if(cmds.objExists('curve1')):
    #    cmds.delete('curve1')  
    #if(cmds.objExists('curve2')):
    #    cmds.delete('curve2')  
    #if(cmds.objExists('curve3')):
    #    cmds.delete('curve3')  
    #if(cmds.objExists('curve1insertedKnotCurve1')):
    #    cmds.delete('curve1insertedKnotCurve1')
    nearestPointList=cmds.ls('*nearestPoint*')
    for i in nearestPointList:
        if(cmds.objExists(i)):
            cmds.delete(i)
    restList=cmds.ls('*groupId*')
    restList+=cmds.ls('*tweak*')
    restList+=cmds.ls('*groupParts*')
    restList+=cmds.ls('*transform*')
    restList+=cmds.ls('*joint*')
    restList+=cmds.ls('*Cluster*')
    for i in map(str,restList):
        if(cmds.objExists(i)):
            cmds.delete(i)
    restList=cmds.ls('*groupId*')
    restList+=cmds.ls('*tweak*')
    restList+=cmds.ls('*groupParts*')
    restList+=cmds.ls('*transform*')
    restList+=cmds.ls('*joint*')
    restList+=cmds.ls('*Cluster*')
    a=cmds.ls("*arcLength*")
    for i in a:
        if cmds.objExists(i):
            cmds.delete(i)

#def createJoint(name):
#    center=calcCentroid(name)
#    cmds.select(clear=True)
#    cmds.joint( p=(center[0], center[1], center[2]),scale=(0.6,0.6,0.6),radius=0.3)
 
def createJoint(center):
    cmds.select(clear=True)
    cmds.joint( p=(center[0], center[1], center[2]),scale=(0.6,0.6,0.6),radius=0.1)

def createJointChain(nameList,tailList):
    posList=[]
    for name in nameList:
        posList.append(calcCentroid(name))
    # dernier joint (L6)
    createJoint([-20.91, 33.43, -7.87]) 
    for i in range(25):
        center=pdt(0.5,sum(posList[i],posList[i+1]))
        createJoint(center)
        cmds.parent('joint'+str(i+2),'joint'+str(i+1))
    createJoint([-20.65, 31.59, 11.94])
    cmds.parent('joint27','joint26')
    #mil tete
    createJoint([-20.84, 31.588147934268626, 13.395785063192402])
    cmds.parent('joint28','joint27')
    # tete
    createJoint([-21.187440416932613, 31.778254582324013, 19.917467419599596])
    cmds.parent('joint29','joint28')


        
def bindSkeleton(nameList,tailList):
    cmds.select('joint1')
    for i in range(len(nameList)):
        cmds.select(nameList[i],add=True)
    for i in range(len(tailList)):
        cmds.select(tailList[i],add=True)    
    cmds.select('obj8_Crane_Exterior',add=True)
    cmds.select('obj181_Mandibule_Exterior',add=True)
    cmds.select('obj182_Mandibule_Crane',add=True)
    cmds.bindSkin()

def ClosestPoint(curvePoint):
    posi=position(curvePoint)
    distMax=10000
    indiceMax=-1
    for i in range(MaxCV()):
        temp=[position(curvei(i))[j]-posi[j] for j in range(3)]
        distTemp=math.sqrt(temp[0]**2+temp[1]**2+temp[2]**2)
        if (distTemp<distMax):
            distMax=distTemp
            indiceMax=i 
    return indiceMax

    
def createCurve(pointOnCurveList,nameList):   
    cmds.select('joint1','joint29', add=1)
    handle=cmds.ikHandle(n='ikHandle',ns=1, sol='ikSplineSolver',simplifyCurve=False)
    if('curve1' in cmds.listRelatives('objGroup')):
        cmds.parent( 'curve1', world=True )

    tmpArclenDim=cmds.arcLengthDimension( 'curveShape1.u[0]' )   
    npC = cmds.createNode("nearestPointOnCurve")
    cmds.connectAttr("curveShape1.worldSpace", npC + ".inputCurve")
    cmds.rename('nearestPointOnCurve1', 'nearestPointOnCurveGetParam')

    minValue=cmds.getAttr("curve1.minValue")
    maxValue=cmds.getAttr("curve1.maxValue")
    # peut etre pas besoin aleatoire si position ok, juste pas ws
    for i in range(100):
        param=minValue+(maxValue-minValue)*i/100
        cmds.insertKnotCurve( 'curve1.u['+str(param)+']', ch=True, rpo=True) 
    cmds.delete('curve1' , ch = 1)
    KeepList=[]
    maxCV = cmds.getAttr("curve1.spans")+cmds.getAttr("curve1.degree")
    for curvePoint in pointOnCurveList :
        KeepList.append(ClosestPoint(curvePoint))
    for i in range(maxCV-2,1,-1):
        newMaxCV=cmds.getAttr("curve1.spans")+cmds.getAttr("curve1.degree")
        if(i not in KeepList and i!= newMaxCV):
            cmds.delete(curvei(i))
    cmds.delete('curve1.cv[1]')

    ##cree point de multiplicite 2 au niveau de la tete
    #paramTete=cmds.getAttr("curve1.maxValue")
    #paramC0=getParameter(nearestPoint('C0'))
    ##print "paramC0",paramC0
    ##param=(paramTete+3.0*paramC0)/4.0
    ##cmds.insertKnotCurve( 'curve1.u['+str(paramC0)+']', ch=True) 




def ReplacePoints(pointOnCurveList,nameList):
    cmds.delete('curve1')
    cmds.delete('ikHandle')
    createCurve(pointOnCurveList,nameList)
    createClusters(nameList)
    defPivot()
    
def createClusters(nameList):
    cmds.select('curve1',r=1)   
    cmds.cluster(curvei(n2N('C3')),n='ClusterC')
    cmds.makeIdentity(a=1)
    
    cmds.cluster(curvei(n2N('T11')),n='ClusterL')
    cmds.makeIdentity(a=1)


