# -*- coding: utf-8 -*-

import maya

import time
import maya.mel as mel

#path="C:/Users/alexa/Documents/alexandra/scripts/"
execfile(path+"mesures.py")
execfile(path+"Mouvements.py")

# Alogs qui placent la courbe


# ALGO DE CORRECTION

def calcPosRelatifHB(locator,Cote="",nLocator=-1,exact=False):
    """ calcul relatif vertical entre la courbe et le localisateur 
    locator : position du localisateur
    Cote : Cote sur lequel projeter
    nLocator : numéro du localisateur
    exact : boolean, pour la comparaison avec un point exact sur la courbe (cervicales) """
    if exact:
        locatorOnCurve=position('C2')
    else:
        parLocOnCurve=getParameter(locator)
        locatorOnCurve=getPoint(parLocOnCurve)
    #vect=sub(locator,locatorOnCurve)
    vectProj2D=projPlanPosture2DLocator(locatorOnCurve,locator,Cote)
    tan=normalize(getTangent(locatorOnCurve))
    if nLocator==0: # on prend l'ooposé de la tangente pour les lombaires car vecteur ne part pas du pivot mais l'inverse 
        tan=pdt(-1,tan)
    tanProj2D=projPlanPosture2DLocator(locatorOnCurve,sum(locatorOnCurve,tan),Cote)
    # angle du locator vers la courbe
    angle=angle2D(vectProj2D,tanProj2D)
    if angle<0:
        string="courbe dessous"
    else:
        string="courbe dessus"
    return [angle,norm(vectProj2D)*angle/100.0,string]


def calcPosRelatifGD(locatorPosition,Cote="",nLocator=-1,exact=False):
    """ calcul relatif latéral entre la courbe projetée horizontalement et le localisateur projeté aussi
    locatorPosition : position du localisateur
    Cote : Cote sur lequel projeter
    nLocator : numéro du localisateur
    exact : boolean, pour la comparaison avec un point exact sur la courbe (cervicales) """
    if exact:
        locatorOnCurve=position('C2')
    else:
        par=getParameterProj(projHor3D(locatorPosition))     
        locatorOnCurve=getPoint(par)
    tan=projHor(getTangent(locatorOnCurve))
    vect=projHor(sub(locatorOnCurve,locatorPosition))
    if angle2D(tan,vect)<0:
        string="courbe a gauche"
    else:
        string="courbe a droite"
    return [angle2D(tan,vect),norm(vect),string]

def calcPosRelatifHBNum(numLocator,Cote=""):
    """ calcul relatif vertical entre la courbe et le localisateur"""    
    return calcPosRelatifHB(position(locator(numLocator)),Cote,numLocator)

def calcPosRelatifGDNum(numLocator,Cote=""):
    """ calcul relatif latéral entre la courbe projetée horizontalement et le localisateur projeté aussi"""
    return calcPosRelatifGD(position(locator(numLocator)),Cote,numLocator)


def correctionRot(nGroup,nLocator,sliderList,HB,Croiss,Cote,nMax,precision,tour=0,coeff=0.5,exact=False):
    """ corrige la rotation concernée pour que la courbe passe par le localisateur correspondant """
    locatorP=position(locator(nLocator))
    f = calcPosRelatifHB if HB  else calcPosRelatifGD
    if exact:
        distI=distance(locatorP,findHighestPointT())
    else:
        distI=distance(locatorP,getPoint(getParameter(locatorP)))
    dist=distI
    slider=sliderList[nGroup].slider
    valInit=slider.sliderValue()
    minSlider=slider.minValue
    maxSlider=slider.maxValue
    relatif=1
    maxi=min(valInit+dist*coeff*(slider.maxValue-slider.minValue),maxSlider)
    mini=max(valInit-dist*coeff*(slider.maxValue-slider.minValue),minSlider)
    i=0
    while i<nMax and abs(dist)>0.01 and abs(mini-maxi)>precision*0.01:
        i+=1
        testV=(mini+maxi)/2
        slider.setValue(testV)
        slider.update()
        [relatif,dist,str]=f(locatorP,Cote=Cote,nLocator=nLocator,exact=exact)
        if (relatif<0 and Croiss) or (relatif>0 and (not Croiss)):
            maxi=testV
        else:
            mini=testV 
    if distI<dist-0.5:
        if tour==0 :
            correctionRot(nGroup,nLocator,sliderList,HB,Croiss,Cote,nMax,precision,tour=1,coeff=coeff*2,exact=exact)
        else:
            slider.setValue(valInit)
            slider.update()
            print("correctionRot failed",slider.label)



