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

def resetCurve(sliderGrp,length,pos,jtPos):
    keepLengthValue(length)     
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

def calcPosRelatifHB(locator,Cote="",nLocator=-1):
    orientation=calcOrientation(Cote)
    parLocOnCurve=getParameter(locator)
    locatorOnCurve=getPoint(parLocOnCurve)

    vect=sub(locator,locatorOnCurve)
    vectProj=projPlanPosture3D(locatorOnCurve,locator,Cote)
    vectProj2D=projPlanPosture2D(locatorOnCurve,locator,Cote)
    #print "proj2Dvect",vectProj2D
    #vectAngle=angleHB(vectProj) 

    tan=normalize(getTangent(locatorOnCurve))
    if np.dot(projHor(tan),projHor(PostureVector(Cote="")))<0:
        print "recul"
    #print "dot",projHor(tan),projHor(PostureVector(Cote="")),projHor(PostureVector(Cote=Cote)),np.dot(projHor(tan),projHor(PostureVector(Cote=""))),np.dot(projHor(tan),projHor(PostureVector(Cote=Cote)))
    if nLocator==0:
        tan=pdt(-1,tan)
    tanProj=projPlanPosture3D(locatorOnCurve,sum(locatorOnCurve,tan),Cote)
    tanProj2D=projPlanPosture2D(locatorOnCurve,sum(locatorOnCurve,tan),Cote)
    #print "proj2Dtan",tanProj2D,angle2D(vectProj2D,tanProj2D)
    #tanAngle=angleHB(tanProj)
    #print "angles",valPrincDeg(tanAngle-vectAngle),angleHB2V(vectProj,tanProj)

    #p("vectProj3D2D",projPlanPosture3D(locatorOnCurve,sum(locatorOnCurve,tan),Cote))
    #p("locOn",locatorOnCurve,vectProj,tanProj,"finTan",str(sum(locatorOnCurve,tanProj)))
    #p("vect",str(vectAngle),"tan",str(tanAngle),"angle",str(angleHB2V(vectProj,tanProj)),str(valPrincDeg(tanAngle-vectAngle)))

    # angle du locator vers la courbe
    angle=angle2D(vectProj2D,tanProj2D) #angleHB2V(vectProj,tanProj)
    if angle<0:
        string="courbe dessous"
    else:
        string="courbe dessus"

    return [angle,norm(vectProj)*angle/100.0,string]
    return [valPrincDeg(tanAngle-vectAngle),norm(vectProj),string]

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
def correctionRot(sliderGrp,nButton,nLocator,Croiss=True,precision=10,Cote=""):
    locatorP=position(locator(nLocator))
    f = calcPosRelatifHB if nButton%2==sliderGrp.string2num("rotCHB")%2  else calcPosRelatifGD
    distI=norm(sub(locatorP,getPoint(getParameter(locatorP))))
    dist=distI
    button=sliderGrp.buttonList[nButton]
    slider=button.slider
    valInit=slider.sliderValue()
    minSlider=slider.minValue
    maxSlider=slider.maxValue
    relatif=1
    maxi=min(valInit+dist*0.2*(slider.maxValue-slider.minValue),maxSlider)
    mini=max(valInit-dist*0.2*(slider.maxValue-slider.minValue),minSlider)
    i=0
    while i<precision and abs(relatif)>0.01:
        i+=1
        testV=(mini+maxi)/2
        #print "mini",mini,maxi,testV
        slider.setValue(testV)
        slider.update()
        [relatif,dist,str]=f(locatorP,Cote=Cote,nLocator=nLocator)
        if (relatif<0 and Croiss) or (relatif>0 and (not Croiss)):
            maxi=testV
        else:
            mini=testV 
    if distI<dist:
        slider.setValue(valInit)
        slider.update()
        p("correctionRot failed",slider.label)
    

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



def translateToCV(numCV,numLocator):
    posCV=nearestPoint(curvei(numCV))
    posLoc=position(locator(numLocator))
    diff=sub(posLoc,posCV)
    select('curve1')
    cmds.move(diff[0],diff[1],diff[2],r=True)

def translateToLocator(numLocator):
    posLoc=position(locator(numLocator))
    posLocOnCurve=nearestPoint(locator(numLocator))
    t=sub(posLoc,posLocOnCurve)
    select('curve1')
    cmds.move(t[0],t[1],t[2],r=True)

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

#def calcAngleDorsalesLocator():
#    v1=sub(position(locator(0)),position(locator(1)))
#    v2=sub(position(locator(2)),position(locator(1)))
#    print angleHB(v1,v2)

#def calcAngleDorsales():
#    v1=sub(position(curvei(1)),position(curvei(2)))
#    v2=sub(position(curvei(3)),position(curvei(2)))
#    print angleHB(v1,v2)


