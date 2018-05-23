import maya.api.OpenMaya as om2
#import maya.cmds as cmds
#import maya
#import math
import sys
sys.path.append("C:/Users/alexandra/Documents/alexandra/scripts")

path="C:/Users/alexandra/Documents/alexandra/scripts/"
execfile(path+"Short.py")
execfile(path+"mesures.py")
execfile(path+"GeneralCalculs.py")

def vertexOm2():
 selectionLs = om2.MGlobal.getActiveSelectionList()
 selObj = selectionLs.getDagPath(0)
 mfnObject = om2.MFnMesh(selObj)
 a=mfnObject.getPoints()
 del selectionLs 
 del mfnObject
 del selObj
 return a

def calcCentroid(name):
    cmds.select(name)
    vertPos=vertexOm2()
    n=len(vertPos)
    center=[0,0,0]
    for i in range(n):
        point=vertPos[i]
        center=[center[i]+point[i] for i in range(3)]
    center=[center[i]/(n) for i in range(3)]
    del vertPos
    return center

#def calcTan(beginVertebre,endVertebre, *_):
#    posV1=position(beginVertebre)
#    posV2=position(endVertebre)
#    tan=[posV2[i]-posV1[i] for i in range(3)]
#    #tan[0]=0
#    norm=tan[1]**2+tan[2]**2
#    if norm!=0 :
#        return [tan[i]/math.sqrt(norm) for i in range(3)]
#    return [0,0,0]

def getTangent(name): # nom ou position directement
    # position du locator
    if isinstance(name,str):
        pos=position(name)
    else:
        pos=name
    # point le plus proche sur la courbe
    param=getParameter(pos)
    if(cmds.objExists('locator1')):
        cmds.delete('locator1')
    # tangente a la courbe en ce point
    return cmds.pointOnCurve( 'curve1', pr=param,tangent=True )
     

# orientation par rapport au corps et pas la tete
def getCurvePosition(num=-1):
    positionList=[num2Name(i) for i in range(5)]
    return GeneralCalculs.getPosition(positionList,num)

def getX(L=[]):
    return getCurvePosition(0)
def getY(L=[]):
    return getCurvePosition(1)
def getZ(L=[]):
    return getCurvePosition(2)

def getCurveLength(L=[]):
    return cmds.arclen("curve1") 

def getChainLength(L=[]):
    len=0
    for i in range(1,26):
       len+=distance(position('joint'+str(i)),position('joint'+str(i+1)))
    return len

def locatorCurveLength():
    positionList=[num2Name(i) for i in range(5)]
    return GeneralCalculs().getChainLength(positionList) 

def HalfChainCurveLengthL():
    positionList=[num2Name(i) for i in range(5)]
    return GeneralCalculs.HalfChainLengthL(positionList)

def HalfChainCurveLengthC():
    positionList=[num2Name(i) for i in range(5)]
    return GeneralCalculs.HalfChainLengthC(positionList)

def RapportChainCurveLength():
    positionList=[num2Name(i) for i in range(5)]
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


   
def calcCourbure(L):
    [v1,v2]=L
    rot1=getTangent(n2J(v1)) #n2J
    rot2=getTangent(n2J(v2))
    return angleHB(rot2,rot1)
    return RadToDeg(rot2[1]-rot1[1])

# en deg
def calcLordoseC(L=[]):
    return calcCourbure(['C0','T2'])

# en deg
def calcCyphoseD(L=[]):
    return calcCourbure(['T1','L1'])

# en deg
def calcLordoseL(L=[]):
    return -calcCourbure(['T7','L3'])

def PostureVector(L=[]):
    positionList=[num2Name(i) for i in range(5)]
    return GeneralCalculs.PostureVector(positionList)

# en degres   
def calcPosture(L=[]):
    positionList=[num2Name(i) for i in range(5)]
    return GeneralCalculs.getPosture(positionList)

def calcPostureGD(L=[]):
    return valPrincDeg(angleGD(PostureVector(),[1,0,0])+90.0)

def calcAlign():
    posT1=position(n2J('C1'))
    posL6=position(n2J('L6'))
    posColonne=sub(posT1,posL6)
    res=valPrincDeg(RadToDeg(math.atan2(posColonne[2],posColonne[0]))+90)
    return res

def calcRotCHB(L=[]):
    positionList=[num2Name(i) for i in range(5)]
    return GeneralCalculs.angleCHB(positionList)
def calcRotCGD(L=[]):
    positionList=[num2Name(i) for i in range(5)]
    return GeneralCalculs.angleCGD(positionList)
def calcRotDHB(L=[]):
    positionList=[num2Name(i) for i in range(5)]
    return GeneralCalculs.angleDHB(positionList)
def calcRotDGD(L=[]):
    positionList=[num2Name(i) for i in range(5)]
    return GeneralCalculs.angleDGD(positionList)
def calcRotLHB(L=[]):
    positionList=[num2Name(i) for i in range(5)]
    return GeneralCalculs.angleLHB(positionList)
def calcRotLGD(L=[]):
    positionList=[num2Name(i) for i in range(5)]
    return GeneralCalculs.angleLGD(positionList)


def calcComp(crvInfos=[]):
    positionList=[num2Name(i) for i in range(5)]
    return GeneralCalculs.angleComp(positionList)

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


def getDist(v,factor,beginP,endP,tmpArclenDim):
    cmds.move(factor*v[0],factor*v[1],factor*v[2],r=True)
    # on calcule la difference
    [crvLengthNew,distBegin,distEnd]=getLen(beginP,endP,tmpArclenDim)
    cmds.move(-v[0],-v[1],-v[2],r=True)
    return distBegin

def calcParameters():
    maxCV = cmds.getAttr("curve1.spans")+cmds.getAttr("curve1.degree")
    param=[]
    positions=[]
    for i in range(maxCV):
        pos=position(curvei(i))
        positions.append(pos)
        param.append(getParameter(pos))
    return [param,positions]



    



