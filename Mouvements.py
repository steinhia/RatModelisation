# -*- coding: utf-8 -*-

import sys


sys.path.append("C:/Users/alexa/Documents/alexandra/scripts")
path="C:/Users/alexa/Documents/alexandra/scripts/"
execfile(path+"Calculs.py")


def UndoGui(sliderList,*_):
    cmds.undo()
    for sliderDuo in sliderList:
        sliderDuo.update()


def setLength(newLengthvalue,numPivot=2):
    posInit=position(curvei(numPivot))

    L=cmds.arclen('curve1')
    scaleValue=newLengthvalue/L
    cmds.select('joint1',r=1,add=True)
    #maya.mel.eval('ModObjectsMenu MayaWindow|mainModifyMenu;')
    #maya.mel.eval('ProportionalModificationTool;')
    #maya.mel.eval('setToolTo $gPropMod;')
    #maya.mel.eval('propModValues PropMod;')
    #maya.mel.eval('toolPropertyShow;')
    #maya.mel.eval('changeToolIcon;')
    #maya.mel.eval('dR_contextChanged;')
    #maya.mel.eval('currentCtx;')
    #maya.mel.eval('if(`exists dR_updateCommandPanel`) dR_updateCommandPanel;')
    #maya.mel.eval('dR_updateToolSettings;')
    #maya.mel.eval('EnterEditMode;')
    #maya.mel.eval('ctxEditMode;')
    #cmds.manipPivot( p=posInit )
    #print getLLen(),getCLen(),getTLen()
    ##cmds.scale(scaleValue,scaleValue,scaleValue,r=True,pivot=posInit)
    #maya.mel.eval('propModTypeCallback 2;')
    #maya.mel.eval('propModValues PropMod;')
    #maya.mel.eval('toolPropertyShow;')
    #maya.mel.eval('dR_updateToolSettings;')
    #maya.mel.eval('propModCtx -e -pd 5 `currentCtx`;')
    #maya.mel.eval('propModValues PropMod;')
    #maya.mel.eval('toolPropertyShow;')
    #maya.mel.eval('dR_updateToolSettings;')
    select('curve1')
    cmds.propMove(px=1,py=1,pz=1,s=[scaleValue,scaleValue,scaleValue],pivot=posInit)
    #print getLLen(),getCLen(),getTLen()
    #cmds.manipPivot( r=True )
    clear()


#    manipPivot -p -21.588785 33.082133 -2.598126 ;
#scale -r -p -21.588785cm 33.082133cm -2.598126cm 0.951209 0.951209 0.951209 ;


def keepChainLengthValue(newValue,L=[]):
    Length=getJointChainLength()
    posInit=getCurvePosition()
    cmds.select('joint1',r=1)
    scaleValue=newValue/Length
    cmds.scale(scaleValue,scaleValue,scaleValue,r=True,pivot=posInit)

def scaleGui(sliderList,*_):
    sf=ScaleFactor()
    setLength(sf)
    sliderList[15].update()

def scaleCPOCGui(sliderList,*_):
    sf=ScaleFactorCPOC()
    setLength(sf)
    sliderList[15].update()


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

# marche pas   
def keepParameters(param):
    maxCV = cmds.getAttr("curve1.spans")+cmds.getAttr("curve1.degree")
     #influence sur les 2 points d'a cote
    for j in range(1):
        #print calcCVParameters()
        for i in range(len(param)): 
            par=calcCVParameter(i)
            if abs(param[i]-par)>0.0001:
                recalageTangentWithName(param[i],par,i)

# marche pas
def keepJointParameters(jtParam):
    for i,paramJ in enumerate(jtParam):
        oldJtPos=getPoint(paramJ)
        newPoint=nearestPoint('joint'+str(i+1))
        trans=sub(oldJtPos,newPoint)
        cmds.select('joint'+str(i+1))
        cmds.move(trans[0],trans[1],trans[2],r=True)


# marche pas
def replaceC():
    for i in range(2):
        posC5=nearestPoint('C5')
        posCVOnCurve=nearestPoint(curvei(5))
        trans=sub(posC5,posCVOnCurve)
        cmds.select(curvei(5))
        cmds.move(trans[0],trans[1],trans[2],r=True)

# marche pas    
def keepCLen(newCLen):
    for i in range(3):
        pos=position(curvei(5))
        a=getCLen()
        sc=newCLen/a
        cmds.select(curvei(4),curvei(5),curvei(6))
        cmds.scale(sc,sc,sc,pivot=pos)
        sc=newCLen/a

