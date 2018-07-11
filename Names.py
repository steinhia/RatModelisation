class Names(object):
    
    @classmethod
    def getFunction(self,name):
        return eval("angle"+str(name))
    @classmethod
    def getValue(self,name):
        return angleCrv(name)

    @classmethod
    def getFunctionArgs(self,name):
        return []

    @classmethod
    def getFunctionLocator(self,name):
        return eval("angle"+str(name)+"Loc")

    @classmethod
    def setAngleFunction(self,name):
        return eval("setAngle"+name)

    @classmethod
    def rotFunction(self,name):
        return eval("rot"+name)

    @classmethod
    def corrFunction(self,name):
        return eval("corr"+name)

    @classmethod
    def Cote(self,name):
        prefix=name[0]
        if prefix=="C" or prefix=="T":
            return "C"
        if prefix=="L":
            return "L"
        return ""

    @classmethod
    def CoteOpp(self,name):
        prefix=name[0]
        if prefix=="L":
            return "C"
        if prefix=="C" or prefix=="T" or "Comp" in name:
            return "L"
        return ""


    @classmethod
    def Numero(self,name):
        dico={"CGD":2,"CHB":3,"DGD":4,"DHB":5,"LGD":6,"LHB":7,"CompGD":8,"CompHB":9,"TGD":10,"THB":11}
        if name in dico :
            return dico[name]
        return -1

class CurveNames(object):

    @classmethod
    def getFunction(self,name):
        return eval("get"+str(name))

    @classmethod
    def setFunction(self,name):
        return eval("set"+str(name))

    @classmethod
    def Numero(self,name):
        dico={"X":12,"Y":13,"Z":14,"Scale":15,"Posture":16,"Orientation":17}
        if name in dico :
            return dico[name]
        return -1
        








