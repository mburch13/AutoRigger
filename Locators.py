#this file will create locators in a default structure that can be moved around
#for customizable position.  hierarchy will be preserved during all modified transformtions

#all of the move commands are to arrbitrary posisitons to help illustrate the
#type of right that will be created.  Values are meant to be changed via the interactive windows
#in maya.  DO NOT CHANGE THE VALUES IN THE CODE.

#import maya commands
import maya.cmds as base

#global variable that accesses the input values from the gui
global spineCount
global fingerCount

#returns the gui value
def ReturnFingerAmount():
    return base.intSliderGrp(fingerCount, query = True, value = True)

#returns the gui value
def ReturnSpineAmount():
    return base.intSliderGrp(spineCount, query = True, value = True)

#"main" fuction that creates all of the locators
def createLocators(spineValue, fingerValue):
    global spineCount
    global fingerCount

    spineCount = spineValue
    fingerCount = fingerValue

    print spineCount

    if base.objExists("Loc_Master"):
        print "Already Exists"
    else:
        base.group(em = True, name = "Loc_Master")

    root = base.spaceLocator(n = "Loc_ROOT")
    base.scale(0.1,0.1,0.1, root)
    base.move(0,1,0, root)
    base.parent(root, "Loc_Master")

    #calling helper functions that create other locators
    createSpine()
    createHead()
    createEyes(1)
    createEyes(-1)
    createArms(1)
    createArms(-1)
    createLegs(1)
    createLegs(-1)
    print "created locators"

#create spine locators
def createSpine():
    #loop through the value gathered from the gui for spine amount
    for i in range(0, ReturnSpineAmount()):
        #creates the locator
        spine = base.spaceLocator(n = "Loc_SPINE_" + str(i))
        #scales the locator
        base.scale(0.1,0.1,0.1, spine)

        #names each locator using the increment value from the for loop
        if i == 0:
            base.parent(spine, "Loc_ROOT")
        else:
            base.parent(spine, "Loc_SPINE_" + str(i-1))
        base.move(0, 1.25 + (0.25 * i), 0, spine)
    print "spine created"

#creates the head locators
def createHead():
    #does the head locator group exist
    if base.objExists("Loc_HEAD_GRP"):
        print "nothing"

    #if not create the head locator group
    else:
        headGrp = base.group(em = True, name = "Loc_HEAD_GRP")
        base.parent(headGrp, "Loc_SPINE_" + str(ReturnSpineAmount() - 1))

        #create the neck start
        neck = base.spaceLocator(n = "Loc_Head_0neck_START")
        base.scale(0.1,0.1,0.1, neck)
        base.parent(neck, headGrp)
        base.move(0, 1.25 + (0.25 * ReturnSpineAmount()), 0, neck)

        #create the neck end
        neck = base.spaceLocator(n = "Loc_Head_1neck_END")
        base.parent(neck, "Loc_Head_0neck_START")
        base.scale(1,1,1,neck)
        base.move(0,1.4+(0.25*ReturnSpineAmount()),0,neck)

        #mouth connecter for the mouth
        head = base.spaceLocator(n = "Loc_Head_2Head")
        base.scale(0.1,0.1,0.1, head)
        base.parent(head, neck)
        base.move(0, 1.6 + (0.25 * ReturnSpineAmount()), 0, head)

        #create the lower jaw
        jaw_Start = base.spaceLocator(n = "Loc_Head_3Jaw_start")
        jaw_End = base.spaceLocator(n = "Loc_Head_4Jaw_end")
        base.parent(jaw_Start, head)
        base.parent(jaw_End, jaw_Start)
        base.scale(1,1,1, jaw_End)
        base.scale(0.5,0.5,0.5, jaw_Start)
        base.move(0, 1.6 + (0.25 * ReturnSpineAmount()), 0.02, jaw_Start)
        base.move(0, 1.6 + (0.25 * ReturnSpineAmount()), 0.15, jaw_End)

    print "create head"

#create eye locators
#side argurment will be used to  move the L and R sides to the correct side of the Y axis
def createEyes(side):
    #does the locator eye group exist
	if base.objExists("Loc_Eye_Grp"):
		print "nothing"

    #if not create eye locator group
	else:
		eyeGrp = base.group(em = True, name = "Loc_Eye_Grp")
		base.parent(eyeGrp, "Loc_Head_2Head")

		#create eye connector
		eyeC = base.spaceLocator(n = "Loc_Eye_0connect")
		base.scale(0.1,0.1,0.1, eyeC)
		base.parent(eyeC, eyeGrp)
		base.move(0, 1.7 + (0.25 * ReturnSpineAmount()), 0.15, eyeC)

	if side == 1:
		#left eye locator
		l_eye = base.spaceLocator(n = "Loc_Eye_1L")
		base.scale(0.1,0.1,0.1, l_eye)
		base.parent(l_eye, "Loc_Eye_0connect")
		base.move(0.1 * side, 1.7 + (0.25 * ReturnSpineAmount()), 0.2, l_eye)

	else:
		#right eye locator
		r_eye = base.spaceLocator(n = "Loc_Eye_2R")
		base.scale(0.1,0.1,0.1, r_eye)
		base.parent(r_eye, "Loc_Eye_0connect")
		base.move(0.1 * side, 1.7 + (0.25 * ReturnSpineAmount()), 0.2, r_eye)

