# -*- coding: utf-8 -*-
path="C:/Users/alexa/Documents/alexandra/scripts/"
execfile(path+"GuiObject.py")
execfile(path+"Mouvements.py")
execfile(path+"affichage.py")

class SliderGrp(object):
    def __init__(self,title,buttonList,checkBoxList,nameList,pointOnCurveList,locatorList,planesList,droites=[]):
        self.buttonList=buttonList
        self.sliderList=self.buttonList[0].sliderList
        self.droites=droites
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
        cmds.rowColumnLayout(numberOfColumns=5,columnWidth=[(1,300),(2,300),(4,50),(5,50),(6,50)])

        if self.droites==[]:
            for i in range(2,12):
                buttonList[i].create()
                self.droites.append(buttonList[i].calcDroite())
        else :
            for i in range(2,12):
                buttonList[i].create()
                buttonList[i].affectDroite(self.droites[i-2])
        #checkParameters(param)

        cmds.setParent('..')
        cmds.text("\nParametres de la courbe")
        cmds.rowColumnLayout(numberOfColumns=4,columnWidth=[(1,200),(2,300),(4,50),(5,50),(6,50)])
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
        cmds.text("\n")

        # Planes
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=1)#,columnWidth=[(1, 200),(2,500)])

        for buttonRadio in planesList:
            buttonRadio.create()


    def do(self,string,value,updateText=True,nMax=30):
        button=self.string2button(string)
        button.slider2.setValue(value)
        button.slider2.update(updateText,nMax=nMax)

    def string2num(self,string):
        string=string.lower()
        if "courbure c" in string :
            return 0
        #if ("courbure d" in string) or ("courbure t" in string):
        #    return [1]
        if "courbure l" in string :
            return 1
        if "rotcgd" in string :
            return 2
        if "rotchb" in string :
            return 3
        if "rotdgd" in string :
            return 4
        if "rotdhb" in string :
            return 5
        if "rotlgd" in string :
            return 6
        if "rotlhb" in string :
            return 7
        if "compression g" in string :
            return 8
        if "comp" in string :
            return 9
        if "rottgd" in string:
            return 10
        if "rotthb" in string:
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
        else:
            print "mauvaise operation : ",string

    def string2button(self,string):
        return self.buttonList[self.string2num(string)]


def clearSliderVariables(): 
    blinnList=cmds.ls('*blinn*')
    for i in blinnList:
        if(cmds.objExists(i)):
            cmds.delete(i)
    if (cmds.window("window1", exists=True)):
        cmds.deleteUI("window1") 
    if(cmds.objExists('sliderGrp')):
        cmds.delete('sliderGrp')

def courbureGroup(sliderList,i,sliderName,min,max,min2,max2,value,step,influence,valueReset=0,getFunction=0,setOneFunction=setOneRot,Cote="",CoteOpp=""):
    getValue=getFunction()
    action = SimpleAction(0,"t",0,2,0,influence,Cote=Cote,CoteOpp=CoteOpp,keepPosture=False,keepPosition=False,keepCurveLength=False)
    slider=SliderOffset(sliderName,action,min,max,value,step,sliderList)
    action2 = FunctionAction(getValue,setRot,args=[slider,getFunction,[],[],min,max],Cote=Cote,CoteOpp=CoteOpp,keepPosture=False,keepPosition=False,mvt=True,keepCurveLength=False)
    slider2=SliderAbs(sliderName,action2,-100,100,getValue,step,sliderList)
    return Group("reset","set to 0",slider,sliderList,i,getValue,0,slider2,setOneFunction)

def postureGroup(sliderList,i,sliderName,min,max,step,influence,valueReset=0,pivot=-1,valueSetTo=0,functionSet=0,args=[],keepPosture=True,keepPosition=True,keepCurveLength=True,name2="set to 0",Cote="",CoteOpp=""):
    action2 = FunctionAction(valueReset,functionSet,Cote=Cote,CoteOpp=CoteOpp,keepPosture=keepPosture,keepPosition=keepPosition,keepCurveLength=keepCurveLength,args=[],mvt=True)
    slider2=SliderAbs(sliderName,action2,min,max,valueReset,step,sliderList)
    return Group("reset",name2,-1,sliderList,i,valueReset,valueSetTo,slider2)
 
