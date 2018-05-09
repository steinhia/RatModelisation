#import maya.cmds as cmds
#import maya
#import math
import sys
#import time

sys.path.append("C:/Users/alexandra/Documents/alexandra/scripts")


path="C:/Users/alexandra/Documents/alexandra/scripts/"
import main
reload(main)
from random import random


class UnitTest(object):

    def __init__(self,button,buttonList,sequenceValue,*_):
        self.button=button
        self.buttonList=buttonList
        self.sequenceValue=sequenceValue

    def execute2(self,*_):
        dist=[]
        max=-1
        #beginP=getParameter(position(curvei(n2N("T1"))))
        #cmds.setAttr ('arcLengthDimension1.uParamValue', beginP)  
        #dist.append(cmds.getAttr ('arcLengthDimension1.al'))
        valueReset=self.button.valueReset
        self.button.update(valueReset,True)
        val1=[]
        returnValue=True
        for i in self.buttonList[:9]:
            val1.append(i.slider2.value)
        for i in self.sequenceValue:
            self.button.slider2.setValue(i)
            self.button.slider2.update(False)
            valueFinal=self.button.slider2.sliderValue()
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
        self.button.update(valueReset,True)
        val2=[]
        for i in self.buttonList[:9]:
            val2.append(i.slider2.value)
        #cmds.delete (tmpArclenDim)
        if max>0.5:
            1#p("variation longueur cervicale (%)",max)
        if maxDiff(val1,val2)>0.01 or (not returnValue):
            p("maxdiff",maxDiff(val1,val2))
            print "FAIL " + self.button.slider.label
            print val1
            print val2
            print self.sequenceValue
            return False
        else:
            print "PASS " + self.button.slider2.label
            return True

class Test(object):

    def __init__(self,*_):
        self.label="test1"

    def execute(self):
        p("TEST")
        sliderGrp=main.mainFct()
        n=len(sliderGrp.buttonList[:9])

        # un unit test
        nbFailures=0
        nbTot=0
        for i in range(n):
            sliderGrp=main.mainFct()
            button=sliderGrp.buttonList[i]
            min=button.slider2.minValue
            max=button.slider2.maxValue
            seq=[]
            for j in range(5):
                seq.append(min+random()*max)
            testUnit=UnitTest(button,sliderGrp.buttonList,seq)
            res2=testUnit.execute2()

            if not res2:
                nbFailures+=1
            nbTot+=1
        print "NUMBER OF FAILURES : " + str(nbFailures) + "/" + str(nbTot) + "\n"

    # un bouton*10 un reset, un bouton*10 un reset etc TOUT
    def executeRandom(self):
        p("TEST RANDOM")
        sliderGrp=main.mainFct()
        n=len(sliderGrp.buttonList)
        nbFailures=0
        nbTot=0
        for i in range(10):
            button=sliderGrp.buttonList[int((random()*100000)%11)]
            min=button.slider2.minValue
            max=button.slider2.maxValue
            seq=[]
            for j in range(5):
                seq.append(min+random()*max)
            testUnit=UnitTest(button,sliderGrp.buttonList,seq)
            res=testUnit.execute2()

            if not res:
                nbFailures+=1
            nbTot+=1
        print "NUMBER OF FAILURES : " + str(nbFailures) + "/" + str(nbTot) + "\n"

    def executeCV(self):
        p("TEST CV")
        sliderGrp=main.mainFct()
        n=len(sliderGrp.buttonList)
        resParam=[]
        resPos=[]
        for i in range(10):
            button=sliderGrp.buttonList[3+int((random()*100000)%7)]
            if button.slider!=-1:
                slider=button.slider
            else:
                slider=button.slider2
            mini=slider.minValue
            maxi=slider.maxValue
            seq=[]
            [param,positions]=calcParameters()
            for j in range(3):
                slider.setValue(mini+random()*maxi)
                slider.update()
            slider.setValue(0.0)
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
            p("FAIL pos : max diff= " + str(max(resPos))+"\n")


    def executeMinMax(self):
        p("TEST MIN MAX")
        sliderGrp=main.mainFct()
        n=len(sliderGrp.buttonList[:9])
        # un unit test
        nbFailures=0
        nbTot=0
        for i in range(n):
            sliderGrp=main.mainFct()
            button=sliderGrp.buttonList[i]
            slider=button.slider
            min=button.slider.minValue
            max=button.slider.maxValue
            min2=button.slider2.minValue
            max2=button.slider2.maxValue
            fMin=setOneRot(0,min2,[slider,button.sliderList[button.indiceText].fct,button.sliderList[button.indiceText].args,[]])
            fMax=setOneRot(0,max2,[slider,button.sliderList[button.indiceText].fct,button.sliderList[button.indiceText].args,[]])          
            seq=[]
            res=True
            for j in range(5):
                button.slider2.setValue(min2+random()*max2)
                button.slider2.update()
            button.reset()
            fMinAfter=setOneRot(0,min2,[slider,button.sliderList[button.indiceText].fct,button.sliderList[button.indiceText].args,[]])
            fMaxAfter=setOneRot(0,max2,[slider,button.sliderList[button.indiceText].fct,button.sliderList[button.indiceText].args,[]]) 
            if abs(fMin-fMinAfter)>0.1 or abs(fMax-fMaxAfter)>0.1:
                print "DECALAGE SLIDER : " + button.slider2.label
                print "fMin " +str(fMin) + " " + str(fMinAfter) 
                print "fMax " +str(fMax) + " " + str(fMaxAfter) 
                res=False
            else :
                print "PASS MIN " + button.slider2.label
            if not res:
                nbFailures+=1
            nbTot+=1
        print "NUMBER OF FAILURES : " + str(nbFailures) + "/" + str(nbTot) + "\n"


            
        





test=Test()
test.executeMinMax()
test.execute()
test.executeCV()
test.executeRandom()



        
        

