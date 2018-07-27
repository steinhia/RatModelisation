# -*- coding: utf-8 -*-

execfile(path+"Calculs.py")



# opérations sur la Gui (fonctions callback )

def UndoGui(sliderList,*_):
    """ callback undo """
    cmds.undo()
    for sliderDuo in sliderList:
        sliderDuo.update()


def scaleGui(sliderList,*_):
    """ callback scaleSegment """
    sf=getScale()
    setLength(sf)
    sliderList[11].update()

def scaleCPOCGui(sliderList,*_):
    """ callback scaleCPOC """
    sf=getScaleCPOC()
    setLength(sf)
    sliderList[11].update()


def scaleOffsetGui(sliderList,*_):
    """ callback scaleOffset """
    num=-1
    result = cmds.promptDialog(title="scaleOffset",message='Enter the scale Factor : ',button=['OK', 'Cancel'],\
	defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
    if result == 'OK' :
	    num=float(cmds.promptDialog(query=True, text=True))
    if num>0.1 and num<5:
        sf=getLength()
        setLength(sf*num)
        sliderList[11].update()
    else:
        print("Please choose a multiplicative scale Factor (a number near 1)")

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
    select('curve1')
    cmds.select('joint1',add=True)
    cmds.scale(scaleValue,scaleValue,scaleValue,r=True,pivot=posInit)
    clear()

def setScale(newLengthvalue,*_):
    """ deuxieme nom de setLength, parfois utilisée quand nom automatique à partir de l'opération Scale """
    setLength(newLengthvalue)


def keepChainLengthValue(newValue,*_):
    """ effectue un scaling sur la chaine de joints """
    Length=getJointChainLength()
    posInit=getPosition()
    cmds.select('joint1',r=1)
    scaleValue=newValue/Length
    cmds.scale(scaleValue,scaleValue,scaleValue,r=True,pivot=posInit)

def keepJointParameters(param,*_):
    jtPos=map(getPoint,param)
    for i,pos in enumerate(jtPos):
        cmds.select(joint(i+1))
        mv(pos)
    


def setValue():
    """ replace les joints au bon parmètre pour éviter le décalage le long de la courbe """
    points=map(getPoint,param)
    for i,pt in enumerate(points):
        cmds.select(joint(i+1))
        mv(pt)
 

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

def parabolicRotation(value,list):
    """ effectue la rotation 
    value : float, offset du slider """
    [pivotNum,begin,end,x,y,z]=list
    if begin<pivotNum:
        for i in range(begin,end+1):
            dist=(abs(i-pivotNum))
            angle=math.atan(dist)*5
            cmds.select(curvei(i),add=True) 
            pivotPos=position(curvei(i+1))
            cmds.rotate(value*angle,r=True,p=pivotPos,x=x,y=y,z=z)
    else:
        for i in range(end,begin-1,-1):
            #dist=(abs(i-pivotNum))
            #angle=math.atan(dist)**(-1)*5
            cmds.select(curvei(i),add=True) 
            pivotPos=position(curvei(i-1))
            cmds.rotate(value*5,r=True,p=pivotPos,x=x,y=y,z=z) #TODO vérifier que c'est la meme fonction à la fin


def parabolicRotationGD(value,list,*_):
    """ effectue la rotation latérale 
    value : float """
    t=time.time()
    [pivotNum,begin,end,x,y,z]=list
    pivotPos=position(curvei(pivotNum))
    for i in range(end,begin-1,-1):
        dist=(abs(i-pivotNum))
        angle=3.0/dist#math.atan(dist)**(-2)
        cmds.select(curvei(i),add=True) 
        cmds.rotate(value*angle,r=True,p=pivotPos,x=x,y=y,z=y)



def rot(value,name,*_):
    """ effectue le mouvement de rotation précisé par name et avec une intensité value
    value : float, offset du slider
    name : string parmi "CGD" etc """
    if name=="LHB":
        parabolicRotation(value*1.5,[1,0,0,1,0,0]) 
    elif name=="LGD":
        parabolicRotation(value*1.5,[1,0,1,0,1,0])
    elif name=="CHB":
        parabolicRotation(value*0.5,[4,5,7,1,0,0]) 
    elif name=="CGD":
        parabolicRotationGD(value*1.05,[4,5,7,0,1,0])
    elif name=="THB":
        parabolicRotation(value,[6,7,7,1,0,0])
    elif name=="TGD":
        parabolicRotationGD(value*1.7,[6,7,7,0,1,0])
    elif name=="CompHB":
        rotCompHB(value*1.2)
    elif name=="CompGD":
        parabolicRotationGD(value*0.5,[1,2,7,0,1,0])
   

def rotCompHB(value,*_):
    """ effectue la compression du rat
    value : float """

    posB=position(curvei(4))
    posE=position(curvei(1))

    cmds.select(curvei(2),curvei(3),curvei(4))
    cmds.rotate(-value*5,0,0,pivot=position(curvei(1)))

    cmds.select(curvei(2))
    cmds.rotate(value*2,0,0,pivot=position(curvei(1)))
    cmds.select(curvei(3))
    cmds.rotate(value*1,0,0,pivot=position(curvei(1)))

    #translation pour ramener les points extremes
    tB=sub(position(curvei(4)),posB)
    cmds.select(curvei(5),curvei(6),curvei(7))
    cmds.move(tB[0],tB[1],tB[2],r=True)

    tE=sub(position(curvei(1)),posE)
    cmds.select(curvei(0))
    cmds.move(tE[0],tE[1],tE[2],r=True)


def setOneRot(valeur,test,slider,moveSlider=False):
    """ calcule l'angle obtenu si l'on fait bouger le slider1 jusqu'à la valeur de test
    valeur : float, valeur initiale à rétablir à la fin
    test : float, valeur à tester
    slider : slider, slider à bouger
    moveSlider : boolean, effectuer l'opération en bougeant le slider ou juste calculer la bonne rotation à appliquer sans utilisr la Gui?"""
    fTest=setOneRotWithChangement(test,slider)
    if moveSlider :
        slider.setValue(valeur) 
        slider.update(False,True)  
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
        slider.update(False,True,False)
    else :
        # execute action sans changer la valeur du slider pour eviter les manipulations de Gui
        slider.setActionWithoutMoving(test)
    fTest=angleCrv(slider.label)
    return fTest

def isInside(theta,fMin,fMax):
    return (theta >=fMin and theta <=fMax) or (theta >=fMax and theta <=fMin)

def setRot2(theta,slider,nMax=30):
    """ effectue la rotation nécessaire pour atteindre un angle precis, par dichotomie
    slider : sliderOffset, slider qui effectue l'opération absolue 
    theta : float 
    nMax : int, nombre max d'itérations """
    jointParam=JointParameters()
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
        while abs(fTest-theta)>0.01 and i<nMax and abs(mini-maxi)>0.000001:
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
    if(abs(theta-angleCrv(slider.label))>2 and test!=mini and test!=maxi):
        print("FAIL SETROT", slider.label,abs(theta-angleCrv(slider.label)))
    keepJointParameters(jointParam)
    return test

#TODO revoir comp a gauche marche pas, bornes du slider ??
def setRot(theta,slider,nMax=30):
    """ effectue la rotation nécessaire pour atteindre un angle precis, par dichotomie
    slider : sliderOffset, slider qui effectue l'opération absolue 
    theta : float 
    nMax : int, nombre max d'itérations """
    jointParam=JointParameters()
    minSlider=slider.minValue
    maxSlider=slider.maxValue
    distance=abs(theta-angleCrv(slider.label))
    pas=0.1
    if slider.dte!=[]:
        a=slider.dte[0] # coefficient directeur
    else:
        a=1
    fTest=100000.0
    val=slider.sliderValue()

    mini=max(val-pas*distance/a,slider.minValue)
    maxi=min(val+pas*distance/a,slider.maxValue)
    fMin=setOneRot(val,mini,slider)
    fMax=setOneRot(val,maxi,slider)
    i=0
    # si jamais intervalle trop petit
    while (not isInside(theta,fMin,fMax)) and (((minSlider<mini or maxSlider>maxi) and minSlider<maxSlider) or ((minSlider<maxi or maxSlider>mini) and minSlider>maxSlider)) and i<5:
        i+=1
        pas*=5
        mini=max(val-pas*distance,slider.minValue)
        maxi=min(val+pas*distance,slider.maxValue)
        fMin=setOneRot(val,mini,slider)
        fMax=setOneRot(val,maxi,slider)
    if isInside(theta,fMin,fMax):
        i=0
        # début de la dichotomie
        while abs(fTest-theta)>0.1 and i<nMax and abs(mini-maxi)>0.000001:
            i+=1
            test=float(mini+maxi)/2.0
            fTest=setOneRot(val,test,slider)
            if((fTest>theta and fMin<fMax) or (fTest<theta and fMin>fMax )):
                maxi=test
            else :
                mini=test
        # on garde la dernière valeur
        setOneRotWithChangement(test,slider)
    else:
        test=-1
        setOneRotWithChangement(val,slider)
        print ("failRot",slider.label,theta,fMin,fMax,mini,maxi)
    keepJointParameters(jointParam)
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

def setValue(sliderList,name,param,nMax=30,*_):
    """ applique la bonne rotation avec la valeur prise dans la liste de tous les paramètres à atteindre
    sliderList : liste des sliderDuo
    name : string, opération concernée ex "CGD"
    param : liste de tous les paramètres """
    if "HB" in name or "GD" in name:
        setRot(param[numSlider(name)],sliderList[numSlider(name)].slider,nMax)
    elif "Scale" in name:
        setLength(param[13])
    else:
        CurveNames.setFunction(name)(param[numSlider(name)])
    for sliderDuo in sliderList:
        sliderDuo.update()
    clear()

def setParam(sliderList,name,Cote="",*_):
    CurveNames.setFunction(name)(CurveNames.getFunctionLoc(name)(Cote),Cote)
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
