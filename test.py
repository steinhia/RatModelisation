import sys
sys.path.append("C:/Users/alexandra/Documents/alexandra/scripts")
path="C:/Users/alexandra/Documents/alexandra/scripts/"

#for i in range(1):
#    execfile(path+"TestClass.py")

#print "\n"

#a=getBoundingVolumeList(nameList)
#HidePolygons()
#b=getBoundingVolumeList(nameList)

#for i in range(len(a)):
#    print a[i]/b[i]
cvParam=calcCVParameters()
cvParam2=calcCVParameters()
print cvParam
print cvParam2
keepParameters(cvParam)
print calcCVParameters()
#getDistCVPoint()
recalageTangent(2,2)
#a=sliderGrp
#liste=a.buttonList
#n=len(liste)
#for i in range(n):
#    print liste[i].valueReset