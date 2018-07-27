# -*- coding: utf-8 -*-
def defPath():
    return "C:/Users/alexa/Documents/alexandra/spine/"
path=defPath()  
execfile(path+"createModel.py")
execfile(path+"SliderGrp.py")
execfile(path+"mesures.py")
execfile(path+"EvalClass.py")

def createGraphicalElements(pointOnCurveList,nameList,tailList):

    """ crée les éléments graphiques, joints, courbe etc """
    pointOnCurveList=map(n2J,pointOnCurveList)
    createJointChain(nameList,tailList)
    bindSkeleton(nameList,tailList)
    createCurve(pointOnCurveList,nameList)
    colorSkeleton(nameList)


def mainFct(pointOnCurveList=['L6','L3','T11','T8','T2','C4','C0'],locatorList=['L6','L3','T8','T2','C0'],reset=False,droites=[]):

    nameList=['obj55_VertebreL6_Exterior','obj53_VertebreL5_Exterior','obj51_VertebreL4_Exterior','obj50_VertebreL3_Exterior',\
               'obj98_VerterbreL2_Exterior','obj100_VertebreL1_Exterior','obj48_VertebreT13_Exterior','obj43_VertebreT12_Exterior',\
               'obj42_VertebreT11_Exterior','obj40_VertebreT10_Exterior','obj38_VertebreT9_Exterior','obj37_VertebreT8_Exterior',\
               'obj36_VertebreT7_Exterior','obj34_VertebreT6_Exterior','obj32_VertebreT5_Exterior','obj30_VertebreT4_Exterior',\
               'obj29_VertebreT3_Exterior','obj74_VertebreT2_Exterior','obj72_VertebreT1_Exterior',\
               'obj70_VertebreC7_Exterior','obj69_VertebreC6_Exterior','obj103_VertebreC5_Exterior','obj105_VertebreC4_Exterior', \
               'obj107_VertebreC3_Exterior','obj47_VertebreC2_Axis_Exterior','obj45_VertebreC1_Atlas_Exterior']
           
    tailList=['obj57_Sacrum_Exterior','obj59_VertebreCaudale1_Exterior','obj60_VertebreCaudale2_Exterior','obj61_VertebreCaudale3_Exterior',\
             'obj63_VertebreCaudale4_Exterior','obj64_VertebreCaudale5_Exterior','obj65_VertebreCaudale6_Exterior','obj66_VertebreCaudale7_Exterior',\
             'obj67_VertebreCaudale8_Exterior','obj68_VertebreCaudale9_Exterior','obj78_VertebreCaudale10_Exterior','obj79_VertebreCaudale11_Exterior',\
             'obj80_VertebreCaudale12_Exterior','obj81_VertebreCaudale13_Exterior','obj82_VertebreCaudale14_Exterior','obj83_VertebreCaudale15_Exterior',\
             'obj84_VertebreCaudale16_Exterior','obj85_VertebreCaudale17_Exterior','obj86_VertebreCaudale18_Exterior','obj87_VertebreCaudale19_Exterior',\
             'obj88_VertebreCaudale20_Exterior','obj89_VertebreCaudale21_Exterior','obj90_VertebreCaudale22_Exterior','obj91_VertebreCaudale23_Exterior',\
             'obj92_VertebreCaudale24_Exterior','obj93_VertebreCaudale25_Exterior','obj94_VertebreCaudale26_Exterior','obj95_VertebreCaudale27_Exterior',\
             'obj96_VertebreCaudale28_Exterior']

    if not reset:
        ShowPolygons()
        clearVariables(nameList)
        createGraphicalElements(pointOnCurveList,nameList,tailList)
    sliderGrp=createWindows(nameList,pointOnCurveList,locatorList,droites)
    return sliderGrp


nameList=['obj55_VertebreL6_Exterior','obj53_VertebreL5_Exterior','obj51_VertebreL4_Exterior','obj50_VertebreL3_Exterior',\
            'obj98_VerterbreL2_Exterior','obj100_VertebreL1_Exterior','obj48_VertebreT13_Exterior','obj43_VertebreT12_Exterior',\
            'obj42_VertebreT11_Exterior','obj40_VertebreT10_Exterior','obj38_VertebreT9_Exterior','obj37_VertebreT8_Exterior',\
            'obj36_VertebreT7_Exterior','obj34_VertebreT6_Exterior','obj32_VertebreT5_Exterior','obj30_VertebreT4_Exterior',\
            'obj29_VertebreT3_Exterior','obj74_VertebreT2_Exterior','obj72_VertebreT1_Exterior',\
            'obj70_VertebreC7_Exterior','obj69_VertebreC6_Exterior','obj103_VertebreC5_Exterior','obj105_VertebreC4_Exterior', \
            'obj107_VertebreC3_Exterior','obj47_VertebreC2_Axis_Exterior','obj45_VertebreC1_Atlas_Exterior']
pointOnCurveList=['L6','L2','T12','T8','T3','C6','C0','Tete'] 
locatorList=[pointOnCurveList[i] for i in range(8) if i not in [1,3,5]]

  
maxCV = MaxCV()
sliderGrp=mainFct(pointOnCurveList,locatorList)
droites=sliderGrp.droites

length=getLength()
CVpos=calcPosCV()
jtPos=JointPositions()
par=calcCVParameters() 
jtParam=JointParameters()


#setAllCurves() # rétablit les anciennes courbes 
for i in range(0,1):
    cmds.currentTime(110, edit=True ) # choisit la frame 
    resetCurve(length,CVpos,jtPos) # rétablit la courbe dans sa position d'origine
    sliderGrp=mainFct(pointOnCurveList,locatorList,reset=True,droites=droites) # crée les éléments graphiques du maillage et la Gui
    checkParameters(par,CVpos,jtPos,jtParam) # vérifie la stabilité
    Placement(sliderGrp.sliderList,length,CVpos,jtPos,save=True) # place la courbe 
    cmds.hide('curveShape2->arcLengthDimension2')
    cmds.hide('curveShape1->arcLengthDimension1')


cmds.displaySmoothness('curveShape1',full=True,du=2,dv=2,pw=16,ps=4)