def placeAnglesCalcules(sliderGrp,nBoucles):
    compression=angleCompLoc()
    compressionGD=angleCompGDLoc()

    angleCervicales=angleCHBLoc()
    angleCervicalesGD=angleCGDLoc()
    angleTete=angleTHB()
    angleTeteGD=angleTGD()

    angleLombaires=angleLHBLoc()
    angleLombairesGD=angleLGDLoc()

    posture=locatorPosture()
    orientation=locatorOrientation()
    pos=getLocatorCurvePosition()

    oldParamC=getParameter(position(curvei(5)))
    oldParamD=getParameter(position(curvei(3)))
    param=calcCVParameters()

    sliderGrp.do("orientation",orientation)
    sliderGrp.do("scale",ScaleFactor())
    sliderGrp.do("x",pos[0])
    sliderGrp.do("y",pos[1])
    sliderGrp.do("z",pos[2])

    # on place d'abord les angles GD -> plus facile a placer maintenant
    locatorList=map(position,[locator(i) for i in range(6)])

    t=time.time()

    for i in range(1):#nBoucles):
            correctionRot(sliderGrp,sliderGrp.string2num("rotLGD"),0,True)#True
            correctionRot(sliderGrp,sliderGrp.string2num("compression g"),3,False)
            correctionRot(sliderGrp,sliderGrp.string2num("rotCGD"),4,False)
            correctionRot(sliderGrp,sliderGrp.string2num("rotTGD"),5,False)


    #print "apres GD",time.time()-t
    t=time.time()

    t=time.time()
    for i in range(nBoucles):
        #print "vant omp",getCLen(),getTLen()
        sliderGrp.do("compression",compression)
        #print getCLen(),getTLen()
        sliderGrp.do("rotLHB",angleLombaires) 
        sliderGrp.do("rotCHB",angleCervicales)  

        #correctionRot(sliderGrp,sliderGrp.string2num("compression g"),locatorList[3],False)
        #correctionRot(sliderGrp,sliderGrp.string2num("rotLGD"),locatorList[0],True)
        #correctionRot(sliderGrp,sliderGrp.string2num("rotCGD"),locatorList[4],False)
        #correctionRot(sliderGrp,sliderGrp.string2num("rotTGD"),locatorList[5],False)
        #sliderGrp.do("compression g",compressionGD)
        #sliderGrp.do("rotLGD",angleLombairesGD) 
        #sliderGrp.do("rotCGD",angleCervicalesGD)  
        # on place la tete que a la fin par meilleur passage, sinon prochaine rotation cervicale va tout bousiller -> TODO ameliorer ce probleme
        #sliderGrp.do("rotTHB",angleTete)
        #sliderGrp.do("rotTGD",angleTeteGD)


    print "apres nBGD",time.time()-t
    t=time.time()

    sliderGrp.do("orientation",orientation)
    sliderGrp.do("scale",ScaleFactor())
    sliderGrp.do("x",pos[0])
    sliderGrp.do("y",pos[1])
    sliderGrp.do("z",pos[2])

    print "apres fin",time.time()-t
    t=time.time()

