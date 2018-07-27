# -*- coding: utf-8 -*-
execfile(path+"GuiObject.py")
execfile(path+"Mouvements.py")
execfile(path+"affichage.py")
execfile(path+"Names.py")
execfile(path+"placementManuel.py")
execfile(path+"Short.py")

class SliderGrp(object):
    """ classe définissant la fenêtre de l'interface graphique """
    def __init__(self,title,buttonList,checkBoxList,nameList,pointOnCurveList,locatorList,planesList,droites=[]):
        self.buttonList=buttonList
        self.sliderList=self.buttonList[0].sliderList
        self.droites=droites
        self.nameList=nameList
        self.pointOnCurveList=list(pointOnCurveList)
        self.locatorList=list(locatorList)
        self.window = cmds.window('window1',title =title,le=50,te=50,width=400,height=450)
        self.column = cmds.columnLayout()
  
        cmds.text("\nMouvement de la colonne")
        cmds.rowColumnLayout(numberOfColumns=4,columnWidth=[(1,300),(2,300),(4,50),(5,50),(6,50)])

        # opérations de rotation
        if self.droites==[]:
            for i in range(0,8):
                buttonList[i].create()
                if i!=6 or True:
                    self.droites.append(buttonList[i].calcDroite())
        else :
            for i in range(0,8):
                buttonList[i].create()
                if i!=6 or True:
                    buttonList[i].affectDroite(self.droites[i-2])

        cmds.setParent('..')
        cmds.text("\nParametres de la courbe")
        cmds.rowColumnLayout(numberOfColumns=5,columnWidth=[(1,1),(2,300),(3,50),(4,50),(5,50)])

        # position etc
        for i in range(8,len(buttonList)):
            buttonList[i].create()
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=1,columnWidth=[(1,300)])

        # Planes
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=1)

        for buttonRadio in planesList:
            buttonRadio.create()

        cmds.setParent('..')
        cmds.rowColumnLayout( numberOfColumns=3,columnWidth=[(1, 100),(2,100)])
        self.GuiButtonTTL=cmds.button(label="TranslateToLocator",command=partial(translateToLocatorGui,self.sliderList))
        self.GuiButtonTTCV=cmds.button(label="TranslateToCV",command=partial(translateToCVGui,self.sliderList))
        self.GuiButtonTTCV=cmds.button(label="TranslateExtrema",command=partial(translateToExtremaGui,self.sliderList))
        self.GuiButtonS=cmds.button(label="ScaleSegment",command=partial(scaleGui,self.sliderList))
        self.GuiButtonRedo=cmds.button(label="ScaleFactor",command=partial(scaleOffsetGui,self.sliderList))
        self.GuiButtonSCPOC=cmds.button(label="ScaleCPOC",command=partial(scaleCPOCGui,self.sliderList))
        self.GuiButtonRedo=cmds.button(label="ScaleComp",command=partial(scaleCompGui,self.sliderList))
        self.GuiButtonSelect=cmds.button(label="Select",command=selectGui)
        self.GuiButtonSelect=cmds.button(label="SelectCV",command=selectCVGui)
        length=getLength();CVpos=calcPosCV();jtPos=JointPositions()
        self.GuiButtonSelect=cmds.button(label="Place",command=partial(Placement,self.sliderList,length,CVpos,jtPos,False))
        self.GuiButtonSelect=cmds.button(label="Place And Save",command=partial(Placement,self.sliderList,length,CVpos,jtPos,True))
        self.GuiButtonUndo=cmds.button(label="Undo",command=partial(UndoGui,self.sliderList))
        self.GuiButtonUndo=cmds.button(label="ApproxCurve",command=ApproxGui)
        
        # CheckBox
        cmds.setParent('..')
        cmds.rowColumnLayout( numberOfColumns=2,columnWidth=[(1, 200),(2,200)])
        for checkbox in checkBoxList : 
            checkbox.create() 

        cmds.showWindow(self.window)
        cmds.text("\n")

    
    def string2num(self,string):
        """ numéro de slider correspondant à l'opération """
        string=string.lower()
        if "rotcgd" in string :
            return 0
        if "rotchb" in string :
            return 1
        if "rotlgd" in string :
            return 2
        if "rotlhb" in string :
            return 3
        if "compression g" in string :
            return 4
        if "comp" in string :
            return 5
        if "rottgd" in string:
            return 6
        if "rotthb" in string:
            return 7
        if "x" in string :
            return 8
        if "y" in string :
            return 9
        if "z" in string :
            return 10
        if "scale" in string :
            return 11
        if "posture" in string :
            return 12
        if "orientation" in string :
            return 13
        else:
            print("mauvaise operation : ",string)

    def string2button(self,string):
        """ slider correspondant à l'opération """
        return self.buttonList[self.string2num(string)]


