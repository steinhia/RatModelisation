import sys


sys.path.append("C:/Users/alexa/Documents/alexandra/scripts")
path="C:/Users/alexa/Documents/alexandra/scripts/"
execfile(path+"Calculs.py")

#TODO pos different
def keepLengthValue(newLengthvalue,L=[]):
    #defPivot()
    posInit=getCurvePosition()
    L=cmds.arclen('curve1')
    scaleValue=newLengthvalue/L
    cmds.select('joint1',r=1,add=True)
    select('curve1')
    cmds.scale(scaleValue,scaleValue,scaleValue,r=True,pivot=posInit)

def keepChainLengthValue(newValue,L=[]):
    Length=getChainLength()
    posInit=getCurvePosition()
    cmds.select('joint1',r=1)
    scaleValue=newValue/Length
    cmds.scale(scaleValue,scaleValue,scaleValue,r=True,pivot=posInit)

def recalageTangent(numLocator,numPoint):
    for i in range(2):
        posLocOnCurve=nearestPoint(locator(numLocator))
        posCVOnCurve=getPoint(getParameter(position(curvei(numPoint))))
        vect=sub(posLocOnCurve,posCVOnCurve)
        cmds.select(curvei(numPoint))
        cmds.move(vect[0],vect[1],vect[2],r=True)

def recalageTangentSansLocator(oldParam,newParam,numPoint):
    #p("recalage",numPoint)
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
   
def keepParameters(param):
    maxCV = cmds.getAttr("curve1.spans")+cmds.getAttr("curve1.degree")
     #influence sur les 2 points d'a cote
    for j in range(1):
        #print calcCVParameters()
        for i in range(len(param)): 
            par=calcCVParameter(i)
            if abs(param[i]-par)>0.0001:
                recalageTangentWithName(param[i],par,i)

def keepJointParameters(jtParam):
    for i,paramJ in enumerate(jtParam):
        oldJtPos=getPoint(paramJ)
        newPoint=nearestPoint('joint'+str(i+1))
        trans=sub(oldJtPos,newPoint)
        cmds.select('joint'+str(i+1))
        cmds.move(trans[0],trans[1],trans[2],r=True)


def replaceC():
    for i in range(2):
        posC5=nearestPoint('C5')
        posCVOnCurve=nearestPoint(curvei(5))
        trans=sub(posC5,posCVOnCurve)
        cmds.select(curvei(5))
        cmds.move(trans[0],trans[1],trans[2],r=True)
    
def keepCLen(newCLen):
    #p("keep")
    #cmds.select(clear=True)
    for i in range(3):
        pos=position(curvei(5))
        a=getCLen()
        sc=newCLen/a
        cmds.select(curvei(4),curvei(5),curvei(6))
        cmds.scale(sc,sc,sc,pivot=pos)
        sc=newCLen/a
    #p("cLen fin",getCLen())
    #if abs(newCLen-getCLen())>0.001:
    #    print "Error CLen"

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
    pos=getCurvePosition(Cote=Cote)
    for i in range(5):
        posture=calcPosture(Cote)
        orient=PostureVector(Cote)
        angle=posture-ThetaVoulu
        select('curve1')
        cmds.rotate(angle*orient[2],0.0,angle*orient[2],r=True,pivot=pos)


#TODO PB A 180 -> bon calcul? regarder modif avec compression
def setOrientation(ThetaVoulu,Cote=""):
    pos=getCurvePosition(Cote)
    orient=calcOrientation(Cote)
    angle=ThetaVoulu-orient
    select('curve1')
    cmds.rotate(0.0,angle,0.0,r=True,pivot=pos)

def Align():
    val=calcAlign()
    pivot=position(curvei(0))
    pivot=-1
    select('curve1')
    cmds.rotate(0.0,val,0.0,r=True,pivot=pivot)
    setCurvePosition([0.0,7.0,0.0])




    

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
#        keepLengthValue(Ncurve)
#        for i in range(5):
#            scaleValue=crvLengthVoulu/crvLengthNew
#            pivot=getBarycentre(begin,end,0.5) 
#            cmds.select(clear=True )
#            for j in range(int(begin[-2]),int(end[-2])+1):
#                cmds.select(curvei(j),add=True)
#            cmds.scale(scaleValue,scaleValue,scaleValue,r=True,p=pivot)
#            keepLengthValue(Ncurve)
#            [crvLengthNew,distBegin2]=getLen(beginP,endP)
#        [crvLengthNew,distBegin2]=getLen(beginP,endP)