#create the arm Locators
#side argurment will be used to  move the L and R sides to the correct side of the Y axis
def createArms(side):
    #left arm locators
	if side == 1:
		if base.objExists("Loc_L_Arm_GRP"):
		     print "nothing"
		else:
			L_arm = base.group(em = True, name = "Loc_L_Arm_GRP")
			base.parent(L_arm, "Loc_SPINE_" + str(ReturnSpineAmount() - 1))
			#clavicle
			clavicle = base.spaceLocator(n = "Loc_L_Arm_0Clavicle")
			base.scale(0.1,0.1,0.1, clavicle)
			base.parent(clavicle, L_arm)
			base.move(0.1 * side, 1.5 + (0.25 * ReturnSpineAmount()), 0.1, clavicle)

			#upperArm
			shoulder = base.spaceLocator(n = "Loc_L_Arm_1Upper")
			base.scale(0.1,0.1,0.1, shoulder)
			base.parent(shoulder, clavicle)
			base.move(0.35 * side, 1.5 + (0.25 * ReturnSpineAmount()), 0, shoulder)

			#elbow
			elbow = base.spaceLocator(n = "Loc_L_Arm_2Elbow")
			base.scale(0.1,0.1,0.1, elbow)
			base.parent(elbow, shoulder)
			base.move(0.8 * side, 1.5 + (0.25 * ReturnSpineAmount()), elbow)

			#wrist
			wrist = base.spaceLocator(n = "Loc_L_Arm_3Wrist")
			base.scale(0.1,0.1,0.1, wrist)
			base.parent(wrist, elbow)
			base.move(1.3 * side, 1.5 + (0.25 * ReturnSpineAmount()), 0, wrist)

			base.move(0.35 * side, (0.05 * ReturnSpineAmount()), 0, L_arm)

			#move wrist

			createHands(1, wrist)
	#right
	else:
		if base.objExists("Loc_R_Arm_GRP"):
			print "nothing"
		else:
			R_arm = base.group(em = True, name = "Loc_R_Arm_GRP")
			base.parent(R_arm, "Loc_SPINE_" + str(ReturnSpineAmount() - 1))

			#clavicle
			clavicle = base.spaceLocator(n = "Loc_R_Arm_0Clavicle")
			base.scale(0.1,0.1,0.1, clavicle)
			base.parent(clavicle, R_arm)
			base.move(0.1 * side, 1.5 + (0.25 * ReturnSpineAmount()), 0.1, clavicle)

			#shoulder
			shoulder = base.spaceLocator(n = "Loc_R_Arm_1Upper")
			base.scale(0.1,0.1,0.1, shoulder)
			base.parent(shoulder, clavicle)
			base.move(0.35 * side, 1.5 + (0.25 * ReturnSpineAmount()), 0, shoulder)

			#elbow
			elbow = base.spaceLocator(n = "Loc_R_Arm_2Elbow")
			base.scale(0.1,0.1,0.1, elbow)
			base.parent(elbow, shoulder)
			base.move(0.8 * side, 1.5 + (0.25 * ReturnSpineAmount()), -0.2, elbow)

			#wrist
			wrist = base.spaceLocator(n = "Loc_R_Arm_3Wrist")
			base.scale(0.1,0.1,0.1)
			base.parent(wrist, elbow)
			base.move(1.3 * side, 1.5 + (0.25 * ReturnSpineAmount()), 0, wrist)

			base.move(0.35 * side, (0.05 * ReturnSpineAmount()), 0, R_arm)

			#move wrist

			createHands(-1, wrist)
	print "arm created"

def createHands(side, wrist):
	if side == 1:
		if base.objExists("Loc_L_Hand_GRP"):
			print "nothing"
		else:
			L_Hand = base.group(em = True, name = "Loc_L_Hand_GRP")
			pos = base.xform(wrist, q = True, t = True, ws = True)
			base.move(pos[0], pos[1], pos[2], L_Hand)
			base.parent(L_Hand, "Loc_L_Arm_3Wrist")
			for i in range(0, ReturnFingerAmount()):
				createFingers(1, pos, i)
	else:
		if base.objExists("Loc_R_Hand_GRP"):
			print "nothing"
		else:
			R_Hand = base.group(em = True, name = "Loc_R_Hand_GRP")
			pos = base.xform(wrist, q = True, t = True, ws = True)
			base.move(pos[0], pos[1], pos[2], R_Hand)
			base.parent(R_Hand, "Loc_R_Arm_3Wrist")
			for i in range(0, ReturnFingerAmount()):
				createFingers(-1,pos, i)
	print "hand created"

