# -*- coding: utf-8 -*-

import sys


sys.path.append("C:/Users/alexa/Documents/alexandra/scripts")
path="C:/Users/alexa/Documents/alexandra/scripts/"
execfile(path+"Calculs.py")



# opérations sur la Gui (fonctions callback )

def UndoGui(sliderList,*_):
    """ callback undo """
    cmds.undo()
    for sliderDuo in sliderList:
        sliderDuo.update()


def scaleGui(sliderList,*_):
    sf=getScale()
    setLength(sf)
    sliderList[11].update()

def scaleCPOCGui(sliderList,*_):
    sf=getScaleCPOC()
    setLength(sf)
    sliderList[11].update()


def scaleOffsetGui(sliderList,*_):
    num=-1
    result = cmds.promptDialog(title="scaleOffset",message='Enter the scale Factor : ',button=['OK', 'Cancel'],\
	defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
    if result == 'OK' :
	    num=float(cmds.promptDialog(query=True, text=True))
    if num>0.1 and num<5:
        sf=getScale()
        setLength(sf*num)
        sliderList[11].update()
    else:
        print "Please choose a number near 1"

def scaleCompGui(sliderList,*_):
    sf=getScaleComp()
    setLength(sf)
    sliderList[11].update()


# opérations sur la courbe (pas sur les points de controle)


def setLength(newLengthvalue,*_):
    """ effectue le bon scaling pour atteindre la longueur de courbe voulue 
    newLengthvalue : float """
    posInit=getPoint(MaxParam()/2.0)
    posInit=getPosition()
    L=cmds.arclen('curve1')
    scaleValue=newLengthvalue/L
    cmds.select('joint1')
    cmds.scale(scaleValue,scaleValue,scaleValue,r=True,pivot=posInit)
    clear()

def setScale(newLengthvalue,*_):
    """ deuxieme nom de setLength, parfois utilisée quand nom automatique à partir de l'opération Scale """
    setLength(newLengthvalue)


def keepChainLengthValue(newValue,L=[]):
    """ effectue un scaling sur la chaine de joints """
    Length=getJointChainLength()
    posInit=getPosition()
    cmds.select('joint1',r=1)
    scaleValue=newValue/Length
    cmds.scale(scaleValue,scaleValue,scaleValue,r=True,pivot=posInit)
 





def setCurvePosition(pos,Cote=""):
    """ set la position correspondant à Cote
    Cote : string parmi 'C','L' ou '' """
    posInit=getPosition(Cote=Cote)
    translation=[pos[i]-posInit[i] for i in range(3)]
    select('curve1')
    cmds.move(translation[0],translation[1],translation[2],r=1)


def setX(x,Cote=""):
    pos=getPosition(0,Cote)
    xTrans=x-pos
    select('curve1')
    cmds.move(xTrans,0,0,r=1)

def setY(y,Cote=""):
    pos=getPosition(1,Cote)
    yTrans=y-pos
    select('curve1')
    cmds.move(0,yTrans,0,r=1)

def setZ(z,Cote=""):
    pos=getPosition(2,Cote)
    zTrans=z-pos
    select('curve1')
    cmds.move(0,0,zTrans,r=1)

def setPosture(ThetaVoulu,Cote=""):
    """ donne la posture à la courbe, calculée à partir du Coté donné
    Cote : string parmi 'C', 'L' ou '' """
    # position du centre au depart
    pos=getPosition()
    select('curve1')
    for i in range(30):
        posture=getPosture(Cote)
        orient=PostureVector(Cote)
        angle=posture-ThetaVoulu
        cmds.rotate(angle*orient[2],0.0,angle*orient[0],r=True,pivot=pos)

def setOrientation(ThetaVoulu,Cote=""):
    """ donne l'orientation à la courbe, calculée à partir du Coté donné
    Cote : string parmi 'C', 'L' ou '' """
    pos=getPosition()
    orient=getOrientation(Cote)
    angle=ThetaVoulu-orient
    select('curve1')
    cmds.rotate(0.0,angle,0.0,r=True,pivot=pos)
  


## effectue les différents mouvements des lombaires etc

def parabolicRotation(theta,list):
    """ effectue la rotation 
    theta : float, offset du slider """
    t=time.time()
    [pivotNum,begin,end,x,y,z]=list
    if begin<pivotNum:
        dist=(abs(i-pivotNum))
        angle=math.atan(dist)*5
        cmds.select(curvei(i),add=True) 
        for i in range(begin,end+1):
            pivotPos=position(curvei(i+1))
            cmds.rotate(theta*angle,r=True,p=pivotPos,x=x,y=y,z=z)
    else:
        for i in range(end,begin-1,-1):
            pivotPos=position(curvei(i-1))
            cmds.rotate(theta*5,r=True,p=pivotPos,x=x,y=y,z=z) #TODO vérifier que c'est la meme fonction à la fin

        # TODO revoir difference, pas si importante 
def parabolicRotationGD(theta,list,*_):
    """ effectue la rotation latérale 
    theta : float """
    t=time.time()
    [pivotNum,begin,end,x,y,z]=list
    pivotPos=position(curvei(pivotNum))
    for i in range(end,begin-1,-1):
        dist=(abs(i-pivotNum))
        angle=math.atan(dist)*5 
        cmds.select(curvei(i)) 
        cmds.rotate(theta*angle*0.5,r=True,p=pivotPos,x=x,y=y,z=y)

def rot(theta,name,*_):
    """ effectue le mouvement de rotation précisé par name et avec une intensité theta
    theta : float, offset du slider
    name : string parmi "CGD" etc """
    if name=="LHB":
        parabolicRotation(theta*3,[1,0,0,1,0,0]) # 2 0 1 #TODO regarder si bon pivot ou harmoniser
    elif name=="LGD":
        parabolicRotation(theta,[1,0,1,0,1,0])# 3 0 2
    elif name=="CHB":
        parabolicRotation(theta,[4,5,7,1,0,0]) 
    elif name=="CGD":
        parabolicRotation(theta,[4,5,7,0,1,0])
    elif name=="THB":
        parabolicRotation(theta,[6,7,7,1,0,0])
    elif name=="TGD":
        parabolicRotation(theta,[6,7,7,0,1,0])
    elif name=="CompHB":
        rotCompHB(theta)
    elif name=="CompGD":
        parabolicRotationGD(theta,[2,3,7,0,1,0])


def rotCompHB(value,*_):
    """ effectue la compression du rat
    value : float """
    nPivot=1
    pivot=position(curvei(nPivot))

    posB=position(curvei(4))
    posE=position(curvei(1))

    pos3=position(curvei(3))
    pos2=position(curvei(1))

    parabolicRotation(-value,[1,2,4,1,0,0])

    #translation pour ramener les points extremes
    tB=sub(position(curvei(4)),posB)
    cmds.select(curvei(5),curvei(6),curvei(6),curvei(7))
    cmds.move(tB[0],tB[1],tB[2],r=True)

    #tE=sub(position(curvei(3)),posE)
    #cmds.select(curvei(0),curvei(1))
    #cmds.move(tE[0],tE[1],tE[2],r=True)

# TODO revoir l'idee de faire la rot lombaire en meme temps que la compression





def setOneRot(valeur,test,slider,moveSlider=False):
    """ calcule l'angle obtenu si l'on fait bouger le slider1 jusqu'à la valeur de test
    valeur : float, valeur initiale à rétablir à la fin
    test : float, valeur à tester
    slider : slider, slider à bouger
    moveSlider : boolean, effectuer l'opération en bougeant le slider ou juste calculer la bonne rotation à appliquer sans utilisr la Gui?"""
    fTest=setOneRotWithChangement(test,slider)
    if moveSlider :
        slider.setValue(valeur) 
        slider.update(False,True)  # attention ne pas changer le false en true
    else:
        setOneRotWithChangement(valeur,slider)
    return fTest

def setOneRotWithChangement(test,slider,moveSlider=True):
    """ effectue une rotation et met à jour les sliders 
    test : float, valeur à set
    moveSlider : boolean, effectuer l'opération en bougeant le slider ou juste calculer la bonne rotation à appliquer ?"""
    t=time.time()
    if moveSlider :
        slider.setValue(test)
        t=time.time()
        slider.update(False,True)
    else :
        # execute action sans changer la valeur du slider pour eviter les manipulations de Gui
        slider.setActionWithoutMoving(test)
    fTest=angleCrv(slider.label)
    return fTest

def isInside(theta,fMin,fMax):
    return (theta >=fMin and theta <=fMax) or (theta >=fMax and theta <=fMin)

def setRot(theta,slider,nMax=30):
    """ effectue la rotation nécessaire pour atteindre un angle precis, par dichotomie
    slider : sliderOffset, slider qui effectue l'opération absolue 
    theta : float 
    nMax : int, nombre max d'itérations """
    minSlider=slider.minValue
    maxSlider=slider.maxValue
    fTest=100000.0
    fx=slider.f(theta)
    test=fx
    val=slider.getValue()
    if fx==[] : 
        mini=minSlider
        maxi=maxSlider
        # on peut eventuellement avoir fMin>fMax
        fMin=setOneRot(val,mini,slider)
        fMax=setOneRot(val,maxi,slider)
    else: # approximation de la valeur du slider1 nécessaire
        pas=(maxSlider-minSlider)/500.0
        mini=fx-pas
        maxi=fx+pas
         #on regarde si croissant ou decroissant
        fMin=setOneRot(val,mini,slider)
        fMax=setOneRot(val,maxi,slider)
        i=0
        # mauvaise approximation au départ
        while (not isInside(theta,fMin,fMax)) and ((minSlider<mini and maxSlider>maxi and minSlider<maxSlider) or (minSlider<maxi and maxSlider>mini and minSlider>maxSlider)) and i<10:
            i+=1
            pas*=5.0
            mini=fx-pas
            maxi=fx+pas
            fMin=setOneRot(val,mini,slider)
            fMax=setOneRot(val,maxi,slider)
        if i==10 or (mini<minSlider or maxi>maxSlider): # si on a trop élargi
            mini=minSlider
            maxi=maxSlider
            fMin=setOneRot(val,minSlider,slider)
            fMax=setOneRot(val,maxSlider,slider)
    if isInside(theta,fMin,fMax):
        i=0
        # début de la dichotomie
        while abs(fTest-theta)>0.01 and i<nMax and abs(mini-maxi)>0.0001:
            i+=1
            test=float(mini+maxi)/2.0
            fTest=setOneRot(val,test,slider)
            if((fTest>theta and fMin<fMax) or (fTest<theta and fMin>fMax )):
                maxi=test
            else :
                mini=test
        # on garde la dernière valeur
        setOneRotWithChangement(test,slider)
    elif (theta <=fMin and fMin<=fMax) or (theta>=fMin and fMin>=fMax) :
        setOneRotWithChangement(mini,slider)
        test=mini
        #print "en dehors des bornes! plus petit que le minimum",fMin,fMax,getFunction,theta
    else:
        setOneRotWithChangement(maxi,slider)
        test=maxi
        #print "en dehors des bornes! plus grand que le maximum",fMin,fMax,getFunction,theta
    # regarde si angle effectivement atteint
    if(abs(theta-angleCrv(slider.label))>1 and test!=mini and test!=maxi):
        print "FAIL SETROT", slider.label,abs(theta-angleCrv(slider.label))
    return test




def setAngle(sliderList,name,offset=1,*_):
    """ calcule l'angle avec les localisateurs et applique la bonne rotation 
    sliderList : liste des sliderDuo
    name : string, opération concernée ex "CGD"
    offset : float, pour rajouter un facteur multiplicatif à la valeur appliquée (scaling) """
    if "HB" in name or "GD" in name:
        setRot(angleLoc(name),sliderList[numSlider(name)].slider)
    elif "Scale" in name:
        setLength(eval("get"+name)()*offset)
    else:
        CurveNames.setFunction(name)(CurveNames.getFunctionLoc(name)())
    for sliderDuo in sliderList:
        sliderDuo.update()
    clear()

def setValue(sliderList,name,param,*_):
    """ applique la bonne rotation avec la valeur prise dans la liste de tous les paramètres à atteindre
    sliderList : liste des sliderDuo
    name : string, opération concernée ex "CGD"
    param : liste de tous les paramètres """
    if "HB" in name or "GD" in name:
        setRot(param[numSlider(name)],sliderList[numSlider(name)].slider)
    elif "Scale" in name:
        setLength(param[13])
    else:
        CurveNames.setFunction(name)(param[numSlider(name)])
    for sliderDuo in sliderList:
        sliderDuo.update()
    clear()



    


# utilise translations pour replacer points de controle, pas fonctionnel

    
def recalageTangent(numLocator,numPoint):
    for i in range(2):
        posLocOnCurve=nearestPoint(locator(numLocator))
        posCVOnCurve=getPoint(getParameter(position(curvei(numPoint))))
        vect=sub(posLocOnCurve,posCVOnCurve)
        cmds.select(curvei(numPoint))
        cmds.move(vect[0],vect[1],vect[2],r=True)

def recalageTangentSansLocator(oldParam,newParam,numPoint):
    for i in range(2):
        newParam=calcCVParameter(numPoint)
        pos1=getPoint(oldParam)
        pos2=getPoint(newParam)
        v=sub(pos1,pos2)
        cmds.select(curvei(numPoint))
        cmds.move(v[0],v[1],v[2],r=True)


        

def recalageTangentWithName(oldParam,newParam,numPoint):
    for i in range(3):
        #newParam=calcCVParameter(numPoint)
        pos1=position(pointOnCurveList[numPoint])#getPoint(oldParam)
        pos2=nearestPoint(curvei(numPoint))
        v=sub(pos1,pos2)
        cmds.select(curvei(5))
        cmds.move(v[0],v[1],v[2],r=True)