def clearSliderVariables():
    """ clear objets résiduels """
    blinnList=cmds.ls('*blinn*')
    for i in blinnList:
        if(cmds.objExists(i)):
            cmds.delete(i)
    if (cmds.window("window1", exists=True)):
        cmds.deleteUI("window1") 
    if(cmds.objExists('sliderGrp')):
        cmds.delete('sliderGrp')

def postureGroup(sliderList,sliderName,min,max,keepPosition=True,keepCurveLength=True):
    """ crée les boutons de paramètre de courbe """
    functionSet=eval("set"+sliderName)
    value=Names.getFunction(sliderName)()
    action2 = FunctionAction(value,functionSet,Cote="",CoteOpp="",keepPosition=keepPosition,keepCurveLength=keepCurveLength,args=[],mvt=True)
    slider2=SliderAbs(sliderName,action2,min,max,value,0.00000001,sliderList)
    return Group(sliderName,-1,sliderList,slider2)
 
def functionGroup(sliderList,sliderName,min,max,min2,max2,value,valueReset=0):
    """ crée les boutons de rotation """
    getValue=angleCrv(sliderName)
    Cote=Names.Cote(sliderName)
    CoteOpp=Names.CoteOpp(sliderName)
    action=FunctionAction(value,rot,args=sliderName,keepPosition=True,Cote=Cote,CoteOpp=CoteOpp)
    slider=SliderOffset(sliderName,action,min,max,value,0.00000001,sliderList)
    action2 = FunctionAction(getValue,setRot,args=slider,mvt=True,keepPosition=True,Cote=Cote,CoteOpp=CoteOpp)
    slider2=SliderAbs(sliderName,action2,min2,max2,getValue,0.00000001,sliderList)
    return Group(sliderName,slider,sliderList,slider2)     

def functionCheckBox(label,functionCheck,functionUnCheck,value,args=[]):
    """ crée les checkbox """
    actionCheck=FunctionAction(value,functionCheck,Cote="",CoteOpp="",keepPosition=True,args=args,mvt=False)
    actionUnCheck=FunctionAction(not value,functionUnCheck,Cote="",CoteOpp="",keepPosition=True,args=args,mvt=False)
    return CheckBox(label,actionCheck,actionUnCheck,value,args=args)

       
def createWindows(nameList,pointOnCurveList,locatorList,droites=[]):
    """ crée la liste des boutons etc contenus dans l'interface graphique """
    clearSliderVariables()

    #liste des textes (courbures etc)
    names=OperationsList() # CGD CHB etc
    fcts=[angleCrv for i in range(2,10)]+[getX,getY,getZ,getPosture,getOrientation,getLength]   
    
    #liste mise a jour a chaque modification
    sliderList=[]
    for i,name in enumerate(names):
        sliderList.append(SliderDuo(name,fcts[i],[]))

    buttonList=[]

    # cervicales GD HB 
    buttonList.append(functionGroup(sliderList,names[0],-30,30,-30,30,0))
    buttonList.append(functionGroup(sliderList,names[1],-30,30,-40,40,0))


    #lombaires
    buttonList.append(functionGroup(sliderList,names[2],-30,30,-30,30,0))
    buttonList.append(functionGroup(sliderList,names[3],-30,30,-40,40,0))

    # compression
    buttonList.append(functionGroup(sliderList,names[4],-30,30,-5,5,0))
    buttonList.append(functionGroup(sliderList,names[5],0,15,0,70,0))

    #tete
    buttonList.append(functionGroup(sliderList,names[6],-30,30,-90,90,0))
    buttonList.append(functionGroup(sliderList,names[7],-30,30,-50,50,0)) 


    # position
    buttonList.append(postureGroup(sliderList,names[8],-60,60,keepPosition=False,keepCurveLength=False))
    buttonList.append(postureGroup(sliderList,names[9],-60,60,keepPosition=False,keepCurveLength=False))
    buttonList.append(postureGroup(sliderList,names[10],-60,60,keepPosition=False,keepCurveLength=False))

    # posture generale
    buttonList.append(postureGroup(sliderList,names[11],-90,90,keepPosition=True,keepCurveLength=True))
    buttonList.append(postureGroup(sliderList,names[12],-180,180,keepPosition=True,keepCurveLength=True))
    # scaling
    buttonList.append(postureGroup(sliderList,names[13],1,30,keepCurveLength=False,keepPosition=True))

    # checkBox pour la gestion d'affichage
    checkBoxList=[]
    HideRestOfSkeleton()
    HideHeadAndTail()
    HideSkeletonJoints()
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

def do(sliderList,string,value,updateText=True,nMax=30):
    """ effectue la bonne opération (angles précis) 
    string : opération ex CGD
    value : paramètre à fixer """
    sl=sliderList[numSlider(string)]
    sl.slider2.setValue(value)
    sl.slider2.update(updateText,nMax=nMax)