def functionGroup(sliderList,i,sliderName,min,max,min2,max2,value,step,function,valueReset=0,getFunction=0,setOneFunction=setOneRot,keepPosition=True,keepPosture=True,Cote="",CoteOpp="",functionCorr=-1):
    getValue=getFunction()
    action=FunctionAction(value,function,keepPosture=False,keepPosition=True,Cote=Cote,CoteOpp=CoteOpp)
    slider=SliderOffset(sliderName,action,min,max,value,step,sliderList)
    action2 = FunctionAction(getValue,setRot,args=[slider,getFunction,[],[],min,max],mvt=True,keepPosture=False,keepPosition=True,Cote=Cote,CoteOpp=CoteOpp)
    slider2=SliderAbs(sliderName,action2,min2,max2,getValue,step,sliderList)
    return Group("reset","set to 0",slider,sliderList,i,getValue,0,slider2,setOneFunction,functionCorr=functionCorr)     

def functionCheckBox(label,functionCheck,functionUnCheck,value,args=[]):
    actionCheck=FunctionAction(value,functionCheck,Cote="",CoteOpp="",keepPosture=False,keepPosition=True,args=args,mvt=False)
    actionUnCheck=FunctionAction(not value,functionUnCheck,Cote="",CoteOpp="",keepPosture=False,keepPosition=True,args=args,mvt=False)
    return CheckBox(label,actionCheck,actionUnCheck,value,args=args)

       
