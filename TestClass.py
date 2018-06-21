#import maya.cmds as cmds
#import maya
#import math
import sys
#import time

sys.path.append("C:/Users/alexa/Documents/alexandra/scripts")


path="C:/Users/alexa/Documents/alexandra/scripts/"
execfile(path+"main.py")
from random import random


def getXFromY(button,y):
    val=button.slider.sliderValue()  
    button.slider2.setValue(y)
    button.slider2.update(True,True)
    x=button.slider.sliderValue()
    button.slider.setValue(val)
    button.slider.update(True,True)
    return x        

def getYFromX(button,x):
    val=button.slider.sliderValue()  
    button.slider.setValue(x)
    button.slider.update(True,True)
    y=button.slider2.sliderValue()
    y2=button.calcValue()
    if abs(y-y2)>0.00001:
        p(" fail getYFromX sliderValue!=calcValue()) " + button.slider2.label +" "+str(y)+" "+str(y2))
    button.slider.setValue(val)
    button.slider.update(True,True)
    return y


class UnitTest(object):

    def __init__(self,button,buttonList,sequenceValue,*_):
        self.button=button
        self.buttonList=buttonList
        self.sequenceValue=sequenceValue

    def execute2(self,*_):
        # est-ce que le reset nous ramene comme avant
        dist=[]
        max=-1
        #beginP=getParameter(position(curvei(n2N("T1"))))
        #cmds.setAttr ('arcLengthDimension1.uParamValue', beginP)  
        #dist.append(cmds.getAttr ('arcLengthDimension1.al'))
        valueReset=self.button.valueReset
        self.button.reset()
        val1=[]
        returnValue=True
        liste=[" courbureC "," rotCG ", " rotCB "," rotDG "," rotDB ","rotLG "," rotLB "," compression "]
        for i in self.buttonList[:8]:
            v1=i.calcValue()
            v2=i.sliderValue()
            val1.append(v1)
            if (v1-v2)>0.00001:
                print "FAIL depart slider/calcValue " + i.slider2.label +" "+str(v1)+" "+str(v2)
        for i in self.sequenceValue:
            self.button.slider2.setValue(i)
            self.button.slider2.update()
            valueFinal=self.button.calcValue()
            valueFinal2=self.button.sliderValue()
            if abs(valueFinal-valueFinal2)>0.0001:
                print "FAIL mise a jour slider/calcValue lors du set " + i.slider2.label + " " + str(valueFinal) + " "+str(valueFinal2)
            if abs(valueFinal-i)>0.01:
                print "FAIL SET " + self.button.slider2.label
                print "expected : "+ str(i)
                print "got : "+ str(valueFinal)
                returnValue=False
            #res=cmds.getAttr ('arcLengthDimension1.al')
            #dist.append(res)
            #tmp=abs(dist[0]-res)/dist[0]*100
            #if tmp>max:
            #    max=tmp
        self.button.reset()#update(valueReset,True)
        val2=[]
        for i in self.buttonList[:8]:
            v1=i.calcValue()
            v2=i.sliderValue()
            val2.append(v1)
            if abs(v1-v2)>0.00001:
                print "FAIL mise a jour slider/calcValue comparaison finale" + i.slider2.label +" "+str(v1)+" "+str(v2)
        #cmds.delete (tmpArclenDim)
        if max>0.5:
            1#p("variation longueur cervicale (%)",max)
        [indice,maxdiff]=maxDiff(val1,val2)
        if maxdiff>0.01 or (not returnValue):
            print "\n maxdiff",maxdiff,val1[indice],val2[indice],liste[indice]
            print "FAIL " + self.button.slider2.label
            #print "courbureC rotCG rotCB rotDG rotDB rotLG rotLB compression x y z scale posture"
            print val1
            print val2
            return False
        else:
            print "PASS " + self.button.slider2.label
            return True

