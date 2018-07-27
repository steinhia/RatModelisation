# -*- coding: utf-8 -*-

execfile(path+"Action.py")
import time
import numpy as np
from scipy import stats


class GuiObject(object):
    """ classe des différents objets de l'interface graphique """

    def __init__(self,label,*_):
        self.label=label

    def create(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

class Group(GuiObject):
    
    def __init__(self,label,slider,sliderList,slider2=-1,corrArgs=[],*_):
        GuiObject.__init__(self, label)     
        self.slider=slider # slider commandant un mouvement absolu
        self.slider2=slider2  # slider cherchant un angle par dichotomie en faisant bouger le premier slider
        self.sliderList=sliderList # liste des autres groupes de sliders pour la mise à jour
        self.corrArgs=corrArgs

      
    def create(self,*_):
        if self.slider!=-1: # certaines fonctions sont directes et ne nécessitent pas de premier slider
            self.slider.create()
        else:
            cmds.text(label="")
        if self.slider2!=-1:
            self.slider2.create()
            # on associe chaque texte a son slider
            self.sliderList[numSlider(self.label)].associate(self.slider,self.slider2)
        if "HB" in self.label or "GD" in self.label: # bouton de correction et set angle calculé à partir des localisateurs
            self.GuiButtonCorr=cmds.button(label="Corr",command=partial(self.updateCorr,self.corrArgs))
            self.GuiButtonSetAngle=cmds.button(label="SetAngle",command=partial(setAngle,self.sliderList,self.label))
        # orientation et position
        elif numSlider(self.label)!=-1:
            self.GuiButtonSetAngle=cmds.button(label="Set",command=partial(setParam,self.sliderList,self.label)) # calculés avec les loc.
            if self.label!="Length":
                self.GuiButtonSetAngle=cmds.button(label="Set L",command=partial(setParam,self.sliderList,self.label,"L"))
                self.GuiButtonSetAngle=cmds.button(label="Set C",command=partial(setParam,self.sliderList,self.label,"C"))

    def calcDroite(self,*_):
        """ calcule une régression de l'angle en fct de la valeur du slider de gauche """
        slider=self.slider #slider1
        if slider!=-1:
            min=slider.minValue
            max=slider.maxValue
            valInit=slider.value
            x=[]
            y=[]
            for i in range(0,10):
                val=min+(i+20)*(max-min)/50.0 # pas de valeurs extremes
                slider.setValue(val)
                slider.update(False,True)
                valy=angleCrv(self.label)
                slider2=self.sliderList[numSlider(self.label)].slider2
                if (slider2!=-1 and valy<slider2.maxValue and valy>slider2.minValue) or True:
                    x.append(val)
                    y.append(valy)
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            if abs(1.0-abs(r_value))>0.01 or abs(slope)<0.02:
                print("pas de droite pour ",slider.label, r_value, slope, intercept)
            else:
                print("droite ok",slider.label, r_value, slope, intercept)
            if abs(slope)>0.1:
                slider.dte=[slope,intercept]
            else:
                slider.dte=[]
            slider.setValue(valInit)
            slider.update(False,True) 
            return slider.dte
        else:
            return -1

    def affectDroite(self,droite):
        """ affecte la droite dejà calculée précédemment """
        self.slider.dte=droite


    def updateCorr(self,updateText=True,*_):
        """ callback du bouton de correction """
        if "HB" in self.label or "GD" in self.label:
            corr(self.sliderList,self.label)
            if updateText:
                for i in self.sliderList :
                    i.update(True)


    def sliderValue(self):
        """ valeur du slider """
        return self.slider2.sliderValue()

    def calcValue(self):
        """ calcul de l'angle correspondant au slider """
        return self.sliderList[numSlider(self.label)].fct(self.label)


class SliderDuo(GuiObject):
    """ groupement du slider de gauche et du slider de droite utilisé pour mettre à jour les sliders"""
    def __init__(self,label,fct,args,*_):
        GuiObject.__init__(self,label)
        self.fct=fct
        self.slider=-1
        self.slider2=-1

    def associate(self,slider,slider2,*_):
        """ associe les sliders à l'objet, car doit créer les sliderDuo avant les slider eux memes, 
        pour pouvoir leur passer la lsite en argument """
        self.slider=slider
        self.slider2=slider2

    def update(self,slider1Update=True,*_):
        """ met à jour les 2 sliders """
        if "HB" in self.label or "GD" in self.label:
            value=angleCrv(self.label)
        else:
            value=self.fct()
        if self.slider2!=-1:
            self.slider2.setValue(value)
            self.slider2.value=value
        if self.slider!=-1 and slider1Update: 
            a=self.slider.f(value)
            #if a>self.slider.maxValue: # décale pour la suite
            #    a=self.slider.maxValue
            #if a<self.slider.minValue:
            #    a=self.slider.minValue              
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
        self.sliderList=sliderList # liste des autres sliderDuo pour la mise à jour
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
        """ crée l'objet graphique """
        self.GuiSlider=cmds.floatSliderGrp(label=self.label, field=True,height=30, s=self.step, minValue=self.minValue, maxValue=self.maxValue, value=self.value , cc= partial(self.update,True,True,30)) # pas de dc car trop long      

    def f(self,x,*_):
        """ approximation de la valeur du slider de gauche nécessaire pour obtenir l'angle voulu
        x : float, valeur du paramètre cherchée """
        if self.dte==[]:
            return []
        elif self.dte[0] !=0 :
            return (float(x)-float(self.dte[1]))/float(self.dte[0])
        else :
            print("probleme polyfit",self.dte)
            return float(self.dte[1])


class SliderOffset(Slider):

    def __init__(self,label,action,minValue,maxValue,value,step,sliderList,*_):
        Slider.__init__(self, label,action,minValue,maxValue,value,step,sliderList)

    def create(self):
        Slider.create(self)
        
    def update(self,updateText=True,ajust=True,joint1Update=True,*_):
        """ effectue l'action et met tous les sliders à jour après un mouvement d'un slider 
        updateText : boolean, met les sliders à jour
        ajust : boolean, effectue les opérations d'ajustement ou pas """
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
                            sl2=i.slider2
                            # si depasse la valeur limite a droite (angles) , on affecte l'angle limite, pas encore testé
                            val2=sl2.value
                            #if val2>=sl2.maxValue or val2<=sl2.minValue:
                            #    sl2.setValue(val2)
                            #    sl2.update()

    def sliderValue(self,*_):
        return Slider.sliderValue(self)

    def setActionWithoutMoving(self,testValue,ajust=True):
        """ effectue l'action sans bouger les slider """
        self.action.offset=(self.value-testValue)
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

     
    def update(self,updateText=True,ajust=True,nMax=10,*_):
        """ fonction callback après mouvement du second slider """
        self.value=self.sliderValue()
        self.action.offset=self.value 
        self.action.execute(ajust,nMax)
        if updateText:
            for i in self.sliderList:
                if i.slider2!=self:
                    i.update(True)
                else:
                    i.update(False)


    def setValue(self,val,*_):
        Slider.setValue(self,val)

    def getValue(self,*_):
        return Slider.getValue(self)

    def sliderValue(self,*_):
        return Slider.sliderValue(self)

    def f(self,x,*_):
        return Slider.f(self,x)

class CheckBox(GuiObject):
    """ checkbox d'affichage """
    
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

    """ boutons utilisés pour choisir les paramètres d'affichage du plan """

    def __init__(self,label,actionList,labelArray,numberOfRadioButtons,paramList):
        GuiObject.__init__(self,label)
        self.actionList=actionList # liste des actions à effectuer
        self.labelArray=labelArray
        self.numberOfRadioButtons=numberOfRadioButtons

    def create(self):
        if self.numberOfRadioButtons==2:
            self.RadioButton=cmds.radioButtonGrp( label=self.label, labelArray2=self.labelArray, numberOfRadioButtons=self.numberOfRadioButtons, on1=self.actionList[0],on2=self.actionList[1],select=1)
        else:
            self.RadioButton=cmds.radioButtonGrp( label=self.label, labelArray4=self.labelArray, numberOfRadioButtons=self.numberOfRadioButtons, on1=self.actionList[0],on2=self.actionList[1],on3=self.actionList[2],on4=self.actionList[3],select=1)



        






