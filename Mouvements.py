import sys


sys.path.append("C:/Users/alexandra/Documents/alexandra/scripts")
path="C:/Users/alexandra/Documents/alexandra/scripts/"
execfile(path+"Calculs.py")


def keepLengthValue(newLengthvalue,L=[]):
    defPivot()
    if L!=[]:
        Infos=L
    else:
        posInit=getCurvePosition()
    Length=cmds.arclen('curve1')
    scaleValue=newLengthvalue/Length
    cmds.select('curve1','joint1',r=1)
    cmds.scale(scaleValue,scaleValue,scaleValue,r=True)

def keepChainLengthValue(newValue,L=[]):
    Length=getChainLength()
    cmds.select('joint1',r=1)
    scaleValue=newValue/Length
    cmds.scale(scaleValue,scaleValue,scaleValue,r=True)
    

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

def setCurvePosition(pos,L=[]):
    posInit=L if L!=[] else getCurvePosition()
    translation=[pos[i]-posInit[i] for i in range(3)]
    cmds.select("curve1")
    cmds.move(translation[0],translation[1],translation[2],'curve1',r=1)


def setX(x,L=[]):
    pos=L[1][0] if L!=[] else getCurvePosition(0)
    xTrans=x-pos
    cmds.select("curve1")
    cmds.move(xTrans,0,0,r=1)

def setY(y,L=[]):
    pos=L[1][1] if L!=[] else getCurvePosition(1)
    yTrans=y-pos
    cmds.select("curve1")
    cmds.move(0,yTrans,0,r=1)

def setZ(z,L=[]):
    pos=L[1][2] if L!=[] else getCurvePosition(2)
    zTrans=z-pos
    cmds.select("curve1")
    cmds.move(0,0,zTrans,r=1)

def setPosture(ThetaVoulu,crvInfos=[],):
    # position du centre au depart
    pos=crvInfos[1] if crvInfos!=[] else getCurvePosition()
    posture=calcPosture()
    cmds.select('curve1')
    cmds.rotate(-ThetaVoulu+posture,0.0,0.0,r=True,pivot=pos)

def setPostureGD(ThetaVoulu,crvInfos=[],):
    pos=crvInfos[1] if crvInfos!=[] else getCurvePosition()
    posture=calcPostureGD()
    cmds.select('curve1')
    cmds.rotate(0.0,ThetaVoulu-posture,0.0,r=True,pivot=pos)

def Align():
    val=calcAlign()
    pivot=position(curvei(0))
    pivot=-1
    cmds.select('curve1')
    cmds.rotate(0.0,val,0.0,r=True,pivot=pivot)
    setCurvePosition([0.0,7.0,0.0])


def parabolicRotation(theta,list):
    [pivotName,begin,end,x,y,z]=list
    nPivot=n2N(pivotName)
    pivot=position(curvei(nPivot))
    for i in range(n2N(end),n2N(begin)-1,-1):
        dist=abs(i-nPivot)
        angle=math.atan(dist)
        cmds.select(curvei(i))
        cmds.rotate(theta*angle*20.0,r=True,p=pivot,x=x,y=y,z=z)

def rotLHB(theta,L=[]):
    parabolicRotation(theta,[num2Name(1),num2Name(0),num2Name(0),1,0,0]) # L3 L6 L6
def rotLGD(theta,L=[]):
    parabolicRotation(theta,[num2Name(1),num2Name(0),num2Name(0),0,1,0])
def rotCHB(theta,L=[]):
    parabolicRotation(theta,[num2Name(3),num2Name(3),num2Name(4),1,0,0]) # C7 C7 C0
def rotCGD(theta,L=[]):
    parabolicRotation(theta,[num2Name(3),num2Name(3),num2Name(4),0,1,0])
def rotDHB(theta,L=[]):
    parabolicRotation(theta,['T12',num2Name(0),num2Name(1),1,0,0])
def rotDGD(theta,L=[]):
    parabolicRotation(theta,['T12',num2Name(0),num2Name(1),0,1,0])

def getRatios(beginPD,endPD,beginPC,endPC):
    [crvLengthNewD,distBeginD]=getLen(beginPD,endPD)
    [crvLengthNewC,distBeginC]=getLen(beginPC,endPC)
    return  [distBeginD,distBeginC,crvLengthNewD,crvLengthNewC]

def keepGroupLen(Len2,Ncurve):
    #for i in range(5):
        #keepOneLen(curvei(2),curvei(5),Len1,Ncurve,beginPD,endPD)
    beginPC=getParameter(position(curvei(n2N("C7"))))
    endPC=getParameter(position(curvei(n2N("C1"))))
    keepOneLen(curvei(4),curvei(6),Len2,Ncurve,beginPC,endPC)