class Test(object):

    def __init__(self,*_):
        self.label="test1"

    def execute(self):
        p("\n TEST STABILITE")
        sliderGrp=mainFct(pointOnCurveList,locatorList)
        n=len(sliderGrp.buttonList[:9])
        # un unit test
        nbFailures=0
        nbTot=0
        for i in range(n):
            button=sliderGrp.buttonList[i]
            min=button.slider2.minValue
            max=button.slider2.maxValue
            seq=[]
            for j in range(10):
                seq.append(min+random()*(max-min))
            testUnit=UnitTest(button,sliderGrp.buttonList,seq)
            res2=testUnit.execute2()
            if not res2:
                nbFailures+=1
            nbTot+=1
        print "NUMBER OF FAILURES : " + str(nbFailures) + "/" + str(nbTot) + "\n"

    # un bouton*10 un reset, un bouton*10 un reset etc TOUT
    def executeRandom(self):
        p("\n TEST RANDOM")
        sliderGrp=mainFct(pointOnCurveList,locatorList)
        n=len(sliderGrp.buttonList)
        nbFailures=0
        nbTot=0
        for i in range(10):
            button=sliderGrp.buttonList[int((random()*100000)%11)]
            min=button.slider2.minValue
            max=button.slider2.maxValue
            seq=[]
            for j in range(2):
                seq.append(min+random()*(max-min))
            testUnit=UnitTest(button,sliderGrp.buttonList,seq)
            res=testUnit.execute2()

            if not res:
                nbFailures+=1
            nbTot+=1
        print "NUMBER OF FAILURES : " + str(nbFailures) + "/" + str(nbTot) + "\n"

    def executeCV(self):
        p("\n TEST CV")
        sliderGrp=mainFct(pointOnCurveList,locatorList)
        n=len(sliderGrp.buttonList)
        resParam=[]
        resPos=[]
        buttonNameList=[]
        valueList=[]
        for i in range(20):
            button=sliderGrp.buttonList[1+int((random()*100000)%7)]
            buttonNameList.append(button.slider2.label)
            resetValue=-1
            if button.slider!=-1:
                slider=button.slider
                resetValue=slider.value
            else:
                slider=button.slider2
                resetValue=slider.value
            mini=slider.minValue
            maxi=slider.maxValue
            seq=[]
            [param,positions]=calcParameters()
            for j in range(5):
                value=mini+random()*(maxi-mini)
                valueList.append(value)
                slider.setValue(value)
                slider.update()
            slider.setValue(resetValue)
            slider.update()
            [param2,positions2]=calcParameters()
            Sub=sub(param,param2)
            SubP=[]
            for i,pos in enumerate(positions):
                SubP.append(sub(pos,positions2[i]))
            resParam.append(max(map(abs,Sub)))
            resPos.append(max(map(norm,SubP)))
        moy=0   
        for i in resPos:
            moy+=i
        moy/=len(resPos)
        #p("param",resParam,"maxParam",str(max(resParam)) +"/" + str(cmds.getAttr("curveShape1.maxValue"))+"(maxParam)")
        #p("pos",resPos,"maxPos",max(resPos),"moyenne Pos",str(moy)+"/"+str(getCurveLength())+"(curve length)")
        if max(resParam) < 0.01:
            p("PASS param : max diff = " +str(max(resParam)))
        else :
            p("FAIL param : max diff= " + str(max(resParam)))
        if max(resPos) < 0.01:
            p("PASS pos : max diff = " +str(max(resPos))+"\n")
        else :
            p("FAIL pos : max diff= " + str(max(resPos))+" " +  buttonNameList[resPos.index(max(resPos))])
            for i,pos in enumerate(resPos):
                if pos>0.01:
                    print pos, " ",buttonNameList[i]
            #print valueList



    def execute0(self):
        p("\n TEST 0")
        sliderGrp=mainFct(pointOnCurveList,locatorList)
        n=len(sliderGrp.buttonList[:8])
        # un unit test
        nbFailures=0
        nbTot=0
        nbFailures2=0
        nbTot2=0
        for i in range(n):
            button=sliderGrp.buttonList[i]
            slider=button.slider
            min=button.slider.minValue
            max=button.slider.maxValue
            min2=button.slider2.minValue
            max2=button.slider2.maxValue
            val=slider.value
            val2=slider.sliderValue()
            if abs(val-val2)>0.00001:
                p("value differente de la valeur du slider " + button.slider2.label + " " +str(val)+ " "+ str(val2))
            # min du slider2 = meme valeur a gauche
            # fMin = valeur a gauche si met min2 et max2
            x0=getXFromY(button,(min2+max2)/2.0)
            # min du slider 1 = meme valeur a droite
            # fMin2 = valeur a droite si met le min a gauche 
            y0=getYFromX(button,(min+max)/2.0)
            seq=[]
            res=True
            for j in range(10):
                button.slider2.setValue(min2+random()*(max2-min2))
                button.slider2.update(True,True)
            button.reset()
            x0After=getXFromY(button,(min2+max2)/2.0)
            # min du slider 1 -> meme valeur pour slider2
            y0After=getYFromX(button,(min+max)/2.0)
 
 
            if abs(x0-x0After)>0.01:
                print "DECALAGE X  : " + button.slider2.label
                print "X0 " +str(x0) + " " + str(x0After) 
                res=False
            else :
                print "PASS X " + button.slider2.label
            if not res:
                nbFailures+=1
            nbTot+=1
            if abs(y0-y0After)>0.01:
                print "DECALAGE Y  : " + button.slider2.label
                print "Y0 " +str(y0) + " " + str(y0After) 
                res=False
            else :
                print "PASS Y " + button.slider2.label
            if not res:
                nbFailures2+=1
            nbTot2+=1
        print "NUMBER OF FAILURES X: " + str(nbFailures) + "/" + str(nbTot) 
        print "NUMBER OF FAILURES Y: " + str(nbFailures2) + "/" + str(nbTot2) + "\n"