def setCurvePosition(pos,Cote=""):
    posInit=getCurvePosition(Cote=Cote)
    translation=[pos[i]-posInit[i] for i in range(3)]
    select('curve1')
    cmds.move(translation[0],translation[1],translation[2],r=1)


def setX(x,Cote=""):
    pos=getCurvePosition(0,Cote)
    xTrans=x-pos
    select('curve1')
    cmds.move(xTrans,0,0,r=1)

def setY(y,Cote=""):
    pos=getCurvePosition(1,Cote)
    yTrans=y-pos
    select('curve1')
    cmds.move(0,yTrans,0,r=1)

def setZ(z,Cote=""):
    pos=getCurvePosition(2,Cote)
    zTrans=z-pos
    select('curve1')
    cmds.move(0,0,zTrans,r=1)

def setPosture(ThetaVoulu,Cote=""):
    # position du centre au depart
    pos=getCurvePosition()
    for i in range(5):
        posture=getPosture(Cote)
        orient=PostureVector(Cote)
        angle=posture-ThetaVoulu
        select('curve1')
        cmds.rotate(angle*orient[2],0.0,angle*orient[2],r=True,pivot=pos)

def setOrientation(ThetaVoulu,Cote=""):
    pos=getCurvePosition()
    orient=getOrientation(Cote)
    angle=ThetaVoulu-orient
    select('curve1')
    cmds.rotate(0.0,angle,0.0,r=True,pivot=pos)
  

#def rotC2HB(theta,L=[]):
#    parabolicRotation(theta,[pointOnCurveList[4],pointOnCurveList[5],pointOnCurveList[6],1,0,0]) # C7 C7 C0
#def rotC2GD(theta,L=[]):
#    parabolicRotation(theta,[pointOnCurveList[4],pointOnCurveList[5],pointOnCurveList[6],0,1,0])

#def getRatios(beginPD,endPD,beginPC,endPC):
#    [crvLengthNewD,distBeginD]=getLen(beginPD,endPD)
#    [crvLengthNewC,distBeginC]=getLen(beginPC,endPC)
#    return  [distBeginD,distBeginC,crvLengthNewD,crvLengthNewC]

#def keepGroupLen(Len2,Ncurve):
#    #for i in range(5):
#        #keepOneLen(curvei(2),curvei(5),Len1,Ncurve,beginPD,endPD)
#    beginPC=getParameter(position(curvei(n2N("C7"))))
#    endPC=getParameter(position(curvei(n2N("C1"))))
#    keepOneLen(curvei(4),curvei(6),Len2,Ncurve,beginPC,endPC)


#def keepOneLen(begin,end,crvLengthVoulu,Ncurve,beginP,endP):
#    [crvLengthNew,distBegin2]=getLen(beginP,endP)
#    if(crvLengthNew>0):
#        setLength(Ncurve)
#        for i in range(5):
#            scaleValue=crvLengthVoulu/crvLengthNew
#            pivot=getBarycentre(begin,end,0.5) 
#            cmds.select(clear=True )
#            for j in range(int(begin[-2]),int(end[-2])+1):
#                cmds.select(curvei(j),add=True)
#            cmds.scale(scaleValue,scaleValue,scaleValue,r=True,p=pivot)
#            setLength(Ncurve)
#            [crvLengthNew,distBegin2]=getLen(beginP,endP)
#        [crvLengthNew,distBegin2]=getLen(beginP,endP)


# teste une valeur du premier slider pour obtenir la theta voulue -> envoie premier slider dans la fonction
# trop long
def setOneRot(valeur,test,slider,moveSlider=False):
    t=time.time()
    fTest=setOneRotWithChangement(test,slider)
    t=time.time()
    if moveSlider :
        slider.setValue(valeur) 
        slider.update(False,True)  # attention ne pas changer le false en true
    else:
        setOneRotWithChangement(valeur,slider)
    t=time.time()
    return fTest

# applique le changement
def setOneRotWithChangement(test,slider,moveSlider=True):
    t=time.time()
    if moveSlider :
        slider.setValue(test)
        t=time.time()
        slider.update(False,True) # attention ne pas changer le false en true
    else :
        # execute action sans changer la valeur du slider pour eviter les manipulations de Gui
        slider.setActionWithoutMoving(test)
    t=time.time()
    fTest=angleCrv(slider.label)
    return fTest

def isInside(theta,fMin,fMax):
    return (theta >=fMin and theta <=fMax) or (theta >=fMax and theta <=fMin)

