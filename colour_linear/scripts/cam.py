#!/usr/bin/env python3

# rospy for the subscriber
import rospy
# ROS Image message
from sensor_msgs.msg import Image
# ROS Image message -> OpenCV2 image converter
from cv_bridge import CvBridge, CvBridgeError
# OpenCV2 for saving an image
import cv2

from std_msgs.msg import Float32

import numpy as np

# Instantiate CvBridge
bridge = CvBridge()


class Camera:

    def __init__(self):
        # Set up your subscriber and define its callback
        self.sub= rospy.Subscriber("/camera/image_raw", Image, self.image_callback)
        self.pub = rospy.Publisher('blue_percentage', Float32, queue_size=1)

    def image_callback(self,msg):
        rospy.loginfo_once("Received an image!")
        try:
            # Convert your ROS Image message to OpenCV2
            cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError:
            print("CvBridgeError")
        else:
            self.process_image(cv2_img)


    def process_image(self,img):

        # Here, you define your target color as
        # a tuple of three values: RGB
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([100,150,0])
        upper_blue = np.array([140,255,255])

        # Here we are defining range of bluecolor in HSV
        # This creates a mask of blue coloured 
        # objects found in the frame.
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # percentage of blue pixels in the original image:
        ratio_blue = cv2.countNonZero(mask)/(img.size/3)

        colorPercent = (ratio_blue * 100)

        self.pub.publish(colorPercent)


if __name__ == '__main__':
    rospy.init_node('blue_detector')
    camera = Camera()
    # Spin until ctrl + c
    rospy.spin()