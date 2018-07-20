# -*- coding: utf-8 -*-

import maya.api.OpenMaya as om2
#import maya.cmds as cmds
#import maya
#import math
import sys
sys.path.append("C:/Users/alexa/Documents/alexandra/scripts")

path="C:/Users/alexa/Documents/alexandra/scripts/"
execfile(path+"Short.py")
execfile(path+"mesures.py")
execfile(path+"GeneralCalculs.py")


# CALCULS SUR LE MESH

def getBoundingVolume(name):
    size=cmds.getAttr(name+'.boundingBoxSize')[0]
    return size[0]*size[1]*size[2] 

def getBoundingVolumeList(nameList):
    res=[]
    ShowPolygons()
    for i in nameList:
        res.append(getBoundingVolume(i))
    return res

def checkVolumes(nameList,volumeList):
    volumeList2=getBoundingVolumeList(nameList)
    rapportList=[]
    for i,vol in enumerate(volumeList):
        rapportList.append(vol/volumeList2[i])
    return rapportList

def vertexOm2():
 selectionLs = om2.MGlobal.getActiveSelectionList()
 selObj = selectionLs.getDagPath(0)
 mfnObject = om2.MFnMesh(selObj)
 a=mfnObject.getPoints(MSpace.kWorld)
 del selectionLs 
 del mfnObject
 del selObj
 return a

def vertexCmds():
 selTemp = str(cmds.ls(selection=True))
 sel = selTemp.split("'")[1]
 vertPosTemp = cmds.xform(sel + '.vtx[*]', q=True, ws=True, t=True)
 vertPos = zip(*[iter(vertPosTemp)]*3)
 return vertPos

def calcCentroid(name):
    clear()
    cmds.select(name)
    vertPos=vertexCmds()
    n=len(vertPos)
    center=[0,0,0]
    for i in range(n):
        point=vertPos[i]
        center=[center[i]+point[i] for i in range(3)]
    center=[center[i]/(n) for i in range(3)]
    del vertPos
    return center



# CALCULS SUR LA COURBE

def getScale():
    #print getLengthLoc(),locatorCurveLength(),getLength()
    return getLengthLoc()/locatorCurveLength()*getLength()


# trouver une solution car locator bouge pas
def ScaleFactorL():
    pL=pointOnCurveList
    return (distance(locator(0),locator(1))+distance(locator(1),locator(2)))/(distance(pL[0],pL[2])+distance(pL[2],pL[3]))*getLength()

def getScaleCPOC():
    return getLengthLoc()/locatorCPOCCurveLength()*getLength()

def getScaleExtremities():
    d1=distance(projHor(position(locator(0))),projHor(position(locator(3))))
    d2=distance(projHor(position(curvei(0))),projHor(position(curvei(7))))
    sf=d1/d2*getLength()
    return sf

def getScaleComp():
    d1=abs(position(locator(1))[1]-position(locator(2))[1])
    d2=abs(position(locator(1))[1]-findLowestPointC()[1])
    sf=d1/d2*getLength()
    return sf

def ScaleFactor2D():
    posLocT=position(locator(4))
    posLocL=position(locator(0))

    posCrvT=position(curvei(8))
    posCrvL=position(curvei(0))

    distLoc=norm(projHor3D(sub(posLocT,posLocL)))
    distCrv=norm(projHor3D(sub(posCrvT,posCrvL)))
    return getLength()*distLoc/distCrv

         
# orientation par rapport au corps et pas la tete
def getPosition(num=-1,Cote=""):
    return GeneralCalculs.getPosition(posList(),num,Cote=Cote)

def getX(Cote=""):
    return getPosition(0,Cote=Cote)
def getY(Cote=""):
    return getPosition(1,Cote=Cote)
def getZ(Cote=""):
    return getPosition(2,Cote=Cote)

def getLength(L=[]):
    return cmds.arclen("curve1") 

def PostureVector(Cote=""):
    return GeneralCalculs.PostureVector(posList(),Cote=Cote)

