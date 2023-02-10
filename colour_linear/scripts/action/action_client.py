#! /usr/bin/env python

import roslib
import rospy
import actionlib

from colour_linear.msg import CustomActAction,CustomActGoal

class MoveClient:
    def __init__(self):

        client = actionlib.SimpleActionClient('stop_blue', CustomActAction)
        rospy.loginfo("Waiting for action server to come up...")
        client.wait_for_server()
        
        # Fill in the goal here
        client.send_goal(CustomActGoal(10),
                        active_cb=self.callback_active,
                        feedback_cb=self.callback_feedback,
                        done_cb=self.callback_done)
        rospy.loginfo("Goal has been sent to the action server.")

        # Waits for the server to finish performing the action.
        client.wait_for_result()

    def callback_active(self):
        rospy.loginfo("Action server is processing the goal")

    def callback_done(self,state, result):
        rospy.loginfo("Action server is done.")
        rospy.loginfo("Linear Actuator is stoped at: %s" % (str(result.stop_position)))

    def callback_feedback(self,feedback):
        rospy.loginfo("Current Position:%s" % str(feedback.my_feedback))

if __name__ == '__main__':
    try:
        rospy.init_node('stop_blue_client')
        MoveClient()
        #rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("program interrupted before completion")