def correctionCompHB(sliderList):
    """ correction de la compression fondée sur le minimum local de l'ordonnée, si le localisateur est placé sur le minimum local de la courbe idéal """
    locatorP=position(locator(2))
    Low=findLowestPointC()
    dist=distance(Low,locatorP)
    slider=sliderList[5].slider
    valInit=slider.sliderValue()
    minSlider=slider.minValue
    maxSlider=slider.maxValue
    relatif=1
    maxi=min(valInit+dist*(slider.maxValue-slider.minValue),maxSlider)
    mini=max(valInit-dist*(slider.maxValue-slider.minValue),minSlider)
    i=0
    while abs(relatif)>0.01 and i<20:
        i+=1
        mil=(mini+maxi)/2.0
        slider.setValue(mil)
        slider.update()
        relatif=getParameter(position(locator(2)))-getParameter(findLowestPointC())
        if relatif<0:
            mini=mil
        else:
            maxi=mil
    Low=findLowestPointC()
    locatorOnCrvP=nearestPoint(locatorP)
    if abs(getParameter(locatorOnCrvP)-getParameter(Low))>0.2 or abs(Low[1]-locatorP[1])>0.2: 
        print("deuxieme correction",abs(getParameter(locatorOnCrvP)-getParameter(Low)))
        correctionCompHBTete(sliderList)
        #correctionRot(7,2,sliderList,True,True,"",nMax=20,precision=0.01)
        Low=findLowestPointC()
        locatorOnCrvP=nearestPoint(locatorP)
        if abs(getParameter(locatorOnCrvP)-getParameter(Low))>0.1 and abs(Low[1]-locatorOnCrvP[1])<0.5:
            print("troisieme correction")
            correctionCompHBTete(sliderList)

def correctionCompHBTete(sliderList):
    locatorP=position(locator(3))
    High=position('C1')
    dist=distance(High,locatorP)
    slider=sliderList[5].slider
    valInit=slider.sliderValue()
    minSlider=slider.minValue
    maxSlider=slider.maxValue
    relatif=1
    dist=2
    maxi=min(valInit+dist*(slider.maxValue-slider.minValue),maxSlider)
    mini=max(valInit-dist*(slider.maxValue-slider.minValue),minSlider)
    i=0
    while abs(dist)>0.01 and i<20:
        i+=1
        mil=(mini+maxi)/2.0
        slider.setValue(mil)
        slider.update()
        relatif=position(locator(3))[1]-position('C0')[1]
        dist=distance(nearestPoint(locatorP),locatorP)
        if relatif<0:
            mini=mil
        else:
            maxi=mil