# cherche a atteindre une theta par dichotomie
# slider envoye = slider1
def setRot(theta,slider,nMax=30):
    #[slider,getFunction,getFunctionArgs,crvInfos,minSlider,maxSlider]=L

    #getFunction=angleCrv
    #getFunctionArgs=Names.getFunctionArgs(slider.label)
    minSlider=slider.minValue
    maxSlider=slider.maxValue
    fTest=100000.0
    fx=slider.f(theta)
    test=fx
    val=slider.getValue()
    #print "fx",fx
    if fx==[] :
        mini=minSlider
        maxi=maxSlider
        # on peut eventuellement avoir fMin>fMax
        fMin=setOneRot(val,mini,slider)
        fMax=setOneRot(val,maxi,slider)
    else:
        #fVal=setOneRot(val,fx,[slider,getFunction,getFunctionArgs,crvInfos])
        pas=(maxSlider-minSlider)/500.0
        mini=fx-pas
        maxi=fx+pas
         #on regarde si croissant ou decroissant
        fMin=setOneRot(val,mini,slider)
        fMax=setOneRot(val,maxi,slider)
        i=0
        #print "mininit",mini,maxi
        while (not isInside(theta,fMin,fMax)) and ((minSlider<mini and maxSlider>maxi and minSlider<maxSlider) or (minSlider<maxi and maxSlider>mini and minSlider>maxSlider)) and i<10:
            i+=1
            pas*=5.0
            mini=fx-pas
            maxi=fx+pas
            #print "minimaxi",mini,maxi
            fMin=setOneRot(val,mini,slider)
            fMax=setOneRot(val,maxi,slider)
        if i==10 or (mini<minSlider or maxi>maxSlider):
            #print "tentative f-1 failed",getFunction,"calcMinMax",mini,maxi,fx,pas
            mini=minSlider
            maxi=maxSlider
            fMin=setOneRot(val,minSlider,slider)
            fMax=setOneRot(val,maxSlider,slider)
        print "iinit",i
        #print ("i",i)
        #mini=max(mini,minSlider)
        #maxi=min(maxi,maxSlider)
    if isInside(theta,fMin,fMax):
        i=0
        while abs(fTest-theta)>0.01 and i<nMax and abs(mini-maxi)>0.0001:
            i+=1
            test=float(mini+maxi)/2.0
            fTest=setOneRot(val,test,slider)
            #print "test",test,fTest,mini,maxi
            if i>15:
                1#print "gde value",test,"fTest",fTest,"theta",theta
            if((fTest>theta and fMin<fMax) or (fTest<theta and fMin>fMax )):
                maxi=test
            else :
                mini=test
        #print "testend",test
        setOneRotWithChangement(test,slider)
        t=time.time()
        print "ifin",i,mini,maxi
    elif (theta <=fMin and fMin<=fMax) or (theta>=fMin and fMin>=fMax) :
        setOneRotWithChangement(mini,slider)
        test=mini
        #print "en dehors des bornes! plus petit que le minimum",fMin,fMax,getFunction,theta
    else:
        setOneRotWithChangement(maxi,slider)
        test=maxi
        #print "en dehors des bornes! plus grand que le maximum",fMin,fMax,getFunction,theta
    # TODO regarder ici si ca passe pas trop souvent -> TestClass Mini
    if(abs(theta-angleCrv(slider.label))>1 and test!=mini and test!=maxi):
        print "FAIL SETROT", slider.label,abs(theta-angleCrv(slider.label))
    #print "duree",time.time()-t
    return test

def setAngle(sliderList,name,*_):
    if "HB" in name or "GD" in name:
        setRot(angleLoc(name),sliderList[numSlider(name)].slider)
    else:
        CurveNames.setFunction(name)(CurveNames.getFunctionLoc(name)())

def parabolicRotation(theta,list):
    t=time.time()
    [pivotName,begin,end,x,y,z]=list
    if isinstance(pivotName,str):
        nPivot=n2N(pivotName)
        pivot=position(curvei(nPivot))
    else:
        nPivot=pivotName
        pivot=position(curvei(pivotName))
    tan=PostureVector()
    for i in range(n2N(end),n2N(begin)-1,-1):
        dist=(abs(i-nPivot))
        angle=math.atan(dist)**1*5 # carre c'est trop
        cmds.select(curvei(i)) # pas de add car la rotation est deja calculee en fonction de la distance
        cmds.rotate(theta*angle,r=True,p=pivot,x=x,y=y,z=z)

        # TODO revoir difference, pas si importante 
