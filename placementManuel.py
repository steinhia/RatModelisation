# -*- coding: utf-8 -*-

import sys
sys.path.append("C:/Users/alexa/Documents/alexandra/scripts")
import maya

import time
import maya.mel as mel
import inspect

path="C:/Users/alexa/Documents/alexandra/scripts/"
execfile(path+"mesures.py")




# ALGO DE CORRECTION

def calcPosRelatifHB(locator,Cote="",nLocator=-1,exact=False):
    #orientation=getOrientation(Cote)
    if exact:
        locatorOnCurve=position('C2')
    else:
        parLocOnCurve=getParameter(locator)
        locatorOnCurve=getPoint(parLocOnCurve)
    vect=sub(locator,locatorOnCurve)
    vectProj=projPlanPosture3DLocator(locatorOnCurve,locator,Cote)
    vectProj2D=projPlanPosture2DLocator(locatorOnCurve,locator,Cote)


    tan=normalize(getTangent(locatorOnCurve))
    if nLocator==0:
        tan=pdt(-1,tan)
    #tanProj=projPlanPosture3DLocator(locatorOnCurve,sum(locatorOnCurve,tan),Cote)
    tanProj2D=projPlanPosture2DLocator(locatorOnCurve,sum(locatorOnCurve,tan),Cote)


    #p("vectProj3D2D",projPlanPosture3D(locatorOnCurve,sum(locatorOnCurve,tan),Cote))
    #p("locOn",locatorOnCurve,vectProj,tanProj,"finTan",str(sum(locatorOnCurve,tanProj)))
    #print "tan2D",vectProj2D,tanProj2D
    #p("vect",str(vectAngle),"tan",str(tanAngle),"angle",str(angleHB2V(vectProj,tanProj)),str(valPrincDeg(tanAngle-vectAngle)))

    # angle du locator vers la courbe
    angle=angle2D(vectProj2D,tanProj2D) #angleHB2V(vectProj,tanProj)
    if angle<0:
        string="courbe dessous"
    else:
        string="courbe dessus"
    return [angle,norm(vectProj)*angle/100.0,string]


def calcPosRelatifGD(locatorPosition,Cote="",nLocator=-1,exact=False):
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
    return calcPosRelatifHB(position(locator(numLocator)),Cote,numLocator)

def calcPosRelatifGDNum(numLocator,Cote=""):
    return calcPosRelatifGD(position(locator(numLocator)),Cote,numLocator)

# garde en memoire le meilleur si marche pas bien
def correctionRot(nGroup,nLocator,sliderList,HB,Croiss,Cote,nMax,precision,tour=0,coeff=0.5,exact=False):
    locatorP=position(locator(nLocator))
    f = calcPosRelatifHB if HB  else calcPosRelatifGD
    distI=norm(sub(locatorP,getPoint(getParameter(locatorP))))
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
    if distI<dist:
        if tour==0 :
            correctionRot(nGroup,nLocator,sliderList,HB,Croiss,Cote,nMax,precision,tour=1,coeff=coeff*2,exact=exact)
        else:
            slider.setValue(valInit)
            slider.update()
            p("correctionRot failed",slider.label)


def correctionCompHB(sliderList):
    locatorP=position(locator(2))
    Low=findLowestPointC()
    dist=distance(Low,locatorP)
    slider=sliderList[7].slider
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
    if abs(getParameter(locatorOnCrvP)-getParameter(Low))>0.1 or abs(locatorP[1]-locatorOnCrvP[1])>0.1: 
        print "deuxieme correction",abs(getParameter(locatorOnCrvP)-getParameter(Low))
        correctionCompHBTete(sliderList)

def correctionCompHBTete(sliderList):
    locatorP=position(locator(3))
    High=position('C0')
    dist=distance(High,locatorP)
    slider=sliderList[7].slider
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
    locatorOnCrvP=nearestPoint(locatorP)
    if distance(locatorOnCrvP,locatorP)>0.5:
        print "troisieme correction"
        #correctionRot(7,2,sliderList,True,True,"",nMax=20,precision=0.01)