# teste une valeur du premier slider pour obtenir la courbure voulue -> envoie premier slider dans la fonction
# trop long
def setOneRot(valeur,test,L,moveSlider=False):
    t=time.time()
    [slider,getFunction,getFunctionArgs]=L
    fTest=setOneRotWithChangement(test,slider,getFunction,getFunctionArgs,moveSlider=moveSlider)
    t=time.time()
    if moveSlider :
        slider.setValue(valeur) 
        slider.update(False,True)  # attention ne pas changer le false en true
    else:
        setOneRotWithChangement(valeur,slider,getFunction,getFunctionArgs,moveSlider=moveSlider)
    t=time.time()
    return fTest

# applique le changement
def setOneRotWithChangement(test,slider,getFunction,getFunctionArgs,moveSlider=True):
    t=time.time()
    if moveSlider :
        slider.setValue(test)
        #p("apres set",time.time()-t)
        t=time.time()
        slider.update(False,True) # attention ne pas changer le false en true
        #p("apres upd",time.time()-t)
    else :
        # execute action sans changer la valeur du slider pour eviter les manipulations de Gui
        slider.setActionWithoutMoving(test)
        #p("setAction",time.time()-t)
    t=time.time()
    fTest=getFunction(getFunctionArgs)
    return fTest

def isInside(courbure,fMin,fMax):
    return (courbure >=fMin and courbure <=fMax) or (courbure >=fMax and courbure <=fMin)

# cherche a atteindre une courbure par dichotomie
# slider envoye = slider1
def setRot(courbure,L):
    [slider,getFunction,getFunctionArgs,crvInfos,minSlider,maxSlider]=L
    fTest=100000.0
    fx=slider.f(courbure)
    test=fx
    #fx=[]
    val=slider.getValue()
    #print "fx",fx
    #print "setR"
    if fx==[] or True:
        mini=minSlider
        maxi=maxSlider
        # on peut eventuellement avoir fMin>fMax
        fMin=setOneRot(val,mini,[slider,getFunction,getFunctionArgs])
        fMax=setOneRot(val,maxi,[slider,getFunction,getFunctionArgs])
    #else:
    #    #fVal=setOneRot(val,fx,[slider,getFunction,getFunctionArgs,crvInfos])
    #    pas=(maxSlider-minSlider)/2000.0
    #    mini=fx-pas
    #    maxi=fx+pas
    #     #on regarde si croissant ou decroissant
    #    fMin=setOneRot(val,mini,[slider,getFunction,getFunctionArgs])
    #    fMax=setOneRot(val,maxi,[slider,getFunction,getFunctionArgs])
    #    i=0
    #    while (not isInside(courbure,fMin,fMax)) and ((minSlider<mini and maxSlider>maxi and minSlider<maxSlider) or (minSlider<maxi and maxSlider>mini and minSlider>maxSlider)) and i<10:
    #        i+=1
    #        pas*=5.0
    #        mini=fx-pas
    #        maxi=fx+pas
    #        fMin=setOneRot(val,mini,[slider,getFunction,getFunctionArgs])
    #        fMax=setOneRot(val,maxi,[slider,getFunction,getFunctionArgs])
    #    if i==10 or (mini<minSlider or maxi>maxSlider):
    #        print "tentative f-1 failed",getFunction,"calcMinMax",mini,maxi,fx,pas
    #        mini=minSlider
    #        maxi=maxSlider
    #        fMin=setOneRot(val,minSlider,[slider,getFunction,getFunctionArgs])
    #        fMax=setOneRot(val,maxSlider,[slider,getFunction,getFunctionArgs])
        #print ("i",i)
        #mini=max(mini,minSlider)
        #maxi=min(maxi,maxSlider)
        #fMin=setOneRot(val,mini,[slider,getFunction,getFunctionArgs])
        #fMax=setOneRot(val,maxi,[slider,getFunction,getFunctionArgs])
        #p("min",mini,maxi,minSlider,maxSlider,fMin,fMax)
    if isInside(courbure,fMin,fMax):
        i=0
        while abs(fTest-courbure)>0.1 and i<20:
            i+=1
            test=float(mini+maxi)/2.0
            fTest=setOneRot(val,test,[slider,getFunction,getFunctionArgs])
            if i>15:
                1#print "gde value",test,"fTest",fTest,"courbure",courbure
            if((fTest>courbure and fMin<fMax) or (fTest<courbure and fMin>fMax )):
                maxi=test
            else :
                mini=test
        setOneRotWithChangement(test,slider,getFunction,getFunctionArgs)
        t=time.time()
        #print "boucle 2 ",  i
    elif (courbure <=fMin and fMin<=fMax) or (courbure>=fMin and fMin>=fMax) :
        setOneRotWithChangement(mini,slider,getFunction,getFunctionArgs)
        test=mini
        #print "en dehors des bornes! plus petit que le minimum",fMin,fMax,getFunction,courbure
    else:
        setOneRotWithChangement(maxi,slider,getFunction,getFunctionArgs)
        test=maxi
        #print "en dehors des bornes! plus grand que le maximum",fMin,fMax,getFunction,courbure
    # TODO regarder ici si ca passe pas trop souvent -> TestClass Mini
    if(abs(courbure-getFunction(getFunctionArgs))>0.01 and test!=mini and test!=maxi):
        print "FAIL SETROT", getFunction,abs(courbure-getFunction(getFunctionArgs))
    #print "duree",time.time()-t
    return test
    

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
        #p(i)
        angle=math.atan(dist)**1*5 # carre c'est trop
        cmds.select(curvei(i)) # pas de add car la rotation est deja calculee en fonction de la distance
        cmds.rotate(theta*angle,r=True,p=pivot,x=x,y=y,z=z)
    #p("parRot",str(time.time()-t))
        #if x==1:
        #    norm=[-tan[0],tan[2],-tan[1]]
        #    cmds.rotate(theta*angle,r=True,p=pivot,x=x,y=y,z=z)
        #    #cmds.rotate(theta*angle*norm[0],theta*angle*norm[1],theta*angle*norm[2],r=True,p=pivot)
        #else:
        #    cmds.rotate(theta*angle,r=True,p=pivot,x=x,y=y,z=z)