def parabolicRotationGD(theta,list,*_):
    t=time.time()
    [pivotName,begin,end,x,y,z]=list
    if isinstance(pivotName,str):
        nPivot=n2N(pivotName)
        pivot=position(curvei(nPivot))
    else:
        nPivot=pivotName
        pivot=position(curvei(pivotName))
    for i in range(n2N(end),n2N(begin)-1,-1):
        dist=(abs(i-nPivot))
        angle=math.atan(dist)**1*5 # carre c'est trop
        cmds.select(curvei(i),add=True) # pas de add car la rotation est deja calculee en fonction de la distance
    cmds.rotate(theta*5,r=True,p=pivot,x=0,y=1,z=0)

def rot(theta,name,*_):
    if name=="LHB":
        parabolicRotation(theta,[pointOnCurveList[1],pointOnCurveList[0],pointOnCurveList[1],1,0,0]) 
    elif name=="LGD":
        parabolicRotationGD(theta,[pointOnCurveList[2],pointOnCurveList[0],pointOnCurveList[1],0,1,0])
    elif name=="CHB":
        parabolicRotation(theta,[pointOnCurveList[4],pointOnCurveList[5],pointOnCurveList[8],1,0,0]) 
    elif name=="CGD":
        parabolicRotationGD(theta,[pointOnCurveList[4],pointOnCurveList[5],pointOnCurveList[8],0,1,0])
    elif name=="DHB":
        parabolicRotation(theta,[num2Name(2),num2Name(0),num2Name(1),1,0,0])
    elif name=="DGD":    
        parabolicRotationGD(theta,[num2Name(2),num2Name(0),num2Name(1),0,1,0])
    elif name=="THB":
        parabolicRotation(theta,[6,'Tete','Tete',1,0,0])
    elif name=="TGD":
        parabolicRotationGD(theta,[6,'Tete','Tete',0,1,0])
    elif name=="CompHB":
        rotCompHB(theta)
    elif name=="CompGD":
        parabolicRotation(theta*0.05,[num2Name(1),num2Name(2),pointOnCurveList[8],0,1,0])


def rotCompGD(value,L=[]):
    parabolicRotation(value*0.05,[num2Name(1),num2Name(2),pointOnCurveList[8],0,1,0])
def rotCompHB(value,crvInfos=[]):
    nPivot=2
    pivot=position(curvei(nPivot))#n2N(num2Name(2))))

    posB=position(curvei(4))
    posE=position(curvei(2))

    #parabolicRotation(-value*0.1,[pointOnCurveList[2],pointOnCurveList[2],pointOnCurveList[3],1,0,0])
    parabolicRotation(-value,[pointOnCurveList[2],pointOnCurveList[2],pointOnCurveList[4],1,0,0])


    
    #translation pour ramener les points extremes
    tB=sub(position(curvei(4)),posB)
    cmds.select(curvei(5),curvei(6),curvei(7),curvei(8))
    cmds.move(tB[0],tB[1],tB[2],r=True)

    tE=sub(position(curvei(2)),posE)
    cmds.select(curvei(0),curvei(1))
    cmds.move(tE[0],tE[1],tE[2],r=True)


    ##print "LLenm()",getLLen()

    ##posB=position(curvei(4))
    ##posE=position(curvei(2))

    ####print "LLenm()",getLLen()
    #### pivot milieu des dorsales
    ##clear()
    ##cmds.select(curvei(2),curvei(4))
    ##pivot=position(curvei(3))
    ##cmds.rotate(value*0.3,0,0,pivot=pivot)
    ##clear()
    
    ##posB2=position(curvei(4))
    ##posE2=position(curvei(2))
    ##tB=sub(posB2,posB)
    ##tE=sub(posE2,posE)

    ##print "LLenfr()",getLLen()

    ##    #translation pour ramener les points extremes
    ##clear()
    ### 5 6 7 8
    #cmds.select(curvei(5),curvei(6),curvei(7),curvei(8))
    #cmds.move(tB[0],tB[1],tB[2],r=True)
    #clear()
    ### 0 1
    #cmds.select(curvei(0),curvei(1))
    #cmds.move(tE[0],tE[1],tE[2],r=True)
    #clear()
    ##print "LLenf()",getLLen()


# TODO revoir l'idee de faire la rot lombaire en meme temps que la compression
    #cmds.select(curvei(0))
    #cmds.rotate(value*0.5,0,0,pivot=pivot)
    #clear()
    
    #angle=(angleDHB()-angleHB())*0.0005
    #tan=normalize(sub(position(locator(2)),position(locator(3))))
    #cmds.select(curvei(3))
    #cmds.move(0,0,angle,r=True)
    #clear()





def calcPosRelatifHB(locator,Cote="",nLocator=-1):
    #orientation=getOrientation(Cote)
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

def projHor(v):
    return [v[0],v[2]]

