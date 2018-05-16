import sys
sys.path.append("C:/Users/alexandra/Documents/alexandra/scripts")


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



#53 ou 83 selon pendant ou avant
def placageManuel(nBoucles=3,courbureC=53,courbureL=5):
    t=time.time()
    sliderGrp=mainFct(pointOnCurveList,locatorList)
    compression=angleComp()

    angleCervicales=angleC()
    angleCervicalesGD=angleCGD()
    
    angleDorsales=angleD()
    angleDorsalesGD=angleDGD()

    angleLombaires=angleL()
    angleLombairesGD=angleLGD()

    posture=locatorPosture()
    postureGD=locatorPostureGD()
    pos=getLocatorCurvePosition()

    #sliderGrp.do("courbure c",courbureC)

    for i in range(nBoucles):
        print i
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

    

       
    p("duree placage : "+str(time.time()-t))
        
    a=Evaluate()
    res=a.execute()
    return res

#iMin=placageOpti()
placageManuel(1,40)
#cmds.currentTime( query=True )
cmds.currentTime( 2, edit=True )
placageManuel(3,40)



