class Names(object):
    
    @classmethod
    def getFunction(self,name):
        if "GD" in name or "HB" in name:
            return partial(eval("angleCrv"),name)
        return eval("get"+str(name))

    @classmethod
    def getValue(self,name):
        return angleCrv(name)

    @classmethod
    def getFunctionArgs(self,name):
        return []

    @classmethod
    def getFunctionLocator(self,name):
        if "GD" in name or "HB" in name:
            return eval("angle"+str(name)+"Loc")
        return eval("get"+str(name)+"Loc")

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
        if prefix=="C" or prefix=="T":# or "Comp" in name:
            return "L"
        return ""


    @classmethod
    def Numero(self,name):
        dico={"CGD":0,"CHB":1,"LGD":2,"LHB":3,"CompGD":4,"CompHB":5,"TGD":6,"THB":7,"X":8,"Y":9,"Z":10,"Posture":11,"Orientation":12,"Length":13}
        if name in dico :
            return dico[name]
        return -1