def projHor3D(v):
    return [v[0],0,v[2]]

def calcPosRelatifGD(locatorPosition,Cote="",nLocator=-1):
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
def correctionRot(nGroup,nLocator,sliderList,HB,Croiss,Cote,nMax,precision,tour=0,coeff=0.5):
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
        [relatif,dist,str]=f(locatorP,Cote=Cote,nLocator=nLocator)
        if (relatif<0 and Croiss) or (relatif>0 and (not Croiss)):
            maxi=testV
        else:
            mini=testV 
    if distI<dist:
        if tour==0 :
            correctionRot(nGroup,nLocator,sliderList,HB,Croiss,Cote,nMax,precision,tour=1,coeff=coeff*2)
        else:
            slider.setValue(valInit)
            slider.update()
            p("correctionRot failed",slider.label)

def corr(sliderList,name,nMax=20,precision=0.01):
    if name=="LHB":
        correctionRot(7,0,sliderList,True,False,"L",nMax,precision) 
    elif name=="LGD":
        correctionRot(6,0,sliderList,False,True,"L",nMax,precision)
    elif name=="CHB":
        correctionRot(3,4,sliderList,True,False,"C",nMax,precision) 
    elif name=="CGD":
        correctionRot(2,4,sliderList,False,False,"C",nMax,precision)
    elif name=="DHB":
        correctionRot(5,1,sliderList,True,False,"",nMax,precision)
    elif name=="DGD":    
        correctionRot(4,1,sliderList,False,False,"",nMax,precision)
    elif name=="THB":
        correctionRot(11,5,sliderList,True,False,"C",nMax,precision)
    elif name=="TGD":
        correctionRot(10,5,sliderList,False,False,"C",nMax,precision)
    elif name=="CompHB":
        correctionRot(9,3,sliderList,True,True,"",nMax,precision)
    elif name=="CompGD":
        correctionRot(8,3,sliderList,False,False,"",nMax,precision)


def translateToLocator(numLocator):
    posLoc=position(locator(numLocator))
    posLocOnCurve=nearestPoint(locator(numLocator))
    t=sub(posLoc,posLocOnCurve)
    select('curve1')
    cmds.move(t[0],t[1],t[2],r=True)
    clear()

def translateToLocatorGui(sliderList,*_):
    num=-1
    result = cmds.promptDialog(message='Num of Locator:',button=['OK', 'Cancel'],\
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
    posLoc=position(locator(numLocator))
    diff=sub(posLoc,posCV)
    select('curve1')
    cmds.move(diff[0],diff[1],diff[2],r=True)
    clear()

    
def translateToCVGui(sliderList,*_):
    num=-1
    result = cmds.promptDialog(message='Num of Locator:',button=['OK', 'Cancel'],\
	defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
    if result == 'OK' :
	    num=int(cmds.promptDialog(query=True, text=True))
    if num==0:
        translateToCV(0,0)
    elif num==2:
        translateToCV(2,2)
    elif num==3:
        translateToCV(4,3)
    elif num==4:
        translateToCV(6,4)
    elif num==5:
        translateToCV(8,5)
    #update position Gui
    for i in range(12,15):
        sliderList[i].update()





            
# garde en memoire le meilleur si marche pas bien
#def correctionRot(sliderGrp,nButton,nLocator,Croiss=True,precision=10,Cote=""):
#    locatorP=position(locator(nLocator))
#    f = calcPosRelatifHB if nButton%2==sliderGrp.string2num("rotCHB")%2  else calcPosRelatifGD
#    distI=norm(sub(locatorP,getPoint(getParameter(locatorP))))
#    dist=distI
#    button=sliderGrp.buttonList[nButton]
#    slider=button.slider
#    valInit=slider.sliderValue()
#    minSlider=slider.minValue
#    maxSlider=slider.maxValue
#    relatif=1
#    maxi=min(valInit+dist*0.2*(slider.maxValue-slider.minValue),maxSlider)
#    mini=max(valInit-dist*0.2*(slider.maxValue-slider.minValue),minSlider)
#    i=0
#    while i<precision and abs(relatif)>0.01:
#        i+=1
#        testV=(mini+maxi)/2
#        #print "mini",mini,maxi,testV
#        slider.setValue(testV)
#        slider.update()
#        [relatif,dist,str]=f(locatorP,Cote=Cote,nLocator=nLocator)
#        if (relatif<0 and Croiss) or (relatif>0 and (not Croiss)):
#            maxi=testV
#        else:
#            mini=testV 
#    if distI<dist:
#        slider.setValue(valInit)
#        slider.update()
#        p("correctionRot failed",slider.label)


