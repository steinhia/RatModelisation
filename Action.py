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

    def __init__(self,offset,Cote,CoteOpp,keepPosition,keepCurveLength,mvt=True,*_):
        self.offset=offset
        #self.crvInfos=crvInfos #length position posture chainLength cLen
        self.mvt=mvt
        self.keepCurveLength=keepCurveLength
        self.keepPosition=keepPosition
        self.function=-1
        self.Cote=Cote
        self.CoteOpp=CoteOpp

    def execute(self,ajust=True,nMax=10,*_):
        param=calcCVParameters()
        #orientation=getOrientation(Cote=self.Cote)
        orientationOpp=getOrientation(Cote=self.CoteOpp)
        pos=getPosition(Cote=self.CoteOpp)
        posture=getPosture(Cote=self.CoteOpp)
        lenC=getLength()
        lenChain=getJointChainLength()
        jtParam=JointParameters()
        clear()
        if self.mvt and ajust:
            setOrientation(0,self.Cote)
        clear()
        #print getLLen(),getCLen(),getLLen()
        self.executeAction(nMax=nMax)
        #print getLLen(),getCLen(),getLLen()
        clear()
        if self.function!=setOrientation and self.mvt and ajust:
            setOrientation(orientationOpp,Cote=self.CoteOpp)
        if self.mvt and ajust:
            #keepJointParameters(jtParam)
            newPos=getPosition(Cote=self.CoteOpp)
            newPosture=getPosture(Cote=self.CoteOpp)
            newLen=getLength()
            if self.keepCurveLength:
                setLength(lenC)
                keepChainLengthValue(lenChain)
            else:
                cL=getLength()
                rapport=cL/lenC
                #keepChainLengthValue(lenChain*rapport)
            if self.keepPosition:        
                setCurvePosition(pos,Cote=self.CoteOpp)
        clear()
        #select('curve1')






    def executeAction(self,nMax=10,*_):
        raise NotImplementedError

class SimpleAction(Action):

    def __init__(self,offset,type,x,y,z,listOfSelection,Cote,CoteOpp,keepPosition,keepCurveLength=True,pivot=-1,mvt=True,*_): # pivot = position du pivot
        Action.__init__(self,offset,Cote,CoteOpp,keepPosition,keepCurveLength) 
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
            cmds.scale(self.offset,x=self.x,y=self.y,z=self.z,r=True,pivot=getPosition()) # pivot ? 
    

# les arguments de la fonction doivent etre une unique liste        
class FunctionAction(Action):

    def __init__(self,offset,function,Cote,CoteOpp,keepPosition,keepCurveLength=True,args=[],mvt=True,*_):
        Action.__init__(self, offset,Cote,CoteOpp,keepPosition,keepCurveLength) 
        self.function=function
        self.args=args
        self.mvt=mvt

    def execute(self,ajust=True,nMax=10,*_):
        Action.execute(self,ajust,nMax)# rajouter args?

    def executeAction(self,nMax=10,*_):
        if self.args==[] :
            self.function(self.offset,nMax)
        else :
            self.function(self.offset,self.args,nMax)






        

    
        
    