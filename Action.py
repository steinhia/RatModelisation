# -*- coding: utf-8 -*-

# une classe pour une action a executer
# -*- coding: utf-8 -*-
#from functools import partial
#import maya.cmds as cmds
#import maya.mel as mel
#import math
import sys
import time

execfile(path+"Mouvements.py")
execfile(path+"Short.py")

class Action(object):
    """ classe définissant les actions exécutées lors du mouvement d'un slider 
    offset : float, offset du slider 
    mvt : boolean -> pas de réajustement si pas de mouvement (checkbox)
    keep... : boolean
    function : fonction a exécuter
    Cote : string parmi "C" (cervicales), "L" (lombaires), "" (aucun) , Coté où l'action s'exécute
    CoteOpp : idem pour coté opposé """

    def __init__(self,offset,Cote,CoteOpp,keepPosition,keepCurveLength,mvt=True,*_):
        self.offset=offset 
        self.mvt=mvt 
        self.keepCurveLength=keepCurveLength 
        self.keepPosition=keepPosition 
        self.function=-1 
        self.Cote=Cote 
        self.CoteOpp=CoteOpp 

    def execute(self,ajust=True,nMax=10,jointUpdate=False,*_):
        """ effectue tous les ajustements nécessaires à chaque exécution d'action """ 
        orientationOpp=getOrientation(Cote=self.CoteOpp)
        pos=getPosition(Cote=self.CoteOpp)
        lenC=getLength()
        lenChain=getJointChainLength()
        jointParam=JointParameters()
        clear()
        if self.mvt and ajust:
            setOrientation(0,self.Cote) # pour avoir un mouvement absolu qui ne dépende pas de la tangente
        clear()
        self.executeAction(nMax=nMax)
        clear()
        if self.function!=setOrientation and self.mvt and ajust:
            setOrientation(orientationOpp,Cote=self.CoteOpp) # orientation opposée ne doit pas avoir varié
        if self.mvt and ajust:
            newPos=getPosition(Cote=self.CoteOpp)
            newLen=getLength()
            if self.keepCurveLength:
                setLength(lenC)   
                #keepChainLengthValue(lenChain)   
            else:
                cL=getLength() # TODO vérifier que pas besoin Joint Chain
                rapport=cL/lenC        
            if self.keepPosition:        
                setCurvePosition(pos,Cote=self.CoteOpp) # posiiton du cote opposé doit rester fixe
        if jointUpdate:
            keepJointParameters(jointParam)
        clear()


    def executeAction(self,nMax=10,*_):
        """ simple exécution de la fonction concernée """
        raise NotImplementedError

class SimpleAction(Action):

    """ action simple de maya : translation, rotation ou scale
        non utilisé finalement car actions complexifiées """

    def __init__(self,offset,type,x,y,z,listOfSelection,Cote,CoteOpp,keepPosition,keepCurveLength=True,pivot=-1,mvt=True,*_): # pivot = position du pivot
        Action.__init__(self,offset,Cote,CoteOpp,keepPosition,keepCurveLength) 
        self.type=type # string : 't','r','s'
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
        
class FunctionAction(Action):

    """ actions définies par une fonction ayant un offset et eventuellement d'autres arguments """

    def __init__(self,offset,function,Cote,CoteOpp,keepPosition,keepCurveLength=True,args=[],mvt=True,*_):
        Action.__init__(self, offset,Cote,CoteOpp,keepPosition,keepCurveLength) 
        self.function=function
        self.args=args
        self.mvt=mvt

    def execute(self,ajust=True,nMax=10,*_):
        """ ajuste : boolean
            nMax : int, nombre max d'itérations (pour une fonction de type dichotomie) """
        Action.execute(self,ajust,nMax)

    def executeAction(self,nMax=10,*_):
        if self.args==[] :
            self.function(self.offset,nMax)
        else :
            self.function(self.offset,self.args,nMax)






        

    
        
    
