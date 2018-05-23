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
        print val
        subPos=sum(subPos,val)
    subPos=pdt(0.2,subPos)
    cmds.select("curve1")
    cmds.move(subPos[0],subPos[1],subPos[2],r=True)

def calcPosRelatif(locator):
    locatorOnCurve=getPoint(getParameter(locator))
    tan=getTangent(locatorOnCurve)
    vect=sub(locatorOnCurve,locator)
    return [angleHB(tan,vect),norm(vect)]

def correctionRot(sliderGrp,nButton,locator,precision=10):
    [angle,dist]=calcPosRelatif(locator)
    slider=sliderGrp.buttonList[nButton].slider
    valInit=slider.sliderValue()
    # compression et cervicales dans l'autre sens
    if (angle>0 and nButton!=3 and nButton!=8 and nButton!=0 and nButton!=1) or (angle<0 and (nButton==3 or nButton==8 or nButton==0 or nButton==1)):
        max=valInit
        min=valInit-5*dist*(slider.maxValue-slider.minValue)
    else:
        min=valInit
        max=valInit+5*dist*(slider.maxValue-slider.minValue)
    i=0
    while dist>0.01 and i<precision:
        i+=1
        test=(min+max)/2
        slider.setValue(test)
        slider.update()
        [angle,dist]=calcPosRelatif(locator)
        # cervicales et compression decroissant
        if (angle>0 and nButton!=3 and nButton!=8 and nButton!=0 and nButton!=1) or (angle<0 and (nButton==3 or nButton==8 or nButton==0 or nButton==1)):
            max=test
        else:
            min=test   

def correctionPos(sliderGrp,nPoint,locator):
    vect=sub(locator,getPoint(getParameter(locator)))
    cmds.select(curvei(nPoint))
    cmds.move(vect[0],vect[1],vect[2],r=True)

def calcAngleDorsalesLocator():
    v1=sub(position(locator(0)),position(locator(1)))
    v2=sub(position(locator(2)),position(locator(1)))
    print angleHB(v1,v2)

def calcAngleDorsales():
    v1=sub(position(curvei(1)),position(curvei(2)))
    v2=sub(position(curvei(3)),position(curvei(2)))
    print angleHB(v1,v2)

#53 ou 83 selon pendant ou avant
def placageManuel(nBoucles=3,courbureC=53,courbureL=5):
    t=time.time()
    compression=angleComp()

    angleCervicales=angleC()
    angleCervicalesGD=angleCGD()
    
    angleDorsales=angleD()
    angleDorsalesGD=angleDGD()

    angleLombaires=angleL()
    angleLombairesGD=angleLGD()

    posture=locatorPosture()
    #postureGD=locatorPostureGD()
    pos=getLocatorCurvePosition()

    #sliderGrp.do("courbure c",courbureC)

    for i in range(nBoucles):
        sliderGrp.do("posture",posture)
        sliderGrp.do("compression",compression)
        sliderGrp.do("rot dorsale",angleDorsales)
        sliderGrp.do("rot dorsale GD",angleDorsalesGD)
        sliderGrp.do("rot cervicale",angleCervicales)  
        sliderGrp.do("rot cervicale GD",angleCervicalesGD)  

        sliderGrp.do("rot lombaire",angleLombaires) 
        sliderGrp.do("rot lombaire GD",angleLombairesGD) 
        #sliderGrp.do("courbure c",courbureC)

    scaleFactor=locatorLength()/locatorCurveLength()*getCurveLength()
    sliderGrp.do("scale",scaleFactor)
    sliderGrp.do("x",pos[0])
    sliderGrp.do("y",pos[1])
    sliderGrp.do("z",pos[2])

    # calcul des distances des locators a la courbe
    #print inspect.getmembers(GeneralCalculs(), predicate=inspect.ismethod)
    locatorList=map(position,[locator(i) for i in range(5)])
    locatorOnCurveList=map(getPoint,map(getParameter,locatorList))
    diff=[sub(locatorList[i],locatorOnCurveList[i]) for i in range(5)]
    res=[]
    for i,posi in enumerate(diff):
        if norm(posi)>0.03:
            res.append(True)
        else:
            res.append(False)
    #for i in range(2):

    #lordoseC=calcLordoseC()
    #p("lordoseL1",calcLordoseL())
    #sliderGrp.do("courbure l",lordoseC)
    #p("lordoseL2",calcLordoseL())

        #if res[1]:
        #    #dorsales
        #    correctionRot(sliderGrp,5,locatorList[1])
        #if res[0]:
        #    #lombaires
        #    correctionRot(sliderGrp,7,locatorList[0])
        #if res[3]:
        #    correctionRot(sliderGrp,8,locatorList[3])
        #if res[4]:
        #    #cervicales
        #    correctionRot(sliderGrp,3,locatorList[4])

     #pour que tous les locators passent exactement par la courbe
    for i in range(2):
        correctionRot(sliderGrp,0,position("locatorC"))
        correctionRot(sliderGrp,1,position("locatorL"),10)
        correctionPos(sliderGrp,2,position(locator(2)))
        correctionPos(sliderGrp,3,position(locator(3)))
        correctionPos(sliderGrp,1,position(locator(1)))
        correctionPos(sliderGrp,5,position(locator(4)))
        correctionPos(sliderGrp,0,position(locator(0)))

    for i in sliderGrp.buttonList[0].sliderList:
        i.update(True)

    ##ajustePos()
    p("duree placage : "+str(time.time()-t))       
    a=Evaluate()
    res=a.execute()
    return res
    
#iMin=placageOpti()
sliderGrp=mainFct(pointOnCurveList,locatorList)
maxCV = cmds.getAttr("curve1.spans")+cmds.getAttr("curve1.degree")
for i in range(2,3):
    j=1
    cmds.currentTime( j, edit=True )
    placageManuel(1,40) 
    string='setKeyframe -breakdown 0 -hierarchy none -controlPoints 1 -shape 0 {"curve1"};'
    #mel.eval(string)
    for j in range(maxCV):
        string='setKeyframe -breakdown 0 -hierarchy none -controlPoints 0 -shape 0 -i {"curve1.cv['+str(j)+']"};'
        mel.eval(string)

        
EvalPositionLocator2()