def corr(sliderList,name,nMax=20,precision=0.01):
    if name=="LHB":
        correctionRot(5,0,sliderList,True,False,"L",nMax,precision) 
    elif name=="LGD":
        correctionRot(4,0,sliderList,False,True,"L",nMax,precision)
    elif name=="CHB":
        correctionRot(3,3,sliderList,True,False,"C",nMax,precision,exact=True) 
    elif name=="CGD":
        correctionRot(2,3,sliderList,False,False,"C",nMax,precision,exact=False)
    elif name=="DHB":
        correctionRot(5,1,sliderList,True,False,"",nMax,precision)
    elif name=="DGD":    
        correctionRot(4,1,sliderList,False,False,"",nMax,precision)
    elif name=="THB":
        correctionRot(9,4,sliderList,True,False,"C",nMax,precision)
    elif name=="TGD":
        correctionRot(8,4,sliderList,False,False,"C",nMax,precision)
    elif name=="CompHB":
        #correctionRot(7,2,sliderList,True,True,"",nMax,precision,Lowest=True)
        correctionCompHB(sliderList)
    elif name=="CompGD":
        correctionRot(6,2,sliderList,False,False,"",nMax,precision)

def Correction(sliderList):
    ##t=time.time()
    1
    #G objectif utiliser HighestPoint/LowestPoint que si resultat mauvais ou utilise de toute facon pour ameliorer les resultats

    # pour replacer GD :
    # Comp C Comp C T C T
    # decalage le long de la courbe, surtout quand grande compression


    #b utilise translate to extream C car ca corrige en partie l'incertitude sur la compresison juste avant -> ou l'utiliser?

    for _ in range(1):
            translateToHighestPointL()
            corr(sliderList,"LGD")
            corr(sliderList,"LHB")
            translateToCV(0,0)
            translateToLocator(1)

    corr(sliderList,"CompGD")
    corr(sliderList,"CompHB")
    corr(sliderList,"CGD")
    corr(sliderList,"TGD")
    corr(sliderList,"LGD")
    corr(sliderList,"LHB")
    corr(sliderList,"CompGD")
    corr(sliderList,"CGD")
    corr(sliderList,"TGD")


    for _ in range(3):
        setAngle(sliderList,"ScaleTot")
        corr(sliderList,"CHB")
        corr(sliderList,"THB")
        corr(sliderList,"CGD")
        corr(sliderList,"TGD")


## seulement pour les cas compliques, les autres localisateurs un peu partout
#    setAngle(sliderList,"ScaleCPOC")
#    for _ in range(1):
#        translateToLowestPointC()
#        translateToLocator(1)
#    corr(sliderList,"LGD")
#    corr(sliderList,"LHB")
#    corr(sliderList,"CompGD")
#    corr(sliderList,"CompHB")
#    for _ in range(1):
#        corr(sliderList,"CGD")
#        corr(sliderList,"CHB")
#        corr(sliderList,"TGD")
#        corr(sliderList,"THB")


    #for _ in range(3):
    #    translateToCV(6,3)
    #    translateToLocator(1)
    #    corr(sliderList,"CGD")
    #    corr(sliderList,"CHB")
    #corr(sliderList,"LGD")
    #corr(sliderList,"LHB")

    #corr(sliderList,"CompGD")
    #corr(sliderList,"CompHB")
    #for _ in range(1):
    #    corr(sliderList,"CGD")
    #    corr(sliderList,"CHB")
    #    corr(sliderList,"TGD")
    #    corr(sliderList,"THB")


#    for _ in range(3):
#        translateToCV(0,0)
#        translateToLocator(1)
#        corr(sliderList,"LGD")
#        corr(sliderList,"LHB")
#    corr(sliderList,"CGD")
#    corr(sliderList,"CHB")

