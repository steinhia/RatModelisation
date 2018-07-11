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
          
# orientation par rapport au corps et pas la tete
def getCurvePosition(num=-1,Cote=""):
    positionList=[num2Name(i) for i in range(6)]
    return GeneralCalculs.getPosition(positionList,num,Cote=Cote)

def getX(Cote=""):
    return getCurvePosition(0,Cote=Cote)
def getY(Cote=""):
    return getCurvePosition(1,Cote=Cote)
def getZ(Cote=""):
    return getCurvePosition(2,Cote=Cote)

def getLength(L=[]):
    return cmds.arclen("curve1") 

def PostureVector(Cote=""):
    positionList=[num2Name(i) for i in range(6)]
    return GeneralCalculs.PostureVector(positionList,Cote=Cote)

# en degres   
def getPosture(Cote=""):
    positionList=[num2Name(i) for i in range(6)]
    return GeneralCalculs.getPosture(positionList,Cote=Cote)

def getOrientation(Cote=""):
    positionList=[num2Name(i) for i in range(6)]
    return GeneralCalculs.getOrientation(positionList,Cote=Cote)
   
def calcCourbure(L):
    [v1,v2]=L
    rot1=getTangent(n2J(v1)) #n2J
    rot2=getTangent(n2J(v2))
    #return angleHB(rot2,rot1)
    return np.degrees(rot2[1]-rot1[1])

# en deg
def calcLordoseC(L=[]):
    return calcCourbure([pointOnCurveList[6],pointOnCurveList[4]])

# en deg
def calcCyphoseD(L=[]):
    return calcCourbure(['T1','L1'])

# en deg
def calcLordoseL(L=[]):
    return -calcCourbure([pointOnCurveList[3],pointOnCurveList[1]])

def projPlanPosture(v,Cote=""):
    positionList=[num2Name(i) for i in range(6)]
    return GeneralCalculs.projPlanPosture(positionList,v,Cote)

def projPlanPosture3D(p1,p2,Cote=""):
    positionList=[num2Name(i) for i in range(6)]
    return GeneralCalculs.projPlanPosture3D(positionList,p1,p2,Cote)

def projPlanPosture2D(p1,p2,Cote=""):
    positionList=[num2Name(i) for i in range(6)]
    return GeneralCalculs.projPlanPosture2D(positionList,p1,p2,Cote)

def projPtPV(p1,Cote=""):
    positionList=[num2Name(i) for i in range(6)]
    return GeneralCalculs.projPtPV(positionList,p1,Cote)

def createCurvePlane(Cote=""):
    positionList=[num2Name(i) for i in range(6)]
    return GeneralCalculs.createPlane(positionList,Cote)

def angle2D(v1, v2):
    v1_n=normalize(v1)
    v2_n=normalize(v2)
    C = (v1_n[0]*v2_n[0]+v1_n[1]*v2_n[1])
    S = (v1[0]*v2[1]-v1[1]*v2[0]);
    angle= np.sign(S)*np.arccos(C)
    return np.degrees(angle) 

def angleHB(v1,PV=False):
    positionList=[num2Name(i) for i in range(6)]
    return GeneralCalculs.angleHB(positionList,v1,PV)

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
    positionList=[num2Name(i) for i in range(6)]
    return GeneralCalculs.angle(positionList,string)

#def angleCHB():
#    positionList=[num2Name(i) for i in range(6)]
#    return GeneralCalculs.angleCHB(positionList,pointOnCurveList)
#def angleCGD():
#    positionList=[num2Name(i) for i in range(6)]
#    return GeneralCalculs.angleCGD(positionList,pointOnCurveList)
#def angleDHB():
#    positionList=[num2Name(i) for i in range(6)]
#    return GeneralCalculs.angleDHB(positionList)
#def angleDGD():
#    positionList=[num2Name(i) for i in range(6)]
#    return GeneralCalculs.angleDGD(positionList)
#def angleLHB():
#    positionList=[num2Name(i) for i in range(6)]
#    return GeneralCalculs.angleLHB(positionList)
#def angleLGD():
#    positionList=[num2Name(i) for i in range(6)]
#    return GeneralCalculs.angleLGD(positionList)

