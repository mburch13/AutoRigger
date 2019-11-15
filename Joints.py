#This file creates joints by finding the corresponging locator (name search)
#and placing the joints in the same position as the locator.

#impoted maya commands
import maya.cmds as base

#import the locator file so that you can access the locator's names and attributes
import Locators

#reload so you don't have to restart maya after every change
Locators = reload(Locators)

#"main" function to create all of the joints
def createJoints():
    #dose a rig/joint group alread exist
    if base.objExists("JNT_RIG"):
        print "RIG exists"
    else:
        #if not create a rig/joint group
        jointGRP = base.group(em = True, name = "JNT_RIG")

    #find all of the finger locations
    allFingers = base.ls("Loc_L_Finger_*_0", type = "transform")

    #find all of the spine locators by listing one locator
    #and finding all of the relatives from the locator hierarchy
    root = base.ls("Loc_ROOT")
    allSpines = base.ls("Loc_SPINE_*", type = "locator")
    spine = base.listRelatives(*allSpines, p = True, f = True)
    print "Spine: " + str(spine)

    #xform finds the transfromations of an object and query's the values
    #query means taking the transformation values from string to usable int or float values
    rootPos = base.xform(root, q = True, t = True, ws = True)
    #create the joint
    rootJoint = base.joint(radius = 1, p = rootPos, name = "JNT_ROOT")

    for i, s in enumerate(spine):
        spinePos = base.xform(s, q = True, t = True, ws = True)
        j = base.joint(radius = 1, p = spinePos, name = "JNT_SPINE_" + str(i))

    #call all of the helper functions to create all of the joints
    createHeadJoints(len(allSpines))
    createEyeJoints()
    createArmJoints(len(allSpines))
    createFingerJoints(len(allFingers))
    createLegJoints()

    #this helper function will set all of the joint orientation for proper deformations
    setJointOrientation()


def createHeadJoints(amount):
    #create head Joints

    #make sure that nothing is selected
    base.select(deselect = True)

    #select the last spine joint to start the spine joint hierarchy
    base.select("JNT_SPINE_" + str(amount - 1))
    allHead = base.ls("Loc_Head_*", type = "locator")
    head = base.listRelatives(*allHead, p = True, f = True)
    print "Head: " + str(head)
    #loop through all of the head locators so that joints can be created
    for i, h in enumerate(head):
        #get the position of the Locators
        headPos = base.xform(h, q = True, t = True, ws = True)
        #create the joint at the same position of the locator
        j = base.joint(radius = 1, p = headPos, name = "JNT_HEAD_" + str(i))

def createEyeJoints():
    #create eye Joints

    #make sure that nothing is selected
	base.select(deselect = True)

    #select the head joint to start the eye hierarchy
	base.select("JNT_HEAD_2")
	all_eyes = base.ls("Loc_Eye_*", type = "locator")
	eye = base.listRelatives(*all_eyes, p = True, f = True)
    #loop through all of the head locators so that joints can be created
	for i, e in enumerate(eye):
        #get the position of the Locators
		eyePos = base.xform(e, q = True, t = True, ws = True)
        #create the joint at the same position of the locator
		j = base.joint(radius = 1, p = eyePos, name = "JNT_EYE_" + str(i))
		#to make sure that the eyes are both parented to the eye connector joint
		if i == 2:
			base.parent(j, "JNT_EYE_0")

