# -*- coding: utf-8 -*-
import sys
sys.path.append("C:/Users/alexandra/Documents/alexandra/scripts")
import time
import maya.mel as mel
import inspect

path="C:/Users/alexandra/Documents/alexandra/scripts/"
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
    #for button in sliderGrp.buttonList[:12]:
    #    button.slider.setValue(0)
    #    button.slider.update(True)
        
    for i,posi in enumerate(pos):
        cmds.select(curvei(i))
        cmds.move(posi[0],posi[1],posi[2])
    for i,posj in enumerate(jtPos):
        cmds.select('joint'+str(i+1))
        cmds.move(posj[0],posj[1],posj[2])

    #p("crv",calcParameters()[1])

def calcPosCV():
    pos=[]
    for i in range(MaxCV()):
        pos.append(position(curvei(i)))
    return pos

# c'etait mieux quand on calculait l'angle
# angle marche au bout -> mais pas bon avec l'orientation
def calcPosRelatifHB(locator):
    locatorOnCurve=getPoint(getParameter(locator))
    tan=getTangent(locatorOnCurve)
    vect=sub(locator,locatorOnCurve)
    #p("locOn",locatorOnCurve,vect,tan)
    #if angleHB2DWithSign(vect)-angleHB2DWithSign(tan)<0:
    #    p("courbe dessous")
    #else:
    #    p("courbe dessus")
    #p(str(angleHB2D(vect)),str(angleHB2D(tan)))
    #p(vect)
    #return [vect[1],norm(vect)]
    #s= 1 if abs(calcOrientation())>90 else 1
    return [angleHB2DWithSign(tan)-angleHB2DWithSign(vect),norm(vect)]

def calcPosRelatifGD(locatorPosition):
    locatorOnCurve=getPoint(getParameter(locatorPosition))
    tan=getTangent(locatorOnCurve)
    vect=sub(locatorOnCurve,locatorPosition)
    return [angleGD(tan,vect),norm(vect)]

def correctionRot(sliderGrp,nButton,locator,Croiss=True,precision=10):
    f = calcPosRelatifHB if nButton%2==sliderGrp.string2num("rot c")%2  else calcPosRelatifGD
    [relatif,dist]=f(locator)
    distI=dist
    button=sliderGrp.buttonList[nButton]
    slider=button.slider
    valInit=slider.sliderValue()
    minSlider=slider.minValue
    maxSlider=slider.maxValue
    if (relatif<0 and Croiss) or (relatif>0 and (not Croiss)) :
        maxi=min(valInit,maxSlider)
        mini=max(valInit-dist*2*(slider.maxValue-slider.minValue),minSlider)
    else:
        mini=max(valInit,minSlider)
        maxi=min(valInit+dist*2*(slider.maxValue-slider.minValue),maxSlider)
    i=0
    #p("mini",mini,maxi,relatif)
    while abs(relatif)>0.01 and i<precision:
        #p("i",i,relatif)
        i+=1
        test=(mini+maxi)/2
        slider.setValue(test)
        slider.update()
        [relatif,dist]=f(locator)
        #p("i",i,relatif)
        if (relatif<0 and Croiss) or (relatif>0 and (not Croiss)):
            maxi=test
        else:
            mini=test   
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

def calcAngleDorsalesLocator():
    v1=sub(position(locator(0)),position(locator(1)))
    v2=sub(position(locator(2)),position(locator(1)))
    print angleHB(v1,v2)

def calcAngleDorsales():
    v1=sub(position(curvei(1)),position(curvei(2)))
    v2=sub(position(curvei(3)),position(curvei(2)))
    print angleHB(v1,v2)

