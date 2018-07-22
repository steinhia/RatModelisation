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
    """ calcule le volume de la boîte englobante de chaque Mesh (pour voir les variations) 
    name : nom complet de l'objet """
    size=cmds.getAttr(name+'.boundingBoxSize')[0]
    return size[0]*size[1]*size[2] 

def getBoundingVolumeList(nameList):
    """ calcule la liste des volumes de boites englobantes de chaque vertebre 
    nameList : liste des maillages de chaque vertèbre """
    res=[]
    ShowPolygons()
    for i in nameList:
        res.append(getBoundingVolume(i))
    return res

def checkVolumes(nameList,volumeList):
    """ compare les volumes de boundingBox avant et après opérations, renvoie la liste des ratios
    volumeList : liste calculée précédemment """
    volumeList2=getBoundingVolumeList(nameList)
    rapportList=[]
    for i,vol in enumerate(volumeList):
        rapportList.append(vol/volumeList2[i])
    return rapportList


def vertexCmds():
    """ renvoie la liste des vertices d'un maillage sélectionné """
 selTemp = str(cmds.ls(selection=True))
 sel = selTemp.split("'")[1]
 vertPosTemp = cmds.xform(sel + '.vtx[*]', q=True, ws=True, t=True)
 vertPos = zip(*[iter(vertPosTemp)]*3)
 return vertPos

def calcCentroid(name):
    """ calcule la posiiton (le centre de masse) d'une vertèbre """
    clear()
    cmds.select(name)
    vertPos=vertexCmds()
    n=len(vertPos)
    center=[0,0,0]
    for i in range(n):
        point=vertPos[i]
        center=sum(center,point)
    center=[center[i]/n for i in range(3)]
    del vertPos
    return center



# CALCULS SUR LA COURBE

def getScale():
    """ calcule le facteur de redimensionnement nécessaire en fonction des longuers des segments des localisateurs """
    return getLengthLoc()/locatorCurveLength()*getLength()


def ScaleFactorL():
    """ scaleFactor seulement avec la longuer des lombaires """
    pL=pointOnCurveList
    return (distance(locator(0),locator(1))+distance(locator(1),locator(2)))/(distance(pL[0],pL[2])+distance(pL[2],pL[3]))*getLength()

def getScaleCPOC():
    """ calcul du facteur de redimensionnement mais utilise le point le plus proche du localisateur au lieu de la vertèbre correspondante
    utile car localisateurs placés de manière imprécise """
    return getLengthLoc()/locatorCPOCCurveLength()*getLength()

def getScaleExtremities():
    """ scaleFactor en fonction de la longueur du segment lombaires-Tete """
    d1=distance(projHor(position(locator(0))),projHor(position(locator(4))))
    d2=distance(projHor(position(curvei(0))),projHor(position(curvei(7))))
    sf=d1/d2*getLength()
    return sf

def getScaleComp():
    """ scaleFactor pour que le minimum local de la courbe soit à la même hauteur  que le localisateur """
    # TODO pourquoi le minimum local ?? 
    d1=abs(position(locator(1))[1]-position(locator(2))[1])
    d2=abs(position(locator(1))[1]-findLowestPointC()[1])
    sf=d1/d2*getLength()
    return sf


         

def getPosition(num=-1,Cote=""):
    """ position de la courbe
    num : int, -1 = vecteur de taille 3, 0<3 = composante correspondante """
    return GeneralCalculs.getPosition(posList(),num,Cote=Cote)

def getX(Cote=""):
    return getPosition(0,Cote=Cote)
def getY(Cote=""):
    return getPosition(1,Cote=Cote)
def getZ(Cote=""):
    return getPosition(2,Cote=Cote)

def getLength(L=[]):
    """ vraie longueur de la courbe """
    return cmds.arclen("curve1") 

def PostureVector(Cote=""):
    """ vecteur de posture de la courbe """
    return GeneralCalculs.PostureVector(posList(),Cote=Cote)

def getPosture(Cote=""):
    """ angle de posture (en degrés) de la courbe """
    return GeneralCalculs.getPosture(posList(),Cote=Cote)

def getOrientation(Cote=""):
    """ angle d'orientation (en degrés) de la courbe """
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
    """ crée le plan postural de la courbe correspondant au coté choisi
    Cote : string "C"=cervicales, "L"=lombaires, "" = tout le corps """
    return GeneralCalculs.createPlane(posList(),Cote)

def angle2D(v1, v2):
    """ angle 2D entre deux vecteurs de dimension 2 """
    v1_n=normalize(v1)
    v2_n=normalize(v2)
    C = (v1_n[0]*v2_n[0]+v1_n[1]*v2_n[1])
    S = (v1[0]*v2[1]-v1[1]*v2[0]);
    angle= np.sign(S)*np.arccos(C)
    return np.degrees(angle) 

def angleHB(v1,PV=False):
    """ angle vertical d'un vecteur """
    # TODO utilisé ,???
    return GeneralCalculs.angleHB(posList(),v1,PV)

#TODO utilisé ??
def angleHB2V(v1,v2):
    cosinus=np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))
    angle=math.acos(cosinus)
    aB=cmds.angleBetween(v1=v1, v2=v2)
    v12=sub(v1,v2)
    angle=aB[3]
    angle*=np.sign(dotProduct(np.cross(v1,v2),[0,0,1]) )
    return angle



def angleGD(v1,v2):
    """ angle latéral entre deux vecteurs """
    angle1=np.degrees(math.atan2(v1[0],v1[2]))
    angle2=np.degrees(math.atan2(v2[0],v2[2]))
    return valPrincDeg(angle1-angle2)



