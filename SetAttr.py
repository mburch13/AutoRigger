#this file locks unneeded attributes in the channel box

import maya.cmds as base

def LockAttr():
	axis = ['X', 'Y', 'Z']

	allSpines = base.ls("CTRL_SPINE_*", type = "transform")
	l_allFingers = base.ls("CTRL_L_FINGER_*_0", type = "transform")
	r_allFingers = base.ls("CTRL_R_FINGER_*_0", type = "transform")

	for axe in axis:
		base.setAttr("CTRL_PELVIS.scale"+axe, lock = True, k = False)
		base.setAttr("CTRL_L_WRIST.scale"+axe, lock = True, k = False)
		base.setAttr("CTRL_R_WRIST.scale"+axe, lock = True, k = False)
		base.setAttr("CTRL_L_FOOT.scale"+axe, lock = True, k = False)
		base.setAttr("CTRL_R_FOOT.scale"+axe, lock = True, k = False)

		base.setAttr("CTRL_L_CLAVICLE.scale"+axe, lock = True, k = False)
		base.setAttr("CTRL_L_CLAVICLE.translate"+axe, lock = True, k = False)
		base.setAttr("CTRL_R_CLAVICLE.scale"+axe, lock = True, k = False)
		base.setAttr("CTRL_R_CLAVICLE.translate"+axe, lock = True, k = False)

		for i in range(0, len(allSpines)):
			base.setAttr("CTRL_SPINE_"+str(i)+".translate"+axe, lock = True, k = False)
			base.setAttr("CTRL_SPINE_"+str(i)+".scale"+axe, lock = True, k = False)

		base.setAttr("CTRL_NECK.scale"+axe, lock = True, k = False)
		base.setAttr("CTRL_NECK.translate"+axe, lock = True, k = False)

		base.setAttr("CTRL_JAW.scale"+axe, lock = True, k = False)
		base.setAttr("CTRL_JAW.translate"+axe, lock = True, k = False)
		base.setAttr("CTRL_JAW.rotateY", lock = True, k = False)
		base.setAttr("CTRL_JAW.rotateZ", lock = True, k = False)

		base.setAttr("CTRL_EYES.scale"+axe, lock = True, k = False)
		base.setAttr("CTRL_L_EYE.scale"+axe, lock = True, k = False)
		base.setAttr("CTRL_L_EYE.rotate"+axe, lock = True, k = False)
		base.setAttr("CTRL_R_EYE.scale"+axe, lock = True, k = False)
		base.setAttr("CTRL_R_EYE.rotate"+axe, lock = True, k = False)


		for j in range(0, len(l_allFingers)):
			for k in range(0,3):
				base.setAttr("CTRL_L_FINGER_"+str(j)+"_"+str(k)+".scale"+axe, lock = True, k = False)
				base.setAttr("CTRL_R_FINGER_"+str(j)+"_"+str(k)+".scale"+axe, lock = True, k = False)

				base.setAttr("CTRL_L_FINGER_"+str(j)+"_"+str(k)+".translate"+axe, lock = True, k = False)
				base.setAttr("CTRL_R_FINGER_"+str(j)+"_"+str(k)+".translate"+axe, lock = True, k = False)
