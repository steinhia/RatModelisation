# -*- coding: utf-8 -*-

import sys
sys.path.append("C:/Users/alexa/Documents/alexandra/scripts")


import time
import maya.mel as mel
import inspect

path="C:/Users/alexa/Documents/alexandra/scripts/"
execfile(path+"main.py")
execfile(path+"mesures.py")
execfile(path+"EvalClass.py")

def placageOpti():
    min=100000
    iMin=-1
    for j in range(45,65):
        res=placageManuel(2,j)
        if res<min:
            min=res
            iMin=j
    print iMin
    print min
    return iMin



def ajustePos():
    # position des differents locators / vertebres correspondantes
    posLoc=map(position,[locator(0),locator(1),locator(2),locator(3),locator(4)])
    pos=map(num2Name,range(5))
    pos=map(position,pos)
    subPos=[0,0,0]
    for i,posi in enumerate(pos):
        val=sub(posLoc[i],posi)
        #print val
        subPos=sum(subPos,val)
    subPos=pdt(0.2,subPos)
    select('curve1')
    cmds.move(subPos[0],subPos[1],subPos[2],r=True)

def resetCurve(length,pos,jtPos):
    setLength(length)     
    for i,posi in enumerate(pos):
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

def placeTete():
    C0OnCurve=nearestPoint('locatorAngle4')
    p("C0OnCurve",C0OnCurve)
    posTeteOnCurve=position('Tete')
    posTeteLocator=position(locator(4))
    v1=sub(posTeteOnCurve,C0OnCurve)
    v2=sub(posTeteLocator,C0OnCurve)
    angle=angleHB(v1,v2)
    cmds.select(curvei(7))
    cmds.rotate(angle,0,0,pivot=C0OnCurve)





def correctionPos(sliderGrp,nPoint,locator):
    for i in range(10):
        vect=sub(locator,getPoint(getParameter(locator)))
        cmds.select(curvei(nPoint))
        cmds.move(vect[0],vect[1],vect[2],r=True)

def ajustePosCurvePoints():
    ajustePosOneCurvePoint(0,0)
    ajustePosOneCurvePoint(4,6)

def ajustePosCurvePointsInt():
    ajustePosOneCurvePoint(1,1)
    ajustePosOneCurvePoint(2,2)
    ajustePosOneCurvePoint(3,4)


def ajustePosOneCurvePoint(numLocator,numPoint):
    t=position(locator(numLocator))
    cmds.select(curvei(numPoint))
    cmds.move(t[0],t[1],t[2])

def placeAnglesCalcules(sliderList,nBoucles):
    #compression=angleLoc("CompHB")
    #compressionGD=angleLoc("CompGD")

    #angleCervicales=angleLoc("CHB")
    #angleCervicalesGD=angleLoc("CGD")
    #angleTete=angleLoc("THB")
    #angleTeteGD=angleLoc("TGD")

    #angleLombaires=angleLoc("LHB")
    #angleLombairesGD=angleLoc("LGD")

    #posture=getPostureLoc()
    #orientation=getOrientationLoc()
    #pos=getPositionLoc()

    oldParamC=getParameter(position(curvei(5)))
    oldParamD=getParameter(position(curvei(3)))
    param=calcCVParameters()

    setAngle(sliderList,"Orientation")
    setAngle(sliderList,"Length")
    setAngle(sliderList,"X")
    setAngle(sliderList,"Y")
    setAngle(sliderList,"Z")

    # on place d'abord les angles GD -> plus facile a placer maintenant
    locatorList=map(position,[locator(i) for i in range(6)])

    t=time.time()
    #print "TLEN",getTLen()
    for i in range(1):#nBoucles):
            corr(sliderList,"LGD")
            corr(sliderList,"CompGD")
            corr(sliderList,"CGD")
            corr(sliderList,"TGD")

    print "apres GD",time.time()-t
    t=time.time()
    #print "TLEN",getTLen(),getLLen()

    for i in range(1):#nBoucles):

        setAngle(sliderList,"CompHB")
        #print "TLEN1",getTLen(),getLLen()
        setAngle(sliderList,"LHB")
        #print "TLEN2",getTLen(),getLLen()
        setAngle(sliderList,"CHB")
        #print "TLEN3",getTLen(),getLLen()
        setAngle(sliderList,"THB")

    #print "apres setRot",time.time()-t
    #t=time.time()

    #setAngle("orientation",orientation)
    setAngle(sliderList,"Length")
    setAngle(sliderList,"X")
    setAngle(sliderList,"Y")
    setAngle(sliderList,"Z")

    #print "apres fin",time.time()-t
    #t=time.time()