def angleCrv(string,*_):
    """ angles des opérations calculés sur la courbe
    string : string, opération choisie ex CGD = cervicales latéral """
    return GeneralCalculs.angle(posList(),string)


def getDistCVPoint():
    maxCV = cmds.getAttr("curve1.spans")+cmds.getAttr("curve1.degree")
    res=[]
    for i in range(maxCV):
        cvPos=getPoint(getParameter(position(curvei(i))))
        vertPos=getPoint(getParameter(position(n2J(pointOnCurveList[i]))))
        res.append(distance(cvPos,vertPos))
    return res

def getTangent(name): 
    """ tangente à la courbe en un point 
    name : string pour nom dela vertèbre, ou objet de maya
           ou bien position directement """
    # position du locator
    if isinstance(name,str):
        pos=position(name)
    else:
        pos=name
    # point le plus proche sur la courbe
    param=getParameter(pos)
    return cmds.pointOnCurve( 'curve1', pr=param,tangent=True )


def getLen(beginP,endP):
    """ [longueur de courbe entre deux paramètres, proportion ]
    beginP,endP : float, paramètres de début et fin """
    cmds.setAttr ('arcLengthDimension1.uParamValue', beginP)
    distBegin = cmds.getAttr ('arcLengthDimension1.al')
    cmds.setAttr ('arcLengthDimension1.uParamValue', endP)
    distEnd = cmds.getAttr ('arcLengthDimension1.al')
    crvL=cmds.arclen("curve1")
    return [distEnd-distBegin,(distEnd-distBegin)/crvL] 


def getCLen():
    """ longueur de courbe  et proportion de la longueur totale de la courbe pour les cervicales """
    beginP=getParameter(position(curvei(n2N("T1"))))
    endP=getParameter(position(curvei(n2N("C0"))))
    return getLen(beginP,endP)[1]

def getTLen():
    """ longueur de courbe  et proportion de la longueur totale de la courbe pour la tete """
    beginP=getParameter(position(curvei(n2N("C0"))))
    endP=getParameter(position(curvei(n2N("Tete"))))
    return getLen(beginP,endP)[1]

def getLLen():
    """ longueur de courbe  et proportion de la longueur totale de la courbe pour les lombaires """
    beginP=getParameter(position(curvei(n2N("L6"))))
    endP=getParameter(position(curvei(n2N("L4"))))
    return getLen(beginP,endP)[1]



# TODO je sais plus
def getDist(v,factor,beginP,endP,tmpArclenDim):
    cmds.move(factor*v[0],factor*v[1],factor*v[2],r=True)
    # on calcule la difference
    [crvLengthNew,distBegin,distEnd]=getLen(beginP,endP,tmpArclenDim)
    cmds.move(-v[0],-v[1],-v[2],r=True)
    return distBegin




# CALCULS D' EVALUATION DU MODELE

def calcParameters():
    """ renvoie les paramètres et positions des points de controle """
    maxCV = cmds.getAttr("curve1.spans")+cmds.getAttr("curve1.degree")
    param=[]
    positions=[]
    for i in range(maxCV):
        pos=position(curvei(i))
        positions.append(pos)
        param.append(getParameter(pos))
    return [param,positions]


def getJointChainLength(*_):
    """ calcule la longueur de la chaine formée par les joints """
    len=0
    for i in range(1,26):
       len+=distance(position('joint'+str(i)),position('joint'+str(i+1)))
    return len

def locatorCurveLength():
    """ longueur de la courbe calculée à partir des segments correspondant aux vertèbres représentées par les localisateurs """
    return GeneralCalculs().getLength(posList()) 

def locatorCPOCCurveLength():
    """ longueur de la courbe calculée à partir points les plus proches des localisateurs sur la courbe """
    posList=[]
    # pour les premiers et derniers points, on prend les points exacts, car ils doivent correspondre, pas passer par et continuer
    posList.append(position(curvei(0)))
    posList+=map(nearestPoint,locList()[1:-1])
    posList.append(position(curvei(7)))

    length=0
    for i in range(len(posList)-1):
        length+=distance(posList[i],posList[i+1])
    return length

def HalfChainCurveLengthL():
    """ longueur de la chaine de segments au niveau des lombaires """
    return GeneralCalculs.HalfChainLengthL(posList())

def HalfChainCurveLengthC():
    """ longueur de la chaine de segments au niveau des cervicales """
    return GeneralCalculs.HalfChainLengthC(posList())

def RapportChainCurveLength():
    # TODO je sais plus
    return GeneralCalculs.RapportChainLength(posList())

def RapportCurveLength():
        # TODO je sais plus
    return RapportChainCurveLength()/RapportChainLength()

def LRapport():
        # TODO je sais plus
    crv=distance(num2Name(0),num2Name(1))/distance(num2Name(1),num2Name(2))
    loc=distance(locator(0),locator(1))/distance(locator(1),locator(2))
    return crv/loc

def CRapport():
        # TODO je sais plus
    crv=distance(num2Name(3),num2Name(4))/distance(num2Name(2),num2Name(3))
    loc=distance(locator(3),locator(4))/distance(locator(2),locator(3))
    return crv/loc


def checkParameters(CVparam=[],CVpos=[],jtPos=[],jtParam=[],angles=[],printOK=False):
    """ vérification que les paramètres et positions des points de controle et des joints ainsi que les angles 
    n'ont pas bougé par rapport aux valeurs de référence 
    arguments : listes de parmètres et positions """
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
    """ evaluation du placement des localisateurs par calcul de rapports de longueur """
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


    