#def angleTHB():
#    positionList=[num2Name(i) for i in range(6)]
#    liste=[num2Name(i) for i in range(6)]
#    v=SubVector(liste[5],liste[4])
#    l=norm([v[0],v[2]])
#    sens=np.sign(np.dot(projHor3D(v),projHor3D(GeneralCalculs.PostureVector(liste))))
#    #print "vlsens",v,l,np.dot(projHor3D(v),projHor3D(GeneralCalculs.PostureVector(liste))),angle2D([l,0],[sens*l,v[1]]),projHor3D(GeneralCalculs.PostureVector(liste))
#    return GeneralCalculs.angleTHB(positionList)

#def angleTGD():
#    positionList=[num2Name(i) for i in range(6)]
#    return GeneralCalculs.angleTGD(positionList)

#def angleCompHB():
#    positionList=[num2Name(i) for i in range(6)]
#    return GeneralCalculs.angleCompHB(positionList)
#def angleCompGD():
#    positionList=[num2Name(i) for i in range(6)]
#    return GeneralCalculs.angleCompGD(positionList)


def getDistCVPoint():
    maxCV = cmds.getAttr("curve1.spans")+cmds.getAttr("curve1.degree")
    res=[]
    for i in range(maxCV):
        cvPos=getPoint(getParameter(position(curvei(i))))
        vertPos=getPoint(getParameter(position(n2J(pointOnCurveList[i]))))
        res.append(norm(sub(cvPos,vertPos)))
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
    positionList=[num2Name(i) for i in range(6)]
    return GeneralCalculs().getChainLength(positionList) 

def locatorCPOCCurveLength():
    posList=map(nearestPoint,[locator(i) for i in range(6)])
    posList=[posList[i] for i in range(6) if i!=1]
    length=0
    for i in range(len(posList)-1):
        length+=distance(posList[i],posList[i+1])
    return length

def HalfChainCurveLengthL():
    positionList=[num2Name(i) for i in range(6)]
    return GeneralCalculs.HalfChainLengthL(positionList)

def HalfChainCurveLengthC():
    positionList=[num2Name(i) for i in range(6)]
    return GeneralCalculs.HalfChainLengthC(positionList)

def RapportChainCurveLength():
    positionList=[num2Name(i) for i in range(6)]
    return GeneralCalculs.RapportChainLength(positionList)

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
            if norm(sub(cvpos,cvposnew))>0.00001:
                res=False
                print "cv position bouge",cvpos,cvposnew
            else:
                if printOK:
                    print "cv pos ok"
    if jtPos!=[]:
        newJtpos=JointPositions()
        for (jtpos,jtposnew) in zip(jtPos,newJtpos):
            if norm(sub(jtpos,jtposnew))>0.00001:
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

    



# aucun sens parce que projection seulement pour un vecteur
#def angleGD(v1,v2):
#    v=sub(v1,v2)
#    positionList=[num2Name(i) for i in range(6)]
#    return GeneralCalculs.angleGD2D(positionList,v)
#def angleHB(v1,v2):
#    v=SubVector(v1,v2)
#    positionList=[num2Name(i) for i in range(6)]
#    return GeneralCalculs.angleHB(positionList,v)

#def angleHB(v):
#    l=norm([v[0],v[2]])
#    if l==0:
#        return 90*np.sign(v[1])
#    return angle2D([l,0],[l,v[1]])

#def vect3DTo2D(v):
#    return [norm([v[0],v[2]]),v[1]]    

#def angleHB2DWithSign(v):
#    if abs(v[0])>abs(v[0]):
#        l=norm([v[0],v[2]])*np.sign(v[0])
#    else:
#        l=norm([v[0],v[2]])*np.sign(v[2])
#    if l==0:
#        return 90*np.sign(v[1])
#    return angle2D([abs(l),0],[l,v[1]])

#def angleHBOld(v1,v2):
#    angle1=RadToDeg(math.atan2(v1[1],v1[2]))
#    angle2=RadToDeg(math.atan2(v2[1],v2[2]))
#    return valPrincDeg(angle1-angle2)

#def angleGDOld(v1,v2):
#    angle1=RadToDeg(math.atan2(v1[0],v1[2]))
#    angle2=RadToDeg(math.atan2(v2[0],v2[2]))
#    return valPrincDeg(angle1-angle2)


#def angleHB(v1,v2):
#    angle1=np.degrees(math.atan2(v1[1],v1[2]))
#    angle2=np.degrees(math.atan2(v2[1],v2[2]))
#    return valPrincDeg(angle2-angle1)