#    corr(sliderList,"CompGD")
#    corr(sliderList,"CompHB")
#    for _ in range(1):
#        corr(sliderList,"CGD")
#        corr(sliderList,"CHB")
#        corr(sliderList,"TGD")
#        corr(sliderList,"THB")







    #corr(sliderList,"CGD")
    #corr(sliderList,"TGD")
    #corr(sliderList,"LGD")
    #corr(sliderList,"LHB")
    #for _ in range(1):
    #    corr(sliderList,"CGD")
    #    corr(sliderList,"CHB")
    #    corr(sliderList,"TGD")
    #    corr(sliderList,"THB")

    #for i in range(0):
    #    translateToCV(6,4)
    #    translateToLocator(1)
    #corr(sliderList,"LGD")
    #corr(sliderList,"LHB")
    #corr(sliderList,"CGD")
    #corr(sliderList,"CHB")
    #corr(sliderList,"TGD")
    #corr(sliderList,"THB")



            #corr(sliderGrp.sliderList,"LGD")
            #corr(sliderGrp.sliderList,"LHB")

            # toute facon pas possible placer compression autrement qu'avec un scaling trop grand
            # a parti si au milieu et dans ce cas cervicales courbure toute petite


    ##replacer gauche
    #corr(sliderList,"LGD",nMax=10)
    #corr(sliderList,"CompGD",nMax=10)
    #corr(sliderList,"CGD",nMax=10)
    #corr(sliderList,"CompGD",nMax=10)
    #corr(sliderList,"CGD",nMax=10)
    #corr(sliderList,"TGD",nMax=10)
    #corr(sliderList,"CGD",nMax=10)
    #corr(sliderList,"TGD",nMax=10)

    #setAngle(sliderList,"Scale",offset=1.1)
    #for _ in range(2):
    #    corr(sliderList,"CompGD")
    #    corr(sliderList,"CompHB")

        #corr(sliderList,"LGD")
        #corr(sliderList,"LHB")
    #for _ in range(1):
        #corr(sliderList,"CGD",nMax=25)
    #    corr(sliderList,"CHB",nMax=25)
    #    corr(sliderList,"CompGD",nMax=20)
    #    corr(sliderList,"CompHB",nMax=20)
    #    corr(sliderList,"TGD")
    #    corr(sliderList,"THB")
    #    
    #    for _ in range(2):
    #        corr(sliderList,"TGD",nMax=15)
    #        corr(sliderList,"THB",nMax=15)





    #for i in range(2):
    #    for _ in range(2):
    #        translateToCV(0,0)
    #        translateToLocator(1)
    #        setAngle(sliderList,"Scale")
    ### on translate la courbe pour qu'elle repasse par le localisateur milieu
    #    for _ in range(1):
    #        corr(sliderList,"CompGD")
    #    #    corr(sliderGrp.sliderList,"CompHB")
    #    for _ in range(1):
    #        corr(sliderList,"LGD")
    #        corr(sliderList,"LHB")
    #    for _ in range(2):
    #        corr(sliderList,"CGD")
    #        corr(sliderList,"CHB")
    #    for _ in range(2):
    #        corr(sliderList,"TGD")
    #        corr(sliderList,"THB")
    #setAngle(sliderList,"Scale")
    # a ce moment la typiquement tout ok sauf creux des cervicales -> scaling base uniquement sur les lombaires


    #hGui(sliderList)

    #for _ in range(2):
    #    translateToCV(0,0)
    #    translateToLocator(1)
    #    corr(sliderList,"LGD")
    #    corr(sliderList,"LHB")
    #for _ in range(1):
    #    corr(sliderList,"CompGD")
    ##    corr(sliderGrp.sliderList,"CompHB")
    #for _ in range(1):

    #for _ in range(2):
    #    corr(sliderList,"CGD")
    #    corr(sliderList,"CHB")
    #for _ in range(2):
    #    corr(sliderList,"TGD")
    #    corr(sliderList,"THB")



            # on translate la courbe pour que la courbe coincide parfaitement au niveau des lombaires
    #for i in range(0):
    #    setAngle("scale",getScale())
    #    translateToCV(0,0)
    ### on translate la courbe pour qu'elle repasse par le localisateur milieu
    #    translateToLocator(1)
        #corr(sliderGrp.sliderList,"LGD")
        #corr(sliderGrp.sliderList,"CompGD")
        #corr(sliderGrp.sliderList,"CGD")
        #corr(sliderGrp.sliderList,"LHB")
        #corr(sliderGrp.sliderList,"CompHB")
        #corr(sliderGrp.sliderList,"CHB")
        #corr(sliderGrp.sliderList,"TGD")
        #corr(sliderGrp.sliderList,"THB")


    #print "apres translate",time.time()-t 
    #t=time.time()

 #   # on translate la courbe pour que la courbe coincide parfaitement au niveau des lombaires
 #   for i in range(1):
 #       for _ in range(1):
 #           translateToCV(0,0)
 #   #        ### on translate la courbe pour qu'elle repasse par le localisateur milieu
 #           translateToLocator(1)
 #           setAngle(sliderList,"Scale")
 #       for _ in range(1):
 #           corr(sliderList,"LGD",nMax=5)
 #           corr(sliderList,"LHB",nMax=5)
 #       for _ in range(1):
 #           corr(sliderList,"CompGD",nMax=5)
 #           corr(sliderList,"CompHB",nMax=5)

 #       for _ in range(1):
 #           corr(sliderList,"CGD",nMax=5)
 #           corr(sliderList,"CHB",nMax=5)
 #           corr(sliderList,"TGD",nMax=5)
 #           corr(sliderList,"THB",nMax=5)

 #   #for _ in range(0):
 #   #    translateToLocator(0)
 #   #    translateToLocator(1)
 #       #translateToLocator(3)
 #       #translateToLocator(1)
 #       #translateToLocator(0)
 #       #translateToLocator(1)

 #       #print "apres corr",time.time()-t
 #   #t=time.time() 


 #   for i in range(2):
 #       setAngle(sliderList,"Scale") # TODO!!!!! CPOC
 #       translateToCV(7,4)
 #       translateToLocator(1)

 #   ### on translate la courbe pour qu'elle repasse par le localisateur milieu
 ## autre locator reference ?
 #       for _ in range(1):
 #           corr(sliderGrp.sliderList,"CompGD")
 #           corr(sliderGrp.sliderList,"CompHB")
 #       for _ in range(1):
 #           corr(sliderGrp.sliderList,"LGD")
 #           corr(sliderGrp.sliderList,"LHB")
 #       for i in range(2):
 #           corr(sliderGrp.sliderList,"TGD",nMax=5)
 #           corr(sliderGrp.sliderList,"THB",nMax=5)
 #           #corr(sliderGrp.sliderList,"CGD",nMax=5)
 #           #corr(sliderGrp.sliderList,"CHB",nMax=5)

    #for i in range(1):
    #    for _ in range(2):
    #        translateToCV(0,0)
    #        translateToLocator(1)
    #        setAngle("scale",getScaleCPOC())
    ## on translate la courbe pour qu'elle repasse par le localisateur milieu
        #for _ in range(1):
        #    corr(sliderGrp.sliderList,"CompGD")
        #    corr(sliderGrp.sliderList,"CompHB")
        #for _ in range(1):
        #    corr(sliderGrp.sliderList,"LGD")
        #    corr(sliderGrp.sliderList,"LHB")
        #for _ in range(2):
        #    corr(sliderGrp.sliderList,"CGD")
        #    corr(sliderGrp.sliderList,"CHB")
        #for _ in range(2):
        #    corr(sliderGrp.sliderList,"TGD")
        #    corr(sliderGrp.sliderList,"THB")




        #print getCLen(),getTLen()

        #print "apres corrT",time.time()-t
        #t=time.time() 

        #for _ in range(1): 
        #    translateToLocator(2)
        #    translateToLocator(1)
        #    translateToLocator(3) 
        #    translateToLocator(1)

            #translateToLocator(2)
            #translateToLocator(1)


    # svt pb cervicales mal calees car tete passe
    # cale la tete tout a la fin
    # ou si jamais on est quand meme dans ce cas la, trCV tete trLoc C

