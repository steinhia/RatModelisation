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
    cmds.select("curve1")
    cmds.move(subPos[0],subPos[1],subPos[2],r=True)

def calcPosRelatifHB(locator):
    locatorOnCurve=getPoint(getParameter(locator))
    tan=getTangent(locatorOnCurve)
    vect=sub(locatorOnCurve,locator)
    #p("locOn",locatorOnCurve)
    #if vect[1]<0:
    #    p("courbe dessous")
    #else:
    #    p("courbe dessus")
    return [vect[1],norm(vect)]

def calcPosRelatifGD(locatorPosition):
    locatorOnCurve=getPoint(getParameter(locatorPosition))
    tan=getTangent(locatorOnCurve)
    vect=sub(locatorOnCurve,locatorPosition)
    return [angleGD(tan,vect),norm(vect)]

def correctionRot(sliderGrp,nButton,locator,Croiss=True,precision=10):
    f = calcPosRelatifHB if nButton%2==sliderGrp.string2num("rot c")%2  else calcPosRelatifGD
    [relatif,dist]=f(locator)
    button=sliderGrp.buttonList[nButton]
    slider=button.slider
    valInit=slider.sliderValue()
    minSlider=slider.minValue
    maxSlider=slider.maxValue
    if (relatif<0 and Croiss) or (relatif>0 and (not Croiss)) :
        maxi=min(valInit,maxSlider)
        mini=max(valInit-dist*(slider.maxValue-slider.minValue),minSlider)
    else:
        mini=max(valInit,minSlider)
        maxi=min(valInit+dist*(slider.maxValue-slider.minValue),maxSlider)
    i=0
    #p("mini",mini,maxi,relatif)
    while abs(relatif)>0.0001 and i<precision:
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

