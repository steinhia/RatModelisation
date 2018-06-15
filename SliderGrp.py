# -*- coding: utf-8 -*-
path="C:/Users/alexandra/Documents/alexandra/scripts/"
execfile(path+"GuiObject.py")
execfile(path+"Mouvements.py")
execfile(path+"affichage.py")

class SliderGrp(object):
    def __init__(self,title,buttonList,checkBoxList,nameList,pointOnCurveList,locatorList):
        self.buttonList=buttonList
        self.nameList=nameList
        self.pointOnCurveList=list(pointOnCurveList)
        self.locatorList=list(locatorList)
        self.window = cmds.window('window1',title =title,le=50,te=50,width=400,height=450)
        self.column = cmds.columnLayout()
        cmds.text("\nParametres de courbure ")
        cmds.rowColumnLayout(numberOfColumns=4,columnWidth=[(1,300),(2,300),(4,50),(5,50)])

        for i in range(2):
            buttonList[i].create()
        cmds.setParent('..')
        cmds.text("\nMouvement de la colonne")
        cmds.rowColumnLayout(numberOfColumns=4,columnWidth=[(1,300),(2,300),(4,50),(5,50)])
        #param=calcParameters()

        for i in range(2,12):
            buttonList[i].create()
            buttonList[i].calcDroite()
        #checkParameters(param)

        cmds.setParent('..')
        cmds.text("\nParametres de la courbe")
        cmds.rowColumnLayout(numberOfColumns=4,columnWidth=[(1,200),(2,300),(4,50),(5,50)])
        for i in range(12,len(buttonList)):
            buttonList[i].create()
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=1,columnWidth=[(1,300)])

        # CheckBox
        cmds.setParent('..')
        cmds.rowColumnLayout( numberOfColumns=2,columnWidth=[(1, 200),(2,200),(3,200)])
        for checkbox in checkBoxList : 
            checkbox.create() 
        cmds.textFieldGrp( label='Select', text='???',editable=True , cc=select)
        cmds.showWindow(self.window)
        for sliderDuo in self.buttonList[0].sliderList:
            sliderDuo.update(True)


    def do(self,string,value,updateText=True):
        button=self.string2button(string)
        button.slider2.setValue(value)
        button.slider2.update(updateText)

    def string2num(self,string):
        string=string.lower()
        if "courbure c" in string :
            return 0
        #if ("courbure d" in string) or ("courbure t" in string):
        #    return [1]
        if "courbure l" in string :
            return 1
        if "rot cervicale g" in string :
            return 2
        if "rot c" in string :
            return 3
        if "rot dorsale g" in string :
            return 4
        if "rot d" in string :
            return 5
        if "rot lombaire g" in string :
            return 6
        if "rot l" in string :
            return 7
        if "compression g" in string :
            return 8
        if "comp" in string :
            return 9
        if "rot tete g" in string:
            return 10
        if "rot t" in string:
            return 11
        if "x" in string :
            return 12
        if "y" in string :
            return 13
        if "z" in string :
            return 14
        if "scale" in string :
            return 15
        if "posture" in string :
            return 16
        if "orientation" in string :
            return 17

    def string2button(self,string):
        return self.buttonList[self.string2num(string)]

    #def Reset(self):
    #    for button in self.buttonList[:12]:
    #        button.slider.setValue(0)
    #    for sliderDuo in self.buttonList[0].sliderList:
    #        sliderDuo.update(True)


def clearSliderVariables(): 
    blinnList=cmds.ls('*blinn*')
    for i in blinnList:
        if(cmds.objExists(i)):
            cmds.delete(i)
    if (cmds.window("window1", exists=True)):
        cmds.deleteUI("window1") 
    if(cmds.objExists('sliderGrp')):
        cmds.delete('sliderGrp')

def courbureButton(sliderList,crvInfos,i,sliderName,min,max,min2,max2,value,step,influence,valueReset=0,getFunction=0,setOneFunction=setOneRot,Cote=""):
    getValue=getFunction()
    action = SimpleAction(0,crvInfos,"t",0,2,0,influence,Cote=Cote,keepPosture=False,keepPosition=False,keepCurveLength=False)
    slider=SliderOffset(sliderName,action,min,max,value,step,sliderList)
    action2 = FunctionAction(getValue,crvInfos,setRot,args=[slider,getFunction,[],crvInfos,min,max],Cote=Cote,keepPosture=False,keepPosition=False,mvt=True,keepCurveLength=False)
    slider2=SliderAbs(sliderName,action2,-100,100,getValue,step,sliderList)
    return Button("reset","set to 0",slider,sliderList,i,getValue,0,slider2,setOneFunction)

