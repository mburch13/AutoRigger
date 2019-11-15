#this file creates all of the controls for the rig and positions them at the
#same location of the joint

# the functions to create the controls follow theh same formate
# create and modify a curve to a unique shapes
# position the control to the joint that it will controls
# parent the control to mimic the hierarchy of the joints

import maya.cmds as base
import maya.OpenMaya as om

#access gui values
def ReturnFingerAmount():
    return base.intSliderGrp(fingerCount, query = True, value = True)

def ReturnSpineAmount():
    return base.intSliderGrp(spineCount, query = True, value = True)

#create all the controls
def createCTRL(spineValue, fingerValue):
	global spineCount
	global fingerCount
	spineCount = spineValue
	fingerCount = fingerValue

    #helper functions to create controls
	createMaster()
	createPelvis()

	createFeet()
	createSpines(spineCount)
	createClavicles(spineCount)
	createWrists()
	createNeck(spineCount)
	createHead()
	createEye()
	createFingers(fingerCount)
	setColors()
	print "controls created"

#create master control
def createMaster():
	master_ctrl = base.circle(nr = (0,1,0), c = (0,0,0), radius = 1, name = "CTRL_MASTER")
	base.scale(1,1,1, master_ctrl)

	base.makeIdentity(master_ctrl, apply = True, t = 1, r = 1, s = 1)

#create the pelvis control
def createPelvis():
	pelvis_ctrl = base.circle(nr = (0,1,0), c = (0,0,0), radius = 1, degree = 1, s = 8, name = "CTRL_PELVIS")
	rootPos = base.xform(base.ls("JNT_ROOT", type = "joint"), q = True, t = True, ws = True)
	base.move(rootPos[0], rootPos[1], rootPos[2], pelvis_ctrl)
	base.scale(0.3, 0.3, 0.3, pelvis_ctrl)
	base.makeIdentity(pelvis_ctrl, apply = True, t = 1, r = 1, s = 1)
	base.parent(pelvis_ctrl, "CTRL_MASTER")

#create the wrist controls
def createWrists():
	sides = ['L', 'R']

	for side in sides:
		wrist_ctrl = base.group(em = True, name = "CTRL_"+side+"_WRIST")

		ctrl1 = base.circle(nr = (0,1,0), c = (0,0,0), radius = 1, degree = 1, s = 16, name = "CTRL_"+side+"_WRIST0")
		ctrl2 = base.circle(nr = (0,1,0), c = (0,0,0), radius = 1, degree = 1, s = 16, name = "CTRL_"+side+"_WRIST1")
		ctrl3 = base.circle(nr = (0,1,0), c = (0,0,0), radius = 1, degree = 1, s = 16, name = "CTRL_"+side+"_WRIST2")

		curves = [ctrl1, ctrl2, ctrl3]
		for cv in curves:
			crvShape = base.listRelatives(cv, shapes = True)
			base.parent(crvShape, wrist_ctrl, s = True, r = True)
			base.delete(cv)
		base.select("CTRL_"+side+"_WRIST")
		base.addAttr(shortName = "PV", longName = "Elbow_PV", attributeType = "double", defaultValue = 0, minValue = -100, maxValue = 100, keyable = True)
		base.scale(0.07,0.07,0.07, wrist_ctrl)

		wristPos = base.xform(base.ls("JNT_"+side+"_ARM_3"), q = True, t = True, ws = True)
		wristRot = base.joint(base.ls("JNT_"+side+"_ARM_3"), q = True, o = True)
		if base.objExists("JNT_L_ArmTwist_*"):
			armTwists = base.ls("JNT_L_ArmTwist_*")
			print base.xform(base.ls("JNT_"+side+"_ArmTwist_"+str(len(armTwists) - 1)), q = True, ws = True, ro = True)
			wristRotation = base.xform(base.ls("JNT_"+side+"_ArmTwist_"+str(len(armTwists) - 1)), q = True, ws = True, ro = True)
		else:
			wristRotation = base.xform(base.ls("JNT_"+side+"ARM_3"), q = True, ws = True, ro = True)
		base.move(wristPos[0], wristPos[1], wristPos[2], wrist_ctrl)
		wristGrp = base.group(em = True, name = "CTRL_GRP_"+side+"_WRIST")
		base.move(wristPos[0], wristPos[1], wristPos[2], wristGrp)
		base.parent(wrist_ctrl, wristGrp)

		base.rotate(0,0, -wristRotation[2], wristGrp)
		base.parent(wristGrp, "CTRL_"+side+"_CLAVICLE")
	wristGrpList = base.listRelatives(wristGrp)

