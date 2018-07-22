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


# NAMES / NUM

def curvei(i,curve='curve1'):
    """ nom du ième point du controle """
    return curve+'.cv['+str(i)+']'

def posList(*_):
    """ liste des vertèbres qui correspondent à un localisateur """
    if 'sliderGrp' in globals() and hasattr(sliderGrp, 'locatorList'):
        return sliderGrp.locatorList
    return [num2Name(i) for i in range(6)]

def POCList():
    """ liste des vertèbres correspondant aux points de controle """
    if 'sliderGrp' in globals() and hasattr(sliderGrp, 'pointOnCurveList'):
        return sliderGrp.pointOnCurveList
    return -1

def curveList():
    """ liste des points de controle """
    return [curvei(i) for i in range(MaxCV())]

def locator(i):
    """ nom du ième localisateur """
    return 'locatorAngle'+str(i)

def locList(Cote=""):
    """ liste des noms des localisateurs """
    return [locator(i) for i in range(5)]

def joint(i):
    """ nom du ième joint """
    if i>0 and i<29:
        return 'joint'+str(i)
    return -1

def n2J(name):
    """ nom du joint correspondant au nom de vertèbre """
    return joint(name2Num(name))

def name2Num(name):
    """ numéro du joint correspondant au nom de vertèbre """
    dico={'L6':1, 'L5':2,'L4':3,'L3':4,'L2':5,'L1':6,'T13':7, \
        'T12':8,'T11':9,'T10':10,'T9':11,'T8':12,'T7':13,'T6':14, \
        'T5':15,'T4':16,'T3':17,'T2':18,'T1':19,'C7':20,'C6':21,\
        'C5':22,'C4':23,'C3':24,'C2':25,'C1':26,'C0':27,'Tete':28}
    if (not isinstance(name,list)) and name in dico :
        return dico[name]
    else:
        return -1

def paramList():
    """ liste des paramètres/opérations à effectuer """
    return ['CGD','CHB','LGD','LHB','CompGD','CompHB','TGD','THB','X','Y','Z','Posture','Orientation','Length']

def numSlider(name):
    """ numéro du slider effectuant l'opération indiquée par name """
    l=paramList()
    return l.index(name)


def n2N(name):
    """ numéro du point de controle le plus proche de la vertèbre """
    liste=[abs(name2Num(name)-name2Num(num2NameCV(i))) for i in range(MaxCV())]
    return liste.index(min(liste))

def nLoc2nCurve(num):
    """ numéro du point de controle correspondant au numéro de localisateur """
    dico={0:0,1:1,2:2,3:4,4:6}
    if num in dico :
        return dico[name]
    else :
        return -1

def num2NameCV(num):
    """ nom de la vertèbre correspondant au numéro de point de controle """
    return pointOnCurveList[num]

def num2Name(num):
    """ nom de la vertèbre correspondant au numéro de localisateur """
    if 'sliderGrp' in globals() and hasattr(sliderGrp, 'locatorList'):
        return sliderGrp.locatorList[num]
    if num==0:
        return 'L6'
    elif num==1:
        return 'T12'
    elif num==2:
        return 'T2'
    elif num==3:
        return 'C0'
    elif num==4:
        return 'Tete'











# MAYA TOOLS

