# -*- coding: utf-8 -*-
# raccourcis pour fonctions longues a ecrire comme position, valeur de slider etc

from functools import partial
import maya.cmds as cmds
import maya.mel as mel
import math
import time
import sys
import inspect

sys.path.append("C:/Users/alexa/Documents/alexandra/scripts")

path="C:/Users/alexa/Documents/alexandra/scripts/"


#pointOnCurveList=map(n2J,['L6','L3','T11','T8','T2','C4','C1'])
def n2J(name):
    dico={'L6':'joint1', 'L5':'joint2','L4':'joint3','L3':'joint4','L2':'joint5','L1':'joint6','T13':'joint7', \
        'T12':'joint8','T11':'joint9','T10':'joint10','T9':'joint11','T8':'joint12','T7':'joint13','T6':'joint14', \
        'T5':'joint15','T4':'joint16','T3':'joint17','T2':'joint18','T1':'joint19','C7':'joint20','C6':'joint21',\
        'C5':'joint22','C4':'joint23','C3':'joint24','C2':'joint25','C1':'joint26','C0':'joint27','Tete':'joint28'}
    if (not isinstance(name,list)) and name in dico :
        return dico[name]
    elif name=='MilTete':
        return 'joint28'
    else:
        return -1

def n2N(name):
    dico={'L6':0, 'L5':0,'L4':0,'L3':1,'L2':1,'L1':1,'T13':1, \
        'T12':1,'T11':1,'T10':2,'T9':2,'T8':2,'T7':2,'T6':3, \
        'T5':3,'T4':3,'T3':3,'T2':4,'T1':4,'C7':4,'C6':4,\
        'C5':5,'C4':5,'C3':5,'C2':6,'C1':6,'C0':6,'MilTete':7,'Tete':8}
    if name in dico :
        return dico[name]
    elif isinstance(name,str) :
        return name
    else:
        return -1

def nLoc2nCurve(num):
    dico={0:0,1:1,2:2,3:4,4:6}
    if num in dico :
        return dico[name]
    else :
        return -1
    

def num2Name(num):
    if 'sliderGrp' in globals() and hasattr(sliderGrp, 'locatorList'):
        return sliderGrp.locatorList[num]
    if num==0:
        return 'L6'
    elif num==1:
        return 'L4'
    elif num==2:
        return 'T12'
    elif num==3:
        return 'T2'
    elif num==4:
        return 'C0'
    elif num==5:
        return 'Tete'

# select a vertebre
def select(name):
    if name=='curve1':
        for i in range(MaxCV()):
            cmds.select(curvei(i),add=True)
    else:
        pos=position(n2J(name))
        param=getParameter(pos)
        maya.mel.eval("doMenuNURBComponentSelection(\"curve1\", \"curveParameterPoint\");")
        cmds.select('curve1.u['+str(param)+']',r=1)

#def nCurveToJoint(num):
#    dico={0:'joint1',1:'joint4',2:'joint7',3:'joint13',4:'joint19',5:'joint23',6:'joint26'}

def curvei(i):
    return 'curve1.cv['+str(i)+']'

def position(name):
    joint=n2J(name)
    if joint !=-1 :
        return cmds.xform(joint,q=1,t=1,ws=1)
    if cmds.objExists(name):
        return cmds.xform(name,q=1,t=1,ws=1)
    elif name=="MilTete":
        return getMilieu(position('C0'),position('Tete'))
    else:
        return -1
    # nom de la vertebre (objet existe pas)       

def norm(vect) : 
    norm=0.0
    for i in vect:
        norm+=i*i
    return math.sqrt(norm)

def normalize(vect):
    norme=norm(vect)
    if norme!=0 :
        return pdt(1/norme,vect) 
    else : 
        return vect

def dotProduct(vect1,vect2):
    res=0
    for i in range(len(vect1)):
        res+=vect1[i]*vect2[i]
    return res   

def pdt(scalaire,vect):
    return [vect[i]*scalaire for i in range(len(vect))]

def sum(vect1,vect2):
    return [vect1[i]+vect2[i] for i in range(len(vect1))]
    
def sub(vect1,vect2):
    return [vect1[i]-vect2[i] for i in range(len(vect1))]

def SubVector(name1,name2):
    pos1=position(name1)
    pos2=position(name2)
    return sub(pos1,pos2)

def distance(v1,v2):
    if(isinstance(v1,str)):
        v1=position(v1)
        v2=position(v2)
    v=sub(v1,v2)
    return norm(v)  

def pi():
    return 3.14159265359

def degrees(theta):
    return theta*180.0/3.14159265359

def DegToRad(theta):
    return theta/180.0*3.14159265359

def valPrinc(theta):
    bool = (theta<0)
    theta2=theta%(2*pi())
    if bool :
        theta2 -= 2*pi()
    return theta2