#create clavicle controls
def createClavicles(spineCount):
	l_clavicle = base.curve(p = [(1,0,0), (1,1,1), (1,1.5,2), (1,1.7,3), (1,1.5,4), (1,1,5), (1,0,6), (-1,0,6), (-1,1,5), (-1,1.5,4), (-1,1.7,3), (-1,1.5,2), (-1,1,1), (-1,0,0)], degree = 1, name = "CTRL_L_CLAVICLE")
	r_clavicle = base.curve(p = [(1,0,0), (1,1,1), (1,1.5,2), (1,1.7,3), (1,1.5,4), (1,1,5), (1,0,6), (-1,0,6), (-1,1,5), (-1,1.5,4), (-1,1.7,3), (-1,1.5,2), (-1,1,1), (-1,0,0)], degree = 1, name = "CTRL_R_CLAVICLE")

	base.scale(0.02, 0.02, 0.02, l_clavicle)
	base.scale(0.02, 0.02, 0.02, r_clavicle)

	l_armPos = base.xform(base.ls("JNT_L_ARM_0"), q = True, t = True, ws = True)
	r_armPos = base.xform(base.ls("JNT_R_ARM_0"), q = True, t = True, ws = True)

	l_claviclePos = base.xform(base.ls("JNT_L_ARM_0"), q = True, t = True, ws = True)
	r_claviclePos = base.xform(base.ls("JNT_R_ARM_0"), q = True, t = True, ws = True)

	base.move(l_armPos[0], l_armPos[1] + 0.125, l_armPos[2] - 0.1, l_clavicle)
	base.move(r_armPos[0], r_armPos[1] + 0.125, r_armPos[2] - 0.1, r_clavicle)

	base.move(l_claviclePos[0], l_claviclePos[1], l_claviclePos[2], l_clavicle+".scalePivot", l_clavicle+".rotatePivot")
	base.move(r_claviclePos[0], r_claviclePos[1], r_claviclePos[2], r_clavicle+".scalePivot", r_clavicle+".rotatePivot")

	base.parent(l_clavicle, "CTRL_SPINE_"+str(ReturnSpineAmount()-1))
	base.parent(r_clavicle, "CTRL_SPINE_"+str(ReturnSpineAmount()-1))

def createSpines(spineCount):
	for i in range(0, ReturnSpineAmount()):
		spinePos = base.xform(base.ls("JNT_SPINE_"+str(i)), q = True, t = True, ws = True)
		spine = base.curve(p = [(0, spinePos[1], spinePos[2]), (0, spinePos[1], spinePos[2] - 1), (0, spinePos[1] + 0.1, spinePos[2] - 1.1), (0, spinePos[1] + 0.1, spinePos[2] - 1.4), (0, spinePos[1] - 0.1, spinePos[2] - 1.4), (0, spinePos[1] - 0.1, spinePos[2] - 1.1), (0, spinePos[1], spinePos[2] - 1)], degree = 1, name = "CTRL_SPINE_"+str(i))
		base.move(spinePos[0], spinePos[1], spinePos[2], spine+".scalePivot", spine+".rotatePivot")
		base.scale(0.5,0.5,0.5,spine)
		if i == 0:
			base.parent(spine, "CTRL_PELVIS")
		else:
			base.parent(spine, "CTRL_SPINE_"+str(i-1))

def createNeck(spineCount):
	neck = base.curve(p = [(0.5,0,0), (0.25, -0.25, -0.5), (-0.25, -0.25, -0.5), (-0.5,0,0), (-0.25,-0.25,0.5), (0.25, -0.25, 0.5), (0.5,0,0)], degree = 1, name = "CTRL_NECK")
	neckPos = base.xform(base.ls("JNT_HEAD_0"), q = True, t = True, ws = True)
	base.scale(0.3, 0.3, 0.3, neck)
	base.move(neckPos[0], neckPos[1], neckPos[2], neck)
	base.move(neckPos[0], neckPos[1], neckPos[2], neck+".scalePivot", neck+".rotatePivot")
	base.parent(neck, "CTRL_SPINE_"+str(ReturnSpineAmount() - 1))

	base.makeIdentity(neck, apply = True, t = 1, r = 1, s = 1)

