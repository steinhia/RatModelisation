sliderGrp=mainFct()
a=getCLen()
sliderGrp.do("courbure c",45)

p=position(curvei(5))

#b2=position(curvei(n2N('T1')))
for i in range(10):
    a2=getCLen()
    sc=a/a2
    cmds.select(curvei(4),curvei(5),curvei(6))
    cmds.scale(sc,sc,sc,pivot=p)
print getCLen()
print a