def valPrincDeg(theta):
    theta2=theta%(360.0)
    bool = (theta2>180)
    if bool :
        theta2 -= 360.0
    return theta2

def angleHB(v1,v2):
    angle1=np.degrees(math.atan2(v1[1],v1[2]))
    angle2=np.degrees(math.atan2(v2[1],v2[2]))
    return valPrincDeg(angle2-angle1)


def angle_between(v1,v2):
    dot=dotProduct(v1,v2)
    if dot<-1:
        dot=-1
    if dot>1:
        dot=1
    return np.sign(np.cross(v1,v2))*np.degrees(math.acos(dot/(norm(v1)*norm(v2))))

# projette sur le plan forme par la verticale et le vecteur de posture
def angle2D(v1, v2):
    v1_n=normalize(v1)
    v2_n=normalize(v2)
    C = (v1_n[0]*v2_n[0]+v1_n[1]*v2_n[1])
    S = (v1[0]*v2[1]-v1[1]*v2[0]);
    angle= np.sign(S)*np.arccos(C)
    return np.degrees(angle)
    #return np.degrees(np.arctan2(sinang, cosang))
    #return np.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))*np.sign(np.cross(v1,v2))

def angle3DHB(v):
    angle=angle3D(v,[0,0,1])
    

def angleGD(v1,v2):
    angle1=np.degrees(math.atan2(v1[0],v1[2]))
    angle2=np.degrees(math.atan2(v2[0],v2[2]))
    return valPrincDeg(angle1-angle2)

def getPoint(parameter):
    return cmds.pointOnCurve( 'curve1', pr=parameter, p=True )
    
def getParameter(location):
    cmds.setAttr("nearestPointOnCurveGetParam.inPosition", location[0], location[1], location[2], type="double3") 
    uParam = cmds.getAttr("nearestPointOnCurveGetParam.parameter")
    return uParam

def nearestPoint(name): 
    location=position(name)
    cmds.setAttr("nearestPointOnCurveGetParam.inPosition", location[0], location[1], location[2], type="double3") 
    wParam = cmds.getAttr("nearestPointOnCurveGetParam.position")
    return wParam[0]
    

def defPivot():
    pt=getCurvePosition()
    cmds.setAttr('curve1.scalePivot',pt[0],pt[1],pt[2])
    cmds.setAttr('curve1.rotatePivot',pt[0],pt[1],pt[2])

def maxDiff(val1,val2):
    Sub=map(abs,sub(val1,val2))
    maxi=max(Sub)
    i=Sub.index(maxi)
    return [i,maxi]

def p(string,value1=[],value2=[],value3=[],value4=[],value5=[],value6=[]):
    res=str(string)
    if value1!=[]:
        res+=" "
        res+=str(value1)
    if value2!=[]:
        res+=" "
        res+=str(value2)
    if value3!=[]:
        res+=" "
        res+=str(value3)
    if value4!=[]:
        res+=" "
        res+=str(value4)
    if value5!=[]:
        res+=" "
        res+=str(value5)
    if value6!=[]:
        res+=" "
        res+=str(value6)
    print res

def getMilieu(name1,name2):
    if isinstance(name1,str):
        pt1=position(name1)
        pt2=position(name2)
        return (pdt(0.5,sum(pt1,pt2)))
    else:
        return (pdt(0.5,sum(name1,name2)))

def getBarycentre(name1,name2,poids1):
    pt1=position(name1)
    pt2=position(name2)
    return (sum(pdt(poids1,pt1),pdt(1-poids1,pt2)))

def prec(a,n):
    return float(format(a, '.'+str(n)+'f'))

def calcCVParameters():
    maxCV = cmds.getAttr("curve1.spans")+cmds.getAttr("curve1.degree")
    return [getParameter(position(curvei(i))) for i in range(maxCV)]

def CVParam(num):
    return getParameter(position(curvei(num)))

def MaxCV():
    return cmds.getAttr("curve1.spans")+cmds.getAttr("curve1.degree")

def calcAngles():
    res=[]
    res.append(getCurvePosition())
    res.append(getCurveLength())
    res.append(calcPosture())
    res.append(calcOrientation())
    res.append(angleCHB())
    res.append(angleCGD())
    res.append(angleLHB())
    res.append(angleLGD())
    res.append(angleTHB())
    res.append(angleTGD())
    res.append(angleComp())
    res.append(angleCompGD())
    return res

def calcCVPositions():
    res=[]
    for i in range(MaxCV()):
        res.append(position(curvei(i)))
    return res

def JointPositions():
    res=[]
    for i in range(29):
        res.append(position('joint'+str(i+1)))
    return res

def JointParameters():
    return map(getParameter,JointPositions())


    
        

