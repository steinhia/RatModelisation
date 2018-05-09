import maya.api.OpenMaya as om2
#import maya.cmds as cmds
#import maya
#import math
import sys
sys.path.append("C:/Users/alexandra/Documents/alexandra/scripts")

path="C:/Users/alexandra/Documents/alexandra/scripts/"
execfile(path+"Short.py")


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

def getTangent(name):
    # position du locator
    pos=position(name)
    # point le plus proche sur la courbe
    param=getParameter(pos)
    if(cmds.objExists('locator1')):
        cmds.delete('locator1')
    # tangente a la courbe en ce point
    return cmds.pointOnCurve( 'curve1', pr=param,tangent=True )
     

# orientation par rapport au corps et pas la tete
def getCurvePosition(num=-1):
    pos=position(num2Name(2)) 
    if num==-1 or num>2:
        return pos
    else:
        return pos[num]

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
    x=0
    for i in range(4):
        x+=distance(num2Name(i),num2Name(i+1))
    return x     
   
def calcCourbure(L):
    [v1,v2]=L
    rot1=getTangent(n2J(v1)) #n2J
    rot2=getTangent(n2J(v2))
    return RadToDeg(rot1[1]-rot2[1])

# en deg
def calcLordoseC(L=[]):
    return calcCourbure(['C0','T2'])

# en deg
def calcCyphoseD(L=[]):
    return calcCourbure(['T2','L1'])

# en deg
def calcLordoseL(L=[]):
    return calcCourbure(['L1','L6'])

def PostureVector(L=[]):
    v=SubVector(num2Name(1),num2Name(3))
    return v
# en degres 
   
def calcPosture(L=[]):
    #posT1=position(n2J(num2Name(3)))
    #posL6=position(n2J(num2Name(1)))
    #posColonne=sub(posL6,posT1)
    return valPrincDeg(angleHB(PostureVector(),[0,0,1]))

def calcPostureGD(L=[]):
    return valPrincDeg(angleGD(PostureVector(),[1,0,0])+90.0)

def calcAlign():
    posT1=position(n2J('C1'))
    posL6=position(n2J('L6'))
    posColonne=sub(posT1,posL6)
    res=valPrincDeg(RadToDeg(math.atan2(posColonne[2],posColonne[0]))+90)
    return res

def SubVector(name1,name2):
    pos1=position(name1)
    pos2=position(name2)
    return sub(pos1,pos2)

def angleHB(v1,v2):
    angle1=RadToDeg(math.atan2(v1[1],v1[2]))
    angle2=RadToDeg(math.atan2(v2[1],v2[2]))
    return valPrincDeg(angle1-angle2)

def angleGD(v1,v2):
    angle1=RadToDeg(math.atan2(v1[0],v1[2]))
    angle2=RadToDeg(math.atan2(v2[0],v2[2]))
    return valPrincDeg(angle1-angle2)

def calcOrientationHB(L):
    [debut,fin]=L
    angle=angleHB(SubVector(debut,fin),[0,0,1])
    #angle=angleHB(SubVector(debut,fin),locatorPostureVector())
    return angle

def calcOrientationGD(L): # peut etre re besoin de crvInfos
    [debut,fin]=L
    angle=angleGD(SubVector(debut,fin),[0,0,1])
    #angle=angleGD(SubVector(debut,fin),locatorPostureVector())
    return angle

#TODO enregistrer postureVector a la place de posture au debut
def calcRotDHB(L=[]):
    return calcOrientationHB([num2Name(1),num2Name(2)])
def calcRotDGD(L=[]):
    return calcOrientationGD([num2Name(1),num2Name(2)])
def calcRotCHB(L=[]):
    return calcOrientationHB([num2Name(3),num2Name(4)])
def calcRotCGD(L=[]):
    return calcOrientationGD([num2Name(3),num2Name(4)])
def calcRotLHB(L=[]):
    return calcOrientationHB([num2Name(0),num2Name(1)])
def calcRotLGD(L=[]):
    return calcOrientationGD([num2Name(0),num2Name(1)])


def calcCompressionDorsales(crvInfos=[]):
    angle=valPrincDeg(angleHB(SubVector(num2Name(2),num2Name(3)),[0,0,1]))
    return angle

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



    



