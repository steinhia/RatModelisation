import maya.cmds as cm
import sys
sys.path.append("C:/Users/alexa/Documents/alexandra/scripts")

if (cm.contextInfo('dragcamContext',ex=1)==0) :
	maya.mel.eval('source camctxt.mel')
cm.setToolTo('dragcamContext')
