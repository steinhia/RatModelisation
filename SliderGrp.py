path="C:/Users/alexandra/Documents/alexandra/scripts/"
execfile(path+"GuiObject.py")
execfile(path+"Mouvements.py")
execfile(path+"affichage.py")

class SliderGrp(object):
    def __init__(self,title,buttonList,checkBoxList,nameList,pointOnCurveList,locatorList):
        self.buttonList=buttonList
        self.pointOnCurveList=list(pointOnCurveList)
        self.locatorList=list(locatorList)
        self.window = cmds.window(title =title,le=50,te=50,width=400,height=450)
        self.column = cmds.columnLayout()
        cmds.text("\nParametres de courbure ")
        cmds.rowColumnLayout(numberOfColumns=4,columnWidth=[(1,300),(2,300),(4,50),(5,50)])
        for i in range(1):
            buttonList[i].create()
            #buttonList[i].calcDroite()
        cmds.setParent('..')
        cmds.text("\nMouvement de la colonne")
        cmds.rowColumnLayout(numberOfColumns=4,columnWidth=[(1,300),(2,300),(4,50),(5,50)])
        for i in range(1,8):
            buttonList[i].create()
            buttonList[i].calcDroite()

        cmds.setParent('..')
        cmds.text("\nParametres de la courbe")
        cmds.rowColumnLayout(numberOfColumns=4,columnWidth=[(1,200),(2,300),(4,50),(5,50)])
        for i in range(8,len(buttonList)):
            buttonList[i].create()
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=1,columnWidth=[(1,300)])
        # bouton reset all
        ResetAll=ButtonGlobal("RESET ALL",nameList,pointOnCurveList)
        Realign=ButtonGlobal("Realign",[])
   
        # CheckBox
        cmds.setParent('..')
        cmds.rowColumnLayout( numberOfColumns=2,columnWidth=[(1, 200),(2,200),(3,200)])
        for checkbox in checkBoxList : 
            checkbox.create() 
        cmds.textFieldGrp( label='Select', text='???',editable=True , cc=select)
        cmds.showWindow(self.window)


    def do(self,string,value,updateText=False):
        button=self.string2button(string)
        button.slider2.setValue(value)
        button.slider2.update(updateText)


    def string2button(self,string):
        string=string.lower()
        if "courbure c" in string :
            return self.buttonList[0]
        #if ("courbure d" in string) or ("courbure t" in string):
        #    return self.buttonList[1]
        #if "courbure l" in string :
        #    return self.buttonList[2]
        if "rot cervicale g" in string :
            return self.buttonList[1]
        if "rot cervicale" in string :
            return self.buttonList[2]
        if "rot dorsale g" in string :
            return self.buttonList[3]
        if "rot dorsale" in string :
            return self.buttonList[4]
        if "rot lombaire g" in string :
            return self.buttonList[5]
        if "rot lombaire" in string :
            return self.buttonList[6]
        if "compression" in string :
            return self.buttonList[7]
        if "x" in string :
            return self.buttonList[8]
        if "y" in string :
            return self.buttonList[9]
        if "z" in string :
            return self.buttonList[10]
        if "scale" in string :
            return self.buttonList[11]
        if "posture" in string :
            return self.buttonList[12]

def clearSliderVariables(): 
    blinnList=cmds.ls('*blinn*')
    for i in blinnList:
        if(cmds.objExists(i)):
            cmds.delete(i)
    if (cmds.window("window1", exists=True)):
        cmds.deleteUI("window1") 
    if(cmds.objExists('sliderGrp')):
        cmds.delete('sliderGrp')

             


def courbureButton(sliderList,crvInfos,i,sliderName,nameAfter,min,max,min2,max2,value,step,influence,valueReset=0,getFunction=0,setOneFunction=setOneRot,keepPosture=True,keepPosition=True,keepCurveLength=True):
    getValue=getFunction()
    action = SimpleAction(0,crvInfos,"t",0,1,0,influence,keepPosture=keepPosture,keepPosition=keepPosition,keepCurveLength=keepCurveLength)
    slider=SliderOffset(sliderName,action,min,max,value,step,sliderList)
    action2 = FunctionAction(getValue,crvInfos,setRot,args=[slider,getFunction,[],crvInfos,min,max],keepPosture=keepPosition,keepPosition=keepPosition,mvt=True,keepCurveLength=False)
    slider2=SliderAbs(sliderName,action2,0,74,getValue,step,sliderList)
    return Button("reset","set to 0",nameAfter,slider,sliderList,i,getValue,0,slider2,setOneFunction)