# en degres   
def getPosture(Cote=""):
    return GeneralCalculs.getPosture(posList(),Cote=Cote)

def getOrientation(Cote=""):
    return GeneralCalculs.getOrientation(posList(),Cote=Cote)
   
def projPlanPosture(v,Cote=""):
    return GeneralCalculs.projPlanPosture(posList(),v,Cote)

def projPlanPosture3D(p1,p2,Cote=""):
    return GeneralCalculs.projPlanPosture3D(posList(),p1,p2,Cote)

def projPlanPosture2D(p1,p2,Cote=""):
    return GeneralCalculs.projPlanPosture2D(posList(),p1,p2,Cote)

def projPtPV(p1,Cote=""):
    return GeneralCalculs.projPtPV(posList(),p1,Cote)

def projPoint3D(p,pointOnPlane,normal):
    MA=sub(p,pointOnPlane)
    dist=np.dot(normal,MA)/np.linalg.norm(normal)
    pProj=sub(p,pdt(dist,normal))
    return pProj

def createCurvePlane(Cote=""):
    return GeneralCalculs.createPlane(posList(),Cote)

def angle2D(v1, v2):
    v1_n=normalize(v1)
    v2_n=normalize(v2)
    C = (v1_n[0]*v2_n[0]+v1_n[1]*v2_n[1])
    S = (v1[0]*v2[1]-v1[1]*v2[0]);
    angle= np.sign(S)*np.arccos(C)
    return np.degrees(angle) 

def angleHB(v1,PV=False):
   
    return GeneralCalculs.angleHB(posList(),v1,PV)

# voir signe, chercher comment définir
# anglebetween maya!!
def angleHB2V(v1,v2):
    cosinus=np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))
    angle=math.acos(cosinus)
    aB=cmds.angleBetween(v1=v1, v2=v2)
    v12=sub(v1,v2)
    angle=aB[3]
    angle*=np.sign(dotProduct(np.cross(v1,v2),[0,0,1]) )
    return angle

    
def angleGD(v1,v2):
    angle1=np.degrees(math.atan2(v1[0],v1[2]))
    angle2=np.degrees(math.atan2(v2[0],v2[2]))
    return valPrincDeg(angle1-angle2)


def angleCrv(string,*_):
    return GeneralCalculs.angle(posList(),string)


def getDistCVPoint():
    maxCV = cmds.getAttr("curve1.spans")+cmds.getAttr("curve1.degree")
    res=[]
    for i in range(maxCV):
        cvPos=getPoint(getParameter(position(curvei(i))))
        vertPos=getPoint(getParameter(position(n2J(pointOnCurveList[i]))))
        res.append(distance(cvPos,vertPos))
    return res

def getTangent(name): # nom ou position directement
    # position du locator
    if isinstance(name,str):
        pos=position(name)
    else:
        pos=name
    # point le plus proche sur la courbe
    param=getParameter(pos)
    #if(cmds.objExists('locator1')):
    #    cmds.delete('locator1')
    # tangente a la courbe en ce point
    return cmds.pointOnCurve( 'curve1', pr=param,tangent=True )




def getLen(beginP,endP):
    cmds.setAttr ('arcLengthDimension1.uParamValue', beginP)
    distBegin = cmds.getAttr ('arcLengthDimension1.al')
    cmds.setAttr ('arcLengthDimension1.uParamValue', endP)
    distEnd = cmds.getAttr ('arcLengthDimension1.al')
    crvL=cmds.arclen("curve1")
    return [distEnd-distBegin,(distEnd-distBegin)/crvL] 


def getCLen():
    beginP=getParameter(position(curvei(n2N("T1"))))
    endP=getParameter(position(curvei(n2N("C0"))))
    return getLen(beginP,endP)[1]

def getTLen():
    beginP=getParameter(position(curvei(n2N("C0"))))
    endP=getParameter(position(curvei(n2N("Tete"))))
    return getLen(beginP,endP)[1]

