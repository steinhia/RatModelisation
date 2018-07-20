# -*- coding: utf-8 -*-
  
import sys
sys.path.append("C:/Users/alexa/Documents/alexandra/scripts")



path="C:/Users/alexa/Documents/alexandra/scripts/"
execfile(path+"createModel.py")
execfile(path+"SliderGrp.py")
execfile(path+"mesures.py")
execfile(path+"EvalClass.py")

def createGraphicalElements(pointOnCurveList,nameList,tailList):
    # position des points sur la courbe
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
pointOnCurveList=['L6','L3','T13','T10','T4','C5','C0','Tete'] #200
#pointOnCurveList=['L6','L3','T13','T8','T4','C6','C0','Tete'] #100
#O pour image 100 pointOnCurveList=['L6','L2','T13','T8','T4','C5','C0','Tete'] 
#pointOnCurveList=['L6','L4','T13','T8','T3','C5','C0','MilTete','Tete'] # mieux T13 sinon bosse T2 attention
locatorList=[pointOnCurveList[i] for i in range(8) if i not in [1,3,5]]

  
maxCV = MaxCV()
sliderGrp=mainFct(pointOnCurveList,locatorList)
droites=sliderGrp.droites

length=getLength()
CVpos=calcPosCV()
jtPos=JointPositions()
par=calcCVParameters() 
jtParam=JointParameters()


#setAllCurves()
for i in range(0,1):
    t=time.time()
    cmds.currentTime(200, edit=True )
    resetCurve(length,CVpos,jtPos)
    sliderGrp=mainFct(pointOnCurveList,locatorList,reset=True,droites=droites)
    checkParameters(par,CVpos,jtPos,jtParam)
    #print getCLen()
    Placement(sliderGrp.sliderList,length,CVpos,jtPos,save=True)
    #print getCLen()
    cmds.hide('curveShape2->arcLengthDimension2')
    cmds.hide('curveShape1->arcLengthDimension1')
#sliderGrp.do("scale",10)
#sliderGrp.do("z",-5)

#del pointOnCurveList
#del locatorList
#maya.mel.eval("NURBSSmoothnessFineOptions;")
#maya.mel.eval("performDisplaySmoothnessFine 1;")
#maya.mel.eval("displaySmoothnessFineCallback OptionBoxWindow|formLayout128|tabLayout9|formLayout130|tabLayout10|columnLayout62 1; hideOptionBox;")
#maya.mel.eval("editMenuUpdate MayaWindow|mainEditMenu;")
#maya.mel.eval("if (`window -exists OptionBoxWindow`) deleteUI -window OptionBoxWindow;")
#maya.mel.eval("onCloseCommand;")
#maya.mel.eval("saveOptionBoxSize();")