def postureButton(sliderList,crvInfos,i,sliderName,min,max,step,influence,valueReset=0,pivot=-1,valueSetTo=0,functionSet=0,args=[],keepPosture=True,keepPosition=True,keepCurveLength=True,name2="set to 0",Cote=""):
    action2 = FunctionAction(valueReset,crvInfos,functionSet,Cote=Cote,keepPosture=keepPosture,keepPosition=keepPosition,keepCurveLength=keepCurveLength,args=crvInfos,mvt=True)
    slider2=SliderAbs(sliderName,action2,min,max,valueReset,step,sliderList)
    return Button("reset",name2,-1,sliderList,i,valueReset,valueSetTo,slider2)
 
def functionButton(sliderList,crvInfos,i,sliderName,min,max,min2,max2,value,step,function,valueReset=0,getFunction=0,getFunctionArgs=[],setOneFunction=setOneRot,keepPosition=True,keepPosture=True,Cote=""):
    getValue=getFunction(getFunctionArgs)
    action=FunctionAction(value,crvInfos,function,keepPosture=False,keepPosition=True,Cote=Cote)
    slider=SliderOffset(sliderName,action,min,max,value,step,sliderList)
    action2 = FunctionAction(getValue,crvInfos,setRot,args=[slider,getFunction,getFunctionArgs,crvInfos,min,max],mvt=True,keepPosture=False,keepPosition=True,Cote=Cote)
    slider2=SliderAbs(sliderName,action2,min2,max2,getValue,step,sliderList)
    return Button("reset","set to 0",slider,sliderList,i,getValue,0,slider2,setOneFunction)     

def functionCheckBox(label,crvInfos,functionCheck,functionUnCheck,value,args=[]):
    actionCheck=FunctionAction(value,crvInfos,functionCheck,Cote="",keepPosture=False,keepPosition=True,args=args,mvt=False)
    actionUnCheck=FunctionAction(not value,crvInfos,functionUnCheck,Cote="",keepPosture=False,keepPosition=True,args=args,mvt=False)
    return CheckBox(label,actionCheck,actionUnCheck,value)

       
