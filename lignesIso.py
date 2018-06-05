
curve -p 0 0 0 -p 1 0 0 -d 1;
select -r curve2 ;
rename "curve2" "ray1";
select -r ray1;
select -add camX1 ;
parent -r;
select -r ray1 ;
select -r camX1|ptC ;
select -add cmrkX1 ;
select -add ray1 ;
connectAttr -f |camGroup|camX1|ptC.translate rayShape1.controlPoints[0];
connectAttr -f cmrkX1.translate rayShape1.controlPoints[1];

curve -p 0 0 0 -p 1 0 0 -d 1;
select -r curve2 ;
rename "curve2" "ray2";
select -r ray2;
select -add camX2 ;
parent -r;
select -r ray2 ;
select -add camX2|ptC ;
select -add cmrkX2 ;
select -r ray1 ;
select -r ray2 ;
select -r camX2|ptC ;
select -add cmrkX2 ;
select -add ray2 ;
connectAttr -f cmrkX2.translate rayShape2.controlPoints[0];
connectAttr -f |camGroup|camX2|ptC.translate rayShape2.controlPoints[1];


# pour refaire les lignes iso si besoin

#select -r seq002_x1_tex ;
#select -cl  ;
#select -r persp2 ;
#select -r persp2 ;
#select -cl  ;
#select -r persp2 ;
#select -r persp2 ;
#reorder -relative -14 persp2 ;
#select -cl  ;
#// fileTex::compute, plug=[seq002_x1_file.index] // 
#// fileTex::compute, plug=[seq002_x2_file.index] // 
#fileTex::compute, plug=[seq002_x1_file.index]
#fileTex::compute, plug=[seq002_x2_file.index]
#select -r bottom ;
#select -r front ;
#select -r camX1 ;
#select -r camX1|ptF ;
#select -r camGroup ;
#select -r camX1 ;
#select -r camX2 ;
#select -r camX1 ;
#select -r front ;
#select -r camX1 ;
#select -r camX1|ptF ;
#select -r camX1|ptC ;
#select -r mrkX1 ;
#select -r imgX1 ;
#select -r mrkX1 ;
#select -r cmrkX1 ;
#select -r cmrkX1_pointConstraint1 ;
#select -r mrkX1 ;
#select -r cmrkX1 ;
#select -r rayX2 ;
#select -r camX2|ptC ;
#select -r cmrkX2 ;
#select -r mrkX2 ;
#select -r camX1 ;
#select -r rayX2 ;
#select -r rayX2 ;
#select -r camX1|ptC ;
#showHidden -a;
#select -r cmrkX1 ;
#showHidden -a;
#select -r camX1|ptC ;
#select -r cmrkX1 ;
#select -r mrkX1 ;
#select -r cmrkX1 ;
#cmds.curve(p=[[0,0,0],[1,0,0]],d=1)




#select -r ray1 ;
#select -cl  ;
#execfile('C:/Users/alexandra/Documents/alexandra/scripts/setZoom.py')

#select -r mrkX1 ;
#move -r 0.108131 -0.0143795 -1.072555 ;
#execfile('C:/Users/alexandra/Documents/alexandra/scripts/setZoom.py')

#select -r mrkX1 ;
#move -r 0.372472 -0.0488607 -3.64795 ;
#select -r ray1 ;
#select -r mrkX2 ;
#move -r -0.0255189 -1.994211 -2.429566 ;
#select -cl  ;
#select -r camX1 ;
#select -cl  ;