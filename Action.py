# une classe pour une action a executer

#from functools import partial
#import maya.cmds as cmds
#import maya.mel as mel
#import math
#import maya
import sys
#import time

sys.path.append("C:\Users\alexandra\Documents\alexandra\scripts")

path="C:/Users/alexandra/Documents/alexandra/scripts/"
execfile(path+"Mouvements.py")
execfile(path+"Short.py")

class Action(object):

    def __init__(self,offset,crvInfos,keepPosture,keepPosition,keepCurveLength,mvt=True,*_):
        self.offset=offset
        self.crvInfos=crvInfos #length position posture chainLength cLen
        self.mvt=mvt
        self.keepCurveLength=keepCurveLength
        self.keepPosture=keepPosture
        self.keepPosition=keepPosition


    def execute(self,ajust=True,*_):
        param=calcCVParameters()
        cmds.select(clear=True)
        self.executeAction(self)
        if self.mvt and ajust:
            #keepParameters(param)
            newPos=getCurvePosition()
            newPosture=calcPosture()
            if not self.keepPosition:
                self.crvInfos[1]=newPos
            if self.keepCurveLength:
                #keepCLen(self.crvInfos[4])
                keepLengthValue(self.crvInfos[0],[newPos])
                keepChainLengthValue(self.crvInfos[3])
            else:
                cL=getCurveLength()
                rapport=cL/self.crvInfos[0]
                self.crvInfos[0]=cL
                keepChainLengthValue(self.crvInfos[3]*rapport)
                self.crvInfos[3]=getChainLength()
            if self.keepPosture :
               setPosture(self.crvInfos[2],self.crvInfos)
            else:
                self.crvInfos[2]=newPosture
            #if self.keepPosition:        
            setCurvePosition(self.crvInfos[1])





    def executeAction(self,*_):
        raise NotImplementedError

class SimpleAction(Action):

    def __init__(self,offset,crvInfos,type,x,y,z,listOfSelection,keepPosition,keepPosture=True,keepCurveLength=True,pivot=-1,mvt=True,*_): # pivot = position du pivot
        Action.__init__(self,offset,crvInfos,keepPosture,keepPosition,keepCurveLength) 
        self.type=type
        self.x=x
        self.y=y
        self.z=z
        self.listOfSelection=listOfSelection
        self.pivot=pivot
        self.mvt=mvt

    def execute(self,ajust=True,*_):
        Action.execute(self,ajust)


    def executeAction(self,*_):
        for i in self.listOfSelection :
            cmds.select(i,add=True)
        if(self.type=='t'):
            cmds.move(self.offset,x=self.x,y=self.y,z=self.z,r=True)  
        elif(self.type=='r') :
            if self.pivot==-1:
                cmds.rotate(self.offset,x=self.x,y=self.y,z = self.z, r=True)
            else :
                cmds.rotate(self.offset,x=self.x,y=self.y,z=self.z,r=True,p=self.pivot)
        elif(self.type=='s'):
            cmds.scale(self.offset,x=self.x,y=self.y,z=self.z,r=True,pivot=getCurvePosition()) # pivot ? 
    

# les arguments de la fonction doivent etre une unique liste        
class FunctionAction(Action):

    def __init__(self,offset,crvInfos,function,keepPosture,keepPosition,keepCurveLength=True,args=[],mvt=True,*_):
        Action.__init__(self, offset,crvInfos,keepPosture,keepPosition,keepCurveLength) 
        self.function=function
        self.args=args
        self.mvt=mvt

    def execute(self,ajust=True,*_):
        Action.execute(self,ajust)

    def executeAction(self,*_):
        if self.args==[] :
            self.function(self.offset)
        else :
            self.function(self.offset,self.args)






        

    
        
    