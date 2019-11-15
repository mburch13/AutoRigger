#this file create all of the needed ik handles with their specific solver

#import maya commands
import maya.cmds as base

#import locator file
import Locators

#reload so that maya does not needed to be restarted after every change
Locators = reload(Locators)

#this function creates all of the ik handles
def IKHandles():
	#arm IK handles
	base.ikHandle(name = "IK_L_ARM", sj = base.ls("JNT_L_ARM_1")[0], ee = base.ls("JNT_L_ARM_3")[0], sol = "ikRPsolver")
	base.ikHandle(name = "IK_R_ARM", sj = base.ls("JNT_R_ARM_1")[0], ee = base.ls("JNT_R_ARM_3")[0], sol = "ikRPsolver")

	#find each wrist position
	leftWristPos = base.xform(base.ls("JNT_L_ARM_3"), q = True, t = True, ws = True)
	rightWristPos = base.xform(base.ls("JNT_R_ARM_3"), q = True, t = True, ws = True)

	#access the arm IK handles
	leftIK = base.ikHandle("IK_L_ARM", q = True, ee = True)
	rightIK = base.ikHandle("IK_R_ARM", q = True, ee = True)

	#correctly position the IK handles to where they are supposed to be
	base.move(leftWristPos[0], leftWristPos[1], leftWristPos[2], leftIK + ".scalePivot", leftIK + ".rotatePivot")
	base.move(rightWristPos[0], rightWristPos[1], rightWristPos[2], rightIK + ".scalePivot", rightIK + ".rotatePivot")

	#create leg ik handles
	base.ikHandle(name = "IK_L_LEG", sj = base.ls("JNT_L_LEG_0")[0], ee = base.ls("JNT_L_LEG_2")[0], sol = "ikRPsolver")
	base.ikHandle(name = "IK_R_LEG", sj = base.ls("JNT_R_LEG_0")[0], ee = base.ls("JNT_R_LEG_2")[0], sol = "ikRPsolver")

	#create left toes and foot ik handles
	base.ikHandle(name = "IK_L_FOOTBALL", sj = base.ls("JNT_L_LEG_2")[0], ee = base.ls("JNT_L_LEG_3")[0], sol = "ikSCsolver")
	base.ikHandle(name = "IK_L_TOES", sj = base.ls("JNT_L_LEG_3")[0], ee = base.ls("JNT_L_LEG_4")[0], sol = "ikSCsolver")

	#create right toes and foot ik handles
	base.ikHandle(name = "IK_R_FOOTBALL", sj = base.ls("JNT_L_LEG_2")[0], ee = base.ls("JNT_L_LEG_3")[0], sol = "ikSCsolver")
	base.ikHandle(name = "IK_R_TOES", sj = base.ls("JNT_L_LEG_3")[0], ee = base.ls("JNT_L_LEG_4")[0], sol = "ikSCsolver")

	#access the spine joints
	rootPos = base.xform(base.ls("JNT_ROOT", type = "joint"), q = True, t = True, ws = True)
	spines = base.ls("JNT_SPINE_*", type = "joint")

	#createing the ik hierarchy
	base.group(em = True, name = "L_side")
	base.parent("IK_L_ARM", "L_side")
	base.parent("IK_L_LEG", "L_side")
	base.parent("IK_L_FOOTBALL", "L_side")
	base.parent("IK_L_TOES", "L_side")

	base.group(em = True, name = "R_side")
	base.parent("IK_R_ARM", "R_side")
	base.parent("IK_R_LEG", "R_side")
	base.parent("IK_R_FOOTBALL", "R_side")
	base.parent("IK_R_TOES", "R_side")

	#creating a spline ik handle
	spinePos = []

	#loop through all of the spine position and put them into an array
	for i, sp in enumerate(spines):
		spinePos.append(base.xform(spines[i], q = True, t = True, ws = True))

	#create the root curve that will be used for the spline ik
	base.curve(p = [(rootPos[0], rootPos[1], rootPos[2])], n = "SpineCurve", degree = 1)

	#loop through the spine positions to creat the spine curve
	for j, sp in enumerate(spinePos):
		base.curve("SpineCurve", a = True, p = [(spinePos[j][0], spinePos[j][1], spinePos[j][2])])

	#access all of the contorl verticies of the curve
	curveCV = base.ls("SpineCurve.cv[0:]", fl = True)

	#loop through the all of the cv to create clusters for the spline ik
	for k, cv in enumerate(curveCV):
		c = base.cluster(cv, cv, n = "Spine_Cluster_" + str(k) + "_")
		if k > 0:
			base.parent(c, "Spine_Cluster_" + str(k-1) + "_Handle")

	#do the spine locators exist
	if(base.objExists("Loc_SPINE_*")):
		spineAmount = base.ls("Loc_SPINE_*", type = "transform")
	#if not use the spine joints
	else:
		spineAmount = base.ls("JNT_SPINE_*")
	#create the spline ik
	base.ikHandle(n = "IK_Spine", sj = "JNT_ROOT", ee = "JNT_SPINE_" + str(len(spineAmount) - 1), sol = "ikSplineSolver", c = "SpineCurve", ccv = False)
	#create the spine ik hierarchy
	base.group(em = True, name = "IK_Handles")
	base.parent("L_side", "IK_Handles")
	base.parent("R_side", "IK_Handles")
	base.parent("IK_Spine", "IK_Handles")
	base.parent("Spine_Cluster_*", "IK_Handles")
