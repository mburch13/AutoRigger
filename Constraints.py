#this file constrains all of the joints to the controls

#the constraints are point and orient constraints 

import maya.cmds as base

import Controls
import SetAttr

SetAttr = reload(SetAttr)
Controls = reload(Controls)

def ReturnFingerAmount():
    return base.intSliderGrp(fingerCount, query = True, value = True)

def ReturnSpineAmount():
    return base.intSliderGrp(spineCount, query = True, value = True)

def createConstraints(fingerAmount, spineAmount):
	global spineCount
	global fingerCount
	spineCount = spineAmount
	fingerCount = fingerAmount

	l_wristCtrl = base.ls("CTRL_L_WRIST", type = "transform")
	l_wristIK = base.ls("IK_L_ARM")
	l_wristJoint = base.ls("JNT_L_ARM_3")

	r_wristCtrl = base.ls("CTRL_R_WRIST",  type = "transform")
	r_wristIK = base.ls("IK_R_ARM")
	r_wristJoint = base.ls("JNT_R_ARM_3")

	base.pointConstraint(l_wristCtrl, l_wristIK, mo = True)
	base.orientConstraint(l_wristCtrl, l_wristJoint, mo = True)
	base.connectAttr("CTRL_L_WRIST.Elbow_PV", "IK_L_ARM.twist")

	base.pointConstraint(r_wristCtrl, r_wristIK, mo = True)
	base.orientConstraint(r_wristCtrl, r_wristJoint, mo = True)
	base.connectAttr("CTRL_R_WRIST.Elbow_PV", "IK_R_ARM.twist")

	base.orientConstraint("CTRL_L_CLAVICLE", "JNT_L_ARM_0", mo = True)
	base.orientConstraint("CTRL_R_CLAVICLE", "JNT_R_ARM_0", mo = True)

	base.orientConstraint("CTRL_NECK", "JNT_HEAD_0", mo = True)
	base.orientConstraint("CTRL_HEAD", "JNT_HEAD_2", mo = True)
	base.orientConstraint("CTRL_JAW", "JNT_HEAD_3", mo = True)

	clusters = base.ls("Spine_Cluster_*", type = "transform")
	spineCtrl = base.ls("CTRL_SPINE_*", type = "transform")

	for j, cl in enumerate(clusters):
		if j > 0:
			base.parent(cl, spineCtrl[j -1])
		else:
			base.parent(cl, "CTRL_PELVIS")

	for k in range(0, ReturnFingerAmount()):
		l_allFingers = base.ls("JNT_L_FINGER_"+str(k)+"_*")
		r_allFingers = base.ls("JNT_R_FINGER_"+str(k)+"_*")

		for l in range(0, 3):
			if k > 0:
				base.connectAttr("CTRL_L_FINGER_"+str(k)+"_"+str(l)+".rotateZ", l_allFingers[l]+".rotateZ")
				base.connectAttr("CTRL_R_FINGER_"+str(k)+"_"+str(l)+".rotateZ", r_allFingers[l]+".rotateZ")
				base.connectAttr("CTRL_L_FINGER_"+str(k)+"_"+str(l)+".rotateX", l_allFingers[l]+".rotateY")
				base.connectAttr("CTRL_R_FINGER_"+str(k)+"_"+str(l)+".rotateX", r_allFingers[l]+".rotateY")

			else:
				base.connectAttr("CTRL_L_FINGER_"+str(k)+"_"+str(l)+".rotateZ", l_allFingers[l]+".rotateZ")
				base.connectAttr("CTRL_R_FINGER_"+str(k)+"_"+str(l)+".rotateZ", r_allFingers[l]+".rotateZ")
				base.connectAttr("CTRL_L_FINGER_"+str(k)+"_"+str(l)+".rotateX", l_allFingers[l]+".rotateY")
				base.connectAttr("CTRL_R_FINGER_"+str(k)+"_"+str(l)+".rotateX", r_allFingers[l]+".rotateY")


	base.pointConstraint("CTRL_EYES", "JNT_EYE_0", mo = True)
	base.orientConstraint("CTRL_EYES", "JNT_EYE_0", mo = True)

	base.pointConstraint("CTRL_L_EYE", "JNT_EYE_1", mo = True)
	base.orientConstraint("CTRL_L_EYE", "JNT_EYE_1", mo = True)

	base.pointConstraint("CTRL_R_EYE", "JNT_EYE_2", mo = True)
	base.orientConstraint("CTRL_R_EYE", "JNT_EYE_2", mo = True)

	base.parent("IK_L_TOES", "IK_L_FOOTBALL")
	base.parent("IK_L_FOOTBALL", "IK_L_LEG")

	base.parent("IK_R_TOES", "IK_R_FOOTBALL")
	base.parent("IK_R_FOOTBALL", "IK_R_LEG")

	base.pointConstraint("CTRL_R_FOOT", "IK_R_LEG", mo = True)
	base.orientConstraint("CTRL_R_FOOT", "IK_R_LEG", mo = True)

	base.pointConstraint("CTRL_L_FOOT", "IK_L_LEG", mo = True)
	base.orientConstraint("CTRL_L_FOOT", "IK_L_LEG", mo = True)

	base.setAttr("IK_L_LEG.poleVectorX", 1)
	base.setAttr("IK_L_LEG.poleVectorZ", 0)

	l_footAverage = base.shadingNode("plusMinusAverage", asUtility = True, n = "L_Foot_Node")
	base.setAttr(l_footAverage + ".operation", 2)
	base.connectAttr("CTRL_L_FOOT.Knee_Fix", l_footAverage+".input1D[0]")
	base.connectAttr("CTRL_L_FOOT.Knee_Twist", l_footAverage+".input1D[1]")
	base.connectAttr(l_footAverage+".output1D", "IK_L_LEG.twist")
	base.setAttr("CTRL_L_FOOT.Knee_Fix", 90)


	base.setAttr("IK_R_LEG.poleVectorX", 1)
	base.setAttr("IK_R_LEG.poleVectorZ", 0)

	r_footAverage = base.shadingNode("plusMinusAverage", asUtility = True, n = "R_Foot_Node")
	base.setAttr(r_footAverage + ".operation", 2)
	base.connectAttr("CTRL_R_FOOT.Knee_Fix", r_footAverage+".input1D[0]")
	base.connectAttr("CTRL_R_FOOT.Knee_Twist", r_footAverage+".input1D[1]")
	base.connectAttr(r_footAverage+".output1D", "IK_R_LEG.twist")
	base.setAttr("CTRL_R_FOOT.Knee_Fix", 90)

	SetAttr.LockAttr()

	print "Constraints Done"

def BindSkin():
	sel = base.ls(sl = True)
	if len(sel) == 0:
		base.confirmDialog(title = "Empty Selection", message = "Select a Mesh", button = ["OK"])
	else:
		for i in range(0, len(sel)):
			base.skinCluster(sel[i], "JNT_ROOT", bm = 3, sm = 1, dr = 0.1, name = "Mesh"+str(i))
			base.geomBind("Mesh"+str(i), bm = 3, gvp = [256,1])

	if base.objExists("RIG_LAYER"):
		_rig = base.select("JNT_RIG")
		base.editDisplayLayerMembers("RIG_LAYER", "JNT_RIG")
	else:
		_rig = base.select("JNT_RIG")
		base.createDisplayLayer(nr = True, name = "RIG_LAYER")

	_ik = base.ls("IK_*")
	base.editDisplayLayerMembers("RIG_LAYER", _ik)

	if base.objExists("CONTROLERS"):
		base.editDisplayLayerMembers("CONTROLERS", "CTRL_MASTER")
	else:
		_ctrl = base.select("CTRL_MASTER")
		base.createDisplayLayer(nr = True, name = "CONTROLERS")

	print "Skin Bound"