def corr(sliderList,name,nMax=20,precision=0.01):
    """ correction de la rotation de la courbe pour qu'elle passe par le localisateur
    name : string, nom de l'opération
    nMax : n max de tour de boucles
    precision : pré ision recherchée """
    jtParam=JointParameters()
    if name=="LHB":
        correctionRot(3,0,sliderList,True,False,"L",nMax,precision) 
    elif name=="LGD":
        correctionRot(2,0,sliderList,False,True,"L",nMax,precision)
    elif name=="CHB":
        correctionRot(1,3,sliderList,True,False,"C",nMax,precision,exact=True) 
        if CMalCorrige():
            print("tentative2 CHB")
            correctionRot(1,3,sliderList,True,False,"C",nMax,precision,exact=False) 
    elif name=="CGD":
        correctionRot(0,3,sliderList,False,False,"C",nMax,precision,exact=True) 
    elif name=="THB":
        correctionRot(7,4,sliderList,True,False,"C",nMax,precision)
    elif name=="TGD":
        correctionRot(6,4,sliderList,False,False,"C",nMax,precision)
    elif name=="CompHB":
        correctionRot(5,2,sliderList,True,True,"",nMax,precision)
        if LMalCorrige():
            correctionCompHB(sliderList)
    elif name=="CompGD":
        correctionRot(4,2,sliderList,False,False,"",nMax,precision)
    keepJointParameters(jtParam)

def CMalCorrige():
    """ return boolean
    est-ce que le point le plus proche sur la courbe du localisateur tete-cervicales est proche de C0 ? """
    POC=nearestPoint(locator(3))
    parPOC=getParameter(POC)
    parC0=getParameter(position('C0'))
    if parPOC-parC0>0.2:
        #print "CMalCorrige",parPOC-parC0
        return True
    return False

def LMalCorrige():
    """ return boolean
    est-ce que le point sur la courbe le plus proche du localisateur est trop proche de la tete ? """
    POC=nearestPoint(locator(2))
    parPOC=getParameter(POC)
    parC6=getParameter(position('C6'))
    #print "LMalCorrige",parPOC-parC6
    if parPOC-parC6>0.1:
        return True
    return False


def isCorrectExtrema():
    """ return boolean 
    est-ce que déplacer la courbe pour que les extremas locaux correspondent aux localisateurs fait beaucoup bouger la courbe ? """
    res=True
    posCrv=getPosition()
    translateToHighestPointL()
    if distance(posCrv,getPosition())>0.1:
        res=False
        print("Extremum lombaire mal place",distance(posCrv,getPosition()))
    translateToLowestPointC()
    if distance(posCrv,getPosition())>0.1:
        res=False
        print("Extremum cervical mal place",distance(posCrv,getPosition()))
    return res
    setPosition(posCrv)

def isCorrectCV():
    """ return boolean
    est-ce que les localisateurs sont loin des points sur la courbes qui leur correspondent ? """
    res=True
    posCrv=getPosition()
    translateToCV(0,0)
    if distance(posCrv,getPosition())>0.1:
        res=False
        print("CV lombaire mal place",distance(posCrv,getPosition()))
    translateToCV(6,3)
    if distance(posCrv,getPosition())>0.1:
        res=False
        print("CV cervical mal place",distance(posCrv,getPosition()))
    translateToCV(7,4)
    if distance(posCrv,getPosition())>0.1:
        res=False
        print("CV tete mal place",distance(posCrv,getPosition()))
    return res
    setPosition(posCrv)




def OneCorrection(sliderList):
        """ effectue une boucle de correction faisant suite �  une trnaslation / un scale """
        corr(sliderList,"LGD")
        corr(sliderList,"LHB") 
        corr(sliderList,"CompGD")
        corr(sliderList,"CGD")
        corr(sliderList,"TGD")
        corr(sliderList,"CompHB") 
        corr(sliderList,"CHB")
        corr(sliderList,"THB") 
        translateToLocator(1)
        corr(sliderList,"LGD")
        corr(sliderList,"LHB") 
        corr(sliderList,"CompGD")
        corr(sliderList,"CGD")
        corr(sliderList,"TGD")



