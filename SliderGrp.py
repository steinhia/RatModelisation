# -*- coding: utf-8 -*-
path="C:/Users/alexa/Documents/alexandra/scripts/"
execfile(path+"GuiObject.py")
execfile(path+"Mouvements.py")
execfile(path+"affichage.py")
execfile(path+"Names.py")

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
        cmds.rowColumnLayout(numberOfColumns=1,columnWidth=[(1,300),(2,300),(4,50),(5,50)])

        for i in range(2):
            buttonList[i].create()


        cmds.setParent('..')
        cmds.text("\nMouvement de la colonne")
        cmds.rowColumnLayout(numberOfColumns=4,columnWidth=[(1,300),(2,300),(4,50),(5,50),(6,50)])

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
        cmds.rowColumnLayout(numberOfColumns=2,columnWidth=[(1,1),(2,300),(4,50),(5,50),(6,50)])
        for i in range(12,len(buttonList)):
            buttonList[i].create()
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=1,columnWidth=[(1,300)])

        # Planes
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=1)#,columnWidth=[(1, 200),(2,500)])

        for buttonRadio in planesList:
            buttonRadio.create()

        cmds.setParent('..')
        cmds.rowColumnLayout( numberOfColumns=2,columnWidth=[(1, 100),(2,100)])
        self.GuiButtonTTL=cmds.button(label="TranslateToLocator",command=partial(translateToLocatorGui,self.sliderList))
        self.GuiButtonTTCV=cmds.button(label="TranslateToCV",command=partial(translateToCVGui,self.sliderList))
        self.GuiButtonS=cmds.button(label="Scale",command=partial(scaleGui,self.sliderList))
        self.GuiButtonSCPOC=cmds.button(label="ScaleCPOC",command=partial(scaleCPOCGui,self.sliderList))
        self.GuiButtonUndo=cmds.button(label="Undo",command=partial(UndoGui,self.sliderList))
        self.GuiButtonSelect=cmds.button(label="Select",command=selectGui)
        self.GuiButtonSelect=cmds.button(label="Place",command=selectGui)
        self.GuiButtonSelect=cmds.button(label="Place And Save",command=selectGui)
        # CheckBox
        cmds.setParent('..')
        cmds.rowColumnLayout( numberOfColumns=2,columnWidth=[(1, 200),(2,200)])
        for checkbox in checkBoxList : 
            checkbox.create() 

        cmds.showWindow(self.window)
        cmds.text("\n")

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

def courbureGroup(sliderList,i,sliderName,min,max,min2,max2,value,step,influence,valueReset=0,getFunction=0,Cote="",CoteOpp=""):
    getValue=getFunction()
    action = SimpleAction(0,"t",0,2,0,influence,Cote=Cote,CoteOpp=CoteOpp,keepPosture=False,keepPosition=False,keepCurveLength=False)
    slider=SliderOffset(sliderName,action,min,max,value,step,sliderList)
    action2 = FunctionAction(getValue,setRot,args=slider,Cote=Cote,CoteOpp=CoteOpp,keepPosture=False,keepPosition=False,mvt=True,keepCurveLength=False)
    slider2=SliderAbs(sliderName,action2,-100,100,getValue,step,sliderList)
    return Group(sliderName,slider,sliderList,slider2)

def postureGroup(sliderList,sliderName,min,max,keepPosture=True,keepPosition=True,keepCurveLength=True):
    functionSet=CurveNames.setFunction(sliderName)
    value=CurveNames.getFunction(sliderName)()
    action2 = FunctionAction(value,functionSet,Cote="",CoteOpp="",keepPosture=keepPosture,keepPosition=keepPosition,keepCurveLength=keepCurveLength,args=[],mvt=True)
    slider2=SliderAbs(sliderName,action2,min,max,value,0.00000001,sliderList)
    return Group(sliderName,-1,sliderList,slider2)
 
