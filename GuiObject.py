# -*- coding: utf-8 -*-
#import maya.cmds as cmds
#import math
import sys
#import time

sys.path.append("C:/Users/alexa/Documents/alexandra/scripts")


path="C:/Users/alexa/Documents/alexandra/scripts/"
execfile(path+"Action.py")
import time
import numpy as np
from scipy import polyfit
from scipy import stats


class GuiObject(object):

    def __init__(self,label,*_):
        self.label=label

    def create(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

# on lui associe forcement un slider et un texte (courbure, orientation)
# que des boutons reset
class Button(GuiObject):
    
    def __init__(self,label,label2,slider,sliderList,indiceText,valueReset,valueSetTo=0,slider2=-1,setOneFunction=-1,*_):
        GuiObject.__init__(self, label)
        self.label2=label2        
        self.slider=slider
        self.slider2=slider2
        self.sliderList=sliderList
        self.indiceText=indiceText
        self.valueReset=valueReset # pas 0 mais valeur du slider 2 au debut
        self.valueSetTo=valueSetTo # 0 ou autre
        self.setOneFunction=setOneFunction

      
    def create(self,*_):
        if self.slider!=-1:
            self.slider.create()
        else:
            cmds.text(label="")
        if self.slider2!=-1:
            self.slider2.create()
            # on associe chaque texte a son slider
            self.sliderList[self.indiceText].associate(self.slider,self.slider2)
        self.GuiButton=cmds.button(label=self.label,command=partial(self.update,self.valueReset,True)) 
        self.GuiButton=cmds.button(label=self.label2,command=partial(self.update,self.valueSetTo,True)) 


    def calcDroite(self,*_):
        slider=self.slider #slider1
        if slider!=-1:
            min=slider.minValue
            max=slider.maxValue
            valInit=slider.value
            x=[]
            y=[]
            for i in range(0,50):
                val=min+i*(max-min)/50.0
                slider.setValue(val)
                slider.update(False,True) # attention False necessaire
                x.append(val)
                # si ne veut pas actualiser, doit utiliser la fonction de calcul
                val=self.sliderList[self.indiceText].fct(self.sliderList[self.indiceText].args)
                y.append(val) # TODO comparer tps apres
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            if abs(1.0-abs(r_value))>0.01 or abs(slope)<0.1:
                print "pas de droite pour ",slider.label, r_value, slope, intercept
            else:
                print "droite ok",slider.label, r_value, slope, intercept
            if abs(slope)>0.1:
                slider.dte=[slope,intercept]
            else:
                slider.dte=[]
            slider.setValue(valInit)
            slider.update(False,True) # TODO le deuxieme false ?
            return slider.dte
        else:
            return -1

    def affectDroite(self,droite):
        self.slider.dte=droite

    # reset -> valueReset=2.53...
    # set to 0 -> valueSetTo=0
    def update(self,value,updateText=True,*_):
        currentValue=self.sliderValue()
        if(currentValue!=value):
            self.slider2.setValue(value)       
            self.slider2.update(True) # a changer
        if updateText:
            for i in self.sliderList :
                i.update(True)

    def reset(self):
        self.update(self.valueReset,True)

    def setTo(self):
        self.update(self.valueSetTo,True)

    def sliderValue(self):
        return self.slider2.sliderValue()

    def calcValue(self):
        return self.sliderList[self.indiceText].fct(self.sliderList[self.indiceText].args)

class ButtonGlobal(GuiObject):

    def __init__(self,label,nameList,pointOnCurveList=[]):
        GuiObject.__init__(self, label)
        #self.buttonList=buttonList
        self.GuiButton=cmds.button(label=self.label,command=partial(self.update)) 
        self.nameList=nameList
        self.pointOnCurveList=pointOnCurveList

    def update(self,*_):
        #cmds.window(title ="Modelisation de la colonne du rat",le=50,te=50,width=400,height=450)
        sliderGrp=mainFct()
        #cmds.showWindow(sliderGrp.window)

# valeur d'un champ a partir d'une fonction (courbure etc)
class SliderDuo(GuiObject):
    def __init__(self,label,fct,args,*_):
        GuiObject.__init__(self,label)
        self.fct=fct
        self.args=args
        self.slider=-1
        self.slider2=-1

    def associate(self,slider,slider2,*_):
        self.slider=slider
        self.slider2=slider2

    def update(self,slider1Update=True,*_):   
        if self.args==[]:
            value=self.fct()
        else :
            value=self.fct(self.args)
        if self.slider2!=-1:
            self.slider2.setValue(value)
            self.slider2.value=value
        if self.slider!=-1 and slider1Update: # TODO a verifier que sl1Upd pose pas de probleme
            a=self.slider.f(value)
            if a!=[]:
                self.slider.setValue(a)
                self.slider.value=a


class Slider(GuiObject):

    def __init__(self,label,action,minValue,maxValue,value,step,sliderList,*_):
        GuiObject.__init__(self,label)
        self.action=action
        self.minValue=minValue
        self.maxValue=maxValue
        self.value=value
        self.step=step
        self.sliderList=sliderList
        self.dte=[]

        
    def update(self,updateText=True,ajust=True,*_):
        raise NotImplementedError

    def setValue(self,val,*_):
        cmds.floatSliderGrp(self.GuiSlider,e=True,value=val)

    def getValue(self,*_):
        return self.value

    def sliderValue(self):
        return cmds.floatSliderGrp(self.GuiSlider, q=True, v=True)

    def create(self,*_):
        self.GuiSlider=cmds.floatSliderGrp(label=self.label, field=True,height=30, s=self.step, minValue=self.minValue, maxValue=self.maxValue, value=self.value , cc= partial(self.update,True,True)) # pas de dc car trop long      

    def f(self,x,*_):
        if self.dte==[]:
            return []
        elif self.dte[0] !=0 :
            return (float(x)-float(self.dte[1]))/float(self.dte[0])
        else :
            p("probleme polyfit",self.dte)
            return float(self.dte[1])


class SliderOffset(Slider):

    def __init__(self,label,action,minValue,maxValue,value,step,sliderList,*_):
        Slider.__init__(self, label,action,minValue,maxValue,value,step,sliderList)

    def create(self):
        Slider.create(self)
        
    def update(self,updateText=True,ajust=True,*_):
        t=time.time()
        val=self.sliderValue()
        diff=self.value-val
        self.value=val
        self.action.offset=diff
        if diff!=0 :
            self.action.execute(ajust)
            if updateText:
                for i in self.sliderList:
                        if i.slider!=self:
                            i.update(True)
                        else:
                            i.update(False)


    def sliderValue(self,*_):
        return Slider.sliderValue(self)

    def setActionWithoutMoving(self,testValue,ajust=True):
        self.action.offset=self.value-testValue
        self.value=testValue
        self.action.execute(ajust=ajust)


    def setValue(self,val,*_):
        Slider.setValue(self,val)

    def getValue(self,*_):
        return Slider.getValue(self)

    def f(self,x,*_):
        return Slider.f(self,x)

class SliderAbs(Slider):

    def __init__(self,label,action,minValue,maxValue,value,step,sliderList,*_):
        Slider.__init__(self, label,action,minValue,maxValue,value,step,sliderList)
   
    def create(self):
        Slider.create(self)

     
    def update(self,updateText=True,ajust=True,*_):
        self.value=self.sliderValue()
        self.action.offset=self.value
        self.action.execute(ajust)
        if updateText:
            for i in self.sliderList:
                    i.update(True)

    def setValue(self,val,*_):
        Slider.setValue(self,val)

    def getValue(self,*_):
        return Slider.getValue(self)

    def sliderValue(self,*_):
        return Slider.sliderValue(self)

    def f(self,x,*_):
        return Slider.f(self,x)

class CheckBox(GuiObject):

    def __init__(self,label,actionCheck,actionUnCheck,value,args=[],*_):
        GuiObject.__init__(self,label)
        self.actionCheck=actionCheck
        self.actionUnCheck=actionUnCheck
        self.value=value
        self.args=args

    def create(self):

        self.CheckBox=cmds.checkBox(label=self.label,onc=self.CheckFunction,ofc=self.UnCheckFunction,value=self.value)
        if(self.value):
            if self.args==[]:
                self.actionCheck.execute(ajust=False)
            else:
                self.actionCheck.execute(ajust=False,args=self.args)
        else:
            self.actionUnCheck.execute(ajust=False)
            
    def update(self,*_):
        # rien a faire
        a=1

    def CheckFunction(self,*_):
        if self.args==[]:
            self.actionCheck.execute()
        else:
            self.actionCheck.execute(self.args)
        self.value=True

    def UnCheckFunction(self,*_):
        self.actionUnCheck.execute()
        self.value=False


class RadioButtonGrp(GuiObject):

    def __init__(self,label,actionList,labelArray,numberOfRadioButtons,paramList):
        GuiObject.__init__(self,label)
        self.actionList=actionList
        self.labelArray=labelArray
        self.numberOfRadioButtons=numberOfRadioButtons
        self.paramList=paramList

    def create(self):
        if self.numberOfRadioButtons==2:
            self.RadioButton=cmds.radioButtonGrp( label=self.label, labelArray2=self.labelArray, numberOfRadioButtons=self.numberOfRadioButtons, on1=self.actionList[0],on2=self.actionList[1],select=1)
        else:
            self.RadioButton=cmds.radioButtonGrp( label=self.label, labelArray4=self.labelArray, numberOfRadioButtons=self.numberOfRadioButtons, on1=self.actionList[0],on2=self.actionList[1],on3=self.actionList[2],on4=self.actionList[3],select=1)



        






