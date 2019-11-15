#this file calls of all of the seperate files
#creates a gui so that all of the functions can be supposed
#as well as having a function to clear the scene and clean up the outliner so that
#the file will have one node for the entier rig

import maya.cmds as base
import Locators as loc
import Joints as jnt
import CreateIK as ik
import Controls as ctrl
import Constraints

loc = reload(loc)
jnt = reload(jnt)
ik = reload(ik)
ctrl = reload(ctrl)
Constraints = reload(Constraints)

global spineCount
global fingerCount

class AutoRigger():
	def __init__(self):
		self.BuildUI()

	def BuildUI(self):
		global spineCount
		global fingerCount
		base.window("Auto Rigger")

		base.rowColumnLayout(nc = 1, adjustableColumn = True)

		base.separator(st = "none")
		spineCount = base.intSliderGrp(l = "Spine Count", min = 1, max = 12, value = 5, step = 1, field = True)
		fingerCount = base.intSliderGrp(l = "Finger Count", min = 1, max = 5, value = 5, step = 1, field = True)
		base.separator(h = 10, st = "none")

		base.separator(h = 10, st = "none")
		base.button(l = "Create Base Locators", w = 200, c = "loc.createLocators(spineCount, fingerCount)")
		base.button(l = "Mirror L -> R", w = 200, c = "loc.mirrorLocators()")
		base.separator(h = 10, st = "none")

		base.separator(st = "none")
		base.button(l = "Create Joints", w = 200, c = "jnt.createJoints()")
		base.button(l = "Create IK", w = 200, c = "ik.IKHandles()")
		base.button(l = "Create Controls", w = 200, c = "ctrl.createCTRL(spineCount, fingerCount)")
		base.button(l = "Contrain", w = 200, c = "Constraints.createConstraints(fingerCount, spineCount)")
		base.button(l = "Clean Up Outliner", w = 200, c = self.cleanUpOutliner)
		base.button(l = "Bind Skin", w = 200, c = "Constraints.BindSkin()")

		base.separator(h = 10, st = "none")
		base.button(l = "Delete All Locators", w = 200, c = "loc.deleteLocators()")
		base.button(l = "Delete Joints", w = 200, c = "jnt.deleteJoints()")
		base.button(l = "Delete Controls", w = 200, c = "ctrl.deleteControls()")
		base.separator(h = 10, st = "none")
		base.button(l = "CLEAR SCENE", w = 200, c = self.clearScene)

		base.showWindow()

	def cleanUpOutliner(self, void):
	    base.parent("JNT_RIG", "CTRL_MASTER")
	    base.parent("IK_Handles", "CTRL_MASTER")

	def clearScene(self, void):
		base.delete("Loc_*")
		base.delete("JNT_*")
		base.delete("CTRL_*")
		base.delete("IK_*")
		print "Scene Cleared"

AutoRigger()
