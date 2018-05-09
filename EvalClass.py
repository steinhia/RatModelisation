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
        L.append(calcRotCHB())
        L.append(calcRotCGD())
        L.append(calcRotDHB())
        L.append(calcRotDGD())
        L.append(calcRotLHB())
        L.append(calcRotLGD())
        L.append(calcCompressionDorsales())

        # mesure avec les locators
        l=[]
        l.append(getLocatorCurvePosition())
        l.append(locatorLength())
        l.append(locatorPosture())
        l.append(angleC())
        l.append(angleCGD())
        l.append(angleD())
        l.append(angleDGD())
        l.append(angleL())
        l.append(angleLGD())
        l.append(angleComp())

        totalDiff=0
        for i,mesure in enumerate(L):
            if isinstance(mesure,list):
                if norm(sub(mesure,l[i]))>0.001:
                    print names[i],mesure,l[i]
                totalDiff+=norm(sub(mesure,l[i]))
            else:
                totalDiff+=abs(mesure-l[i])
                if abs(mesure-l[i])>0.001:
                    print names[i],abs(mesure-l[i])

        # position des differents locators / vertebres correspondantes
        posLoc=map(position,[locator(0),locator(1),locator(2),locator(3),locator(4)])
        pos=map(num2Name,range(5))
        pos=map(position,pos)
        subPos=[]
        for i,posi in enumerate(pos):
            val=norm(sub(posLoc[i],posi))
            subPos.append(val)
            totalDiff+=val
            if(val)>0.005:
                print i,val
       # print subPos
        p("TOTAL DIFF : ",totalDiff)
        del l
        del L
        
        
        
#a=Evaluate()
#a.execute()

        




