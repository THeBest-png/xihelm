#! /usr/bin/env python3

import roslib
import rospy
import actionlib
from std_msgs.msg import Float64, Float32
from sensor_msgs.msg import JointState

from colour_linear.msg import CustomActAction,CustomActFeedback,CustomActResult


THRESHOLD = rospy.get_param('threshold')
class StopBlueServer:
  def __init__(self):
    self.server = actionlib.SimpleActionServer('stop_blue', CustomActAction, self.execute, False)
    self.pub = rospy.Publisher('/colour_linear/slider_joint_position_controller/command', Float64, queue_size=1)
    self.curr_pos = rospy.Subscriber("/colour_linear/joint_states",JointState,self.joint_states_callback,queue_size=1)
    self.blue_dectected = rospy.Subscriber("/blue_percentage",Float32,self.cam_callback,queue_size=1)
    self.server.start()


  def execute(self, goal):
    # Do lots of awesome groundbreaking robot stuff here
    rospy.loginfo('action server moving linear actuator to  %i meters' % (goal.goal))
    success = True
    rate = rospy.Rate(0.5)
    self.pub.publish(goal.goal)

    while abs(self.pos - goal.goal) > 0.1:
      
      if self.blue_per >= THRESHOLD:
        stop_pos = self.pos
        self.pub.publish(stop_pos)
        break
      
      self.server.publish_feedback(CustomActFeedback(str(self.pos)))
      rate.sleep()

    if success:
      rospy.loginfo('%s: Succeeded' % rospy.get_name())
      self.server.set_succeeded(CustomActResult(self.pos))
      rospy.logwarn("DONE")



  def joint_states_callback(self,message):
    # filter out joint0 position:
    for i,name in enumerate(message.name):
        if name == "slider_joint":
            self.pos = message.position[i]

    return
  
  def cam_callback(self,message):
    self.blue_per = message.data

    return
  



if __name__ == '__main__':
  rospy.init_node('stop_blue_server')
  server = StopBlueServer()
  rospy.spin()