# -*- coding: utf-8 -*-
#import maya.cmds as cmds
#import math
import sys
#import time



class Evaluate(object):
    """ classe d'évaluation du placement de la courbe à l'aide des localisateurs """
    
    def __init(self,*_):
        self.label="eval1"

    def execute(self,printRes=False):
        """ test simple avec les loclaisateurs utilisés pour le placement : 2 distances à la courbe """    
        totalDiff=0
        totalDiffPrec=0

        # position des differents locators / vertebres correspondantes
        posLoc=map(position,[locator(0),locator(1),locator(2),locator(3),locator(4)])
        posPrec=map(num2Name,range(5))
        posPrec=map(position,posPrec) # vertèbres correspondantes
        pos=map(getParameter,posLoc)
        pos=map(getPoint,pos) # points le plus proche du localisateur
        subPos=[]
        subPosPrec=[]
        for i,posi in enumerate(pos):
            val=norm(sub(posLoc[i],posi))
            val2=norm(sub(posLoc[i],posPrec[i]))
            subPos.append(val)
            subPosPrec.append(val2)
            totalDiff+=val
            totalDiffPrec+=val2
            #if printRes :
            #    if(val)>0.01:
            #        print(i,val)
            #    if(val2)>0.01:
            #        print(i,val2)
        if printRes:
            print("TOTAL DIFF locateurs a la courbe : ",totalDiff)
            print("TOTAL DIFF locateurs au point correspondant : ",totalDiffPrec)
        return totalDiff
        
        
        
#a=Evaluate()
#a.execute()


        