def Correction(sliderGrp):
    locatorList=map(position,[locator(i) for i in range(6)])

    for i in range(2):
        sliderGrp.do("scale",ScaleFactor())

        ##t=time.time()


        for _ in range(1):
                translateToLocator(0)
                translateToLocator(2)
                translateToLocator(4)
                translateToLocator(2)
                translateToLocator(0)
                translateToLocator(2)


        correctionRot(sliderGrp,sliderGrp.string2num("compression g"),3,False)
        correctionRot(sliderGrp,sliderGrp.string2num("rotLGD"),0,True)
        correctionRot(sliderGrp,sliderGrp.string2num("rotCGD"),4,False)
        correctionRot(sliderGrp,sliderGrp.string2num("rotTGD"),5,False)


                # on translate la courbe pour que la courbe coincide parfaitement au niveau des lombaires
        #for i in range(0):
        #    sliderGrp.do("scale",ScaleFactor())
        #    translateToCV(0,0)
        ### on translate la courbe pour qu'elle repasse par le localisateur milieu
        #    translateToLocator(2)
        #    correctionRot(sliderGrp,sliderGrp.string2num("rotLGD"),0,True)
        #    correctionRot(sliderGrp,sliderGrp.string2num("compression g"),3,False)
        #    correctionRot(sliderGrp,sliderGrp.string2num("rotCGD"),4,False)
        #    correctionRot(sliderGrp,sliderGrp.string2num("rotLHB"),0,True)
        #    correctionRot(sliderGrp,sliderGrp.string2num("compression"),3)

        #    correctionRot(sliderGrp,sliderGrp.string2num("rotCHB"),4,False)
        #    correctionRot(sliderGrp,sliderGrp.string2num("rotTGD"),5,False)
        #    correctionRot(sliderGrp,sliderGrp.string2num("rotTHB"),5,False)

        #print "apres translate",time.time()-t
        #t=time.time()

        # on translate la courbe pour que la courbe coincide parfaitement au niveau des lombaires
        for i in range(1):
            sliderGrp.do("scale",ScaleFactor())
            translateToCV(0,0)
        ### on translate la courbe pour qu'elle repasse par le localisateur milieu
            translateToLocator(2)
            for _ in range(1):
                correctionRot(sliderGrp,sliderGrp.string2num("compression g"),3,False)
                correctionRot(sliderGrp,sliderGrp.string2num("compression"),3)
            for _ in range(1):
                correctionRot(sliderGrp,sliderGrp.string2num("rotLGD"),0,True,Cote="L")
                correctionRot(sliderGrp,sliderGrp.string2num("rotLHB"),0,False,Cote="L")
            for i in range(2):
                correctionRot(sliderGrp,sliderGrp.string2num("rotCHB"),4,False,Cote="C")
                correctionRot(sliderGrp,sliderGrp.string2num("rotTHB"),5,False,Cote="C")
                correctionRot(sliderGrp,sliderGrp.string2num("rotCGD"),4,False,Cote="C")
                correctionRot(sliderGrp,sliderGrp.string2num("rotTGD"),5,False,Cote="C")

        #print "apres corr",time.time()-t
        #t=time.time() 



        #for i in range(1):
        #    sliderGrp.do("scale",ScaleFactor())
        #    translateToCV(6,4)
        ### on translate la courbe pour qu'elle repasse par le localisateur milieu
        #    translateToLocator(2) # autre locator reference ?
        #    for _ in range(2):
        #        correctionRot(sliderGrp,sliderGrp.string2num("compression g"),3,False)
        #        correctionRot(sliderGrp,sliderGrp.string2num("compression"),3)
        #    for _ in range(2):
        #        correctionRot(sliderGrp,sliderGrp.string2num("rotLGD"),0,True)
        #        correctionRot(sliderGrp,sliderGrp.string2num("rotLHB"),0,True)
        #    translateToLocator(3) # autre locator reference ?
        #    for i in range(2):
        #        correctionRot(sliderGrp,sliderGrp.string2num("rotCGD"),4,False)
        #        correctionRot(sliderGrp,sliderGrp.string2num("rotCHB"),4,False)

        print getCLen(),getTLen()

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
    angleNames=['angleCHB','angleDHB','angleLHB','angleCGD','angleDGD','angleLGD','Posture','Orientation','x','y','z','angleComp','angleCompGD']
    getFunctionNames=[angleCHB,angleDHB,angleLHB,angleCGD,angleDGD,angleLGD,calcPosture,calcOrientation,getX,getY,getZ,angleComp,angleCompGD]
    for angleName,getFunctionName in zip(angleNames,getFunctionNames):
        value=getFunctionName()
        cmds.setAttr('ValeurAngles.'+angleName,value)
        mel.eval('setKeyframe { "ValeurAngles.'+angleName+'" };')
        
    # on enregistre les positions des points de contrôle
    for i in range(maxCV()):
        pos=position(curvei(i))
        cmds.setAttr('posCV.pos'+str(i)+'X',pos[0])
        cmds.setAttr('posCV.pos'+str(i)+'Y',pos[1])
        cmds.setAttr('posCV.pos'+str(i)+'Z',pos[2])
        mel.eval('setKeyframe { "posCV.pos'+str(i)+'" };')


maxCV = MaxCV
sliderGrp=mainFct(pointOnCurveList,locatorList)
droites=sliderGrp.droites
par=calcCVParameters() 
CVpos=calcPosCV()
jtPos=JointPositions()
jtParam=JointParameters()
length=getCurveLength()

#setAllCurves()
for i in range(0,1):
    t=time.time()
    cmds.currentTime(160, edit=True )
    resetCurve(sliderGrp,length,CVpos,jtPos)
    sliderGrp=mainFct(pointOnCurveList,locatorList,reset=True,droites=droites)
    checkParameters(par,CVpos,jtPos,jtParam,printOK=False)
    placeAnglesCalcules(sliderGrp,1)
    Correction(sliderGrp)
    saveKeys()
    a=Evaluate()
    evaluation=a.execute()
    #p("pos finale CV",calcPosCV())
    #p("pos finale Joints",JointPositions())
    print "time",time.time()-t
cmds.select('locatorAngle1')
cmds.hide()


   











    
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
    #sliderGrp.do("courbure l",lordoseC)        
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