import maya.cmds as cm
if (cm.contextInfo('dragcamContext',ex=1)==0) :
	maya.mel.eval('source camctxt.mel')
cm.setToolTo('dragcamContext')
