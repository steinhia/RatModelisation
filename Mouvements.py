# -*- coding: utf-8 -*-

import sys


sys.path.append("C:/Users/alexa/Documents/alexandra/scripts")
path="C:/Users/alexa/Documents/alexandra/scripts/"
execfile(path+"Calculs.py")


def UndoGui(sliderList,*_):
    cmds.undo()
    for sliderDuo in sliderList:
        sliderDuo.update()


def setLength(newLengthvalue,*_):#numPivot=2):
    posInit=getPoint(MaxParam()/2.0)
    posInit=getPosition()
    L=cmds.arclen('curve1')
    scaleValue=newLengthvalue/L
    cmds.select('joint1')# r=1,
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
    select('curve1') # TODO s'occuper du add=True
    cmds.scale(scaleValue,scaleValue,scaleValue,r=True,pivot=posInit)
    #maya.mel.eval('propModTypeCallback 2;')
    #maya.mel.eval('propModValues PropMod;')
    #maya.mel.eval('toolPropertyShow;')
    #maya.mel.eval('dR_updateToolSettings;')
    #maya.mel.eval('propModCtx -e -pd 5 `currentCtx`;')
    #maya.mel.eval('propModValues PropMod;')
    #maya.mel.eval('toolPropertyShow;')
    #maya.mel.eval('dR_updateToolSettings;')
    #select('curve1')
    #cmds.propMove(px=1,py=1,pz=1,s=[scaleValue,scaleValue,scaleValue],pivot=posInit)
    #print getLLen(),getCLen(),getTLen()
    #cmds.manipPivot( r=True )
    clear()

def setScale(newLengthvalue,*_):
    setLength(newLengthvalue)

#    manipPivot -p -21.588785 33.082133 -2.598126 ;
#scale -r -p -21.588785cm 33.082133cm -2.598126cm 0.951209 0.951209 0.951209 ;


def keepChainLengthValue(newValue,L=[]):
    Length=getJointChainLength()
    posInit=getPosition()
    cmds.select('joint1',r=1)
    scaleValue=newValue/Length
    cmds.scale(scaleValue,scaleValue,scaleValue,r=True,pivot=posInit)
 


def setLength2(newValue,L=[]):
    Length=getLength()#JointChainLength()
    posInit=getPosition()
    select('curve1')
    #cmds.select('joint1',add=True,r=True)
    scaleValue=newValue/Length
    cmds.scale(scaleValue,scaleValue,scaleValue,r=True,pivot=posInit)

def setLength2D(val,*_):
    posInit=getPosition()
    L=cmds.arclen('curve1')
    scaleValue=val/L
    cmds.select('joint1',r=1,add=True)
    select('curve1')
    cmds.scale(scaleValue,1,scaleValue,r=True,pivot=posInit)
    clear()

def scaleGui(sliderList,*_):
    sf=getScale()
    setLength(sf)
    sliderList[11].update()

def scaleCPOCGui(sliderList,*_):
    sf=getScaleCPOC()
    setLength(sf)
    sliderList[11].update()

def scale2DGui(sliderList,*_):
    sf=ScaleFactor2D()
    setLength2D(sf)
    sliderList[11].update()

def scaleExtremitiesGui(sliderList,*_):
    sf=getScaleExtremities()
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
        cmds.select(curvei(4),curvei(5),curvei(6),curvei(6))
        cmds.scale(sc,sc,sc,pivot=pos)
        sc=newCLen/a

def setCurvePosition(pos,Cote=""):
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
    # position du centre au depart
    pos=getPosition()
    select('curve1')
    for i in range(30):
        posture=getPosture(Cote)
        orient=PostureVector(Cote)
        angle=posture-ThetaVoulu
        cmds.rotate(angle*orient[2],0.0,angle*orient[0],r=True,pivot=pos)