def Correction(sliderList):
    locatorList=map(position,[locator(i) for i in range(6)])

    ##t=time.time()

    for _ in range(2):
            translateToLocator(0)
            translateToLocator(2)
            setAngle(sliderList,"Length")

    #correctionRot(sliderGrp,sliderGrp.string2num("compression g"),3,False)
    corr(sliderList,"CompGD",nMax=10)
    corr(sliderList,"LGD",nMax=10)
    corr(sliderList,"CGD",nMax=10)
    corr(sliderList,"TGD",nMax=10)



            # on translate la courbe pour que la courbe coincide parfaitement au niveau des lombaires
    #for i in range(0):
    #    setAngle("scale",ScaleFactor())
    #    translateToCV(0,0)
    ### on translate la courbe pour qu'elle repasse par le localisateur milieu
    #    translateToLocator(2)
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

    # on translate la courbe pour que la courbe coincide parfaitement au niveau des lombaires
    for i in range(1):
        for _ in range(2):
            translateToCV(0,0)
    #        ### on translate la courbe pour qu'elle repasse par le localisateur milieu
            translateToLocator(2)
            setAngle(sliderList,"Length")
        for _ in range(1):
            corr(sliderList,"LGD",nMax=5)
            corr(sliderList,"LHB",nMax=5)
        for _ in range(1):
            corr(sliderList,"CompGD",nMax=5)
            corr(sliderList,"CompHB",nMax=5)
        for _ in range(2):
            corr(sliderList,"CGD",nMax=5)
            corr(sliderList,"CHB",nMax=5)
            corr(sliderList,"TGD",nMax=5)
            corr(sliderList,"THB",nMax=5)

    for _ in range(1):
        translateToLocator(0)
        translateToLocator(2)
        #translateToLocator(4)
        #translateToLocator(2)
        #translateToLocator(0)
        #translateToLocator(2)

        #print "apres corr",time.time()-t
    #t=time.time() 


    for i in range(3):
        #translateToCV(6,4)
        translateToLocator(4)
        translateToLocator(3)
        setAngle(sliderList,"Length") # TODO!!!!! CPOC
    ### on translate la courbe pour qu'elle repasse par le localisateur milieu
 # autre locator reference ?
        #for _ in range(1):
        #    translateToLocator(2)
        #    corr(sliderGrp.sliderList,"CompGD")
        #    corr(sliderGrp.sliderList,"CompHB")
        #for _ in range(1):
        #    corr(sliderGrp.sliderList,"LGD")
        #    corr(sliderGrp.sliderList,"LHB")
        #for i in range(2):
        #    corr(sliderGrp.sliderList,"CGD",nMax=5)
        #    corr(sliderGrp.sliderList,"CHB",nMax=5)
        #    corr(sliderGrp.sliderList,"TGD",nMax=5)
        #    corr(sliderGrp.sliderList,"THB",nMax=5)

    #for i in range(1):
    #    for _ in range(2):
    #        translateToCV(0,0)
    #        translateToLocator(2)
    #        setAngle("scale",ScaleFactorCPOC())
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
        #    translateToLocator(3)
        #    translateToLocator(2)
        #    translateToLocator(4) 
        #    translateToLocator(2)
        #    translateToLocator(1)
        #    translateToLocator(2)

            #translateToLocator(3)
            #translateToLocator(2)

        t=time.time()

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

 
def isSet():
    res=0
    res+=cmds.getAttr('posCV.pos0X')+cmds.getAttr('posCV.pos1X')+cmds.getAttr('posCV.pos1X')
    return res!=0


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

        
    # on enregistre les positions des points de contrôle
    for i in range(maxCV()):
        pos=position(curvei(i))
        cmds.setAttr('posCV.pos'+str(i)+'X',pos[0])
        cmds.setAttr('posCV.pos'+str(i)+'Y',pos[1])
        cmds.setAttr('posCV.pos'+str(i)+'Z',pos[2])
        mel.eval('setKeyframe { "posCV.pos'+str(i)+'" };')

def Placement(length,CVpos,jtPos,save=True,evaluate=True):
    resetCurve(length,CVpos,jtPos)
    placeAnglesCalcules(sliderGrp.sliderList,1)
    Correction(sliderGrp.sliderList)
    if save:
        saveKeys()
    if evaluate:
        a=Evaluate()
        evaluation=a.execute()


maxCV = MaxCV
sliderGrp=mainFct(pointOnCurveList,locatorList)
droites=sliderGrp.droites
par=calcCVParameters() 
CVpos=calcPosCV()
jtPos=JointPositions()
jtParam=JointParameters()
length=getLength()

#setAllCurves()
for i in range(0,1):
    t=time.time()
    cmds.currentTime(90, edit=True )
    sliderGrp=mainFct(pointOnCurveList,locatorList,reset=True,droites=droites)
    checkParameters(par,CVpos,jtPos,jtParam)
    Placement(length,CVpos,jtPos)

    print "time",time.time()-t
cmds.select('locatorAngle1')
cmds.hide()


   
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