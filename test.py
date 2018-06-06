import sys
sys.path.append("C:/Users/alexandra/Documents/alexandra/scripts")
path="C:/Users/alexandra/Documents/alexandra/scripts/"


def test():

    for i in range(1):
        execfile(path+"Short.py")

#print "\n"

#a=getBoundingVolumeList(nameList)
#HidePolygons()
#b=getBoundingVolumeList(nameList)

#for i in range(len(a)):
#    print a[i]/b[i]
#cvParam=calcCVParameters()
#cvParam2=calcCVParameters()
#print cvParam
#print cvParam2
#keepParameters(cvParam)
#print calcCVParameters()
#getDistCVPoint()
#recalageTangent(2,2)
#a=sliderGrp
#liste=a.buttonList
#n=len(liste)
#for i in range(n):
#    print liste[i].valueReset


   # a=position(locator(2))
   # b=position(locator(3))
   # mil=getMilieu(a,b)
   # cmds.locator()
   # cmds.move(mil[0],mil[1],mil[2])
   # 
   # a=cmds.ls('Rat5:obj*')
   # for i in a:
   #     if 'Shape' not in i:
   #         newName=i[5:]
   #         cmds.select(i)
   #         cmds.rename(i,newName)
   #       
    param=calcCVParameters()
    print param
    
    #recalageTangent(n2N('L3'),1)
    
    param2=calcCVParameters()
    print param2
    keepParameters(param)
    print calcCVParameters()
        

test()


