# -*- coding: utf-8 -*-
import time
import maya.mel as mel
import numpy as np

execfile(path+"Short.py")



class GeneralCalculs(object):

    """ Calculs généraux utilisés pour les localisateurs et la courbe 
    liste : liste de strings des points utilisés, localisateurs ou vertebres sur la courbe 
    """


    @classmethod
    def PostureVector(cls,liste,Cote="",*_):
        """ vecteur qui détermine l'orientation et la posture du rat """
        if Cote=="C":
            return normalize(sub(CVPosition(liste[3]),CVPosition(liste[2])))
        elif Cote=="L":
            return normalize(sub(CVPosition(liste[1]),CVPosition(liste[0])))
        elif Cote=="T":
            return normalize(sub(CVPosition(liste[4]),CVPosition(liste[3])))
        else:
            return normalize(sub(CVPosition(liste[3]),CVPosition(liste[0])))

    
    @classmethod
    def getPosition(cls,liste,num=-1,Cote="",*_):
        """ Position du rat
        num : int,  coordonnée souhaitée """
        if Cote=="C":
            pos=CVPosition(liste[3])
        elif Cote=="L":
            pos=CVPosition(liste[0])
        elif Cote=="T":
            pos=CVPosition(liste[4])
        else:
            pos=position(liste[1])
        if num<0 or num>2:
            return pos
        return pos[num]

    @classmethod
    def getX(cls,liste,Cote="",*_):
        return cls.getPosition(liste,0,Cote)

    @classmethod
    def getY(cls,liste,Cote="",*_):
        return cls.getPosition(liste,1,Cote)


    @classmethod
    def getZ(cls,liste,Cote="",*_):
        return cls.getPosition(liste,2,Cote)

    
    @classmethod
    def getPosture(cls,liste,Cote="",*_):
        """ angle vertical du vecteur de posture """
        p=cls.PostureVector(liste,Cote)
        return valPrincDeg(angleHB(p,PV=True))

    @classmethod
    def getOrientation(cls,liste,Cote="",*_):
        """ angle latéral du vecteur de posture """
        p=cls.PostureVector(liste,Cote)
        return angle2D([p[0],p[2]],[0,1])
        

    @classmethod
    def getLength(cls,liste,*_):
        """ longueur de la courbe ou de la chaine des localisateurs (calculs de segments pour les deux) """
        posList=map(position,liste)
        length=0
        for i in range(len(posList)-1):
            length+=distance(posList[i],posList[i+1])
        return length



    @classmethod
    def projV(cls,v):
        return [v[0],0,v[2]]

    @classmethod
    def proj2D(cls,v):
        return [v[0],v[2]]

    @classmethod
    def angleHB(cls,liste,v,PV=False):
        """ calcule l'angle vertical entre un vecteur d'un groupe de vertebres choisi et un vecteur de reference horizontal
        Ce vecteur de reference est le projeté de ce vecteur sur l'axe horizontal, 
        inversé si  le vecteur de posture est dans l'autre sens pour permettre le calcul d'angles obtus
        On ne fait pas l'inversion pour calculer la posture et l'orientation
        PV : boolean, Posture Vector """
        l=norm([v[0],v[2]])
        if PV :
            return angle2D([l,0],[l,v[1]])
        sens=np.sign(np.dot(projHor3D(v),projHor3D(cls.PostureVector(liste))))
        return angle2D([l,0],[sens*l,v[1]])

    @classmethod
    def angleGD(cls,liste,v):
        """ angle latéral entre un vecteur d'un groupe de vertèbres choisi et ce vecteur projeté sur le plan postural """
        vProj=cls.proj2D(v)
        pProj=cls.proj2D(cls.PostureVector(liste))
        return angle2D(pProj,vProj)


    @classmethod
    def vector(cls,liste,string,*_):
        """ vecteur utilisé pour calculer les angles de chaque groupe de vertèbres 
            string : string, opération concernée, CGD pour cervicales gauche droite etc """
        if "Comp" in string: # compression, calcul différent pour les deux car pas assez de localisateurs
            if 'locator' in liste[0]  :
                return SubVector(liste[2],liste[1])
            else:
                return SubVector(pointOnCurveList[5],pointOnCurveList[1])
        if "C" in string: # cervicales
            return SubVector(liste[3],liste[2])
        if "L" in string: # lombaires
            if 'locator' in liste[0] :
                return SubVector(liste[1],liste[0])
            else:
                return SubVector(pointOnCurveList[1],pointOnCurveList[0]) 
        if "T" in string: # tete
            return SubVector(liste[4],liste[3])


    @classmethod
    def angle(cls,liste,string,*_):
        """ calcul de l'angle correspondant à l'opération
        string : string, l'opération ex "CGD" = angle latéral des cervicales """
        vect=cls.vector(liste,string)
        if string=="CompHB":
            return -cls.angleHB(liste,vect)
        if "HB" in string:
            return cls.angleHB(liste,vect)
        elif "GD" in string:
            return cls.angleGD(liste,vect)
        else:
            return eval("cls.get"+string)(liste)


    @classmethod
    def angleCHB(cls,liste,pointOnCurveList=[],*_):
        v=SubVector(liste[3],liste[2])
        return cls.angleHB(liste,v)
       

    @classmethod
    def angleCGD(cls,liste,pointOnCurveList=[],*_):
        v=SubVector(liste[3],liste[2])
        return cls.angleGD(liste,v)

    @classmethod
    def angleDHB(cls,liste,*_):
        v=SubVector(liste[1],liste[1])
        return cls.angleHB(liste,v)

    @classmethod
    def angleDGD(cls,liste,*_):
        v=SubVector(liste[1],liste[1])
        return cls.angleGD(liste,v)

    @classmethod
    def angleLHB(cls,liste,*_):
        if 'locator' in liste[0]:
            v=SubVector(liste[1],liste[0])
        else :
            v=SubVector(liste[1],liste[0])
        return cls.angleHB(liste,v)

    @classmethod
    def angleLGD(cls,liste,*_):
        if 'locator' in liste[0]:
            v=SubVector(liste[1],liste[0])
        else :
            v=SubVector(liste[1],liste[0])
        return cls.angleGD(liste,v)

    @classmethod
    def angleTHB(cls,liste,*_):
        v=SubVector(liste[4],liste[3])
        return cls.angleHB(liste,v)

    @classmethod
    def angleTGD(cls,liste,*_):
        v=SubVector(liste[4],liste[3])
        return cls.angleGD(liste,v)

    @classmethod
    def angleCompHB(cls,liste,*_):
        v=SubVector(liste[2],liste[1])
        return -cls.angleHB(liste,v)

    @classmethod
    def angleCompGD(cls,liste,*_):
        v=SubVector(liste[2],liste[1])
        return cls.angleGD(liste,v)

       
    @classmethod
    def projPlanPosture3D(cls,liste,p1,p2,Cote=""):
        """ projeté d'un vecteur sur le plan postural, coordonnées 3D 
        p1 : liste, origine du vecteur
        p2 : liste, arrivée du vecteur """
        normal=normalize(np.cross(cls.PostureVector(liste,Cote),[0,1,0]))
        M=cls.PointOnPlane(liste,Cote)
        p1Proj=projPoint3D(p1,M,normal)
        p2Proj=projPoint3D(p2,M,normal)
        return sub(p2Proj,p1Proj)

    @classmethod
    def projPoint3D(cls,liste,p,Cote=""):
        """ projeté d'un point sur le plan postural, coordonnées 3D """
        normal=normalize(np.cross(cls.PostureVector(liste,Cote),[0,1,0]))
        M=cls.PointOnPlane(liste,Cote)
        return projPoint3D(p,M,normal)

        # on projette le vecteur sur le plan formé par la verticale et le postureVector
    @classmethod
    def projPlanPosture2D(cls,liste,p1,p2,Cote=""):
        """ projeté d'un vecteur sur le plan postural, coordonnées 2D 
        p1 : liste, origine du vecteur
        p2 : liste, arrivée du vecteur """
        normal=normalize(np.cross(cls.PostureVector(liste,Cote),[0,1,0]))
        M=cls.PointOnPlane(liste,Cote)
        p1Proj=projPoint3D(p1,M,normal)
        p2Proj=projPoint3D(p2,M,normal)
        subv=sub(p2Proj,p1Proj)
        return cls.getPlaneCoordinates(liste,subv,Cote)

    @classmethod
    def getPlaneCoordinates(cls,liste,v,Cote=""):
        """ Coordinées du vecteur dans le plan postural """
        b1=normalize(cls.projV(cls.PostureVector(liste,Cote)))
        b2=[0,1,0]
        return [np.dot(v,b1),np.dot(v,b2)]


    @classmethod
    def PointOnPlane(cls,liste,Cote="",*_):
        """ un point du plan pour le calcul """
        if Cote=="C":
            p=CVPosition(liste[3])
        elif Cote=="L":
            p=CVPosition(liste[0])
        elif Cote=="T":
            p=CVPosition(liste[4])
        else:
            p=CVPosition(liste[1])
        return p

    @classmethod
    def createPlane(cls,liste,Cote=""):
        """ crée et affiche le plan postural du mouvement du rat """
        
        # couleur et transparence pour le plan
        HidePlane()
        mel.eval("shadingNode -asShader blinn -n blinn4;")
        mel.eval("sets -renderable true -noSurfaceShader true -empty -name blinn4SG;")
        mel.eval("connectAttr -f blinn4.outColor blinn4SG.surfaceShader;")

        normal=np.cross(cls.PostureVector(liste,Cote),[0,1,0])
        name="PosturePlane"
        cmds.polyPlane(n=name,axis=normal, sx=1, sy=1, w=5, h=5)
        center=cmds.getAttr(name+'.center')[0]
        ptOnPlane=cls.PointOnPlane(liste,Cote)#posL6=CVPosition(liste[0])
        t=sub(ptOnPlane,center)
        cmds.select(name)
        cmds.move(t[0],t[1],t[2],r=True)

        # on lui applique la couleur
        cmds.select('PosturePlane')
        mel.eval("sets -e -forceElement blinn4SG;")
        mel.eval("setAttr \"blinn4.color\" -type double3 1 1 0 ;")
        mel.eval('setAttr "blinn4.transparency" -type double3 0.7 0.7 0.7 ;')



    @classmethod
    def HalfChainLengthL(cls,liste,*_):
        """ calcule la longueur des segments vers les lombaires """
        dL=map(position,liste)
        return distance(dL[2],dL[1])+distance(dL[1],dL[0])

    @classmethod
    def HalfChainLengthC(cls,liste,*_):
        """ calcule la longueur des segments vers les cervicales """
        dL=map(position,liste)
        return distance(dL[4],dL[3])+distance(dL[3],dL[2])

    @classmethod
    def RapportChainLength(cls,liste,*_):
        """ calcule les rapports entre les longueurs des segments du début et de la fin """
        return cls.HalfChainLengthL(liste)/cls.HalfChainLengthC(liste)

    #def CRapport(self,*_): # C/D
    #    dL=map(position,liste)
    #    return distance(dL[4],dL[3])/distance(dL[3],dL[2])

    #def LRapport(self,*_): # L/D
    #    dL=map(position,liste)
    #    return distance(dL[0],dL[0])/distance(dL[1],dL[2])

        






