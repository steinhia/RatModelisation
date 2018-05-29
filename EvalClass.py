#import maya.cmds as cmds
#import math
import sys
#import time

sys.path.append("C:/Users/alexandra/Documents/alexandra/scripts")


path="C:/Users/alexandra/Documents/alexandra/scripts/"
import main
reload(main)

class Evaluate(object):
    
    def __init(self,*_):
        self.label="eval1"

    def execute(self):
        names=["pos","length","posture","rot C HB","rot C GD","rot D HB","rot D GD","rot L HB","rot L GD","compr"] 

        # mesures sur la courbe
        L=[]
        L.append(getCurvePosition())
        L.append(locatorCurveLength())
        L.append(calcPosture())
        L.append(angleCHB())
        L.append(angleCGD())
        L.append(angleDHB())
        L.append(angleDGD())
        L.append(angleLHB())
        L.append(angleLGD())
        L.append(angleComp())

        # mesure avec les locators
        l=[]
        l.append(getLocatorCurvePosition())
        l.append(locatorLength())
        l.append(locatorPosture())
        l.append(angleCHB())
        l.append(angleCGD())
        l.append(angleDHB())
        l.append(angleDGD())
        l.append(angleLHB())
        l.append(angleLGD())
        l.append(angleComp())

        totalDiff=0
        totalDiffPrec=0
        totalDiffAngles=0
        for i,mesure in enumerate(L):
            if isinstance(mesure,list):
                if norm(sub(mesure,l[i]))>0.005:
                    print names[i],mesure,l[i]
                totalDiffAngles+=norm(sub(mesure,l[i]))
            else:
                totalDiffAngles+=abs(mesure-l[i])
                if abs(mesure-l[i])>0.005:
                    print names[i],abs(mesure-l[i])

        # position des differents locators / vertebres correspondantes
        posLoc=map(position,[locator(0),locator(1),locator(2),locator(3),locator(4)])
        posPrec=map(num2Name,range(5))
        posPrec=map(position,posPrec)
        pos=map(getParameter,posLoc)
        pos=map(getPoint,pos)
        subPos=[]
        subPosPrec=[]
        for i,posi in enumerate(pos):
            val=norm(sub(posLoc[i],posi))
            val2=norm(sub(posLoc[i],posPrec[i]))
            subPos.append(val)
            subPosPrec.append(val2)
            totalDiff+=val
            totalDiffPrec+=val2
            if(val)>0.005:
                print i,val
            if(val2)>0.005:
                print i,val2
       # print subPos
        p("TOTAL DIFF locateurs a la courbe : ",totalDiff)
        p("TOTAL DIFF locateurs au point correspondant : ",totalDiffPrec)
        p("TOTAL DIFF angles : ",totalDiffAngles)
        return totalDiff
        
        
        
#a=Evaluate()
#a.execute()


        