def createWindows(nameList,pointOnCurveList,locatorList):
    clearSliderVariables()
    crvInfos=[getCurveLength(),getCurvePosition(),calcPosture(),getChainLength(),getCLen()]

    #liste des textes (courbures etc)
    names=["courbure Cervicale ","courbure Lombaire ","rot Cervicale G ","rot Cervicale B ", \
          "rot Dorsale G ","rot Dorsale B ","rot Lombaire G ","rot Lombaire B ","compression gd","compression ","rot TGD","rot THB","x ","y ","z ","scale ","posture ","orientation"]
    fcts=[calcLordoseC,calcLordoseL,angleCGD,\
              angleCHB,angleDGD,angleDHB,angleLGD,angleLHB,angleCompGD,angleComp,angleTGD,angleTHB,\
              getX,getY,getZ,getCurveLength,calcPosture,calcOrientation]   
    setFcts=[rotCGD,rotCHB,rotDGD,rotDHB,rotLGD,rotLHB,rotCompGD,rotComp,rotTGD,rotTHB,setX,setY,setZ,keepLengthValue,setPosture,setOrientation]
    
    #liste mise a jour a chaque modification
    sliderList=[]
    for i,name in enumerate(names):
        sliderList.append(SliderDuo(name,fcts[i],crvInfos))

    buttonList=[]
    # courbures cervicale, dorsale et lombaire
    buttonList.append(courbureButton(sliderList,crvInfos,0,names[0],-1,1,-3,3,0,0.00000001,['curve1.cv[5]'],getFunction=fcts[0]))
    buttonList.append(courbureButton(sliderList,crvInfos,1,names[1],-3,3,-3,3,0,0.00001,['curve1.cv[0]'],getFunction=fcts[1]))

    # TODO garder les 2 keep=False fait planter les tests
    # cervicales GD HB TODO position tete par rapport  au sol ou aux dorsales (tenir tete droite) -> 2 fonctions align with et setstraight ?
    buttonList.append(functionButton(sliderList,crvInfos,2,names[2],-20,15,-60,60,0,0.00000001,setFcts[0],getFunction=fcts[2],Cote="L"))
    buttonList.append(functionButton(sliderList,crvInfos,3,names[3],-20,15,-60,60,0,0.00000001,setFcts[1],getFunction=fcts[3],Cote="L"))

    # dorsales GD HB -> dorsales HB = dorsales + lombaires
    buttonList.append(functionButton(sliderList,crvInfos,4,names[4],-8,8,-30,50,0,0.00000001,setFcts[2],getFunction=fcts[4],Cote="C"))
    buttonList.append(functionButton(sliderList,crvInfos,5,names[5],-8,8,-30,50,0,0.00000001,setFcts[3],getFunction=fcts[5],Cote="C"))

    #lombaires
    buttonList.append(functionButton(sliderList,crvInfos,6,names[6],-10,10,-60,60,0,0.00000001,setFcts[4],getFunction=fcts[6],Cote="C"))
    buttonList.append(functionButton(sliderList,crvInfos,7,names[7],-10,10,-60,60,0,0.00000001,setFcts[5],getFunction=fcts[7],Cote="C"))

    # compression
    buttonList.append(functionButton(sliderList,crvInfos,8,names[8],-200,100,-40,40,0,0.00000001,setFcts[6],crvInfos,getFunction=fcts[8],getFunctionArgs=crvInfos,Cote=""))
    buttonList.append(functionButton(sliderList,crvInfos,9,names[9],0,40,0,80,0,0.00000001,setFcts[7],crvInfos,getFunction=fcts[9],getFunctionArgs=crvInfos,Cote=""))

    #tete
    buttonList.append(functionButton(sliderList,crvInfos,10,names[10],-18,10,-90,90,0,0.00000001,setFcts[8],getFunction=angleTGD,Cote="L"))
    buttonList.append(functionButton(sliderList,crvInfos,11,names[11],-18,10,-90,90,0,0.00000001,setFcts[9],getFunction=angleTHB,Cote="L")) 


    # position
    buttonList.append(postureButton(sliderList,crvInfos,12,names[12],-60,60,0.00000001,["curve1"],crvInfos[1][0],functionSet=setFcts[10],keepPosition=False,keepPosture=False,keepCurveLength=False))
    buttonList.append(postureButton(sliderList,crvInfos,13,names[13],-60,60,0.00000001,["curve1"],crvInfos[1][1],functionSet=setFcts[11],keepPosition=False,keepPosture=False,keepCurveLength=False))
    buttonList.append(postureButton(sliderList,crvInfos,14,names[14],-60,60,0.00000001,["curve1"],crvInfos[1][2],functionSet=setFcts[12],keepPosition=False,keepPosture=False,keepCurveLength=False))
    # scaling
    buttonList.append(postureButton(sliderList,crvInfos,15,names[15],1,30,0.00000001,["curve1"],valueReset=getCurveLength(),valueSetTo=1,functionSet=setFcts[13],keepCurveLength=False,keepPosition=True,keepPosture=True,args=[],name2="set to 1"))
    # posture generale
    buttonList.append(postureButton(sliderList,crvInfos,16,names[16],-90,90,0.00000001,["curve1"],0,crvInfos[1],functionSet=setFcts[14],args=[],keepPosture=False,keepPosition=True,keepCurveLength=True))
    buttonList.append(postureButton(sliderList,crvInfos,17,names[17],-180,180,0.00000001,["curve1"],0,crvInfos[1],functionSet=setFcts[15],args=[],keepPosture=False,keepPosition=True,keepCurveLength=True))

    # checkBox pour la gestion d'affichage
    checkBoxList=[]
    checkBoxList.append(functionCheckBox('Hide circles',crvInfos,HideCircles,ShowCircles,True))
    checkBoxList.append(functionCheckBox('Hide rest of skeleton',crvInfos,HideRestOfSkeleton,ShowRestOfSkeleton,True))
    checkBoxList.append(functionCheckBox('Hide head and tail',crvInfos,HideHeadAndTail,ShowHeadAndTail,True))
    checkBoxList.append(functionCheckBox('Hide joints',crvInfos,HideSkeletonJoints,ShowSkeletonJoints,True))
    checkBoxList.append(functionCheckBox('Hide polygons',crvInfos,HidePolygons,ShowPolygons,True)) 
    # on cree le sliderGrp a partir de tous les sliders
    sliderGrp1=SliderGrp("Modelisation de la colonne du rat",buttonList,checkBoxList,nameList,pointOnCurveList,locatorList)

    colorSkeleton(nameList)
    return sliderGrp1