def setOrientation(ThetaVoulu,Cote=""):
    pos=getPosition()
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
#        #keepOneLen(curvei(3),curvei(5),Len1,Ncurve,beginPD,endPD)
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
    else:
        #fVal=setOneRot(val,fx,[slider,getFunction,getFunctionArgs,crvInfos])
        pas=(maxSlider-minSlider)/500.0
        mini=fx-pas
        maxi=fx+pas
         #on regarde si croissant ou decroissant
        fMin=setOneRot(val,mini,slider)
        fMax=setOneRot(val,maxi,slider)
        i=0
        while (not isInside(theta,fMin,fMax)) and ((minSlider<mini and maxSlider>maxi and minSlider<maxSlider) or (minSlider<maxi and maxSlider>mini and minSlider>maxSlider)) and i<10:
            i+=1
            pas*=5.0
            mini=fx-pas
            maxi=fx+pas
            fMin=setOneRot(val,mini,slider)
            fMax=setOneRot(val,maxi,slider)
        if i==10 or (mini<minSlider or maxi>maxSlider):
            #print "tentative f-1 failed",getFunction,"calcMinMax",mini,maxi,fx,pas
            mini=minSlider
            maxi=maxSlider
            fMin=setOneRot(val,minSlider,slider)
            fMax=setOneRot(val,maxSlider,slider)
    if isInside(theta,fMin,fMax):
        i=0
        while abs(fTest-theta)>0.01 and i<nMax and abs(mini-maxi)>0.0001:
            i+=1
            test=float(mini+maxi)/2.0
            fTest=setOneRot(val,test,slider)
            if i>15:
                1#print "gde value",test,"fTest",fTest,"theta",theta
            if((fTest>theta and fMin<fMax) or (fTest<theta and fMin>fMax )):
                maxi=test
            else :
                mini=test
        setOneRotWithChangement(test,slider)
        t=time.time()
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
    return test

def setAngle(sliderList,name,offset=1,*_):
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
    if "HB" in name or "GD" in name:
        setRot(param[numSlider(name)],sliderList[numSlider(name)].slider)
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


#def parabolicRotation(theta,list):
#    t=time.time()
#    [pivotNum,begin,end,x,y,z]=list
#    pivotPos=position(curvei(pivotNum))

#    if begin<pivotNum:
#        print "pivot",pivotNum
#        for i in range(begin,end+1):
#            print i
#            dist=(abs(i-pivotNum))
#            pivotPos=position(curvei(i+1))
#            angle=math.atan(dist)**1*5 # carre c'est trop
#            cmds.select(curvei(i),add=True) # pas de add car la rotation est deja calculee en fonction de la distance
#            cmds.rotate(theta*angle,r=True,p=pivotPos,x=x,y=y,z=z)
#    else:
#        print "pivot",pivotNum
#        for i in range(end,begin-1,-1):
#            print i
#            dist=(abs(i-pivotNum))
#            pivotPos=position(curvei(i-1))
#            angle=math.atan(dist)**1*5 # carre c'est trop
#            cmds.select(curvei(i),add=True) # pas de add car la rotation est deja calculee en fonction de la distance
#            cmds.rotate(theta*5,r=True,p=pivotPos,x=x,y=y,z=z)

def parabolicRotation(theta,list):
    t=time.time()
    [pivotNum,begin,end,x,y,z]=list
    pivotPos=position(curvei(pivotNum))

    if begin<pivotNum:
        #print "pivot",pivotNum
        for i in range(begin,end+1):
            #print "pivot point",i+1,i
            dist=(abs(i-pivotNum))
            pivotPos=position(curvei(i+1))
            angle=math.atan(dist)**1*5 # carre c'est trop
            cmds.select(curvei(i),add=True) # pas de add car la rotation est deja calculee en fonction de la distance
            cmds.rotate(theta*angle,r=True,p=pivotPos,x=x,y=y,z=z)
    else:
        #print "pivot",pivotNum
        for i in range(end,begin-1,-1):
            #print "pivot point",i-1,i
            dist=(abs(i-pivotNum))
            pivotPos=position(curvei(i-1))
            angle=math.atan(dist)**1*5 # carre c'est trop
            cmds.select(curvei(i),add=True) # pas de add car la rotation est deja calculee en fonction de la distance
            cmds.rotate(theta*5,r=True,p=pivotPos,x=x,y=y,z=z)

        # TODO revoir difference, pas si importante 
