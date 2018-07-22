#import maya.cmds as cmds
#import math
import sys
#import time

sys.path.append("C:/Users/alexa/Documents/alexandra/scripts")


class Evaluate(object):
    
    def __init(self,*_):
        self.label="eval1"

    def execute(self):
        names=["Position","Length","Posture","X","Y","Z"]
        names2=["CHB","CGD","LHB","LGD","CompHB","CompGD"] 
        

        ## mesures sur la courbe
        L=[]
        for name in names :
            L.append()

        for name in names2:
            L.append(angleCrv(name))

        l=[]
        for name in names :
            L.append()

        for name in names2:
            L.append(angleLoc(name))

        totalDiff=0
        totalDiffPrec=0
        totalDiffAngles=0
        #for i,mesure in enumerate(L):
        #    if isinstance(mesure,list):
        #        if norm(sub(mesure,l[i]))>0.005:
        #            print names[i],mesure,l[i]
        #        totalDiffAngles+=norm(sub(mesure,l[i]))
        #    else:
        #        totalDiffAngles+=abs(mesure-l[i])
        #        if abs(mesure-l[i])>0.005:
        #            print names[i],abs(mesure-l[i])

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


        