#TODO choisir 3 02 ou 2 0 1
def rotLHB(theta,L=[]):
    parabolicRotation(theta,[pointOnCurveList[1],pointOnCurveList[0],pointOnCurveList[1],1,0,0]) # L3 L6 L6
def rotLGD(theta,L=[]):
    parabolicRotation(theta,[pointOnCurveList[1],pointOnCurveList[0],pointOnCurveList[1],0,1,0]) # L3 L6 L6 si besoin pivot a un : comp mal reglee
def rotCHB(theta,L=[]):
    parabolicRotation(theta,[pointOnCurveList[4],pointOnCurveList[5],pointOnCurveList[7],1,0,0]) # C7 C7 C0
def rotCGD(theta,L=[]):
    parabolicRotation(theta,[pointOnCurveList[4],pointOnCurveList[5],pointOnCurveList[7],0,1,0])
def rotDHB(theta,L=[]):
    parabolicRotation(theta,[num2Name(2),num2Name(0),num2Name(1),1,0,0])
def rotDGD(theta,L=[]):
    parabolicRotation(theta,[num2Name(2),num2Name(0),num2Name(1),0,1,0])
def rotTHB(theta,L=[]):
    parabolicRotation(theta,[6,'Tete','Tete',1,0,0])
def rotTGD(theta,L=[]):
    parabolicRotation(theta,[6,'Tete','Tete',0,1,0])


def rotComp(value,crvInfos=[]):

    #parabolicRotation(value*0.5,[num2Name(2),num2Name(0),num2Name(1),1,0,0])

   # premiere partie, rotation dans un sens
    nBegin=n2N(pointOnCurveList[2])
    nEnd=n2N(pointOnCurveList[4]) # TODO ou 5
    nMax= cmds.getAttr("curve1.spans")+cmds.getAttr("curve1.degree")-1
    pivot=position(curvei(n2N(num2Name(2))))
    nPivot=2
    posB=position(curvei(nEnd))
    posE=position(curvei(nMax))
    for i in range(nEnd,nBegin-1,-1):
        cmds.select(curvei(i),add=True)
        cmds.rotate(-value*0.5,0.0,0.0,r=True,pivot=pivot)
    posB2=position(curvei(nEnd))
    posE2=position(curvei(nMax))
    tB=sub(posB2,posB)
    tE=sub(posE2,posE)
    cmds.select(clear=True)
    for i in range(nEnd+1,nMax+1):
        cmds.select(curvei(i),add=True)
    cmds.move(tB[0],tB[1],tB[2],r=True)
    cmds.select(clear=True)
    for i in range(0,nEnd-2):
        cmds.select(curvei(i),add=True)
    cmds.move(tE[0],tE[1],tE[2],r=True)
    cmds.select(clear=True)

    cmds.select(clear=True)
    cmds.select(curvei(2),curvei(4))
    pivot=position(curvei(3))
    cmds.rotate(-value*0.1,0,0,pivot=pivot)
    cmds.select(clear=True)

    cmds.select(curvei(5))
    pivot=position(curvei(4))
    #cmds.rotate(-value*2,0,0,pivot=pivot)

# TODO revoir l'idee de faire la rot lombaire en meme temps que la compression
    #cmds.select(curvei(0))
    #cmds.rotate(value*0.5,0,0,pivot=pivot)
    #cmds.select(clear=True)




    #angle=(angleDHB()-angleComp())*0.0005
    #tan=normalize(sub(position(locator(2)),position(locator(3))))
    #cmds.select(curvei(3))
    #cmds.move(0,0,angle,r=True)
    #cmds.select(clear=True)


def rotCompGD(value,L=[]):
    parabolicRotation(value*0.05,[num2Name(1),num2Name(2),pointOnCurveList[7],0,1,0])




    
    


            



