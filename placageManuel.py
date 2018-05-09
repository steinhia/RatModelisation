import sys
sys.path.append("C:/Users/alexandra/Documents/alexandra/scripts")


path="C:/Users/alexandra/Documents/alexandra/scripts/"
execfile(path+"main.py")
execfile(path+"mesures.py")
execfile(path+"EvalClass.py")

def placageManuel():

    t=time.time()
    sliderGrp=mainFct()
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
    p("duree main",time.time()-t,posture)

    for i in range(5):
        sliderGrp.do("posture",posture,True) 
        sliderGrp.do("compression",compression,True)
        #print "angleD",angleDorsales
        sliderGrp.do("rot dorsale",angleDorsales,True)
        sliderGrp.do("rot dorsale GD",angleDorsalesGD,True)
        sliderGrp.do("rot cervicale",angleCervicales,True)  
        sliderGrp.do("rot cervicale GD",angleCervicalesGD,True)  
        sliderGrp.do("rot lombaire",angleLombaires,True) 
        sliderGrp.do("rot lombaire GD",angleLombairesGD,True) 
        sliderGrp.do("courbure c",45)


    sliderGrp.do("x",pos[0])
    sliderGrp.do("y",pos[1])
    sliderGrp.do("z",pos[2])
    scaleFactor=locatorLength()/locatorCurveLength()*getCurveLength()
    sliderGrp.do("scale",scaleFactor)

    p("duree placage : "+str(time.time()-t))

        
    a=Evaluate()
    a.execute()



placageManuel()