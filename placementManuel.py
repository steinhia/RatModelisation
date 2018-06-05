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
    return [angleHB(tan,vect),norm(vect)]

def calcPosRelatifGD(locatorPosition):
    locatorOnCurve=getPoint(getParameter(locatorPosition))
    tan=getTangent(locatorOnCurve)
    vect=sub(locatorOnCurve,locatorPosition)
    return [angleGD(tan,vect),norm(vect)]

def correctionRot(sliderGrp,nButton,locator,Croiss=True,precision=10):
    f = calcPosRelatifHB if nButton%2==sliderGrp.string2num("rot c")%2  else calcPosRelatifGD
    [angle,dist]=f(locator)
    slider=sliderGrp.buttonList[nButton].slider
    valInit=slider.sliderValue()
    minSlider=slider.minValue
    #p("minSlider",minSlider)
    maxSlider=slider.maxValue
    #p("maxSlider",maxSlider)
    #bool = nButton not in [3,8,0,1,4]
    # compression et cervicales dans l'autre sens
    if (angle>0 and Croiss) or (angle<0 and (not Croiss)):
        maxi=min(valInit,maxSlider)
        mini=max(valInit-3*dist*(slider.maxValue-slider.minValue),minSlider)
    else:
        mini=max(valInit,minSlider)
        maxi=min(valInit+3*dist*(slider.maxValue-slider.minValue),maxSlider)
    i=0
    #p("mi",mini,maxi)
    while dist>0.01 and i<precision:
        i+=1
        test=(mini+maxi)/2
        slider.setValue(test)
        slider.update()
        [angle,dist]=f(locator)
        # cervicales et compression decroissant
        if (angle>0 and Croiss) or (angle<0 and (not Croiss)):
            maxi=test
        else:
            mini=test   
    #print "i",i

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
def placementManuel(nBoucles=3,courbureC=53,courbureL=5):
    t=time.time()
    compression=angleCompLoc()
    compressionGD=angleCompGDLoc()

    angleCervicales=angleCHBLoc()
    angleCervicalesGD=angleCGDLoc()
    
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
    print param

    for i in range(nBoucles):
        sliderGrp.do("posture",posture)

        #print calcCVParameters() 
        sliderGrp.do("compression",compression)
        #print("orientation",orientation)
        #
        sliderGrp.do("compression g",compressionGD)
        #print("compression g",compressionGD)
        ##print calcCVParameters()
        ##keepParameters(param)
        sliderGrp.do("rot dorsale",angleDorsales)
        ##keepParameters(param)
        sliderGrp.do("rot dorsale g ",angleDorsalesGD)
        ##keepParameters(param)
        sliderGrp.do("rot cervicale",angleCervicales)  
        ##keepParameters(param)
        sliderGrp.do("rot cervicale g",angleCervicalesGD)  
        ##keepParameters(param)
        sliderGrp.do("rot lombaire",angleLombaires) 
        ##keepParameters(param)
        sliderGrp.do("rot lombaire GD",angleLombairesGD) 
        ##keepParameters(param)
    sliderGrp.do("orientation",orientation)
    sliderGrp.do("posture",posture)


    scaleFactor=locatorLength()/locatorCurveLength()*getCurveLength()
    sliderGrp.do("scale",scaleFactor)
    sliderGrp.do("x",pos[0])
    sliderGrp.do("y",pos[1])
    sliderGrp.do("z",pos[2])


    #ReplacePoints(pointOnCurveList,nameList)

     #calcul des distances des locators a la courbe
    locatorList=map(position,[locator(i) for i in range(5)])
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
    res=[0,0,0,0,0,0,0,0,0]
    for i in range(1):
        1
        #scaleFactor=locatorLength()/locatorCurveLength()*getCurveLength()
        #sliderGrp.do("scale",scaleFactor)
        ##correctionPos(sliderGrp,5,position("locatorC"))
        #if res[3] or True: 
        #    1#compression
        #    correctionRot(sliderGrp,sliderGrp.string2num("compression"),locatorList[3])
        #    correctionRot(sliderGrp,sliderGrp.string2num("compression gd"),locatorList[3],False,0)
        #if res[1] or True:
        #    1#dorsales
        #    correctionRot(sliderGrp,sliderGrp.string2num("rot dorsale"),locatorList[1])
        #    correctionRot(sliderGrp,sliderGrp.string2num("rot dorsale gd"),locatorList[1],False)
        #if res[0] or True:
        #    1#lombaires
        #    correctionRot(sliderGrp,sliderGrp.string2num("rot lombaire"),locatorList[0],True,3)
        #    correctionRot(sliderGrp,sliderGrp.string2num("rot lombaire gd"),locatorList[0],False)
        #if res[4] or True:
        #    1#cervicales
        #    correctionRot(sliderGrp,sliderGrp.string2num("rot c"),locatorList[4],False)
        #    correctionRot(sliderGrp,sliderGrp.string2num("rot cervicale gd"),locatorList[4])

    #keepParameters(param)
     #pour que tous les locators passent exactement par la courbe
    for i in range(1):
    ##    correctionPos(sliderGrp,1,position("locatorAngle1"))
        1# position precise
        #ajustePosCurvePoints()
        ##### position sur la courbe
        #correctionPos(sliderGrp,2,position(locator(2)))
        #correctionPos(sliderGrp,1,position(locator(1)))

        #for i in range(5):
        #    correctionPos(sliderGrp,4,position(locator(3)))
        #correctionPos(sliderGrp,0,position(locator(0)))
        #correctionPos(sliderGrp,6,position(locator(4)))
        #correctionPos(sliderGrp,3,position("locatorD"))

        ## recale les 3 points hors extremites donc les cv se sont petit a petit decales
        #recalageTangentSansLocator(oldParamC,5)
        ###recalageTangentSansLocator(oldParamD,3)
        #recalageTangent(2,2)
        #recalageTangent(1,1)
        #recalageTangent(3,4)

    p("duree placage : "+str(time.time()-t))      
    #p("param debut",param) 
    a=Evaluate()
    evaluation=a.execute()
    return evaluation
    

sliderGrp=mainFct(pointOnCurveList,locatorList)
maxCV = cmds.getAttr("curve1.spans")+cmds.getAttr("curve1.degree")
for i in range(2,3):
    j=0
    cmds.currentTime( j, edit=True )
    placementManuel(1,40) 
    string='setKeyframe -breakdown 0 -hierarchy none -controlPoints 1 -shape 0 {"curve1"};'
    #mel.eval(string)
    for j in range(maxCV):
        string='setKeyframe -breakdown 0 -hierarchy none -controlPoints 0 -shape 0 -i {"curve1.cv['+str(j)+']"};'
        mel.eval(string)
param=calcCVParameters()
#p("param fin",param)
        
EvalPositionLocator2()
#print param
#print calcCVParameters()



 