def createWindows(nameList,pointOnCurveList,locatorList,droites=[]):
    clearSliderVariables()
    crvInfos=[getCurveLength(),getCurvePosition(),calcPosture(),getJointChainLength(),getCLen()]

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
        sliderList.append(SliderDuo(name,fcts[i],[]))

    buttonList=[]
    # courbures cervicale, dorsale et lombaire
    buttonList.append(courbureGroup(sliderList,0,names[0],-1,1,-3,3,0,0.00000001,['curve1.cv[5]'],getFunction=fcts[0]))
    buttonList.append(courbureGroup(sliderList,1,names[1],-3,3,-3,3,0,0.00001,['curve1.cv[1]'],getFunction=fcts[1]))

    # TODO garder les 2 keep=False fait planter les tests
    # cervicales GD HB TODO position tete par rapport  au sol ou aux dorsales (tenir tete droite) -> 2 fonctions align with et setstraight ?
    buttonList.append(functionGroup(sliderList,2,names[2],-10,10,-60,60,0,0.00000001,setFcts[0],getFunction=fcts[2],Cote="C",CoteOpp="L",functionCorr=corrCGD))
    buttonList.append(functionGroup(sliderList,3,names[3],-10,10,-60,60,0,0.00000001,setFcts[1],getFunction=fcts[3],Cote="C",CoteOpp="L",functionCorr=corrCHB))

    # dorsales GD HB -> dorsales HB = dorsales + lombaires
    buttonList.append(functionGroup(sliderList,4,names[4],-8,8,-30,50,0,0.00000001,setFcts[2],getFunction=fcts[4],Cote="",CoteOpp="",functionCorr=corrDGD))
    buttonList.append(functionGroup(sliderList,5,names[5],-8,8,-30,50,0,0.00000001,setFcts[3],getFunction=fcts[5],Cote="",CoteOpp="",functionCorr=corrDHB))

    #lombaires
    buttonList.append(functionGroup(sliderList,6,names[6],-20,20,-60,60,0,0.00000001,setFcts[4],getFunction=fcts[6],Cote="L",CoteOpp="C",functionCorr=corrLGD))
    buttonList.append(functionGroup(sliderList,7,names[7],-20,20,-60,60,0,0.00000001,setFcts[5],getFunction=fcts[7],Cote="L",CoteOpp="C",functionCorr=corrLHB))

    # compression
    buttonList.append(functionGroup(sliderList,8,names[8],-100,200,-40,50,0,0.00000001,setFcts[6],crvInfos,getFunction=fcts[8],Cote="",CoteOpp="L",functionCorr=corrCompGD))
    buttonList.append(functionGroup(sliderList,9,names[9],0,15,0,80,0,0.00000001,setFcts[7],crvInfos,getFunction=fcts[9],Cote="",CoteOpp="L",functionCorr=corrComp))

    #tete
    buttonList.append(functionGroup(sliderList,10,names[10],-20,17,-90,90,0,0.00000001,setFcts[8],getFunction=angleTGD,Cote="C",CoteOpp="L",functionCorr=corrTGD))
    buttonList.append(functionGroup(sliderList,11,names[11],-20,17,-90,90,0,0.00000001,setFcts[9],getFunction=angleTHB,Cote="C",CoteOpp="L",functionCorr=corrTHB)) 


    # position
    buttonList.append(postureGroup(sliderList,12,names[12],-60,60,0.00000001,["curve1"],crvInfos[1][0],functionSet=setFcts[10],keepPosition=False,keepPosture=False,keepCurveLength=False))
    buttonList.append(postureGroup(sliderList,13,names[13],-60,60,0.00000001,["curve1"],crvInfos[1][1],functionSet=setFcts[11],keepPosition=False,keepPosture=False,keepCurveLength=False))
    buttonList.append(postureGroup(sliderList,14,names[14],-60,60,0.00000001,["curve1"],crvInfos[1][2],functionSet=setFcts[12],keepPosition=False,keepPosture=False,keepCurveLength=False))
    # scaling
    buttonList.append(postureGroup(sliderList,15,names[15],1,30,0.00000001,["curve1"],valueReset=getCurveLength(),valueSetTo=1,functionSet=setFcts[13],keepCurveLength=False,keepPosition=True,keepPosture=True,args=[],name2="set to 1"))
    # posture generale
    buttonList.append(postureGroup(sliderList,16,names[16],-90,90,0.00000001,["curve1"],0,crvInfos[1],functionSet=setFcts[14],args=[],keepPosture=False,keepPosition=True,keepCurveLength=True))
    buttonList.append(postureGroup(sliderList,17,names[17],-180,180,0.00000001,["curve1"],0,crvInfos[1],functionSet=setFcts[15],args=[],keepPosture=False,keepPosition=True,keepCurveLength=True))

    # checkBox pour la gestion d'affichage
    checkBoxList=[]
    checkBoxList.append(functionCheckBox('Hide rest of skeleton',HideRestOfSkeleton,ShowRestOfSkeleton,True))
    checkBoxList.append(functionCheckBox('Hide head and tail',HideHeadAndTail,ShowHeadAndTail,True))
    checkBoxList.append(functionCheckBox('Hide joints',HideSkeletonJoints,ShowSkeletonJoints,True))
    checkBoxList.append(functionCheckBox('Hide polygons',HidePolygons,ShowPolygons,True)) 


    # gestion des plans
    paramList=["Curve","","Off"]
    planesList=[]
    planesList.append(functionCheckBox('Show Plane',partial(ShowPlaneOn,paramList),HidePlane,False))
    planesList.append(RadioButtonGrp('type',[partial(ClickCurve,paramList),partial(ClickLocator,paramList)],['Curve', 'Locator'],2,paramList))
    planesList.append(RadioButtonGrp('portion',[partial(ClickN,paramList),partial(ClickC,paramList),partial(ClickL,paramList),partial(ClickT,paramList)],['Normal', 'Cervicales', 'Lombaires','Tete'],4,paramList))

    # on cree le sliderGrp a partir de tous les sliders
    sliderGrp1=SliderGrp("Modelisation de la colonne du rat",buttonList,checkBoxList,nameList,pointOnCurveList,locatorList,planesList,droites)




    colorSkeleton(nameList)
    return sliderGrp1