# PLACEMENT ANGLES

def placeAnglesCalcules(sliderList,nBoucles=1):

    oldParamC=getParameter(position(curvei(5)))
    oldParamD=getParameter(position(curvei(3)))
    param=calcCVParameters()

    setAngle(sliderList,"X")
    setAngle(sliderList,"Y")
    setAngle(sliderList,"Z")
    setAngle(sliderList,"Orientation")
    setAngle(sliderList,"Scale")


    # on place d'abord les angles GD -> plus facile a placer maintenant
    locatorList=map(position,locList())

    t=time.time()
    for i in range(1):
            setAngle(sliderList,"CompHB")
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
    #setAngle(sliderList,"Scale")

    setAngle(sliderList,"X")
    setAngle(sliderList,"Y")
    setAngle(sliderList,"Z")



# TRANSLATIONS

def translateToLocator(numLocator):
    posLoc=position(locator(numLocator))
    posLocOnCurve=nearestPoint(locator(numLocator))
    t=sub(posLoc,posLocOnCurve)
    select('curve1')
    cmds.move(t[0],t[1],t[2],r=True)
    clear()

def translateToLocatorGui(sliderList,*_):
    num=-1
    result = cmds.promptDialog(title="translateToLocator",message='Num of Locator:',button=['OK', 'Cancel'],\
	defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
    if result == 'OK' :
	    num=int(cmds.promptDialog(query=True, text=True))
    if num>-1 and num<6:
        translateToLocator(num)
    #update position Gui
    for i in range(12,15):
        sliderList[i].update()

    
def translateToCV(numCV,numLocator):
    posCV=nearestPoint(curvei(numCV))
    posCV=nearestPoint(position(POCList()[numCV]))
    posLoc=position(locator(numLocator))
    diff=sub(posLoc,posCV)
    select('curve1')
    cmds.move(diff[0],diff[1],diff[2],r=True)
    clear()

    
def translateToCVGui(sliderList,*_):
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
    for i in range(12,15):
        sliderList[i].update()

def translateToExtremaGui(sliderList,*_):
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
    posLoc=position(locator(1))
    posCrv=findHighestPointL()
    t=sub(posLoc,posCrv)
    select('curve1')
    cmds.move(t[0],t[1],t[2],r=True)
    clear()

def findLowestPointC():
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
    posLoc=position(locator(2))
    posCrv=findLowestPointC()
    t=sub(posLoc,posCrv)
    select('curve1')
    cmds.move(t[0],t[1],t[2],r=True)
    clear()


def findHighestPointT():
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
    posLoc=position(locator(3))
    posCrv=findHighestPointT()
    t=sub(posLoc,posCrv)
    select('curve1')
    cmds.move(t[0],t[1],t[2],r=True)
    clear()


def setScaleLComp(sliderList=-1,*_):
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
    d1=distance(position(locator(3)),position(locator(4)))
    d2=distance(position(locator(3)),position(curvei(7)))
    sf=d1/d2*getLength()
    setLength(sf)

def setScaleComp(sliderList=-1,*_):
    sf=getScaleComp()
    setLength(sf)

def setScaleTot(sliderList=-1,*_):
    sf=getScaleTot()
    setLength(sf)

def ajustePos():
    # position des differents locators / CPOC
    t=time.time()
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
            print i, time.time()-t
            return
        select('curve1')
        cmds.move(subPos[0],subPos[1],subPos[2],r=True)



















    ## effacer la bosse ci besoin -> modifie les deux angles
    #for _ in range(1):
    #    translateToLocator(1)
    #    #setParam(sliderList,"Orientation","L")
    #    corr(sliderList,"LGD")
    #    corr(sliderList,"CompGD")
    #    corr(sliderList,"CGD")
    #    corr(sliderList,"TGD")


    #for i in range(1):

    #    corr(sliderList,"CompGD")
    #    corr(sliderList,"CGD")
    #    corr(sliderList,"TGD")







# GESTION COURBE

def resetCurve(length,CVpos,jtPos):
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
    for j in range(maxCV()):
        posj=cmds.getAttr('posCV.pos'+str(j))[0]
        cmds.select(curvei(j))
        cmds.move(posj[0],posj[1],posj[2])
    saveKeys()

def setAllCurves():
    for i in range(20):
        cmds.currentTime(i, edit=True )
        setOneCurve()
    for i in range(20):
        cmds.currentTime(i*10, edit=True )
        setOneCurve()

def saveKeys():
        # setKey pour enregistrer la position de la courbe a chaque instant
    cmds.setKeyframe("curve1",breakdown=False,hierarchy="None",controlPoints=True,shape=False)
    for k in range(MaxCV()):
        maya.mel.eval('setKeyframe -breakdown 0 -hierarchy none -controlPoints 0 -shape 0 {"curve1.cv['+str(k)+']"};')

    # on enregistre les valeurs des angles
    names1=['CHB','DHB','LHB','CGD','DGD','LGD','CompHB','CompGD']
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
    #resetCurve(length,CVpos,jtPos)
    placeAnglesCalcules(sliderList,1)
    Correction(sliderList)
    if save:
        saveKeys()
    if evaluate and False:
        a=Evaluate()
        evaluation=a.execute()





















   
                #correctionRot(sliderGrp,sliderGrp.string2num("rotCHB"),4,False,Cote="C")
                #correctionRot(sliderGrp,sliderGrp.string2num("rotTHB"),5,False,Cote="C")
                #correctionRot(sliderGrp,sliderGrp.string2num("rotCGD"),4,False,Cote="C")
                #correctionRot(sliderGrp,sliderGrp.string2num("rotTGD"),5,False,Cote="C")
                #correctionRot(sliderGrp,sliderGrp.string2num("rotLGD"),0,True,Cote="L")
                #correctionRot(sliderGrp,sliderGrp.string2num("rotLHB"),0,False,Cote="L")
                #correctionRot(sliderGrp,sliderGrp.string2num("rotLGD"),0,True)
                #correctionRot(sliderGrp,sliderGrp.string2num("rotTGD"),5,False)
                #correctionRot(sliderGrp,sliderGrp.string2num("rotCGD"),4,False)
                #correctionRot(sliderGrp,sliderGrp.string2num("compression g"),3,False)
                #correctionRot(sliderGrp,sliderGrp.string2num("compression g"),3,False)
                #correctionRot(sliderGrp,sliderGrp.string2num("compression"),3)
    
#p("param fin",param)
        
#EvalPositionLocator2()
#print param
#print calcCVParameters()


  #ReplacePoints(pointOnCurveList,nameList)

     #calcul des distances des locators a la courbe

    #locatorOnCurveList=map(getPoint,map(getParameter,locatorList))
    #diff=[sub(locatorList[i],locatorOnCurveList[i]) for i in range(5)]
    #res=[]
    #for i,posi in enumerate(diff):
    #    if norm(posi)>0.03:
    #        res.append(True)
    #    else:
    #        res.append(False)

    #lordoseC=calcLordoseC()
    #p("lordoseL1",calcLordoseL())
    #setAngle("courbure l",lordoseC)        
    #p("lordoseL2",calcLordoseL())
    

        #keepParameters(param)
        #pour que tous les locators passent exactement par la courbe
        #for i in range(1):
        ##    correctionPos(sliderGrp,1,position("locatorAngle1"))
        # position precise
        #ajustePosCurvePoints()
        ##### position sur la courbe
        #correctionPos(sliderGrp,2,position(locator(2)))
        #correctionPos(sliderGrp,1,position(locator(1)))
        #correctionPos(sliderGrp,4,position(locator(3)))
        #correctionPos(sliderGrp,0,position(locator(0)))
        #correctionPos(sliderGrp,6,position(locator(4)))
        #correctionPos(sliderGrp,3,position("locatorD"))

        ## recale les 3 points hors extremites donc les cv se sont petit a petit decales
        #recalageTangentSansLocator(oldParamC,5)
        ###recalageTangentSansLocator(oldParamD,3)
        #recalageTangent(n2N('T10'),2)
        #recalageTangent(n2N('L3'),1)
        #recalageTangent(n2N('T2'),4)

    #p("duree placage : "+str(time.time()-t))      
    #p("param debut",param) 