def translateToCV(numCV,numLocator):
    posCV=nearestPoint(curvei(numCV))
    posLoc=position(locator(numLocator))
    diff=sub(posLoc,posCV)
    cmds.select('curve1')
    cmds.move(diff[0],diff[1],diff[2],r=True)

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
    
    angleDorsales=angleDHBLoc()
    angleDorsalesGD=angleDGDLoc()

    angleLombaires=angleLHBLoc()
    angleLombairesGD=angleLGDLoc()

    posture=locatorPosture()
    orientation=locatorOrientation()
    pos=getLocatorCurvePosition()

    oldParamC=getParameter(position(curvei(5)))
    oldParamD=getParameter(position(curvei(3)))
    param=calcCVParameters()

    for i in range(nBoucles):
        sliderGrp.do("posture",posture)

        #print calcCVParameters() 
        sliderGrp.do("compression",compression)
        sliderGrp.do("compression g",compressionGD)
        sliderGrp.do("rot dorsale",angleDorsales)
        sliderGrp.do("rot dorsale g ",angleDorsalesGD)
        sliderGrp.do("rot cervicale",angleCervicales)  
        sliderGrp.do("rot cervicale g",angleCervicalesGD)  
        sliderGrp.do("rot t",angleTete)
        sliderGrp.do("rot tete g",angleTeteGD)
        sliderGrp.do("rot lombaire",angleLombaires) 
        sliderGrp.do("rot lombaire GD",angleLombairesGD) 
        
    sliderGrp.do("orientation",orientation)
    sliderGrp.do("posture",posture)
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
    for i in range(1):
        scaleFactor=locatorLength()/locatorCurveLength()*getCurveLength()
        sliderGrp.do("scale",scaleFactor)
        #correctionPos(sliderGrp,5,position("locatorC"))

        #compression
        correctionRot(sliderGrp,sliderGrp.string2num("compression"),locatorList[3])
        correctionRot(sliderGrp,sliderGrp.string2num("compression gd"),locatorList[3])

        #dorsales
        correctionRot(sliderGrp,sliderGrp.string2num("rot dorsale"),locatorList[1])
        correctionRot(sliderGrp,sliderGrp.string2num("rot dorsale gd"),locatorList[1])

        #lombaires
        correctionRot(sliderGrp,sliderGrp.string2num("rot lombaire"),locatorList[0],True)
        correctionRot(sliderGrp,sliderGrp.string2num("rot lombaire gd"),locatorList[0])

        ##cervicales
        #correctionRot(sliderGrp,sliderGrp.string2num("rot c"),locatorList[4],False)
        #correctionRot(sliderGrp,sliderGrp.string2num("rot cervicale gd"),locatorList[4],False)

        ##tete
        #correctionRot(sliderGrp,sliderGrp.string2num("rot t"),locatorList[5],False)
        #correctionRot(sliderGrp,sliderGrp.string2num("rot tete gd"),locatorList[5],False)



    #for i in range(2):
        scaleFactor=locatorLength()/locatorCurveLength()*getCurveLength()
        sliderGrp.do("scale",scaleFactor)
        #translateToCV(4,3)    
        ##sliderGrp.do("compression",compression)
        ##correctionRot(sliderGrp,sliderGrp.string2num("compression"),locatorList[3])
        #correctionRot(sliderGrp,sliderGrp.string2num("rot dorsale"),locatorList[1])
        #correctionRot(sliderGrp,sliderGrp.string2num("rot lombaire"),locatorList[0],True)
        #correctionRot(sliderGrp,sliderGrp.string2num("rot c"),locatorList[4],False)
        #correctionRot(sliderGrp,sliderGrp.string2num("rot t"),locatorList[5],False)

    ##    translateToCV(7,5)    
    ##    correctionRot(sliderGrp,sliderGrp.string2num("compression"),locatorList[3])
    ##    correctionRot(sliderGrp,sliderGrp.string2num("rot dorsale"),locatorList[1])
    ##    correctionRot(sliderGrp,sliderGrp.string2num("rot lombaire"),locatorList[0],True)
    ##    correctionRot(sliderGrp,sliderGrp.string2num("rot c"),locatorList[4],False)
    ##    correctionRot(sliderGrp,sliderGrp.string2num("rot t"),locatorList[5],False)

        translateToCV(0,0)
        sliderGrp.do("compression",compression)
        correctionRot(sliderGrp,sliderGrp.string2num("rot c"),locatorList[4],False)
        correctionRot(sliderGrp,sliderGrp.string2num("rot t"),locatorList[5],False)
        correctionRot(sliderGrp,sliderGrp.string2num("rot dorsale"),locatorList[2])
        #correctionRot(sliderGrp,sliderGrp.string2num("compression"),locatorList[3])
        correctionRot(sliderGrp,sliderGrp.string2num("rot lombaire"),locatorList[0],True)







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

    p("duree placage : "+str(time.time()-t))      
    #p("param debut",param) 
    a=Evaluate()
    evaluation=a.execute()
    return evaluation
    


maxCV = cmds.getAttr("curve1.spans")+cmds.getAttr("curve1.degree")
for i in range(0,1):
    j=0
    sliderGrp=mainFct(pointOnCurveList,locatorList)
    cmds.currentTime(j, edit=True )
    placementManuel(1) 
#    string='setKeyframe -breakdown 0 -hierarchy none -controlPoints 1 -shape 0 {"curve1"};'
#    #mel.eval(string)
#    for j in range(maxCV):
#        string='setKeyframe -breakdown 0 -hierarchy none -controlPoints 0 -shape 0 -i {"curve1.cv['+str(j)+']"};'
#        mel.eval(string)
#param=calcCVParameters()
    angleNames=['angleCHB','angleDHB','angleLHB','angleCGD','angleDGD','angleLGD','Posture','Orientation','x','y','z','angleComp','angleCompGD']
    getFunctionNames=[angleCHB,angleDHB,angleLHB,angleCGD,angleDGD,angleLGD,calcPosture,calcOrientation,getX,getY,getZ,angleComp,angleCompGD]
    for angleName,getFunctionName in zip(angleNames,getFunctionNames):
        value=getFunctionName()
        cmds.setAttr('ValeurAngles.'+angleName,value)
        mel.eval('setKeyframe { "ValeurAngles.'+angleName+'" };')
    
#p("param fin",param)
        
EvalPositionLocator2()
#print param
#print calcCVParameters()



 