def getLLen():
    beginP=getParameter(position(curvei(n2N("L6"))))
    endP=getParameter(position(curvei(n2N("L4"))))
    return getLen(beginP,endP)[1]


def getDist(v,factor,beginP,endP,tmpArclenDim):
    cmds.move(factor*v[0],factor*v[1],factor*v[2],r=True)
    # on calcule la difference
    [crvLengthNew,distBegin,distEnd]=getLen(beginP,endP,tmpArclenDim)
    cmds.move(-v[0],-v[1],-v[2],r=True)
    return distBegin




# CALCULS D' EVALUATION DU MODELE

def calcParameters():
    maxCV = cmds.getAttr("curve1.spans")+cmds.getAttr("curve1.degree")
    param=[]
    positions=[]
    for i in range(maxCV):
        pos=position(curvei(i))
        positions.append(pos)
        param.append(getParameter(pos))
    return [param,positions]


def getJointChainLength(L=[]):
    len=0
    for i in range(1,26):
       len+=distance(position('joint'+str(i)),position('joint'+str(i+1)))
    return len

def locatorCurveLength():
    return GeneralCalculs().getLength(posList()) 

# distance sur la courbe
def locatorCPOCCurveLength():
    posList=[]
    posList.append(position(curvei(0)))
    posList+=map(nearestPoint,locList()[1:-1])
    posList.append(position(curvei(7)))
    # pour les premiers et derniers points, on prend les points exacts, car ils doivent correspondre, pas passer par
    length=0
    for i in range(len(posList)-1):
        length+=distance(posList[i],posList[i+1])
    return length

def HalfChainCurveLengthL():  
    return GeneralCalculs.HalfChainLengthL(posList())

def HalfChainCurveLengthC():
    return GeneralCalculs.HalfChainLengthC(posList())

def RapportChainCurveLength():
    return GeneralCalculs.RapportChainLength(posList())

def RapportCurveLength():
    return RapportChainCurveLength()/RapportChainLength()

def LRapport():
    crv=distance(num2Name(0),num2Name(1))/distance(num2Name(1),num2Name(2))
    loc=distance(locator(0),locator(1))/distance(locator(1),locator(2))
    return crv/loc

def CRapport():
    crv=distance(num2Name(3),num2Name(4))/distance(num2Name(2),num2Name(3))
    loc=distance(locator(3),locator(4))/distance(locator(2),locator(3))
    return crv/loc


def checkParameters(CVparam=[],CVpos=[],jtPos=[],jtParam=[],angles=[],printOK=False):
    res=True
    if CVparam!=[]:
        newCVparam=calcCVParameters()
        for (cvparam,cvparamnew) in zip(CVparam,newCVparam):
            if abs(cvparam-cvparamnew)>0.001:
                res=False
                print "cv param bouge",cvparam,cvparamnew
            else:
                if printOK:
                    print "cv param ok"
    if CVpos!=[]:
        newCVpos=calcCVPositions()
        for (cvpos,cvposnew) in zip(CVpos,newCVpos):
            if distance(cvpos,cvposnew)>0.00001:
                res=False
                print "cv position bouge",cvpos,cvposnew
            else:
                if printOK:
                    print "cv pos ok"
    if jtPos!=[]:
        newJtpos=JointPositions()
        for (jtpos,jtposnew) in zip(jtPos,newJtpos):
            if distance(jtpos,jtposnew)>0.00001:
                res=False
                print "joint position bouge",jtpos,jtposnew
            else:
                if printOK:
                    print "joint pos ok"
    if jtParam!=[]:
        newJtparam=JointParameters()
        for (jtparam,jtparamnew) in zip(jtParam,newJtparam):
            if abs(jtparam-jtparamnew)>0.00001:
                res=False
                print "joint param bouge",jtparam,jtparamnew     
            else:
                if printOK:
                    print "joint param ok"
    if angles!=[]:
        newAngles=calcAngles()
        for(i,j) in zip(angles,newAngles):
            if abs(i-j)>0.00001:
                res=False
                print "angles ont bouge",i,j
            else:
                if printOK:
                    print "angles ok"
     
    if not res:
        print "Modele bouge avec le calcul"
    #else :
    #    print "Modele semble stable"