def Correction(sliderList):
    """ algorithme de correction """

    # méthode précédente permet d'avoir un scale presque bon 
    for _ in range(1):
        translateToHighestPointL()        
        OneCorrection(sliderList)
    for _ in range(1):
        # si les cervicales sont décalées
        if distance(position(locator(3)),findHighestPointT())>0.1:
            translateToHighestPointT()
            OneCorrection(sliderList)
        #si les lombaires sont mal placées
        if distance(position(locator(0)),position(curvei(0)))>0.1:
            translateToCV(0,0)
            translateToLocator(1)
            OneCorrection(sliderList)
         #si la longueur de la courbe ne convient pas
        if abs(getScaleCPOC()/getScale()-1)>0.02:
            setAngle(sliderList,"ScaleCPOC")
            OneCorrection(sliderList)



# PLACEMENT ANGLES

def placeAnglesCalcules(sliderList,nBoucles=1):
    """ algo qui place les angles calculés avec les localisateurs """

    oldParamC=getParameter(position(curvei(5)))
    oldParamD=getParameter(position(curvei(3)))
    param=calcCVParameters()

    setAngle(sliderList,"X")
    setAngle(sliderList,"Y")
    setAngle(sliderList,"Z")
    setAngle(sliderList,"Orientation")
    setAngle(sliderList,"Scale")

    locatorList=map(position,locList())

    # on place d'abord les angles GD -> plus facile a placer maintenant
    # mais compHB a besoin de se faire sur une courbe assez plane
    for i in range(1):
            setAngle(sliderList,"CompHB")
            translateToLocator(1)
            corr(sliderList,"LGD")
            corr(sliderList,"CompGD")
            corr(sliderList,"CGD")
            corr(sliderList,"TGD")

    for i in range(1):
        setAngle(sliderList,"LHB")
        corr(sliderList,"LGD")
        setAngle(sliderList,"CHB")
        setAngle(sliderList,"THB")
        corr(sliderList,"CGD")
        corr(sliderList,"TGD")
    setAngle(sliderList,"Scale")

    translateToHighestPointL()
    # replace GD
    for _ in range(3):
        translateToLocator(1)
        corr(sliderList,"LGD")
        corr(sliderList,"CompGD")
        corr(sliderList,"CGD")
        corr(sliderList,"TGD")


    



# TRANSLATIONS

def translateToLocator(numLocator):
    """ translate la courbe le moins possible pour qu'elle passe pas un certain localisateur """
    posLoc=position(locator(numLocator))
    posLocOnCurve=nearestPoint(locator(numLocator))
    t=sub(posLoc,posLocOnCurve)
    select('curve1')
    cmds.move(t[0],t[1],t[2],r=True)
    clear()

