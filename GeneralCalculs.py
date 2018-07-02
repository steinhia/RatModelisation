# -*- coding: utf-8 -*-
import sys
sys.path.append("C:/Users/alexa/Documents/alexandra/scripts")
import time
import maya.mel as mel
import numpy as np

path="C:/Users/alexa/Documents/alexandra/scripts/"
execfile(path+"Short.py")



class GeneralCalculs(object):
    
    #def __init__(self,liste,*_):
    #    liste=liste # noms

    #@classmethod
    #def angleHBOriente(cls,v1,v2):
    #    return abs(valPrincDeg(angleHB(v1,v2)))*np.sign(valPrincDeg(angleHB(v1,[0,0,1])))
    #@classmethod
    #def angleGDOriente(cls,v1,v2):
    #    return abs(valPrincDeg(angleHB(v1,v2)))*np.sign(valPrincDeg(angleHB(v1,[0,0,1])))

    # seuls les points de controle ne bougent pas, alors que le parametre des vertebres change
    # donc positions C et L ont besoin d'etre tres stables -> points de controle et pas position de la vertebre
    # pour la position de la courbe, besoin d'un point sur la courbe (scaling etc) -> plutot joint que cv point
    @classmethod
    def getPosition(cls,liste,num=-1,Cote="",*_):
        milieu=getMilieu(position(liste[0]),position(liste[3]))
        if num<0 or num>2:
            if Cote=="C":
                return CVPosition(liste[4])
            elif Cote=="L":
                return CVPosition(liste[0])
            else:
                return position(liste[2])
        else:
            if Cote=="C":
                return CVPosition(liste[4])[num]
            elif Cote=="L":
                return CVposition(liste[0])[num]
            else:
                return position(liste[2])[num]

    @classmethod
    def PostureVector(cls,liste,Cote="",*_):
        if Cote=="C":
            return normalize(sub(CVPosition(liste[4]),CVPosition(liste[3])))
        elif Cote=="L":
            return normalize(sub(CVPosition(liste[0]),CVPosition(liste[2])))
        else:
            return normalize(sub(CVPosition(liste[3]),CVPosition(liste[0])))


    @classmethod
    def PointOnPlane(cls,liste,Cote="",*_):
        #posture change orientation, pas l'inverse
        if Cote=="C":
            p=CVPosition(liste[4])
        elif Cote=="L":
            p=CVPosition(liste[0])
        else:
            p=CVPosition(liste[2])
        return p

    @classmethod
    def createPlane(cls,liste,Cote=""):
        # couleur et transparence pour le plan
        HidePlane()
        mel.eval("shadingNode -asShader blinn -n blinn4;")
        mel.eval("sets -renderable true -noSurfaceShader true -empty -name blinn4SG;")
        mel.eval("connectAttr -f blinn4.outColor blinn4SG.surfaceShader;")

        normal=np.cross(PostureVector(Cote),[0,1,0])
        name="PosturePlane"
        cmds.polyPlane(n=name,axis=normal, sx=1, sy=1, w=50, h=50)
        center=cmds.getAttr(name+'.center')[0]
        posL6=CVPosition(liste[0])
        t=sub(posL6,center)
        cmds.select(name)
        cmds.move(t[0],t[1],t[2],r=True)

        # on lui applique la couleur
        cmds.select('PosturePlane')
        mel.eval("sets -e -forceElement blinn4SG;")
        mel.eval("setAttr \"blinn4.color\" -type double3 1 1 0 ;")
        mel.eval('setAttr "blinn4.transparency" -type double3 0.7 0.7 0.7 ;')


    @classmethod
    def getPosture(cls,liste,Cote="",*_):
        if Cote=="C":
            p=cls.PostureVector(liste,"C")
        elif Cote=="L":
            p=cls.PostureVector(liste,"L")
        else:
            p=cls.PostureVector(liste)
        return valPrincDeg(angleHB(p,PV=True))

    @classmethod
    def getOrientation(cls,liste,Cote="",*_):
        #posture change orientation, pas l'inverse TODO a changer
        if Cote=="C":
            p=cls.PostureVector(liste,"C")
        elif Cote=="L":
            p=cls.PostureVector(liste,"L")
        else:
            p=cls.PostureVector(liste)
        return angle2D([p[0],p[2]],[0,1])
        

    @classmethod
    def getChainLength(cls,liste,*_):
        posList=map(position,liste)
        length=0
        for i in range(len(posList)-1):
            length+=distance(posList[i],posList[i+1])
        return length

    @classmethod
    def refVector(cls,liste,*_):
        pV=cls.PostureVector(liste)
        pV[1]=0
        return pV

    @classmethod
    def projV(cls,v):
        return [v[0],0,v[2]]

    @classmethod
    def proj2D(cls,v):
        return [v[0],v[2]]

    # que des l positifs, evite les angles au dessus de 90°, c'est ce qu'on veut pourles angles C
    # non un vrai angle, mais qui depend de orientation
    @classmethod
    def angleHB(cls,liste,v,PV=False):
        l=norm([v[0],v[2]])
        #p("vect",[l,0],[l,v[1]],v)
        #print "angles",angleHB(v),angle2D([l,0],[l,v[1]])
        #return angleHB(v)
        if PV :
            #print signe*angle2D([l,0],[l,v[1]]),angle2D([l,0],[l,v[1]])
            return angle2D([l,0],[l,v[1]])
        #signe=-1 if abs(calcOrientation())>135 else 1 
        sens=np.sign(np.dot(v,cls.PostureVector(liste)))
        #p("signe",str(sens))
        #if sens:
        #    print [l,0],[l,v[1]]
        #    return angle2D([l,0],[l,v[1]])
        #print "v",[l,0],[sens*l,v[1]]
        return angle2D([l,0],[sens*l,v[1]])

    @classmethod
    def angleGD2D(cls,liste,p1,p2):
        v=sub(p2,p1)
        #proj1=cls.projPlanPosture(liste,v)
        #proj=cls.projPlanPosture3D(liste,p1,p2)
        #sens=np.sign(np.dot(v,cls.PostureVector(liste)))
        #print sens,np.dot(v,cls.PostureVector(liste,"C"))
        #proj2D=[sens*proj[0],sens*proj[2]]
        #print "vect",v,proj,proj2D
        #p("proj",proj2D,[v[0],v[2]])
        vProj=cls.proj2D(v)
        pProj=cls.proj2D(cls.PostureVector(liste))
        #print "angles",angle2D(pProj,vProj),angle2D(proj2D,[v[0],v[2]])
        #return angle2D(proj2D,[v[0],v[2]])
        return angle2D(pProj,vProj)


    ## on projette le vecteur sur le plan formé par la verticale et le postureVector
    #@classmethod
    #def projPlanPosture(cls,liste,v,Cote=""):
    #    [a,b,c]=cls.PostureVector(liste)
    #    if a!=0:
    #        r=c/a
    #        p0=float((v[0]+r*v[2])/(1.0+r**2))
    #        p2=r*p0
    #    else:
    #        p0=0
    #        p2=v[2]
    #    return [p0,v[1],p2]
    #        #return np.degrees(angle(v,[0,v[1],v[2]]))
    #        #return np.degrees(angle(v,[p0,v[1],p2]))
    #    normal=[-c,0,a]
    #    M=cls.PointOnPlane(liste)
    #    MA=sub(M,v)
    #    dist=np.dot(normal,MA)/np.norm(normal)
        
    # on projette le vecteur sur le plan formé par la verticale et le postureVector
    @classmethod
    def projPlanPosture3D(cls,liste,p1,p2,Cote=""):
        normal=normalize(np.cross(PostureVector(),[0,1,0]))
        M=cls.PointOnPlane(liste)
        p1Proj=projPoint3D(p1,M,normal,Cote)
        p2Proj=projPoint3D(p2,M,normal,Cote)
        return sub(p2Proj,p1Proj)


    @classmethod
    def angleCHB(cls,liste,pointOnCurveList=[],*_):
        v=SubVector(liste[4],liste[3])
        return cls.angleHB(liste,v)
       

    @classmethod
    def angleCGD(cls,liste,pointOnCurveList=[],*_):
        v=SubVector(liste[4],liste[3])
        p1=position(liste[3])
        p2=position(liste[4])
        return cls.angleGD2D(liste,p1,p2)

    @classmethod
    def angleDHB(cls,liste,*_):
        v=SubVector(liste[2],liste[1])
        return cls.angleHB(liste,v)

    @classmethod
    def angleDGD(cls,liste,*_):
        v=SubVector(liste[2],liste[1])
        p1=position(liste[1])
        p2=position(liste[2])
        return cls.angleGD2D(liste,p1,p2)

    @classmethod
    def angleLHB(cls,liste,*_):
        v=SubVector(liste[2],liste[0])
        return cls.angleHB(liste,v)

    @classmethod
    def angleLGD(cls,liste,*_):
        v=SubVector(liste[2],liste[0])
        p1=position(liste[0])
        p2=position(liste[2])
        return cls.angleGD2D(liste,p1,p2)

    @classmethod
    def angleTHB(cls,liste,*_):
        v=SubVector(liste[5],liste[4])
        return cls.angleHB(liste,v)

    @classmethod
    def angleTGD(cls,liste,*_):
        v=SubVector(liste[5],liste[4])
        p1=position(liste[4])
        p2=position(liste[5])
        return cls.angleGD2D(liste,p1,p2)

    @classmethod
    def angleComp(cls,liste,*_):
        v=SubVector(liste[3],liste[2])
        return -cls.angleHB(liste,v)

    @classmethod
    def angleCompGD(cls,liste,*_):
        v=SubVector(liste[3],liste[2])
        p1=position(liste[2])
        p2=position(liste[3])
        return cls.angleGD2D(liste,p1,p2)

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

        






