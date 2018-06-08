import sys
sys.path.append("C:/Users/alexandra/Documents/alexandra/scripts")
import time
import maya.mel as mel
import numpy as np

path="C:/Users/alexandra/Documents/alexandra/scripts/"
execfile(path+"Short.py")



class GeneralCalculs(object):
    
    #def __init__(self,liste,*_):
    #    liste=liste # noms

    @classmethod
    def angleHBOriente(cls,v1,v2):
        return abs(valPrincDeg(angleHB(v1,v2)))*np.sign(valPrincDeg(angleHB(v1,[0,0,1])))
    @classmethod
    def angleGDOriente(cls,v1,v2):
        return abs(valPrincDeg(angleHB(v1,v2)))*np.sign(valPrincDeg(angleHB(v1,[0,0,1])))

    # seuls les points de controle ne bougent pas, alors que le parametre des vertebres change, ainsi que leur position -> TODO pas normal
    @classmethod
    def getPosition(cls,liste,num=-1,Cote="",*_):
        milieu=getMilieu(position(liste[0]),position(liste[3]))
        if num<0 or num>2:
            if Cote=="C":
                return position(curvei(n2N('C0')))
            elif Cote=="L":
                return position(curvei(n2N('L6')))
            else:
                return position(liste[2])
        else:
            if Cote=="C":
                return position(curvei(n2N('C0')))[num]
            elif Cote=="L":
                return position(curvei(n2N('L6')))[num]
            else:
                return position(liste[2])[num]

    @classmethod
    def PostureVector(cls,liste,Cote="",*_):
        if Cote=="C":
            return normalize(SubVector(curvei(n2N('C0')),curvei(n2N('T2'))))
        elif Cote=="L":
            return normalize(SubVector(curvei(n2N('L1')),curvei(n2N('L6'))))
        else:
            return normalize(SubVector(liste[3],liste[1]))

    @classmethod
    def getPosture(cls,liste,Cote="",*_):
        if Cote=="C":
            p=cls.PostureVector(liste,"C")
        elif Cote=="L":
            p=cls.PostureVector(liste,"L")
        else:
            p=cls.PostureVector(liste)
        return angle2D([math.sqrt(p[0]**2+p[2]**2),p[1]],[1,0])
        #return angle(cls.PostureVector(liste),cls.refVector(liste))

    @classmethod
    def getOrientation(cls,liste,Cote="",*_):
        #posture change orientation, pas l'inverse
        if Cote=="C":
            p=cls.PostureVector(liste,"C")
        elif Cote=="L":
            p=cls.PostureVector(liste,"L")
        else:
            p=cls.PostureVector(liste)
        return angle2D([p[0],p[2]],[0,1])
        

    @classmethod
    def getChainLength(cls,liste,*_):
        posList=map(position,liste[:-1])
        length=0
        for i in range(len(posList)-1):
            length+=distance(posList[i],posList[i+1])
            #p("dist",distance(posList[i],posList[i+1]),liste)
        return length

    @classmethod
    def refVector(cls,liste,*_):
        pV=cls.PostureVector(liste)
        pV[1]=0
        return pV

    @classmethod
    def proj(cls,v):
        return [v[0],0,v[2]]

    @classmethod
    def proj2D(cls,v):
        return [v[0],v[2]]

    @classmethod
    def angleHB2D(cls,v):
        l=norm([v[0],v[2]])
        #p("vect",[l,0],[l,v[1]],v)
        return angle2D([l,0],[l,v[1]])

    @classmethod
    def angleGD2D(cls,liste,v):
        proj=cls.projPlanPosture(liste,v)
        return angle2D(proj,[v[0],v[2]])

    # on projette le vecteur sur le plan forme par la verticale et le postureVector
    @classmethod
    def projPlanPosture(cls,liste,v):
        [a,b,c]=cls.PostureVector(liste)
        if a!=0:
            r=c/a
            p0=float((v[0]+r*v[2])/(1.0+r**2))
            p2=r*p0
        else:
            p0=0
            p2=v[2]
        return [p0,p2]
            #return np.degrees(angle(v,[0,v[1],v[2]]))
            #return np.degrees(angle(v,[p0,v[1],p2]))



    @classmethod
    def angleCHB(cls,liste,pointOnCurveList=[],*_):
        #p("c",position(liste[3]),position(liste[4]),position(pointOnCurveList[5]))
        if 'locator' in liste[0] :
            v=SubVector(liste[4],liste[3])
        else:
            v=SubVector(liste[4],pointOnCurveList[5])
        #p("finc")
        return cls.angleHB2D(v)
        #return angleHB(SubVector(liste[4],liste[3]),cls.refVector(liste))
        #return abs(angleHB(SubVector(liste[4],liste[3]),cls.refVector(liste)))*np.sign(angleHB(SubVector(liste[4],liste[3]),[0,0,1]))


    @classmethod
    def angleCGD(cls,liste,pointOnCurveList=[],*_):
        if 'locator' in liste[0] :
            v=SubVector(liste[4],liste[3])
        else:
            v=SubVector(liste[4],pointOnCurveList[4])
        return cls.angleGD2D(liste,v)
        #return angleGD(SubVector(liste[4],liste[3]),cls.refVector(liste))
        #return cls.angleHBOriente(SubVector(liste[4],liste[3],cls.refVector(liste)))

    @classmethod
    def angleCGD2(cls,liste,*_):
        return angleHBProj(SubVector(liste[4],liste[3]),cls.refVector(liste))

    @classmethod
    def angleDHB(cls,liste,*_):
        v=SubVector(liste[2],liste[1])
        return cls.angleHB2D(v)
        #return angleHB(SubVector(liste[2],liste[1]),cls.refVector(liste))

    @classmethod
    def angleDGD(cls,liste,*_):
        v=SubVector(liste[2],liste[1])
        return cls.angleGD2D(liste,v)
        #return angleGD(SubVector(liste[2],liste[1]),cls.refVector(liste))

    @classmethod
    def angleLHB(cls,liste,*_):
        v=SubVector(liste[1],liste[0])
        return cls.angleHB2D(v)
        #return angleHB(SubVector(liste[1],liste[0]),cls.refVector(liste))

    @classmethod
    def angleLGD(cls,liste,*_):
        v=SubVector(liste[1],liste[0])
        return cls.angleGD2D(liste,v)
        #return angleGD(SubVector(liste[1],liste[0]),cls.refVector(liste))

    @classmethod
    def angleTHB(cls,liste,*_):
        v=SubVector(liste[5],liste[4])
        return cls.angleHB2D(v)

    @classmethod
    def angleTGD(cls,liste,*_):
        v=SubVector(liste[5],liste[4])
        return cls.angleGD2D(liste,v)

    @classmethod
    def angleComp(cls,liste,*_):
        v=SubVector(liste[3],liste[2])
        return -cls.angleHB2D(v)

#TODO translation pour la CompGD -> // HB
# et mesure angle cervicales ????????
    @classmethod
    def angleCompGD(cls,liste,*_):
        v=SubVector(liste[3],liste[2])
        return -cls.angleGD2D(liste,v)
        return -valPrincDeg(angleGD(cls.refVector(liste),SubVector(liste[3],liste[2])))

    @classmethod
    def HalfChainLengthL(cls,liste,*_):
        dL=map(position,liste)
        return distance(dL[2],dL[1])+distance(dL[1],dL[0])

    @classmethod
    def HalfChainLengthC(cls,liste,*_):
        dL=map(position,liste)
        return distance(dL[4],dL[3])+distance(dL[3],dL[2])

    @classmethod
    def RapportChainLength(cls,liste,*_):
        return cls.HalfChainLengthL(liste)/cls.HalfChainLengthC(liste)

    #def CRapport(self,*_): # C/D
    #    dL=map(position,liste)
    #    return distance(dL[4],dL[3])/distance(dL[3],dL[2])

    #def LRapport(self,*_): # L/D
    #    dL=map(position,liste)
    #    return distance(dL[0],dL[0])/distance(dL[1],dL[2])

        