def createArmJoints(amount):
    #create Left arm

    #make sure nothing is selected
    base.select(deselect = True)
    #select the last spine joint
    base.select("JNT_SPINE_" + str(amount - 1))
    #find all of the left arm locators
    all_L_Arms = base.ls("Loc_L_Arm_*", type = "locator")
    L_arm = base.listRelatives(*all_L_Arms, p = True, f = True)
    print "L_arm: " + str(L_arm)
    #loop through all of the left arm locators to create joints
    for i, l_a in enumerate(L_arm):
        #get the position of the Locators
        L_armPos = base.xform(l_a, q = True, t = True, ws = True)
        #create the joint at the same position of the locator
        j = base.joint(radius = 1, p = L_armPos, name = "JNT_L_ARM_" + str(i))

    #create Right arm

    #make sure nothing is selected
    base.select(deselect = True)
    #select the last spine joint
    base.select("JNT_SPINE_" + str(amount - 1))
    #find all of the right arm locators
    all_R_Arms = base.ls("Loc_R_Arm_*", type = "locator")
    R_arm = base.listRelatives(*all_R_Arms, p = True, f = True)
    print "R_arm: " + str(R_arm)
    for i, r_a in enumerate(R_arm):
        #get the position of the Locators
        R_armPos = base.xform(r_a, q = True, t = True, ws = True)
        #create the joint at the same position of the locator
        j = base.joint(radius = 1, p = R_armPos, name = "JNT_R_ARM_" + str(i))

#helper funtion for createing the finger joints
#this function will loop throught the number of fingers created by the locators
def createFingerJoints(amount):
    for x in range(0,amount):
        createFinger(x)

def createFinger(i):
    #create Left hand
    base.select(deselect = True)
    #select the left wrist
    base.select("JNT_L_ARM_3")
    all_L_Fingers = base.ls("Loc_L_Finger_" + str(i) + "_*", type = "locator")
    L_finger = base.listRelatives(*all_L_Fingers, p = True, f = True)
    print "L_finger: " + str(L_finger)
    #loop through each finger segment to create the joints
    for z, l_f in enumerate(L_finger):
        L_fingerPos = base.xform(l_f, q = True, t= True, ws = True)
        j = base.joint(radius = 1, p = L_fingerPos, name = "JNT_L_FINGER_" + str(i) + "_" + str(z))

    #create Right hand
    base.select(deselect = True)
    #select the right wrist
    base.select("JNT_R_ARM_3")
    all_R_Fingers = base.ls("Loc_R_Finger_" + str(i) + "_*", type = "locator")
    R_finger = base.listRelatives(*all_R_Fingers, p = True, f = True)
    print "R_finger: " + str(R_finger)
    #loop through each finger segment to create the joints
    for z, r_f in enumerate(R_finger):
        R_fingerPos = base.xform(r_f, q = True, t = True, ws = True)
        j = base.joint(radius = 1, p = R_fingerPos, name = "JNT_R_FINGER_" + str(i) + "_" + str(z))

def createLegJoints():
    #create Left leg
    base.select(deselect = True)
    #select the root joint
    base.select("JNT_ROOT")
    all_L_Legs = base.ls("Loc_L_Leg_*", type = "locator")
    L_leg = base.listRelatives(*all_L_Legs, p = True, f = True)
    print "L_leg: " + str(L_leg)
    #loop through all of the left leg locators to create the joints
    for i, l_l in enumerate(L_leg):
        L_legPos = base.xform(l_l, q = True, t = True, ws = True)
        j = base.joint(radius = 1, p = L_legPos, name = "JNT_L_LEG_" + str(i))

    #create Right leg
    base.select(deselect = True)
    #select the root joint
    base.select("JNT_ROOT")
    all_R_Legs = base.ls("Loc_R_Leg_*", type = "locator")
    R_leg = base.listRelatives(*all_R_Legs, p = True, f = True)
    print "R_leg: " + str(R_leg)
    #loop through all of the right leg locators to create the joints
    for i, r_l in enumerate(R_leg):
        R_legPos = base.xform(r_l, q = True, t = True, ws = True)
        j = base.joint(radius = 1, p = R_legPos, name = "JNT_R_LEG_" + str(i))

#this function orents all of the joints from the root joint and all of the children
def setJointOrientation():
    base.select("JNT_ROOT")
    base.joint(e = True, ch = True, oj = "xyz", secondaryAxisOrient = "xup")
    print "joints oriented"

#function to delete all of the joints
def deleteJoints():
   joints = base.ls("JNT_*")
   base.delete(joints)
   print "deleted joints"