def createFingers(side, handPos, count):
    for x in range(0, 3):
        if side == 1:
            finger = base.spaceLocator(n = "Loc_L_Finger_" + str(count) + "_" + str(x))
            base.scale(0.05,0.05,0.05, finger)
            if x == 0:
                base.parent(finger, "Loc_L_Hand_GRP")
            else:
                base.parent(finger, "Loc_L_Finger_" + str(count) + "_" + str(x-1))
            base.move(handPos[0] + (0.1 + (0.1 * x))* side, handPos[1], handPos[2] + -(0.05*count), finger)
        else:
            finger = base.spaceLocator(n = "Loc_R_Finger_" + str(count) + "_" + str(x))
            base.scale(0.05, 0.05, 0.05, finger)
            if x == 0:
                base.parent(finger, "Loc_R_Hand_GRP")
            else:
                base.parent(finger, "Loc_R_Finger_" + str(count) + "_" + str(x-1))
            base.move(handPos[0] + (0.1 + (0.1*x)) *side, handPos[1], handPos[2] + -(0.05*count), finger)
    print "fingers created"

def createLegs(side):
    if side == 1:
        if base.objExists("Loc_L_Leg_GRP"):
            print "nothing"
        else:
            L_leg = base.group(em = True, name = "Loc_L_Leg_GRP")
            base.parent(L_leg, "Loc_ROOT")

            #hip
            hip = base.spaceLocator(n = "Loc_L_Leg_1Hip")
            base.scale(0.1,0.1,0.1)
            base.parent(hip, L_leg)

            #knee
            knee = base.spaceLocator(n = "Loc_L_Leg_2Knee")
            base.scale(0.1,0.1,0.1)
            base.parent(knee, hip)

            #ankle
            ankle = base.spaceLocator(n = "Loc_L_Leg_3Ankle")
            base.scale(0.1,0.1,0.1)
            base.parent(ankle, knee)

            #ball of foot
            foot = base.spaceLocator(n = "Loc_L_Leg_4Foot")
            base.scale(0.1,0.1,0.1)
            base.parent(foot, ankle)

            #toes
            toes = base.spaceLocator(n = "Loc_L_Leg_5Toes")
            base.scale(0.1,0.1,0.1)
            base.parent(toes, foot)

            base.move(0.35 * side, 0.75, 0, L_leg)
            base.move(0.35 * side, 0.5, 0.2, knee)
            base.move(0.35 * side, 0.1, 0, ankle)
            base.move(0.35 * side, 0, .25, foot)
            base.move(0.35 * side, 0, 0.5, toes)

    else:
        if base.objExists("Loc_R_Leg_GRP"):
            print "nothing"
        else:
            R_leg = base.group(em = True, name = "Loc_R_Leg_GRP")
            base.parent(R_leg, "Loc_ROOT")

            #hip
            hip = base.spaceLocator(n = "Loc_R_Leg_1Hip")
            base.scale(0.1,0.1,0.1)
            base.parent(hip, R_leg)

            #knee
            knee = base.spaceLocator(n = "Loc_R_Leg_2Knee")
            base.scale(0.1,0.1,0.1)
            base.parent(knee, hip)

            #ankle
            ankle = base.spaceLocator(n = "Loc_R_Leg_3Ankle")
            base.scale(0.1,0.1,0.1)
            base.parent(ankle, knee)

            #ball of foot
            foot = base.spaceLocator(n = "Loc_R_Leg_4Foot")
            base.scale(0.1,0.1,0.1)
            base.parent(foot, ankle)

            #toes
            toes = base.spaceLocator(n = "Loc_R_Leg_5Toes")
            base.scale(0.1,0.1,0.1)
            base.parent(toes, foot)

            base.move(0.35 * side, 0.75, 0, R_leg)
            base.move(0.35 * side, 0.5, 0.2, knee)
            base.move(0.35 * side, 0.1, 0, ankle)
            base.move(0.35 * side, 0, .25, foot)
            base.move(0.35 * side, 0, 0.5, toes)
    print "leg created"

def mirrorLocators():
    all_L_loc = base.ls("Loc_L_*")
    L_loc = base.listRelatives(*all_L_loc, p = True, f = True)
    all_R_loc = base.ls("Loc_R_*")
    R_loc = base.listRelatives(*all_R_loc, p = True, f = True)

    for i,l in enumerate(L_loc):
        pos = base.xform(l, q = True, t =True, ws = True)
        base.move(-pos[0], pos[1], pos[2], R_loc[i])
        print pos
    print L_loc
    print R_loc

def deleteLocators():
    nodes = base.ls("Loc_*")
    base.delete(nodes)
    print "deleted locators"
