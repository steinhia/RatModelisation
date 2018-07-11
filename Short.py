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




def curvei(i,curve='curve1'):
    return curve+'.cv['+str(i)+']'

def locator(i):
    return 'locatorAngle'+str(i)

def joint(i):
    if i>0 and i<29:
        return 'joint'+str(i)
    return -1


#pointOnCurveList=map(n2J,['L6','L3','T11','T8','T2','C4','C1'])
def n2J(name):
    #dico={'L6':'joint1', 'L5':'joint2','L4':'joint3','L3':'joint4','L2':'joint5','L1':'joint6','T13':'joint7', \
    #    'T12':'joint8','T11':'joint9','T10':'joint10','T9':'joint11','T8':'joint12','T7':'joint13','T6':'joint14', \
    #    'T5':'joint15','T4':'joint16','T3':'joint17','T2':'joint18','T1':'joint19','C7':'joint20','C6':'joint21',\
    #    'C5':'joint22','C4':'joint23','C3':'joint24','C2':'joint25','C1':'joint26','C0':'joint27','Tete':'joint28'}
    #if (not isinstance(name,list)) and name in dico :
    #    return dico[name]
    #else:
    #    return -1
    return joint(name2Num(name))


def name2Num(name):
    dico={'L6':1, 'L5':2,'L4':3,'L3':4,'L2':5,'L1':6,'T13':7, \
        'T12':8,'T11':9,'T10':10,'T9':11,'T8':12,'T7':13,'T6':14, \
        'T5':15,'T4':16,'T3':17,'T2':18,'T1':19,'C7':20,'C6':21,\
        'C5':22,'C4':23,'C3':24,'C2':25,'C1':26,'C0':27,'Tete':28}
    if (not isinstance(name,list)) and name in dico :
        return dico[name]
    else:
        return -1

def numSlider(name):
    dico={"CGD":2,"CHB":3,"DGD":4,"DHB":5,"LGD":6,"LHB":7,"CompGD":8,"CompHB":9,"TGD":10,"THB":11}
    if name in dico :
        return dico[name]
    return -1


def n2N(name):
    liste=[abs(name2Num(name)-name2Num(num2NameCV(i))) for i in range(9)]
    return liste.index(min(liste))

def nLoc2nCurve(num):
    dico={0:0,1:1,2:2,3:4,4:6}
    if num in dico :
        return dico[name]
    else :
        return -1

def num2NameCV(num):
    return pointOnCurveList[num]

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


def selectGui(*_):
    res = cmds.promptDialog(message='Name of vertebrate:',button=['OK', 'Cancel'],\
	defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
    print res
    if res=='OK':
        name=cmds.promptDialog(query=True, text=True)
        select(name)

# select a vertebre
def select(name):
    if name=='curve1':
        for i in range(MaxCV()):
            cmds.select(curvei(i),add=True)
    else:
        joint=n2J(name)
        if joint!=-1:
            pos=position(joint)
            param=getParameter(pos)
            maya.mel.eval("doMenuNURBComponentSelection(\"curve1\", \"curveParameterPoint\");")
            cmds.select('curve1.u['+str(param)+']',r=1)

#def nCurveToJoint(num):
#    dico={0:'joint1',1:'joint4',2:'joint7',3:'joint13',4:'joint19',5:'joint23',6:'joint26'}



def position(name):
    if cmds.objExists(name):
        return cmds.xform(name,q=1,t=1,ws=1)
    joint=n2J(name)
    if joint !=-1 :
        return cmds.xform(joint,q=1,t=1,ws=1)
    else:
        return -1
    # nom de la vertebre (objet existe pas)  
   
    
def CVPosition(name):
    if 'locator' in name:
        return position(name)
    return position(curvei(n2N(name)))

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

#def angle_between(v1,v2):
#    dot=dotProduct(v1,v2)
#    if dot<-1:
#        dot=-1
#    if dot>1:
#        dot=1
#    return np.sign(np.cross(v1,v2))*np.degrees(math.acos(dot/(norm(v1)*norm(v2))))

def getPoint(parameter):
    return cmds.pointOnCurve( 'curve1', pr=parameter, p=True )

def getPointHor(parameter):
    return cmds.pointOnCurve( 'curve2', pr=parameter, p=True )
    
def getParameter(location):
    cmds.setAttr("nearestPointOnCurveGetParam.inPosition", location[0], location[1], location[2], type="double3") 
    uParam = cmds.getAttr("nearestPointOnCurveGetParam.parameter")
    return uParam

def getParameterProj(location):
    cmds.setAttr("nearestPointOnCurveHorGetParam.inPosition", location[0], location[1], location[2], type="double3") 
    uParam = cmds.getAttr("nearestPointOnCurveHorGetParam.parameter")
    return uParam

def nearestPoint(name): 
    location=position(name)
    cmds.setAttr("nearestPointOnCurveGetParam.inPosition", location[0], location[1], location[2], type="double3") 
    wParam = cmds.getAttr("nearestPointOnCurveGetParam.position")
    return wParam[0]

def nearestPointHor(name):
    location=position(name)
    cmds.setAttr("nearestPointOnCurveHorGetParam.inPosition", location[0], location[1], location[2], type="double3") 
    wParam = cmds.getAttr("nearestPointOnCurveHorGetParam.position")
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
    res.append(getLength())
    res.append(getPosture())
    res.append(getOrientation())
    res.append(angleCHB())
    res.append(angleCGD())
    res.append(angleLHB())
    res.append(angleLGD())
    res.append(angleTHB())
    res.append(angleTGD())
    res.append(angleCompHB())
    res.append(angleCompGD())
    return res

def calcCVPositions():
    res=[]
    for i in range(MaxCV()):
        res.append(position(curvei(i)))
    return res

def JointPositions():
    res=[]
    for i in range(28):
        res.append(position('joint'+str(i+1)))
    return res

def JointParameters():
    return map(getParameter,JointPositions())

def ScaleFactor():
    return locatorLength()/locatorCurveLength()*getLength()

def ScaleFactorCPOC():
    return locatorLength()/locatorCPOCCurveLength()*getLength()


def projPoint3D(p,pointOnPlane,normal):
    MA=sub(p,pointOnPlane)
    dist=np.dot(normal,MA)/np.linalg.norm(normal)
    pProj=sub(p,pdt(dist,normal))
    return pProj

def ex(name):
    path="C:/Users/alexa/Documents/alexandra/scripts/"
    execfile(path+name)

def mv(v,rel=False):
    cmds.move(v[0],v[1],v[2],r=rel)

def clear():
    cmds.select(clear=True)


def projHor(v):
    return [v[0],v[2]]

def projHor3D(v):
    return [v[0],0,v[2]]

    
        