def translateToLocatorGui(sliderList,*_):
    """ fonction Callback de translateToLocator """
    num=-1
    result = cmds.promptDialog(title="translateToLocator",message='Num of Locator:',button=['OK', 'Cancel'],\
	defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
    if result == 'OK' :
	    num=int(cmds.promptDialog(query=True, text=True))
    if num>-1 and num<6:
        translateToLocator(num)
    #update position Gui
    for i in range(10,13):
        sliderList[i].update()

    
def translateToCV(numCV,numLocator):
    """ translate la courbe pour que le point de controle corresponde au localisateur voulu 
    numCV : int, numéro du point de controle
    numLocator : int, numéro du localisateur """
    posCV=nearestPoint(curvei(numCV))
    posCV=nearestPoint(position(POCList()[numCV]))
    posLoc=position(locator(numLocator))
    diff=sub(posLoc,posCV)
    select('curve1')
    cmds.move(diff[0],diff[1],diff[2],r=True)
    clear()

    
def translateToCVGui(sliderList,*_):
    """ callback de translateToCV """
    num=-1
    result = cmds.promptDialog(title="translateToCV",message='Num of Locator:',button=['OK', 'Cancel'],\
	defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
    if result == 'OK' :
	    num=int(cmds.promptDialog(query=True, text=True))
    if num==0:
        translateToCV(0,0)
    elif num==1:
        translateToCV(2,1)
    elif num==2:
        translateToCV(4,2)
    elif num==3:
        translateToCV(6,3)
    elif num==4:
        translateToCV(7,4)
    #update position Gui
    for i in range(10,13):
        sliderList[i].update()

def translateToExtremaGui(sliderList,*_):
    """ fonction callback de translateToHighestPointL, translateToLowestPointC, translateToHighestPointT """
    res=-1
    result = cmds.promptDialog(title="translateExtrema",message='Choose between L, C and T:',button=['OK', 'Cancel'],\
	defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
    if result == 'OK' :
	    res=cmds.promptDialog(query=True, text=True)
    if res=="C":
        translateToLowestPointC()
    elif res=="T":
        translateToHighestPointT()
    else:
        translateToHighestPointL()


def findHighestPointL():
    """ trouve le maximum local des ordonnées autour des lombaires """
    t=time.time()
    minParam=getParameter(position('L4'))
    maxParam=getParameter(position('T11'))
    tanY=-1
    i=0
    while abs(tanY)>0.01 and i<10:
        i+=1
        mil=(minParam+maxParam)/2.0
        tanY=cmds.pointOnCurve( 'curve1', pr=mil,tangent=True )[1]
        if tanY>0:
            minParam=mil
        else:
            maxParam=mil
    return getPoint(mil)

def translateToHighestPointL():
    """ fait coincider le localisateur lombaire avec le point calculé avec findHighestpointL """
    posLoc=position(locator(1))
    posCrv=findHighestPointL()
    t=sub(posLoc,posCrv)
    select('curve1')
    cmds.move(t[0],t[1],t[2],r=True)
    clear()

def findLowestPointC():
    """ trouve le minimum local des ordonnées autour du creux des cervicales """
    t=time.time()
    minParam=getParameter(position('T3'))
    maxParam=getParameter(position('C0'))
    tanY=-1
    i=0
    while abs(tanY)>0.01 and i<10:
        i+=1
        mil=(minParam+maxParam)/2.0
        tanY=cmds.pointOnCurve( 'curve1', pr=mil,tangent=True )[1]
        if tanY<0:
            minParam=mil
        else:
            maxParam=mil
    return getPoint(mil)


def translateToLowestPointC():
    """ fait coincider le localisateur lombaire avec le point calculé avec findLowestPointC """
    posLoc=position(locator(2))
    posCrv=findLowestPointC()
    t=sub(posLoc,posCrv)
    select('curve1')
    cmds.move(t[0],t[1],t[2],r=True)
    clear()


def findHighestPointT():
    """ trouve le maximum local des ordonnées autour de la tete """
    t=time.time()
    minParam=getParameter(position('C2'))
    maxParam=(getParameter(position('Tete'))+2.0*getParameter(position('C0')))/3.0
    tanY=-1
    i=0
    while abs(tanY)>0.01 and i<10:
        i+=1
        mil=(minParam+maxParam)/2.0
        tanY=cmds.pointOnCurve( 'curve1', pr=mil,tangent=True )[1]
        if tanY>0:
            minParam=mil
        else:
            maxParam=mil
    return getPoint(mil)

def translateToHighestPointT():
    """ fait coincider le localisateur lombaire avec le point calculé avec findHighestPointT """
    posLoc=position(locator(3))
    posCrv=findHighestPointT()
    t=sub(posLoc,posCrv)
    select('curve1')
    cmds.move(t[0],t[1],t[2],r=True)
    clear()


def setScaleLComp(sliderList=-1,*_):
    """ trouve le scale nécessaire pour que le localisateur se rapproche du minimum local de la courbe """
    translateToLowestPointC()
    translateToLocator(1)
    dist=-1
    i=-1
    mini=getLength()*0.8
    maxi=getLength()*1.2
    while abs(dist)>0.01 and i<20:
        i+=1
        translateToLowestPointC()
        translateToLocator(1)
        mil=(mini+maxi)/2.0
        setLength(mil)
        posRel=position(locator(3))[1]-findLowestPointC()[1]
        if posRel>0:
            mini=mil
        else:
            maxi=mil


def scaleTete(sliderList=-1,*_):
    """ effectue scaling basé uniquement sur le segment de la tete """
    d1=distance(position(locator(3)),position(locator(4)))
    d2=distance(position(locator(3)),position(curvei(7)))
    sf=d1/d2*getLength()
    setLength(sf)

def setScaleComp(sliderList=-1,*_):
    """ effectue le scaling basé sur la fonction de calcul getScaleComp """  # TODO comparer deux version de sf
    sf=getScaleComp()
    setLength(sf)

def ajustePos():
    """ ajuste la position pour minimiser la moyenne des erreurs (distance entre les localisaterus et la courbe)"""
    posLoc=map(position,locList())
    posLoc=[posLoc[i] for i in range(6) if i!=1]
    for i in range(5):
        pos=map(nearestPoint,posLoc)
        subPos=[0,0,0]
        for posi,posiloc in zip(pos,posLoc):
            val=sub(posiloc,posi)
            subPos=sum(subPos,val)
        subPos=pdt(1.0/5.0,subPos)
        if np.linalg.norm(subPos)<0.01:
            return
        select('curve1')
        cmds.move(subPos[0],subPos[1],subPos[2],r=True)








# GESTION COURBE

def resetCurve(length,CVpos,jtPos):
    """ rétablit la position de la courbe et des joints """
    setLength(length)     
    for i,posi in enumerate(CVpos):
        cmds.select(curvei(i))
        cmds.move(posi[0],posi[1],posi[2])
    for i,posj in enumerate(jtPos):
        cmds.select('joint'+str(i+1))
        cmds.move(posj[0],posj[1],posj[2])

def calcPosCV():
    pos=[]
    for i in range(MaxCV()):
        pos.append(position(curvei(i)))
    return pos  

def setOneCurve():
    """ rétablit une courbe """
    for j in range(MaxCV()):
        posj=cmds.getAttr('posCV.pos'+str(j))[0]
        cmds.select(curvei(j))
        cmds.move(posj[0],posj[1],posj[2])
    saveKeys()

def setAllCurves():
    """ rétablit les courbes précédemment enregistrées : nécessaire car courbe supprimée et recrée �  chaque lancement du script """
    for i in range(20):
        cmds.currentTime(i, edit=True )
        setOneCurve()
    for i in range(20):
        cmds.currentTime(i*10, edit=True )
        setOneCurve()

def saveKeys():
    """ setKey pour enregistrer la position de la courbe a chaque instant, ainsi que la position des points de controle et les valeurs des paramètres """
    cmds.setKeyframe("curve1",breakdown=False,hierarchy="None",controlPoints=True,shape=False)
    for k in range(MaxCV()):
        maya.mel.eval('setKeyframe -breakdown 0 -hierarchy none -controlPoints 0 -shape 0 {"curve1.cv['+str(k)+']"};')

    # on enregistre les valeurs des angles
    names1=['CHB','LHB','CGD','LGD','CompHB','CompGD']
    names2=['Posture','Orientation','X','Y','Y']
    for n in names1:
        value=angleCrv(n)
        cmds.setAttr('ValeurAngles.angle'+n,value)
        mel.eval('setKeyframe { "ValeurAngles.angle'+n+'" };')
    for n in names2:
        value=CurveNames.getFunction(n)()
        cmds.setAttr('ValeurAngles.'+n,value)
        mel.eval('setKeyframe { "ValeurAngles.'+n+'" };')

        
    # on enregistre les positions des points de controle
    for i in range(MaxCV()):
        pos=position(curvei(i))
        cmds.setAttr('posCV.pos'+str(i)+'X',pos[0])
        cmds.setAttr('posCV.pos'+str(i)+'Y',pos[1])
        cmds.setAttr('posCV.pos'+str(i)+'Z',pos[2])
        mel.eval('setKeyframe { "posCV.pos'+str(i)+'" };')

def Placement(sliderList,length,CVpos,jtPos,save,evaluate=True):
    t=time.time()
    a=Evaluate()
    #setAllParameters(sliderList)
    placeAnglesCalcules(sliderList)
    evaluation0=a.execute(False)
    #Correction(sliderList)
    print("temps de placement : ",time.time()-t)
    evaluation=a.execute(False)
    if evaluation>evaluation0 and False:
        print("échec de la correction : replacement des angles de départ, diff= "+str(evaluation))
        setAllParameters(sliderList)
    if save:
        saveKeys()
    if evaluate :
        evaluation=a.execute(True)


def placeCrvTranslations(move=False):
    """ place la courbe de manière très approximative pour la placer plus rapidement avec ces valeurs d'angle, environ 1/10s pour cette fct """
    jtparam=JointParameters()
    # on sauvegarde la position des points de controle
    CVList=[]
    for i in range(MaxCV()):
        CVList.append(position(curvei(i)))

    posL6=position(locator(0))
    posTete=position(locator(4))
    posL4=position(locator(1))
    posT13=sum(posL6,pdt(1.6,sub(posL4,posL6)))
    posT13[1]=(posL6[1]+posL4[1])/2.0
    posC5=position(locator(2))
    posC0=position(locator(3))
    posT3=sum(posC0,pdt(1.5,sub(posC5,posC0)))
    posT3[1]=(posC0[1]+posC5[1])/2.0
    posT8=getMilieu(posT3,posT13)
    cmds.select(curvei(0))
    mv(posL6)
    cmds.select(curvei(1))
    mv(posL4)
    cmds.select(curvei(2))
    mv(posT13)
    cmds.select(curvei(3))
    mv(posT8)
    cmds.select(curvei(4))
    mv(posT3)
    cmds.select(curvei(5))
    mv(posC5)
    cmds.select(curvei(6))
    mv(posC0)
    cmds.select(curvei(7))
    mv(posTete)

    # deplace avec les nearestPoint
    for _ in range(3):
        posC02=sub(posC0,getPoint(getParameter(position(locator(3)))))
        posC52=sub(posC5,getPoint(getParameter(position(locator(2)))))
        posL42=sub(posL4,getPoint(getParameter(position(locator(1)))))
        cmds.select(curvei(5))
        mv(posC52,rel=True)
        cmds.select(curvei(6))
        mv(posC02,rel=True)
        cmds.select(curvei(1))
        mv(posL42,rel=True)

    keepJointParameters(jtparam)
    CVListApprox=[]
    for i in range(MaxCV()):
        CVListApprox.append(position(curvei(i)))
    paramList=getAllParameters()
    # on rétablit la position des CV
    if not move:
        for i in range(MaxCV()):
            cmds.select(curvei(i))
            mv(CVList[i])
        keepJointParameters(jtparam)
    return paramList

def ApproxGui(*_):
    placeCrvTranslations(move=True)


def getAllParameters():
    l=OperationsList()
    res=[]
    for i in l:
        res.append(Names.getFunction(i)())
    return res


def setAllParameters(sliderList,*_):
    paramList=placeCrvTranslations()
    for _ in range(1):
        setValue(sliderList,"X",paramList)
        setValue(sliderList,"Y",paramList)
        setValue(sliderList,"Z",paramList)
        setValue(sliderList,"Orientation",paramList)
        setValue(sliderList,"Length",paramList)
        setValue(sliderList,"CompHB",paramList,nMax=10) 
        corr(sliderList,"LGD")  
        translateToLocator(1)   
        corr(sliderList,"CompGD")
        corr(sliderList,"CGD")
        corr(sliderList,"TGD")  
        setValue(sliderList,"LHB",paramList,nMax=10)          
        setValue(sliderList,"CHB",paramList,nMax=10)  
        setValue(sliderList,"THB",paramList,nMax=10)  


  
    
        
            
        
        