def functionGroup(sliderList,sliderName,min,max,min2,max2,value,valueReset=0):
    getValue=angleCrv(sliderName)
    Cote=Names.Cote(sliderName)
    CoteOpp=Names.CoteOpp(sliderName)
    action=FunctionAction(value,rot,args=sliderName,keepPosture=False,keepPosition=True,Cote=Cote,CoteOpp=CoteOpp)
    slider=SliderOffset(sliderName,action,min,max,value,0.00000001,sliderList)
    action2 = FunctionAction(getValue,setRot,args=slider,mvt=True,keepPosture=False,keepPosition=True,Cote=Cote,CoteOpp=CoteOpp)
    slider2=SliderAbs(sliderName,action2,min2,max2,getValue,0.00000001,sliderList)
    return Group(sliderName,slider,sliderList,slider2)     

def functionCheckBox(label,functionCheck,functionUnCheck,value,args=[]):
    actionCheck=FunctionAction(value,functionCheck,Cote="",CoteOpp="",keepPosture=False,keepPosition=True,args=args,mvt=False)
    actionUnCheck=FunctionAction(not value,functionUnCheck,Cote="",CoteOpp="",keepPosture=False,keepPosition=True,args=args,mvt=False)
    return CheckBox(label,actionCheck,actionUnCheck,value,args=args)

       
def createWindows(nameList,pointOnCurveList,locatorList,droites=[]):
    clearSliderVariables()


    #liste des textes (courbures etc)
    names=["courbure Cervicale ","courbure Lombaire ","CGD","CHB", \
          "DGD","DHB","LGD","LHB","CompGD","CompHB","TGD","THB","X","Y","Z","Length","Posture ","Orientation"]
    fcts=[calcLordoseC,calcLordoseL]+[angleCrv for i in range(2,12)]+[getX,getY,getZ,getLength,getPosture,getOrientation]   
    #setFcts=[Names.rotFunction(names[i]) for i in range(2,12)]+[setX,setY,setZ,setLength,setPosture,setOrientation]
    
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
    buttonList.append(functionGroup(sliderList,names[2],-10,10,-60,60,0))
    buttonList.append(functionGroup(sliderList,names[3],-10,10,-60,60,0))

    # dorsales GD HB -> dorsales HB = dorsales + lombaires
    buttonList.append(functionGroup(sliderList,names[4],-8,8,-30,50,0))
    buttonList.append(functionGroup(sliderList,names[5],-8,8,-30,50,0))

    #lombaires
    buttonList.append(functionGroup(sliderList,names[6],-20,20,-60,60,0))
    buttonList.append(functionGroup(sliderList,names[7],-20,20,-60,60,0))

    # compression
    buttonList.append(functionGroup(sliderList,names[8],-100,200,-40,50,0))
    buttonList.append(functionGroup(sliderList,names[9],0,15,0,80,0))

    #tete
    buttonList.append(functionGroup(sliderList,names[10],-20,17,-90,90,0))
    buttonList.append(functionGroup(sliderList,names[11],-20,17,-90,90,0)) 


    #crvInfos=[getLength(),getCurvePosition(),getPosture(),getJointChainLength(),getCLen()]
    # position
    buttonList.append(postureGroup(sliderList,names[12],-60,60,keepPosition=False,keepPosture=False,keepCurveLength=False))
    buttonList.append(postureGroup(sliderList,names[13],-60,60,keepPosition=False,keepPosture=False,keepCurveLength=False))
    buttonList.append(postureGroup(sliderList,names[14],-60,60,keepPosition=False,keepPosture=False,keepCurveLength=False))
    # scaling
    buttonList.append(postureGroup(sliderList,names[15],1,30,keepCurveLength=False,keepPosition=True,keepPosture=True))
    # posture generale
    buttonList.append(postureGroup(sliderList,names[16],-90,90,keepPosture=False,keepPosition=True,keepCurveLength=True))
    buttonList.append(postureGroup(sliderList,names[17],-180,180,keepPosture=False,keepPosition=True,keepCurveLength=True))

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



