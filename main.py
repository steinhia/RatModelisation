# -*- coding: utf-8 -*-

#import maya.cmds as cmds
#import math      
import sys

sys.path.append("C:/Users/alexandra/Documents/alexandra/scripts")


path="C:/Users/alexandra/Documents/alexandra/scripts/"
execfile(path+"createModel.py")
execfile(path+"SliderGrp.py")
execfile(path+"mesures.py")


#TODO entre placage main et automatique, decalage du pivot ???? 
def mainFct():

    nameList=['Rat:obj55_VertebreL6_Exterior','Rat:obj53_VertebreL5_Exterior','Rat:obj51_VertebreL4_Exterior','Rat:obj50_VertebreL3_Exterior',\
               'Rat:obj98_VerterbreL2_Exterior','Rat:obj100_VertebreL1_Exterior','Rat:obj48_VertebreT13_Exterior','Rat:obj43_VertebreT12_Exterior',\
               'Rat:obj42_VertebreT11_Exterior','Rat:obj40_VertebreT10_Exterior','Rat:obj38_VertebreT9_Exterior','Rat:obj37_VertebreT8_Exterior',\
               'Rat:obj36_VertebreT7_Exterior','Rat:obj34_VertebreT6_Exterior','Rat:obj32_VertebreT5_Exterior','Rat:obj30_VertebreT4_Exterior',\
               'Rat:obj29_VertebreT3_Exterior','Rat:obj74_VertebreT2_Exterior','Rat:obj72_VertebreT1_Exterior',\
               'Rat:obj70_VertebreC7_Exterior','Rat:obj69_VertebreC6_Exterior','Rat:obj103_VertebreC5_Exterior','Rat:obj105_VertebreC4_Exterior', \
               'Rat:obj107_VertebreC3_Exterior','Rat:obj47_VertebreC2_Axis_Exterior','Rat:obj45_VertebreC1_Atlas_Exterior']
           
    tailList=['Rat:obj57_Sacrum_Exterior','Rat:obj59_VertebreCaudale1_Exterior','Rat:obj60_VertebreCaudale2_Exterior','Rat:obj61_VertebreCaudale3_Exterior',\
             'Rat:obj63_VertebreCaudale4_Exterior','Rat:obj64_VertebreCaudale5_Exterior','Rat:obj65_VertebreCaudale6_Exterior','Rat:obj66_VertebreCaudale7_Exterior',\
             'Rat:obj67_VertebreCaudale8_Exterior','Rat:obj68_VertebreCaudale9_Exterior','Rat:obj78_VertebreCaudale10_Exterior','Rat:obj79_VertebreCaudale11_Exterior',\
             'Rat:obj80_VertebreCaudale12_Exterior','Rat:obj81_VertebreCaudale13_Exterior','Rat:obj82_VertebreCaudale14_Exterior','Rat:obj83_VertebreCaudale15_Exterior',\
             'Rat:obj84_VertebreCaudale16_Exterior','Rat:obj85_VertebreCaudale17_Exterior','Rat:obj86_VertebreCaudale18_Exterior','Rat:obj87_VertebreCaudale19_Exterior',\
             'Rat:obj88_VertebreCaudale20_Exterior','Rat:obj89_VertebreCaudale21_Exterior','Rat:obj90_VertebreCaudale22_Exterior','Rat:obj91_VertebreCaudale23_Exterior',\
             'Rat:obj92_VertebreCaudale24_Exterior','Rat:obj93_VertebreCaudale25_Exterior','Rat:obj94_VertebreCaudale26_Exterior','Rat:obj95_VertebreCaudale27_Exterior',\
             'Rat:obj96_VertebreCaudale28_Exterior']

    #cmds.file("C:/Users/alexandra/Documents/alexandra/ScenesMaya/SqueletteRat.mb", o=True,s=False,f=True)
    ShowPolygons()
    clearVariables(nameList)
    # position des points sur la courbe
    pointOnCurveList=map(n2J,['L6','L3','T11','T8','T2','C3','C0'])
    createJointChain2(nameList,tailList)
    bindSkeleton(nameList,tailList)
    createCurve(pointOnCurveList,nameList)
    createClusters(nameList)
    defPivot()
    setPosture(0)
    #cmds.window(title ="Modelisation de la colonne du rat",le=50,te=50,width=400,height=450)
    sliderGrp=createWindows(nameList,tailList)
    #cmds.showWindow(sliderGrp.window)
    return sliderGrp
    
#sliderGrp=mainFct()