def createHead():
	head = base.curve(p = [(0.5,0,0), (0.25,-0.25,-0.5), (0.25,-0.5, -0.5), (0,-0.6,-0.5), (-0.25,-0.5,-0.5), (-0.25, -0.25, -0.5), (-0.5,0,0), (-0.25, -0.25, 0.5), (-0.25, -0.5, 0.5), (0,-0.6,0.5), (0.25, -0.5, 0.5), (0.25, -0.25, 0.5), (0.5,0,0)], degree = 1, name = "CTRL_HEAD")
	base.scale(0.3, 0.3, 0.3, head)
	headPos = base.xform(base.ls("JNT_HEAD_2"), q = True, t = True, ws = True)
	neckPos = base.xform(base.ls("JNT_HEAD_1"), q = True, t = True, ws = True)

	base.move(headPos[0], headPos[1], headPos[2], head)
	base.move(neckPos[0], neckPos[1], neckPos[2], head+".scalePivot", head+".rotatePivot")
	base.parent(head, "CTRL_NECK")
	base.makeIdentity(head, apply = True, t = 1, r = 1, s = 1)

	jaw = base.curve(p = [(0,0,0), (0.1,0.1,0), (0, 0.2, 0), (-0.1, 0.1,0), (0,0,0)], degree = 1, name = "CTRL_JAW")
	base.move(0, 0.1, 0, jaw+".scalePivot", jaw+".rotatePivot")
	jawPos = base.xform(base.ls("JNT_HEAD_4"), q = True, t = True, ws = True)
	jawStart = base.xform(base.ls("JNT_HEAD_3"), q = True, t = True, ws = True)
	base.move(jawPos[0], jawPos[1] - 0.1, jawPos[2] +0.1, jaw)
	base.move(jawStart[0], jawStart[1], jawStart[2], jaw+".scalePivot", jaw+".rotatePivot")
	base.parent(jaw, "CTRL_HEAD")
	base.makeIdentity(jaw, apply = True, t = 1, r = 1, s = 1)

def createEye():
	eyeCon = base.circle(nr = (0,1,0), c = (0,0,0), radius = 0.1, name = "CTRL_EYES")
	eyeConPos = base.xform("JNT_EYE_0", q = True, t = True, ws = True)
	base.move(eyeConPos[0], eyeConPos[1], eyeConPos[2] + 0.1, eyeCon)
	base.rotate(90, 0, 0, eyeCon)
	base.parent(eyeCon, "CTRL_HEAD")

	eyeGrp = base.group(em = True, name = "CTRL_EYE_GRP")
	base.parent(eyeGrp, eyeCon)

	l_eye = base.circle(nr = (0,1,0), c = (0,0,0), radius = 0.1, name = "CTRL_L_EYE")
	l_eyePos = base.xform("JNT_EYE_1", q = True, t = True, ws = True)
	base.move(l_eyePos[0], l_eyePos[1], l_eyePos[2], l_eye)
	base.rotate(90, 0, 0, l_eye)
	base.parent(l_eye, eyeGrp)

	r_eye = base.circle(nr = (0,1,0), c = (0,0,0), radius = 0.1, name = "CTRL_R_EYE")
	r_eyePos = base.xform("JNT_EYE_2", q = True, t = True, ws = True)
	base.move(r_eyePos[0], r_eyePos[1], r_eyePos[2], r_eye)
	base.rotate(90, 0, 0, r_eye)
	base.parent(r_eye, eyeGrp)

