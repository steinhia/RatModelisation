import maya.cmds as cmds
def test():
    len=cmds.arclen('curve1')
    print len
    cmds.select('curve1.cv[1]')
    cmds.move(0,10,0)
    len2=cmds.arclen('curve1')
    print len2
    cmds.select('curve1')
    sc=len/len2
    cmds.scale(sc,sc,sc,r=1)
    
def test2():
    sc=0.66
    cmds.select('joint1')
    cmds.scale(sc,sc,sc)
    
test2()
    