#53 ou 83 selon pendant ou avant
def placementManuel(nBoucles=3):
    t=time.time()
    compression=angleCompLoc()
    compressionGD=angleCompGDLoc()

    angleCervicales=angleCHBLoc()
    angleCervicalesGD=angleCGDLoc()
    angleTete=angleTHB()
    angleTeteGD=angleTGD()
    
    #angleDorsales=angleDHBLoc()
    #angleDorsalesGD=angleDGDLoc()

    angleLombaires=angleLHBLoc()
    angleLombairesGD=angleLGDLoc()

    posture=locatorPosture()
    orientation=locatorOrientation()
    pos=getLocatorCurvePosition()

    oldParamC=getParameter(position(curvei(5)))
    oldParamD=getParameter(position(curvei(3)))
    param=calcCVParameters()

    for i in range(nBoucles):
        1# ne pas utiliser sliderGrp.do("posture",posture)
        sliderGrp.do("compression",compression)
        sliderGrp.do("compression g",compressionGD)
            #sliderGrp.do("rot dorsale",angleDorsales)
            #sliderGrp.do("rot dorsale g ",angleDorsalesGD)
        sliderGrp.do("rot cervicale",angleCervicales)  
        #sliderGrp.do("rot cervicale g",angleCervicalesGD)  
        # on place la tete que a la fin par meilleur passage, sinon prochaine rotation cervicale va tout bousiller -> TODO ameliorer ce probleme
        #sliderGrp.do("rot t",angleTete)
        #sliderGrp.do("rot tete g",angleTeteGD)
        sliderGrp.do("rot lombaire",angleLombaires) 
        sliderGrp.do("rot lombaire GD",angleLombairesGD) 
        
    sliderGrp.do("orientation",orientation)
    #ne pas utiliser sliderGrp.do("posture",posture)
    scaleFactor=locatorLength()/locatorCurveLength()*getCurveLength()
    sliderGrp.do("scale",scaleFactor)
    sliderGrp.do("x",pos[0])
    sliderGrp.do("y",pos[1])
    sliderGrp.do("z",pos[2])

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

    locatorList=map(position,[locator(i) for i in range(6)])
    for i in range(2):
        scaleFactor=locatorLength()/locatorCurveLength()*getCurveLength()
        #sliderGrp.do("scale",scaleFactor)

        #compression
        #correctionRot(sliderGrp,sliderGrp.string2num("compression"),locatorList[3])
        #correctionRot(sliderGrp,sliderGrp.string2num("compression gd"),locatorList[3],False)

        ##dorsales
        ##correctionRot(sliderGrp,sliderGrp.string2num("rot dorsale"),locatorList[1])
        ##correctionRot(sliderGrp,sliderGrp.string2num("rot dorsale gd"),locatorList[1])

        ###lombaires
        #correctionRot(sliderGrp,sliderGrp.string2num("rot lombaire"),locatorList[0],precision=10)
        #correctionRot(sliderGrp,sliderGrp.string2num("rot lombaire gd"),locatorList[0])

        ##cervicales
        #correctionRot(sliderGrp,sliderGrp.string2num("rot c"),locatorList[4],False)
        #correctionRot(sliderGrp,sliderGrp.string2num("rot cervicale gd"),locatorList[4],False)

        #tete
        #correctionRot(sliderGrp,sliderGrp.string2num("rot t"),locatorList[5],False)
        #correctionRot(sliderGrp,sliderGrp.string2num("rot tete gd"),locatorList[5],False)



    for i in range(2):
        scaleFactor=locatorLength()/locatorCurveLength()*getCurveLength()
        #sliderGrp.do("scale",scaleFactor)

        # on translate la courbe pour que la courbe coincide parfaitement au niveau des lombaires
        # a la fin, la courbe ne passera peut etre plus par le localisateur
        #sliderGrp.do("rot lombaire",angleLombaires) 
        for i in range(2):
            translateToCV(0,0)
        ## du coup on translate la courbe pour qu'elle repasse par le localisateur milieu, mais pas nécessairement
            translateToLocator(2)
            #correctionRot(sliderGrp,sliderGrp.string2num("compression"),locatorList[3])
            #correctionRot(sliderGrp,sliderGrp.string2num("compression g"),locatorList[3])
            correctionRot(sliderGrp,sliderGrp.string2num("rot lombaire"),locatorList[0],True)
            correctionRot(sliderGrp,sliderGrp.string2num("rot lombaire g"),locatorList[0],True)
            correctionRot(sliderGrp,sliderGrp.string2num("rot c"),locatorList[4],False)
        # une fois qu'on a trouvé le meilleur point, recalcule les angles ?? hehehe
        for i in range(2):
            translateToCV(6,4)
        ## du coup on translate la courbe pour qu'elle repasse par le localisateur milieu, mais pas nécessairement
            translateToLocator(2)
            #correctionRot(sliderGrp,sliderGrp.string2num("compression"),locatorList[3])
            #correctionRot(sliderGrp,sliderGrp.string2num("compression g"),locatorList[3])

            #correctionRot(sliderGrp,sliderGrp.string2num("rot lombaire g"),locatorList[0],True)
            correctionRot(sliderGrp,sliderGrp.string2num("rot c"),locatorList[4],False)
            correctionRot(sliderGrp,sliderGrp.string2num("rot lombaire"),locatorList[0],True)

            #translateToLocator(3)
            #translateToLocator(2)

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
    #a=Evaluate()
    evaluation=1#a.execute()
    cmds.select(clear=True)
    return evaluation
    

maxCV = MaxCV

sliderGrp=mainFct(pointOnCurveList,locatorList)

par=calcCVParameters() 
CVpos=calcPosCV()
jtPos=JointPositions()
jtParam=JointParameters()
length=getCurveLength()

for i in range(0,1):
    j=60
    cmds.currentTime(j, edit=True )
    #resetCurve(sliderGrp,length,CVpos,jtPos)
    #sliderGrp=mainFct(pointOnCurveList,locatorList,reset=True)
    #checkParameters(par,CVpos,jtPos,jtParam)
    placementManuel(1) 
    #p("pos finale CV",calcPosCV())
    #p("pos finale Joints",JointPositions())


   

    # setKey 
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
        
    cmds.select('locatorAngle1')
    cmds.hide()

    
#p("param fin",param)
        
#EvalPositionLocator2()
#print param
#print calcCVParameters()



 