# TODO quand fait les differents set, reset remet pas les precedents a leurs bonnes valeurs
    def executeSet(self):
        p("\n TEST SET")
        sliderGrp=mainFct(pointOnCurveList,locatorList)
        n=len(sliderGrp.buttonList[:8])
        # un unit test
        nbFailures=0
        nbTot=0      
        for i in range(1,n):
        #    for j in range(n):
        #        button=sliderGrp.buttonList[j]   
        #        print i, " ",button.slider2.sliderValue()  
            button=sliderGrp.buttonList[i]
            slider2=button.slider2
            min=slider2.minValue
            max=slider2.maxValue
            res=True
            nbFailures=0
            nbTot=0
            valInit=button.valueReset
            for j in range(10):
                val=min+float(j)*(max-min)/10.0
                slider2.setValue(val)
                slider2.update()
                valSlider=slider2.sliderValue()
                valSlider2=button.calcValue()
                if abs(valSlider-valSlider2)>0.0001 and valSlider>slider2.minValue and valSlider<slider2.maxValue:
                    p("FAIL maj calcValue/sliderValue " + button.slider2.label +" " +  str(valSlider2) +" "+str(valSlider))
                if abs(valSlider-val)>0.1:
                    res=False
                    print "FAIL SET : " + button.slider2.label
                    print "Wanted : ",val," Got : ",valSlider
            button.reset()
            valEnd=button.calcValue()
            valEnd2=button.sliderValue()
            if abs(valEnd-valEnd2)>0.00001 and valEnd>slider2.minValue and valEnd<slider2.maxValue:
                p("FAIL maj calcValue/sliderValue " + button.slider2.label + " " + str(valEnd) + " " + str(valEnd2))                
            if abs(valInit-valEnd)>0.1:
                print "FAIL RESET : " + "Wanted : ",valInit," Got : ",valEnd
            if res:
                print "PASS " + button.slider2.label 
            else :
                print "Fail " + button.slider2.label 
                nbFailures+=1
        print "NUMBER OF FAILURES : " + str(nbFailures) + "/" + str(n-1) + "\n"            
        





test=Test()
test.execute0()
test.executeSet()
test.execute()
for i in range(10):
    test.executeCV()
test.executeRandom()



        
        

