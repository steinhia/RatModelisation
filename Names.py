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
        dico={"CGD":2,"CHB":3,"LGD":4,"LHB":5,"CompGD":6,"CompHB":7,"TGD":8,"THB":9}
        if name in dico :
            return dico[name]
        return -1

class CurveNames(object):

    @classmethod
    def getFunction(self,name):
        return eval("get"+str(name))

    @classmethod
    def getFunctionLoc(self,name):
        return eval("get"+str(name)+"Loc")

    @classmethod
    def setFunction(self,name):
        return eval("set"+str(name))

    @classmethod
    def Numero(self,name):
        dico={"X":10,"Y":11,"Z":12,"Length":13,"Posture":14,"Orientation":15}
        if name in dico :
            return dico[name]
        return -1
        








