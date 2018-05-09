# create Model

#from functools import partial
#import maya.cmds as cmds
#import maya.mel as mel
#import math
import sys

sys.path.append("C:/Users/alexandra/Documents/alexandra/scripts")


path="C:/Users/alexandra/Documents/alexandra/scripts/"
execfile(path+"Calculs.py")

def clearVariables(nameList=[]):
    for i,name in enumerate(nameList):
        if(name not in cmds.listRelatives('nurbsCircle1')):        
            cmds.parent(name,'nurbsCircle1')
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
    if(cmds.objExists('curve1')):
        cmds.delete('curve1')  
    if(cmds.objExists('curve2')):
        cmds.delete('curve2')  
    if(cmds.objExists('curve3')):
        cmds.delete('curve3')  
    if(cmds.objExists('curve1insertedKnotCurve1')):
        cmds.delete('curve1insertedKnotCurve1')
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
        cmds.delete(i)

def createJoint(name):
    center=calcCentroid(name)
    cmds.select(clear=True)
    cmds.joint( p=(center[0], center[1], center[2]),scale=(0.6,0.6,0.6),radius=0.3)
 
def createJointChain(nameList,tailList):
    for i in range(len(nameList)):
        createJoint(nameList[i])
        #cmds.makeIdentity(a=1)
        if(i>0):
            cmds.parent('joint'+str(i+1),'joint'+str(i))
    #on rajoute un joint pour la tete
    createJoint('Rat:obj8_Crane_Exterior')
    cmds.parent('joint27','joint26')
    # # le reste de la queue est enfant de joint 1
    createJoint(tailList[0])
    cmds.parent('joint28','joint1')
    for i in range(1,len(tailList)):
        createJoint(tailList[i])
        cmds.parent('joint'+str(i+1+27),'joint'+str(i+27))

def createJoint2(center):
    cmds.select(clear=True)
    cmds.joint( p=(center[0], center[1], center[2]),scale=(0.6,0.6,0.6),radius=0.1)

def createJointChain2(nameList,tailList):
    posList=[]
    for name in nameList:
        posList.append(calcCentroid(name))
    # dernier joint (L6)
    createJoint2([-2.50, 5.35, 5.25])
    for i in range(25):
        center=pdt(0.5,sum(posList[i],posList[i+1]))
        createJoint2(center)
        cmds.parent('joint'+str(i+2),'joint'+str(i+1))
    createJoint2([-2.241516596632577, 5.10, -4.65])
    cmds.parent('joint27','joint26')
        
        

def bindSkeleton(nameList,tailList):
    cmds.select('joint1')
    for i in range(len(nameList)):
        cmds.select(nameList[i],add=True)
    for i in range(len(tailList)):
        cmds.select(tailList[i],add=True)    
    cmds.select('Rat:obj8_Crane_Exterior',add=True)
    cmds.select('Rat:obj181_Mandibule_Exterior',add=True)
    cmds.select('Rat:obj182_Mandibule_Crane',add=True)
    cmds.bindSkin()

def ClosestPoint(curvePoint):
    posi=position(curvePoint)
    distMax=10000
    indiceMax=-1
    maxCV = cmds.getAttr("curve1.spans")+cmds.getAttr("curve1.degree")
    for i in range(maxCV):
        temp=[position(curvei(i))[j]-posi[j] for j in range(3)]
        distTemp=math.sqrt(temp[0]**2+temp[1]**2+temp[2]**2)
        if (distTemp<distMax):
            distMax=distTemp
            indiceMax=i 
    return indiceMax

    
def createCurve(pointOnCurveList,nameList):   
    cmds.select(n2J('L6'),n2J('C0'), add=1)
    handle=cmds.ikHandle(n='ikHandle',ns=90, sol='ikSplineSolver',simplifyCurve=False)
    if('curve1' in cmds.listRelatives('nurbsCircle1')):
        cmds.parent( 'curve1', world=True )
    cmds.delete('curve1' , ch = 1)
    KeepList=[]
    maxCV = cmds.getAttr("curve1.spans")+cmds.getAttr("curve1.degree")
    for curvePoint in pointOnCurveList :
        KeepList.append(ClosestPoint(curvePoint))
    for i in range(maxCV-1,1,-1):
        if(i not in KeepList):
            cmds.delete(curvei(i))
    cmds.delete('curve1.cv[1]')
    cmds.cluster('curve1.cv[6]',n='ClusterEnd')
    cmds.makeIdentity(a=1)
    cmds.select('ClusterEndHandle')
    cmds.select("ikHandle")
    cmds.ikHandle(edit=True,curve="curve1",fj=True)
    cmds.parent("effector1","joint27")
    tmpArclenDim=cmds.arcLengthDimension( 'curveShape1.u[0]' )   
    npC = cmds.createNode("nearestPointOnCurve")
    cmds.connectAttr("curveShape1.worldSpace", npC + ".inputCurve")
    cmds.rename('nearestPointOnCurve1', 'nearestPointOnCurveGetParam')

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

    cmds.cluster(curvei(n2N('T6')),n='ClusterD')
    cmds.makeIdentity(a=1)
    
    cmds.cluster(curvei(n2N('L3')),curvei(n2N('T13')),curvei(n2N('T6')),n='ClusterL')
    cmds.makeIdentity(a=1)