def createFeet():
	l_arrow = base.curve(p = [(1,0,0), (1,0,2), (2,0,2), (0,0,6), (-2,0,2), (-1,0,2), (-1,0,0), (1,0,0)], degree = 1, name = "CTRL_L_FOOT")
	base.addAttr(shortName = "KF", longName = "Knee_Twist", attributeType = "double", defaultValue = 0, minValue = -100, maxValue = 100, keyable = True)
	base.addAttr(shortName = "KR", longName = "Knee_Fix", attributeType = "double", defaultValue = 0, minValue = 0, maxValue = 100, keyable = True)
	base.addAttr(shortName = "FR", longName = "Foot_Roll", attributeType = "double", defaultValue = 0, minValue = 0, maxValue = 100, keyable = True)
	base.addAttr(shortName = "BR", longName = "Ball_Roll", attributeType = "double", defaultValue = 0, minValue = 0, maxValue = 100, keyable = True)

	r_arrow = base.curve(p = [(1,0,0), (1,0,2), (2,0,2), (0,0,6), (-2,0,2), (-1,0,2), (-1,0,0), (1,0,0)], degree = 1, name = "CTRL_R_FOOT")
	base.addAttr(shortName = "KF", longName = "Knee_Twist", attributeType = "double", defaultValue = 0, minValue = -100, maxValue = 100, keyable = True)
	base.addAttr(shortName = "KR", longName = "Knee_Fix", attributeType = "double", defaultValue = 0, minValue = 0, maxValue = 100, keyable = True)
	base.addAttr(shortName = "FR", longName = "Foot_Roll", attributeType = "double", defaultValue = 0, minValue = 0, maxValue = 100, keyable = True)
	base.addAttr(shortName = "BR", longName = "Ball_Roll", attributeType = "double", defaultValue = 0, minValue = 0, maxValue = 100, keyable = True)

	base.scale(0.08, 0.08, 0.08, l_arrow)
	base.scale(0.08, 0.08, 0.08, r_arrow)

	l_footPos = base.xform(base.ls("JNT_L_LEG_2"), q = True, t = True, ws = True)
	r_footPos = base.xform(base.ls("JNT_R_LEG_2"), q = True, t = True, ws = True)

	base.move(l_footPos[0], 0, l_footPos[2], l_arrow)
	base.move(r_footPos[0], 0, r_footPos[2], r_arrow)

	base.makeIdentity(l_arrow, apply = True, t = 1, r = 1, s = 1)
	base.makeIdentity(r_arrow, apply = True, t = 1, r = 1, s = 1)

	base.parent(l_arrow, "CTRL_MASTER")
	base.parent(r_arrow, "CTRL_MASTER")

def createFingers(fingerCount):
	sides = ["L", "R"]

	for side in sides:
		for i in range(0, ReturnFingerAmount()):
			for j in range(0,3):
				fingerRotation = base.xform(base.ls("Loc_"+side+"_Finger_"+str(i)+"_"+str(j)), q = True, ws = True, ro = True)
				fingerPosition = base.xform(base.ls("Loc_"+side+"_Finger_"+str(i)+"_"+str(j)), q = True, t = True, ws = True)

				allFingers = base.ls("JNT_"+side+"_FINGER_"+str(i)+"_"+str(j))

				finger = base.curve(p = [(0,0,0), (0,0,0.5), (0.2,0,0.7), (0,0,0.9), (-0.2,0,0.7), (0,0,0.5)], degree = 1, name = "CTRL_"+side+"_FINGER_"+str(i)+"_"+str(j))
				base.rotate(-90,0,0,finger)

				for k, fi in enumerate(allFingers):
					fingerPos = base.xform(fi, q = True, t = True, ws = True)
					fingerRot = base.joint(fi, q = True, o = True)
					base.scale(0.1,0.1,0.1, finger)
					base.move(fingerPos[0], fingerPos[1], fingerPos[2], finger)
				fingerGrp = base.group(em = True, n = "CTRL_GRP_"+side+"_FINGER_"+str(i))
				base.move(fingerPosition[0], fingerPosition[1], fingerPosition[2], fingerGrp)
				base.rotate(0, fingerRotation[1], 0, fingerGrp)
				base.makeIdentity(finger, apply = True, t = 1, r = 1, s = 1)
				base.makeIdentity(fingerGrp, apply = True, t =1, r =1, s =1)
				base.parent(finger, fingerGrp)
				base.rotate(0,fingerRotation[1], 0, fingerGrp, r =True)

				if j > 0:
					base.parent(fingerGrp, "CTRL_"+side+"_FINGER_"+str(i)+"_"+str(j-1))
				else:
					base.parent(fingerGrp, "CTRL_"+side+"_WRIST")

def setColors():
	base.setAttr("CTRL_MASTER.overrideEnabled", 1)
	base.setAttr("CTRL_MASTER.overrideRGBColors", 1)
	base.setAttr("CTRL_MASTER.overrideColorRGB", 1,1,1)

def deleteControls():
	controls = base.ls("CTRL_*")
	base.delete(controls)
	print "deleted controls"