def selectGui(*_):
    """ fonction callback pour sélectionner une vertèbre le long de la courbe """
    res = cmds.promptDialog(message='Name of vertebrate:',button=['OK', 'Cancel'],\
	defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
    print res
    if res=='OK':
        name=cmds.promptDialog(query=True, text=True)
        select(name)

def select(name):
    """ sélectionne une vertèbre le long de la courbe, désignée par name, ou la courbe elle-meme (curve1) """
    if name=='curve1':
        for i in range(MaxCV()):
            cmds.select(curvei(i),add=True)
    else:
        joint=n2J(name)
        if joint!=-1:
            pos=position(joint)
            param=getParameter(pos)
            maya.mel.eval('doMenuNURBComponentSelection("curve1", "curveParameterPoint");')
            cmds.select('curve1.u['+str(param)+']',r=1)
            print "select "+name

def selectCVGui(*_):
    """ fonction callback pour sélectionner un point de controle """
    res = cmds.promptDialog(message='Name of CV point:',button=['OK', 'Cancel'],\
	defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
    if res=='OK':
        name=cmds.promptDialog(query=True, text=True)
        selectCV(name)

def selectCV(name):
    """ sélectionne un point de controle par le nom de vertèbre associé (nom approximatif) """
    num=n2N(name)
    if num>-1 and num<MaxCV():
        maya.mel.eval('doMenuNURBComponentSelection("curve1", "controlVertex");')
        cmds.select('curve1.cv['+str(num)+']',r=1)
        print "select curve1.cv["+str(num)+"]"

def ex(name):
    """ execute un fichier """
    path="C:/Users/alexa/Documents/alexandra/scripts/"
    execfile(path+name)

def mv(v,rel=False):
    """ place l'objet sélectionné à l'endroit sélectionné 
    v : vecteur dim 3 """
    cmds.move(v[0],v[1],v[2],r=rel)

def clear():
    """ clear la scène """
    cmds.select(clear=True)

def position(name):
    """ position d'un objet Maya ou d'un nom de vertèbre """
    if cmds.objExists(name):
        return cmds.xform(name,q=1,t=1,ws=1)
    joint=n2J(name)
    if joint !=-1 :
        return cmds.xform(joint,q=1,t=1,ws=1)
    else:
        return -1

def CVPosition(name):
    """ return la position d'un localisateur ou la position du point de controle le plus proche (pour une vertèbre)"""
    if 'locator' in name:
        return position(name)
    return position(curvei(n2N(name)))

def calcCVParameters():
    """ return la liste des paramètres des points de controle """
    maxCV = cmds.getAttr("curve1.spans")+cmds.getAttr("curve1.degree")
    return [getParameter(position(curvei(i))) for i in range(maxCV)]

def CVParam(num):
    """ return la position du point de controle num """
    return getParameter(position(curvei(num)))

def calcCVPositions():
    """ return la liste des positions de points de controle """
    res=[]
    for i in range(MaxCV()):
        res.append(position(curvei(i)))
    return res

def MaxCV():
    """ return l'indice max de point de controle """
    return cmds.getAttr("curve1.spans")+cmds.getAttr("curve1.degree")

def MaxParam():
    """ return le paramètre de la fin de la courbe """
    return cmds.getAttr("curve1.maxValue")

def JointPositions():
    """ return la liste des positions des joints """
    res=[]
    for i in range(28):
        res.append(position('joint'+str(i+1)))
    return res

def JointParameters():
    """ return la liste des paramètres des joints le long de la courbe """
    return map(getParameter,JointPositions())

def getPoint(parameter):
    """ return la position sur la courbe à un paramètre donné 
    parameter : float """
    return cmds.pointOnCurve( 'curve1', pr=parameter, p=True )

def getPointHor(parameter):
    """ return la position sur la courbe projetée sur l'axe horizontal à un paramètre donné """
    return cmds.pointOnCurve( 'curve2', pr=parameter, p=True )
    
def getParameter(location):
    """ return le paramètre du point le plus proche de location sur la courbe """
    cmds.setAttr("nearestPointOnCurveGetParam.inPosition", location[0], location[1], location[2], type="double3") 
    uParam = cmds.getAttr("nearestPointOnCurveGetParam.parameter")
    return uParam

def getParameterProj(location):
    """ return le paramètre du point le plus proche de location sur la courbe projetée sur l'axe horizontal """
    cmds.setAttr("nearestPointOnCurveHorGetParam.inPosition", location[0], location[1], location[2], type="double3") 
    uParam = cmds.getAttr("nearestPointOnCurveHorGetParam.parameter")
    return uParam

def nearestPoint(name):
    """ point le plus proche sur la courbe 
    name : string (nom de vertèbre) ou position (liste n=3) """
    if isinstance(name,list):
        location=name
    else:
        location=position(name)
    cmds.setAttr("nearestPointOnCurveGetParam.inPosition", location[0], location[1], location[2], type="double3") 
    wParam = cmds.getAttr("nearestPointOnCurveGetParam.position")
    return wParam[0]

def nearestPointHor(name):
    """ point le plus proche sur la courbe projetée horizontalement
    name : string (nom de vertèbre) """
    location=position(name)
    cmds.setAttr("nearestPointOnCurveHorGetParam.inPosition", location[0], location[1], location[2], type="double3") 
    wParam = cmds.getAttr("nearestPointOnCurveHorGetParam.position")
    return wParam[0]

def distLocCrv(num):
    """ distance d'un localisateur à la courbe
    num : int, numéro du localisateur """
    posLoc=position(locator(num))
    CPOC=nearestPoint(locator(num))
    return distance(posLoc,CPOC)

# peut pas prendre une distance a cause du scale, plutot parametre
def distCVV():
    """ liste des différences de paramètre  entre les point les plus proche à la courbe des points de controle et les vertèbre qu'ils sont censés représenter """
    res=[]
    for i in range(MaxCV()):
        cvPosCPOC=nearestPoint(curvei(i))
        vertPos=position(num2NameCV(i))
        res.append(abs(getParameter(cvPosCPOC)-getParameter(vertPos)))
    return [norm(res),res]



# SIMPLE CALCULS
    
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
    return [v*scalaire for v in vect]

def sum(vect1,vect2):
    return [v1+v2 for v1,v2 in zip(vect1,vect2)]#vect1[i]+vect2[i] for i in range(len(vect1))]
    
def sub(vect1,vect2):
        return [v1-v2 for v1,v2 in zip(vect1,vect2)]

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

def getMilieu(v1,v2):
    return pdt(0.5,sum(v1,v2))

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

def maxDiff(val1,val2):
    Sub=map(abs,sub(val1,val2))
    maxi=max(Sub)
    i=Sub.index(maxi)
    return [i,maxi]

def projHor(v):
    return [v[0],v[2]]

def projHor3D(v):
    return [v[0],0,v[2]]

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



















    
        