def EvalPositionLocator():
    rapport=RapportCurveLength()
    d1r=abs(1-rapport)
    cr=CRapport()
    lr=LRapport()
    d1cr=abs(1-cr)
    d1lr=abs(1-lr)
    p("cr",cr,"lr",lr,"rapport",rapport)
    if d1r<0.05:
        if cr>1.1:
            print "decaler T2 vers T8 " + str(cr)
        elif cr<0.9:
            print "decaler T2 vers C1 " + str(cr)
        if lr>1.1:
            print "decaler l3 vers T8 " +str(lr)
        elif lr<0.9:
            print "decaler l3 vers L6 " +str(lr)
        if d1cr<0.1 and d1lr<0.1: 
            print "placement ok " + str(rapport)
    else: 
        if d1lr>0.1 or d1lr>d1cr:
            if rapport>1:
                print "rallonger lombaires"
                if lr<1:
                    print "decaler T8 plus proche des cervicales " + str(lr)
                else :
                    print "decaler L6 vers l'exterieur du squelette " + str(lr)

            else:
                print "raccourcir lombaires"
                if lr<1:
                    print "decaler L6 vers l'interieur du squelette " + str(lr)
                else :
                    print "decaler T8 plus proche des lombaires " + str(lr)
        if d1cr>0.1 or d1cr>d1lr:
            if rapport<1:
                print "rallonger cervicales"
                if cr<1:
                    print "decaler t8 plus proche des lombaires " + str(cr)
                else :
                    print "decaler C1 a l'exterieur du squelette " + str(cr)

            else:
                print "raccourcir cervicales"
                if cr<1:
                    print "decaler C1 vers l'interieur du squelette " + str(cr)
                else :
                    print "decaler T8 plus proche des cervicales " + str(cr)

def EvalPositionLocator2():
    rapport=RapportCurveLength()
    d1r=abs(1-rapport)
    cr=CRapport()
    lr=LRapport()
    d1cr=abs(1-cr)
    d1lr=abs(1-lr)
    p("cr",cr,"lr",lr,"rapport",rapport)
    if d1r<0.05:
        if cr>1.1:
            print "decaler T2 vers T8 " + str(cr)
        elif cr<0.9:
            print "decaler T2 vers C1 " + str(cr)
        if lr>1.1:
            print "decaler T8 vers les lombaires et C1 a l'interieur " +str(lr) #8 decaler T8 en gardant le rapport -> redecale C1
        elif lr<0.9:
            print "decaler T8 vers les cervicales et C1 a l'exterieur " +str(lr) # TODO a ameliorer, cervicales s'etendent ?
        if d1cr<0.1 and d1lr<0.1: 
            print "placement ok " + str(rapport)
    else: 
        if d1lr>0.1 or d1lr>d1cr:
            if rapport>1:
                print "rallonger lombaires"
                if lr<1:
                    print "decaler T8 plus proche des cervicales " + str(lr)
                else :
                    print "decaler T8 plus proche des cervicales " + str(lr)

            else:
                print "raccourcir lombaires"
                if lr<1:
                    print "decaler T8 plus proche des lombaires " + str(lr)
                else :
                    print "decaler T8 plus proche des lombaires " + str(lr)
        if d1cr>0.1 or d1cr>d1lr:
            if rapport<1:
                print "rallonger cervicales"
                if cr<1:
                    print "decaler t8 plus proche des lombaires " + str(cr)
                else :
                    print "decaler C1 a l'exterieur du squelette " + str(cr)

            else:
                print "raccourcir cervicales"
                if cr<1:
                    print "decaler C1 vers l'interieur du squelette " + str(cr)
                else :
                    print "decaler T8 plus proche des cervicales " + str(cr)

    



