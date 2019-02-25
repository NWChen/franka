#!/usr/bin/env python
'''
The file takes in a file name argument and reads in the value in the file as joint value
Then it command the robot to move to those positions sequentially
'''
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
import csv

if len(sys.argv) < 2:
	sys.exit("Expect 2 arguments, got 1")

#set up the commander
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial', anonymous=True)
robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
group_name = "panda_arm"
move_group = moveit_commander.MoveGroupCommander(group_name)
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
	moveit_msgs.msg.DisplayTrajectory,
	queue_size=20)
num_joint = 7

#execute the command in the csv file
with open(sys.argv[1]) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0
	for row in csv_reader:
		#check format
		if len(row) != num_joint:
			print("Your input format is not correct in line "+str(line_count)+"\tExpect "+str(num_joint)+" input\tGot "+str(len(row)))
			exit(0)

		#read in joint value
		joint_goal = []
		for cell in row:
			joint_goal.append(float(cell))

        # The go command can be called with joint values, poses, or without any
		# parameters if you have already set the pose or joint target for the group
		move_group.go(joint_goal, wait=True)

        # Calling ``stop()`` ensures that there is no residual movement
        move_group.stop()

        line_count += 1