def postureButton(sliderList,crvInfos,i,sliderName,nameAfter,min,max,step,influence,valueReset=0,pivot=-1,valueSetTo=0,functionSet=0,args=[],keepPosture=True,keepPosition=True,keepCurveLength=True,name2="set to 0"):
    action2 = FunctionAction(valueReset,crvInfos,functionSet,keepPosture=keepPosture,keepPosition=keepPosition,keepCurveLength=keepCurveLength,args=crvInfos,mvt=True)
    slider2=SliderAbs(sliderName,action2,min,max,valueReset,step,sliderList)
    return Button("reset",name2,nameAfter,-1,sliderList,i,valueReset,valueSetTo,slider2)
 
def functionButton(sliderList,crvInfos,i,sliderName,nameAfter,min,max,min2,max2,value,step,function,valueReset=0,getFunction=0,getFunctionArgs=[],setOneFunction=setOneRot,keepPosition=True,keepPosture=True):
    getValue=getFunction(getFunctionArgs)
    action=FunctionAction(value,crvInfos,function,keepPosture=keepPosture,keepPosition=keepPosition)
    slider=SliderOffset(sliderName,action,min,max,value,step,sliderList)
    action2 = FunctionAction(getValue,crvInfos,setRot,args=[slider,getFunction,getFunctionArgs,crvInfos,min,max],mvt=True,keepPosture=keepPosture,keepPosition=keepPosition)
    slider2=SliderAbs(sliderName,action2,min2,max2,getValue,step,sliderList)
    return Button("reset","set to 0",nameAfter,slider,sliderList,i,getValue,0,slider2,setOneFunction)     

def functionCheckBox(label,crvInfos,functionCheck,functionUnCheck,value,args=[]):
    actionCheck=FunctionAction(value,crvInfos,functionCheck,keepPosture=False,keepPosition=True,args=args,mvt=False)
    actionUnCheck=FunctionAction(not value,crvInfos,functionUnCheck,keepPosture=False,keepPosition=True,args=args,mvt=False)
    return CheckBox(label,actionCheck,actionUnCheck,value)

       