def keepOneLen(begin,end,crvLengthVoulu,Ncurve,beginP,endP):
    [crvLengthNew,distBegin2]=getLen(beginP,endP)
    if(crvLengthNew>0):
        keepLengthValue(Ncurve)
        for i in range(5):
            scaleValue=crvLengthVoulu/crvLengthNew
            pivot=getBarycentre(begin,end,0.5) 
            cmds.select(clear=True )
            for j in range(int(begin[-2]),int(end[-2])+1):
                cmds.select(curvei(j),add=True)
            cmds.scale(scaleValue,scaleValue,scaleValue,r=True,p=pivot)
            keepLengthValue(Ncurve)
            [crvLengthNew,distBegin2]=getLen(beginP,endP)
        [crvLengthNew,distBegin2]=getLen(beginP,endP)


# teste une valeur du premier slider pour obtenir la courbure voulue
def setOneRot(valeur,test,L):
    #t=time.time()
    [slider,getFunction,getFunctionArgs,crvInfos]=L
    fTest=setOneRotWithChangement(test,slider,getFunction,getFunctionArgs,crvInfos)
    slider.setValue(valeur) 
    slider.update(False,True)  
    return fTest

# applique le changement
def setOneRotWithChangement(test,slider,getFunction,getFunctionArgs,crvInfos,ajust=False):
    slider.setValue(test)
    #t=time.time()
    slider.update(False,True) # TODO regarder influence et resultat aux tests + difference de temps au niveau des sliderupdate
    args=getFunctionArgs+[crvInfos] if getFunctionArgs!=[] else crvInfos
    fTest=getFunction(args)
    return fTest

def isInside(courbure,fMin,fMax):
    return (courbure >=fMin and courbure <=fMax) or (courbure >=fMax and courbure <=fMin)

# cherche a atteindre une courbure par dichotomie
# confusion test et fTest
def setRot(courbure,L):
    #p("setRot")
    [slider,getFunction,getFunctionArgs,minSlider,maxSlider,crvInfos]=L
    fTest=100000.0
    fx=slider.f(courbure)
    val=slider.getValue()
    if fx!=[]:
        pas=(maxSlider-minSlider)/2000.0
        mini=fx-pas
        maxi=fx+pas
         #on regarde si croissant ou decroissant
        fMin=setOneRot(val,mini,[slider,getFunction,getFunctionArgs,crvInfos])
        fMax=setOneRot(val,maxi,[slider,getFunction,getFunctionArgs,crvInfos])
        i=0
        while not isInside(courbure,fMin,fMax) and minSlider<mini and maxSlider>maxi and i<10:
            i+=1
            pas*=5.0
            mini=fx-pas
            maxi=fx+pas
            fMin=setOneRot(val,mini,[slider,getFunction,getFunctionArgs,crvInfos])
            fMax=setOneRot(val,maxi,[slider,getFunction,getFunctionArgs,crvInfos])
        mini=max(mini,minSlider)
        maxi=min(maxi,maxSlider)
    else:
        mini=minSlider
        maxi=maxSlider
        fMin=setOneRot(val,mini,[slider,getFunction,getFunctionArgs,crvInfos])
        fMax=setOneRot(val,maxi,[slider,getFunction,getFunctionArgs,crvInfos])
    if isInside(courbure,fMin,fMax):
        i=0
        while abs(fTest-courbure)>0.001 and i<20:
            i+=1
            test=float(mini+maxi)/2.0
            fTest=setOneRot(val,test,[slider,getFunction,getFunctionArgs,crvInfos])
            if i>15:
                1#print "gde value",test,fTest,courbure
            if((fTest>courbure and fMin<fMax) or (fTest<courbure and fMin>fMax )):
                maxi=test
            else :
                mini=test

        setOneRotWithChangement(test,slider,getFunction,getFunctionArgs,crvInfos,True)
    elif (courbure <=fMin and fMin<=fMax) or (courbure>=fMin and fMin>=fMax) :
        setOneRotWithChangement(mini,slider,getFunction,getFunctionArgs,crvInfos,True)
    else:
        setOneRotWithChangement(maxi,slider,getFunction,getFunctionArgs,crvInfos,True)

    
def compresseDorsales(value,crvInfos=[]):
    #p("valComp",value)
    nBegin=n2N('T8')
    nEnd=n2N('T2')
    nMax= cmds.getAttr("curve1.spans")+cmds.getAttr("curve1.degree")-1
    pivot=position(curvei(n2N('L1')))
    posB=position(curvei(nEnd))
    posE=position(curvei(nMax))
    cmds.select(clear=True)
    for i in range(nBegin,nEnd+1):
        cmds.select(curvei(i),add=True)
    cmds.rotate(value,0.0,0.0,r=True,pivot=pivot)
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


    
    


            



