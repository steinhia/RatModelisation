# -*- coding: utf-8 -*-

# une classe pour une action a executer
# -*- coding: utf-8 -*-
#from functools import partial
#import maya.cmds as cmds
#import maya.mel as mel
#import math
#import maya
import sys
#import time

sys.path.append("C:\Users\alexa\Documents\alexandra\scripts")

path="C:/Users/alexa/Documents/alexandra/scripts/"
execfile(path+"Mouvements.py")
execfile(path+"Short.py")

class Action(object):

    def __init__(self,offset,Cote,CoteOpp,keepPosture,keepPosition,keepCurveLength,mvt=True,*_):
        self.offset=offset
        #self.crvInfos=crvInfos #length position posture chainLength cLen
        self.mvt=mvt
        self.keepCurveLength=keepCurveLength
        self.keepPosture=keepPosture
        self.keepPosition=keepPosition
        self.function=-1
        self.Cote=Cote
        self.CoteOpp=CoteOpp

    def execute(self,ajust=True,*_):
        param=calcCVParameters()
        #orientation=calcOrientation(Cote=self.Cote)
        orientationOpp=calcOrientation(Cote=self.CoteOpp)
        pos=getCurvePosition(Cote=self.CoteOpp)
        posture=calcPosture(Cote=self.CoteOpp)
        lenC=getCurveLength()
        lenChain=getJointChainLength()
        jtParam=JointParameters()
        cmds.select(clear=True)
        if self.mvt and ajust:
            setOrientation(0,self.Cote)
        cmds.select(clear=True)
        self.executeAction(self)
        cmds.select(clear=True)
        if self.function!=setOrientation and self.mvt and ajust:
            setOrientation(orientationOpp,Cote=self.CoteOpp)
        if self.mvt and ajust:
            #keepJointParameters(jtParam)
            newPos=getCurvePosition(Cote=self.CoteOpp)
            newPosture=calcPosture(Cote=self.CoteOpp)
            newLen=getCurveLength()
            if self.keepCurveLength:
                keepChainLengthValue(lenChain)
                keepLengthValue(lenC,getCurvePosition())
            else:
                cL=getCurveLength()
                rapport=cL/lenC
                keepChainLengthValue(lenChain*rapport)
            if self.keepPosture :
               setPosture(posture,Cote=self.CoteOpp)
            if self.keepPosition:        
                setCurvePosition(pos,Cote=self.CoteOpp)
        cmds.select(clear=True)





    def executeAction(self,*_):
        raise NotImplementedError

class SimpleAction(Action):

    def __init__(self,offset,type,x,y,z,listOfSelection,Cote,CoteOpp,keepPosition,keepPosture=True,keepCurveLength=True,pivot=-1,mvt=True,*_): # pivot = position du pivot
        Action.__init__(self,offset,Cote,CoteOpp,keepPosture,keepPosition,keepCurveLength) 
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

    def __init__(self,offset,function,Cote,CoteOpp,keepPosture,keepPosition,keepCurveLength=True,args=[],mvt=True,*_):
        Action.__init__(self, offset,Cote,CoteOpp,keepPosture,keepPosition,keepCurveLength) 
        self.function=function
        self.args=args
        self.mvt=mvt

    def execute(self,ajust=True,*_):
        Action.execute(self,ajust,self.args)

    def executeAction(self,*_):
        if self.args==[] :
            self.function(self.offset)
        else :
            self.function(self.offset,self.args)






        

    
        
    