def parabolicRotationGD(theta,list,*_):
    t=time.time()
    [pivotNum,begin,end,x,y,z]=list
    pivotPos=position(curvei(pivotNum))
    for i in range(end,begin-1,-1):
        dist=(abs(i-pivotNum))
        angle=math.atan(dist)**1*5 # carre c'est trop
        cmds.select(curvei(i)) # pas de add car la rotation est deja calculee en fonction de la distance
        cmds.rotate(theta*angle*0.5,r=True,p=pivotPos,x=x,y=y,z=y)

def rot(theta,name,*_):
    if name=="LHB":
        parabolicRotation(theta*3,[1,0,0,1,0,0]) # 2 0 1
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
        # ca ou rotaiton puis decalege -> plus stable pour recalage C T TODO
        rotCompGD(theta)



def rotCompGD(theta,*_):
    #posC=position(curvei(5))
    parabolicRotationGD(theta,[2,3,7,0,1,0])
    #tC=sub(position(curvei(5)),posC)
    #cmds.select(curvei(6),curvei(7))
    #cmds.move(tC[0],tC[1],tC[2],r=True)

#def rotCGD(theta,*_):


#def rotCompGD(value,L=[]):
#    parabolicRotation(value*0.05,[num2Name(2),num2Name(3),pointOnCurveList[8],0,1,0]) 
def rotCompHB(value,*_):



    # trans que pour les cervicales!!!
    nPivot=1
    pivot=position(curvei(nPivot))#n2N(num2Name(2))))

    # quelles positions a garder?
    posB=position(curvei(4))
    posE=position(curvei(1))

    pos3=position(curvei(3))
    pos2=position(curvei(1))

    #cmds.select(curvei(3))
    #cmds.move(0,value*0.0,value*0.5,r=True)
    #cmds.select(curvei(3))
    #cmds.move(0,-value*0.5,value*2,r=True)
    #cmds.select(curvei(3))
    #cmds.move(0,-value*0.25,value*1,r=True)


    #cmds.select(curvei(1))
    #cmds.move(0,value*0,value*3,r=True)

    #cmds.select(curvei(3))
    #cmds.move(0,-value*0.5,+value,r=True)

    #t3=sub(position(curvei(3)),pos3)
    #cmds.select(curvei(4),curvei(5),curvei(6),curvei(7))
    #cmds.move(t3[0],t3[1],t3[2],r=True)

    #t2=sub(position(curvei(3)),pos2)
    #cmds.select(curvei(0),curvei(1))
    ##cmds.move(t2[0],t2[1],t2[2],r=True)
    #cmds.select(curvei(0),curvei(1))
    #cmds.move(t2[0],t2[1],t2[2],r=True)


    parabolicRotation(-value,[1,2,4,1,0,0])
    ##cmds.select(curvei(3),curvei(4))
    ##cmds.rotate(-value*10,0,0,r=True,pivot=position(curvei(3)))



    #translation pour ramener les points extremes
    tB=sub(position(curvei(4)),posB)
    cmds.select(curvei(5),curvei(6),curvei(6),curvei(7))
    cmds.move(tB[0],tB[1],tB[2],r=True)

    #tE=sub(position(curvei(3)),posE)
    #cmds.select(curvei(0),curvei(1))
    #cmds.move(tE[0],tE[1],tE[2],r=True)






# TODO revoir l'idee de faire la rot lombaire en meme temps que la compression
    #cmds.select(curvei(0))
    #cmds.rotate(value*0.5,0,0,pivot=pivot)
    #clear()
    
    #angle=(angleDHB()-angleHB())*0.0005
    #tan=normalize(sub(position(locator(2)),position(locator(3))))
    #cmds.select(curvei(3))
    #cmds.move(0,0,angle,r=True)
    #clear()



