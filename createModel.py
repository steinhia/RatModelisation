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


def placePlanes():
    v0=position('seq002_x1_tex.vtx[0]')
    v2=position('seq002_x1_tex.vtx[2]')
    v02=sub(v0,v2)
    # axe puis valeur
    aA=cmds.angleBetween( v1=v02, v2=(1.0, 0.0, 0.0) )
    angle=aA[-1]
    cmds.select('camGroup')
    cmds.rotate(angle*aA[0],angle*aA[1],angle*aA[2],r=True)


def createJoint(center):
    cmds.select(clear=True)
    cmds.joint( p=(center[0], center[1], center[2]),scale=(0.6,0.6,0.6),radius=0.1)

def ImportMesh():
    maya.mel.eval('file -import -type "OBJ"  -ignoreVersion -ra true -mergeNamespacesOnClash false -namespace "Rat" -options "mo=1"  -pr  -importFrameRate true  -importTimeRange "override" "C:/Users/alexa/Documents/alexandra/ScenesMaya/Rat.obj";')
    # on renomme
    AllMeshes=cmds.ls('Rat:obj*')
    AllMeshes=[obj for obj in AllMeshes if "Shape" not in obj]

    # on cree objGroup
    cmds.CreateEmptyGroup()
    cmds.rename('null1','objGroup')

    AllMeshes2=[]
    for obj in AllMeshes:
        cmds.rename(obj,obj[4:])
        cmds.parent(obj[4:],'objGroup')
        AllMeshes2.append(obj[4:])

    for obj in AllMeshes2:
        cmds.select(obj,add=True)
    cmds.scale(0.002,0.002,0.002,r=True)

    L6=cmds.ls('obj*L6_Exterior')[0]
    posL6=calcCentroid(L6)

    C1=cmds.ls('obj*C1*')[0]
    posC1=calcCentroid(C1)

    for obj in AllMeshes2:
        cmds.select(obj,add=True)
    mv(pdt(-1,posL6))





    # on donne le bon angle
    v=sub(posL6,posC1)
    aA=cmds.angleBetween( v1=v, v2=(1.0, 0.0, 0.0) )
    cmds.select('camGroup')
    cmds.rotate(angle*aA[0],angle*aA[1],angle*aA[2],r=True)




def createJointChain(nameList,tailList):
    posList=[]
    for name in nameList:
        posList.append(calcCentroid(name))
    # dernier joint (L6)
    createJoint(sum([0.0580408770842773, 0.003912234643060231, -1.3959898887303481],calcCentroid(nameList[0])))
    #createJoint([-20.91, 33.43, -7.87]) 
    for i in range(25):
        center=pdt(0.5,sum(posList[i],posList[i+1]))
        createJoint(center)
        cmds.parent('joint'+str(i+2),'joint'+str(i+1))
    #createJoint([-20.65, 31.59, 11.94])
    createJoint(sum(position('joint26'),[-0.048737799484715794, 0.1299700221483242, 0.48699161668587543]))
    cmds.parent('joint27','joint26')
    # tete
    createJoint(sum(position('joint26'),[-0.5374404169326112, 0.18825458232401004, 7.977467419599595]))
    #createJoint([-21.187440416932613, 31.778254582324013, 19.917467419599596])
    cmds.parent('joint28','joint27')
       
def bindSkeleton(nameList,tailList):
    cmds.select('joint1')
    for i in range(len(nameList)):
        cmds.select(nameList[i],add=True)
    for i in range(len(tailList)):
        cmds.select(tailList[i],add=True)    
    cmds.select('obj8_Crane_Exterior',add=True)
    cmds.select('obj181_Mandibule_Exterior',add=True)
    cmds.select('obj182_Mandibule_Crane',add=True)
    cmds.select('obj109_OsHyoide_Exterior',add=True)
    cmds.bindSkin()

def ClosestPoint(curvePoint):
    if isinstance(curvePoint,str):
        posi=position(curvePoint)
    else :
        posi=curvePoint
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
    cmds.select('joint1','joint28', add=1)
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
    point=getPoint(getParameter(position(n2J('C0')))+2)
    KeepList.append(ClosestPoint(point))
    for i in range(maxCV-2,1,-1):
        newMaxCV=cmds.getAttr("curve1.spans")+cmds.getAttr("curve1.degree")
        if(i not in KeepList and i!= newMaxCV):
            cmds.delete(curvei(i))
    cmds.delete('curve1.cv[1]')
    #cmds.insertKnotCurve( 'curve1.u[15]', ch=True, rpo=True) 
    #cmds.hardenPointCurve( 'curve1.cv[6]', ch=True, rpo=True, m=-2 )

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