def createWindows(nameList,pointOnCurveList,locatorList):
    clearSliderVariables()
    crvInfos=[getCurveLength(),getCurvePosition(),calcPosture(),getChainLength(),getCLen()]

    #liste des textes (courbures etc)
    names=["courbure Cervicale ","courbure Dorsale ","courbure Lombaire ","posture ","rot Cervicale G ","rot Cervicale B ", \
          "rot Dorsale G ","rot Dorsale B ","rot Lombaire G ","rot Lombaire B ","compression ","x ","y ","z ","scale ","posture GD"]
    namesAfter=["","","","H","D","H","D","H","D","H","forte","","","","",""]
    fcts=[calcLordoseC,calcCyphoseD,calcLordoseL,calcPosture,calcRotCGD,\
              calcRotCHB,calcRotDGD,calcRotDHB,calcRotLGD,calcRotLHB,calcComp,\
              getX,getY,getZ,getCurveLength,calcPostureGD]   
    setFcts=[rotCGD,rotCHB,rotDGD,rotDHB,rotLGD,rotLHB,compresseDorsales,setX,setY,setZ,keepLengthValue,setPosture,setPostureGD]
    
    #liste mise a jour a chaque modification
    sliderList=[]
    for i,name in enumerate(names):
        sliderList.append(SliderDuo(name,fcts[i],crvInfos))
    buttonList=[]
    # courbures cervicale, dorsale et lombaire
    buttonList.append(courbureButton(sliderList,crvInfos,0,names[0],namesAfter[0],-1,1,-3,3,0,0.00000001,['ClusterCHandle'],getFunction=fcts[0],keepPosture=False,keepPosition=False,keepCurveLength=False))
    #buttonList.append(courbureButton(sliderList,crvInfos,1,names[1],namesAfter[1],-2,2,-3,3,0,0.00001,['ClusterDHandle'],getFunction=fcts[1],keepPosture=False,keepPosition=False,keepCurveLength=False))
    #buttonList.append(courbureButton(sliderList,crvInfos,2,names[2],namesAfter[2],-3,3,-3,3,0,0.00001,['ClusterLHandle'],getFunction=fcts[2],keepPosture=False,keepPosition=False,keepCurveLength=False))

    # TODO garder les 2 keep=False fait planter les tests
    # tete GD HB TODO position tete par rapport  au sol ou aux dorsales (tenir tete droite) -> 2 fonctions align with et setstraight ?
    buttonList.append(functionButton(sliderList,crvInfos,4,names[4],namesAfter[4],-5,5,-30,50,0,0.00000001,setFcts[0],getFunction=fcts[4],keepPosture=False,keepPosition=True))
    buttonList.append(functionButton(sliderList,crvInfos,5,names[5],namesAfter[5],-5,5,-30,50,0,0.00000001,setFcts[1],getFunction=fcts[5],keepPosture=False,keepPosition=True))

    # dorsales GD HB -> dorsales HB = dorsales + lombaires
    buttonList.append(functionButton(sliderList,crvInfos,6,names[6],namesAfter[6],-5,5,-30,50,0,0.00000001,setFcts[2],getFunction=fcts[6],keepPosture=False,keepPosition=True))
    buttonList.append(functionButton(sliderList,crvInfos,7,names[7],namesAfter[7],-5,5,-30,50,0,0.00000001,setFcts[3],getFunction=fcts[7],keepPosture=False,keepPosition=True))

    #lombaires
    buttonList.append(functionButton(sliderList,crvInfos,8,names[8],namesAfter[8],-6,6,-60,50,0,0.00000001,setFcts[4],getFunction=fcts[8],keepPosture=False,keepPosition=True))
    buttonList.append(functionButton(sliderList,crvInfos,9,names[9],namesAfter[9],-6,6,-60,50,0,0.00000001,setFcts[5],getFunction=fcts[9],keepPosture=False,keepPosition=True))

    # compression
    buttonList.append(functionButton(sliderList,crvInfos,10,names[10],namesAfter[10],-10,120,6,85,0,0.00000001,setFcts[6],crvInfos,getFunction=fcts[10],getFunctionArgs=crvInfos,keepPosture=False,keepPosition=True))

    # position
    buttonList.append(postureButton(sliderList,crvInfos,11,names[11],namesAfter[11],-6,4,0.00000001,["curve1"],crvInfos[1][0],functionSet=setX,keepPosition=False,keepCurveLength=False,keepPosture=False))
    buttonList.append(postureButton(sliderList,crvInfos,12,names[12],namesAfter[12],4,10,0.00000001,["curve1"],crvInfos[1][1],functionSet=setY,keepPosition=False,keepCurveLength=False,keepPosture=False))
    buttonList.append(postureButton(sliderList,crvInfos,13,names[13],namesAfter[13],-5,5,0.00000001,["curve1"],crvInfos[1][2],functionSet=setZ,keepPosition=False,keepCurveLength=False,keepPosture=False))
    # scaling
    buttonList.append(postureButton(sliderList,crvInfos,14,names[14],namesAfter[14],3,15,0.00000001,["curve1"],valueReset=getCurveLength(),valueSetTo=1,functionSet=setFcts[10],keepCurveLength=False,keepPosition=False,args=[],name2="set to 1"))
    # posture generale
    buttonList.append(postureButton(sliderList,crvInfos,3,names[3],namesAfter[3],-90,90,0.00000001,["curve1"],0,crvInfos[1],functionSet=setFcts[11],args=[],keepPosture=False,keepPosition=False,keepCurveLength=False))
    buttonList.append(postureButton(sliderList,crvInfos,15,names[15],namesAfter[15],-90,90,0.00000001,["curve1"],0,crvInfos[1],functionSet=setFcts[12],args=[],keepPosture=False,keepPosition=False,keepCurveLength=False))

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



