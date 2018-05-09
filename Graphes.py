import maya.cmds as cmds
import math
import sys
import time

sys.path.append("C:/Users/alexandra/Documents/alexandra/scripts")


path="C:/Users/alexandra/Documents/alexandra/scripts/"
import main
reload(main)
from random import random
execfile(path+"Short.py")

def graphe(buttonName):
    sliderGrp=main.mainFct()
    button=sliderGrp.string2button(buttonName)
    slider=button.slider
    min=slider.minValue
    max=slider.maxValue
    pas=(max-min)/50.0
    x=[]
    y=[]
    for i in range(0,50):
        slider.setValue(min+i*(max-min)/50.0)
        slider.update()
        x.append(min+i*(max-min)/50.0)
        y.append(button.slider2.sliderValue())
    slider.setValue(0.0)
    slider.update()
    #print x
    #print y
    # approximatif pour l'instant
    a=(y[-1]-y[0])/(x[-1]-x[0])
    b=y[25]-a*x[25]
    #print buttonName
    #print a
    #print b
    return [a,b]
    
#graphe("rot cervicale")
#graphe("rot dorsale")
#graphe("rot lombaire")

def essai():
    sliderGrp=main.mainFct()
    button=sliderGrp.string2button("rot cervicale")
    slider=button.slider
    min=slider.minValue
    max=slider.maxValue
    for i in range(0,400):
        slider.setValue(min+i*(max-min)/400.0)
        slider.update()
    slider.setValue(0.0)
    slider.update()
    t=time.time()
    for i in range(0,20):
        slider.setValue(min+i*(max-min)/20.0)
        slider.update()
    p("TIME 50 !!!!!!!!!!!!!!! ",time.time()-t)

    sliderGrp=main.mainFct()
    button=sliderGrp.string2button("rot cervicale")
    slider=button.slider
    for i in range(0,1):
        slider.setValue(min+i*(max-min)/1.0)
        slider.update()
    slider.setValue(0.0)
    slider.update()
    t=time.time()
    for i in range(0,20):
        slider.setValue(min+i*(max-min)/20.0)
        slider.update()
    p("time 5 ",time.time()-t)

essai()
    
    